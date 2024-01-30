# Inxpect Radar 200S

## [Video tutorial](https://www.youtube.com/watch?v=gXUdojU0PK8&list=PL2DBTrkO_vw2XxB7L_wobYaPWWIt-ITiW) about proprietary software
## [Radar logger](https://github.com/AltoRobotics/knowledge-base/blob/main/scripts/radar_logger.py) python3 script (pyModbusTCP required)
## [Tests Dec. 2023](#Tests-December-12th-2023)
## [Tests Jan. 2024](#Tests-January-30th-2024)

## Useful info and parameters to play with
 - 4 consecutive detection ranges for each sensor
 - Maximum response time = 100 ms
 - Time interval for automatic restart >= 4 s
 - Possibility to change the sensors' configuration dynamically via Fieldbus or digital input
 - Sensors and detection fields can be grouped to activate functions like muting

![grouping](https://github.com/AltoRobotics/knowledge-base/assets/32684998/9b67227a-2081-42ed-b8b9-4dae349327a0)

Digital inputs can be configured to:
 - Mute groups of sensors
 - Send stop/restart signals
 - Control the sensor via Fieldbus
 - Change sensors' configuration

Digital outputs can be configured to:
 - Get information about the individual detection fields ('_detection signal i_' in the output signal list). Remember that each detection signal requires a double-channel safety output to ensure the safety level!
 - Report system faults
 - Get output signals from the Fieldbus
 - Get a feedback signal whether the sensors have been muted/restarted

![digital_io](https://github.com/AltoRobotics/knowledge-base/assets/32684998/0da013c8-8b7d-4908-930b-f370cbbf8cc8)

Sensors can be restarted according to three different modalities:
 - Automatic, after a time interval >= 4 seconds
 - Manual, through an external system, like a button
 - Safe Manual, a combination of the two methods above

![restart](https://github.com/AltoRobotics/knowledge-base/assets/32684998/17829408-c321-4661-b883-a3a5cab8f074)

Anti-rotation and anti-masking filters can be activated. The first is to compensate for sensors' rotations, and the second is to overcome sensors' occlusions.

![anti-rotation_and_anti-masking](https://github.com/AltoRobotics/knowledge-base/assets/32684998/8d8fb57f-ac4e-4d72-a928-91c0d88a971d)

Static Object Detection (S.O.D.) function to detect and flag accordingly static objects in the radar range
 - Sensitivity to static objects can be regulated
 - Each detection field can be triggered in an isolated fashion or a cascade one, triggering all the consecutive detection fields

![sod_sensitivity_and_df_dependency](https://github.com/AltoRobotics/knowledge-base/assets/32684998/31eee76c-0f6f-4549-adff-2da5cfdbcde7)

## Tests December 12th 2023

### Sensors' configuration:

Sensor 1 - Detection Field 1
![sensor1_df1](https://github.com/AltoRobotics/knowledge-base/assets/32684998/d0c81f89-0ff9-467d-9ded-1a2eed6a5783)

Sensor 1 - Detection Field 2
![sensor1_df2](https://github.com/AltoRobotics/knowledge-base/assets/32684998/305470c8-52ec-4220-b155-9148828a7095)

Sensor 2 - Detection Field 1
![sensor2_df1](https://github.com/AltoRobotics/knowledge-base/assets/32684998/243f9942-0ceb-47e2-894e-730256ced67f)

Sensor 2 - Detection Field 2
![sensor2_df2](https://github.com/AltoRobotics/knowledge-base/assets/32684998/e3163433-7012-4a48-9449-723b4896fcb2)

### Tests:

| Safety Working | Obstacle Distance [mm] | Detect. Field 1 | Detect. Field 2 | Static Object | Human Detection |
|----------------|------------------------|-----------------|-----------------|---------------|-----------------|
|     Always     |          1500          |        v        |        v        |       x       |        x        |
|     Always     |          1500          |        v        |   x (reset 4)   |       x       |        v        |
|     Always     |          1000          |        v        |        v        |       x       |        x        |
|     Always     |          1000          |        x        |     x (Mask)    |       x       |        v        |
|     Restart    |          2000          |        v        |        v        |       x       |        x        |
|     Restart    |          2000          |        v        |   v (reset 4)   |       x       |        v        |
|     Restart    |          1000          |        x        |        x        |       x       |        v        |

### Conclusion (temp):
Usage of radars could be okay if our goal is to detect something/someone at a 2 m distance and 20 cm height, considering the range of interest as an arc produced by the radar signal. What happens in between these 2 meters can be discarded for safety, as other sensors should detect it during the robot's navigation.

## Tests January 30th 2024

Sensors are placed on Husky at a distance of 22 cm each other, with a heigh of 49 cm from the floor, and tilted of 10° frontward. A RealSense D435i is placed in between of the radars to visualize what the robot is seeing and how the depth works. The detection fields are shaped to cover the whole Husky width (a bit more in further tests), intersecting at the center (this area can be adjusted to completely overlap), and with each detection field long 1.05 meters such that we are able to look at a height of 20 cm from the floor at the first meter, and to the floor at the second meter.

![husky_radar_realsense](https://github.com/AltoRobotics/knowledge-base/assets/32684998/0244a9a5-2e60-4e98-a3ef-0646968967d0)

![realsense_viewer_inxpect](https://github.com/AltoRobotics/knowledge-base/assets/32684998/5328b8d2-2f70-41d1-a6ae-ad7b2b44a827)

### Notes
 - The ST.O.D. threshold has been increased from 0 dB to 3 dB to overcome the issue with Sensor 1 always detecting some static object close to the device;
 - The detection depends on the material type, texture and angle of incidence of the radar waves, not from the object color;
 - The ST.O.D. option does not guarantee the 100% detection of static objects
 
### Conclusion (temp):

We remotely controlled Husky on the street crossing BIC. The radars are robust to motion and rotation with high vibrations, even when stepping on bumpers, but manholes proved to be a strong reason of concern, as they can be easily detected. This would bring the robot to halt in case of small objects or flat things on the floor. For the time being the radar solution is a no, but a better understanding of the normatives will tell us if there is a way to avoid this problem or not. For instance, if it is required to perceive objects/people at 20 cm height in the first meter, there is no way to do so without looking at the floor in the second meter. If somehow this can be avoided, we might still be able to find a solution.

[Videos here](https://teams.microsoft.com/_?tenantId=fdc2c880-f495-4594-8118-e5d270bf792e#/conversations/unknown?threadId=19:WaAvRSyvcNEaLaUhFhgAvuNIzfQ-_xwBDWQ24W4EE9M1@thread.tacv2&messageId=1706622748102&replyChainId=1706622748102&ctx=channel)
