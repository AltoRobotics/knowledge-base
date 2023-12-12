# Inxpect Radar 200S

## [Video tutorial](https://www.youtube.com/watch?v=gXUdojU0PK8&list=PL2DBTrkO_vw2XxB7L_wobYaPWWIt-ITiW) about proprietary software

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
Usage of radars could be okay if our goal is to detect something/someone at a 2 m distance and 20 cm height, considering the range of interest as an arc produced by the radar signal. What happens in between these 2 meters can be discarded for the purpose of safety, as it should be detected by other sensors during the robot's navigation,
