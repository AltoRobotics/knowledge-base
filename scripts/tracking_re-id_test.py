import argparse, cv2, numpy as np
from pathlib import Path

import torch

from boxmot.tracker_zoo import create_tracker
from boxmot.utils import ROOT, WEIGHTS

from ultralytics import YOLO
from ultralytics.utils import ops
from ultralytics.trackers import register_tracker


def init_predictor(yolo, cap, args):

    success, frame = cap.read()
 
    if success:
        kwargs = {
            **yolo.overrides,
            'conf':args.conf,
            'iou':args.iou,
            'show':args.show,
            'device':args.device,
            'verbose':args.verbose,
            'classes':args.classes,
            'imgsz':args.imgsz,
            'line_width':args.line_width,
            'mode':'predict'
        }

        # predictor = yolo.predictor
        predictor = (yolo._smart_load('predictor'))(overrides=kwargs, _callbacks=yolo.callbacks)
        predictor.setup_model(model=yolo.model)

        predictor.setup_source(frame if frame is not None else args.source)
        predictor.model.warmup(imgsz=(1 if predictor.model.pt or predictor.model.triton else predictor.dataset.bs, 3, *predictor.imgsz))
        predictor.custom_args = args
        return predictor
    else:
        print("Impossible to acquire frames from the camera. Closing the application...")
        return -1


def init_tracker(predictor, persist=False):
    """
    Initialize the tracker for object tracking during prediction

    Args:
        predictor (object): The predictor object to initialize trackers for.
        persist (bool, optional): Whether to persist the trackers if they already exist. Defaults to False.
    """
    tracking_config = ROOT / 'boxmot' / 'configs' / (predictor.custom_args.tracking_method + '.yaml')
    tracker = create_tracker(
        predictor.custom_args.tracking_method,
        tracking_config,
        predictor.custom_args.reid_model,
        predictor.device,
        predictor.custom_args.half,
        per_class = False
    )
    # motion only models do not have
    if hasattr(tracker, 'model'):
        tracker.model.warmup()
    predictor.trackers = [tracker]


def update_tracker(predictor, tracker_profiler, frame):
    det = predictor.results[0].boxes.data.cpu().numpy()
    if len(det) == 0:
        tracker_profiler.dt = np.nan
    else:
        with tracker_profiler :
            tracks = predictor.trackers[0].update(det, frame)
        if len(tracks) != 0:
            idx = tracks[:, -1].astype(int)
            predictor.results[0] = predictor.results[0][idx]
            predictor.results[0].update(boxes=torch.as_tensor(tracks[:, :-1]))


def show(predictor):
    predictor.dataset.count = 0
    predictor.plotted_img = predictor.results[0].plot()
    cv2.imshow('camera', predictor.plotted_img)
    cv2.waitKey(1)


def print_comp_times(profilers):
    print({
        'prepr.': "{:.2f}ms".format(profilers[0].dt * 1E3),
        'infer.': "{:.2f}ms".format(profilers[1].dt * 1E3),
        'postpr.': "{:.2f}ms".format(profilers[2].dt * 1E3),
        'tracker': "{:.2f}ms".format(profilers[3].dt * 1E3),
        'show': "{:.2f}ms".format(profilers[4].dt * 1E3)
    })


@torch.no_grad()
def run(args):

    cap = cv2.VideoCapture(int(args.source))

    # Define the model to perform detection
    yolo = YOLO(args.yolo_model)
    yolo.predictor = init_predictor(yolo, cap, args)
    predictor = yolo.predictor

    # Register tracking callbacks to the model for object tracking during prediction
    register_tracker(yolo, persist=True)
    init_tracker(predictor, persist=True)

    path, vid_cap, s = 'camera', None, ''
    profilers = (ops.Profile(), ops.Profile(), ops.Profile(), ops.Profile(), ops.Profile(), ops.Profile())

    cv2.namedWindow('camera', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.resizeWindow('camera', 640, 480)
    
    tot_time = []
    try:
        while True:

            success, frame = cap.read()
            
            if success:

                im0s = [frame]
                predictor.batch = [path, im0s, vid_cap, s]

                # Preprocess (Convert to tensor and use fp16 if True)
                with profilers[0] : im = predictor.preprocess(im0s)

                # Inference (Detection of classes w/YoloV8)
                with profilers[1] : preds = predictor.model(im)#, augment=predictor.args.augment, visualize=args.visualize)

                # Detection postprocess (Apply non-max suppression and processes detections)
                with profilers[2] : predictor.results = predictor.postprocess(preds, im, im0s)

                # Tracker update
                # Method 1 ---------------------------------------
                # with profilers[3] : #predictor.run_callbacks('on_predict_postprocess_end')  # equivalent to below, but more computation
                # Method 2 ---------------------------------------
                update_tracker(predictor, profilers[3], frame)
                
                # Visualize and write results
                with profilers[4] : 
                    if predictor.args.show : show(predictor)

                if predictor.args.verbose : print_comp_times(profilers)
                    
                tot_time.append([profilers[1].dt, profilers[3].dt])

    except KeyboardInterrupt:
        mean_values = np.nanmean(tot_time[3:], axis=0) * 1E3
        print({
            'avg infer. time': "{:.2f}ms".format(mean_values[0]),
            'avg track. time': "{:.2f}ms".format(mean_values[1]),
        })
        print("\nCiaooooo")


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--yolo-model', type=Path, default=WEIGHTS / 'yolov8n-seg', help='yolo model path')
    parser.add_argument('--reid-model', type=Path, default=WEIGHTS / 'osnet_x0_25_market1501.pt', help='reid model path')
    parser.add_argument('--tracking-method', type=str, default='strongsort', help='deepocsort, botsort, strongsort, ocsort, bytetrack')
    parser.add_argument('--source', type=str, default='8', help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--stream', type=bool, default=False, help='whether the input source is a video stream')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    # class 0 is person, 1 is bycicle, 2 is car... 79 is oven
    parser.add_argument('--classes', nargs='+', type=int, default='0', help='filter by class: --classes 0, or --classes 0 2 3')
    parser.add_argument('--verbose', default=True, action='store_true', help='print results per frame')
    parser.add_argument('--show', action='store_true', default=True, help='display tracking video results')
    parser.add_argument('--line-width', default=None, type=int, help='The line width of the bounding boxes. If None, it is scaled to the image size.')
    parser.add_argument('--half', action='store_true', default=True, help='use FP16 half-precision inference')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
    parser.add_argument('--conf', type=float, default=0.5, help='confidence threshold')
    parser.add_argument('--iou', type=float, default=0.7, help='intersection over union (IoU) threshold for NMS')

    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    run(opt)
