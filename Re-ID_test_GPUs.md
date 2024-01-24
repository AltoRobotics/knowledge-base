# TRACKING + RE-IDENTIFICATION TESTS LOG

This page serves as a log for the test conducted on the YoloV8 detection + Tracking + Re-Identification algorithm.

[Here](scripts/tracking_re-id_test.py) is the script used to perform the tests.

The whole pipeline is based on [BoxMOT](https://github.com/mikel-brostrom/yolo_tracking). 

## Installation
While on a classic Ubuntu system the installation should be straightforward, to run the script on NVIDIA platforms you have to:
 - [optional] Create a virtual environment with Python3.8
 - Clone the BoxMOT repository following the instructions from the link above and install the package. Note: the installation process is highly verbose; to reduce the amount of text, omit the ```-v``` command when installing with pip.
 At this point, some issues might pop up:
- ```AttributeError: module ; setuptools.errors' has no attribute 'CompileError'``` -> Solution: ```pip install setuptools==59.5.0```
- ```error: invalid command 'bdist_wheel'``` -> Solution: ```pip install wheel``` and then ```python setup.py bdist_wheel```
- Issue with grpcio -> Solution: ```pip install grpcio``` (takes some time to compile)

Run the installation command from BoxMOT again; everything should work fine.

The torch and torchvision packages installed during the process do not work with NVIDIA platforms. To do so, you have to:
 - Uninstall them with ```pip uninstall torch torchvision```
 - Install torchvision following the steps [here](https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048) at the "Installation" section (*)
 - Install torch following the steps [here](https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html#overview__section_xavier_nx)
Note: versions depend on the JetPack version of the device. In our case, it should be Torch 2.0.0+nv23.05 and Torchvision 0.15.1

(*) if you are in a virtual environment, to install torchvision inside it add to the PYTHONPATH the path to your Python executable (like ~/path/to/venv/lib/python3.8) and run ```python3 setup.py install``` WITHOUT ```--user```.

Finally, uninstall any precedent version you have of ultralytics. This package works only with its specific version. To get it, once all the installations work fine, run the ```track.py``` example in the examples folder to download it automatically.


## Results (with strongsort+osnet_x0_25_market1501)

|                                         | Avg. YoloV8 Inference [ms] | Avg. Tracker update [ms] |
|-----------------------------------------|:--------------------------:|:------------------------:|
| Schenker Vision 16 Pro (RTX3070 Ti 8GB) |            5.01            |           13.34          |
| reComputer J3010 (Jetson Orin Nano 4GN) |            47.86           |           62.59          |
|    Jetson AGX Orin Developer Kit 32GB   |            17.45           |           48.67          |


## Further notes

### General
 - I've had some issues when trying to change the detection model or Re-ID model. It seems like all the Python package versions are not exactly compatible with each other.

### Detection
 - I haven't been able to use Yolo-NAS or YOLOX in place of YoloV8, but it matters relatively as the tracker update is the operation taking more computational time.
 - Both Yolo-NAS and YOLOX are supposed to be faster than YoloV8, but I can't find a comparison between the two.

### Tracking+Re-ID
 - To use other Re-ID models I had to downgrade _gdown_ with ```pip install gdown==4.6.1```. 
 - Apparently, not all the models on [ModelZoo](https://kaiyangzhou.github.io/deep-person-reid/MODEL_ZOO.html) are available. Check the error message when not giving a model as input.
 - The segments _x0_25_, _x1_0_, _x1_4_, and so on represent a scaling factor of the original model. For instance, _osnet_x0_25_ is a network 25% of the original _osnet_ size. This affects of course computational speed and accuracy of the re-identification.
 - The segments _cuhk03_, _market1501_ and _msmt17_, instead, refer to the dataset originally used to train the Re-ID model: [CUHK03](https://paperswithcode.com/dataset/cuhk03), [Market-1501](https://paperswithcode.com/dataset/market-1501), or [MSMT17](https://paperswithcode.com/dataset/msmt17).
 - The tracker+Re-ID model can be accelerated using Nebullvm like showed [here](https://colab.research.google.com/drive/1APUZ1ijCiQFBR9xD0gUvFUOC8yOJIvHm?usp=sharing) (from the Tutorials section of the BoxMOT main page) or from CLI like showed [here](https://github.com/mikel-brostrom/yolo_tracking/wiki/ReID-multi-framework-model-export) (from the Tracking->Select ReID model example section of the BoxMOT main page)
