
# Inxpect Radar 200S

## [Tutorial Playlist](https://www.youtube.com/playlist?list=PLYOEqjmcX3qGQWubPR6m3nTOpJqDv8gj9) (specifically, I followed [this tutorial](https://www.youtube.com/watch?v=rKkS8W7DeXc&list=PLYOEqjmcX3qGQWubPR6m3nTOpJqDv8gj9&index=3&pp=iAQB) to configure the LiDAR)
## Documentation and Safety Designer software [here](https://www.sick.com/it/it/catalog/prodotti/safety/laser-scanner-di-sicurezza/nanoscan3/c/g507056?category=g568283&tab=downloads) 

### General Overview
After downloading and installing the software from the link above, you have to detect and configure the sensor for the first time. 

On the "Panoramica" page, you have a recap of everything regarding the project and the sensor, including its IP and a validation monitor, showing what the LiDAR is sensing in real-time and the associated output. 

![Screenshot 2024-02-19 104559_mod](https://github.com/AltoRobotics/knowledge-base/assets/32684998/0a7ee45c-6814-4e46-9790-36cd9beefb96)

### Setting the IP
The first time you detect the sensor, it has IP 0.0.0.0. To change it, in this or any other case, you can do it here:

![Screenshot 2024-02-19 104626_mod](https://github.com/AltoRobotics/knowledge-base/assets/32684998/ea19b9b7-0969-42fb-a703-106fa4a6db54)

### Shaping the detection fields
The complete capacity of the LiDAR is the one shown in the "Panoramica" tab. Still, you can design the sensor to respond in specific ways only for hand-crafted detection fields. You can have multiple groups ("Set di campo") with one or more detection fields. Each of the latter can trigger a specific behavior (like warning, protection, ...) and respond to specific resolutions.

![Screenshot 2024-02-19 104835_mod](https://github.com/AltoRobotics/knowledge-base/assets/32684998/eee771d0-1c8b-42b5-9c39-fd8f90f28f73)

### Safety signals
Once you designed the desired group of detection fields, you can set the specific signals associated with the I/O pins of the connection cable.

![Screenshot 2024-02-19 104909](https://github.com/AltoRobotics/knowledge-base/assets/32684998/d58d6833-386d-4185-aab1-138d1470a1a4)

### Apply configuration
Finally, send the custom configuration to the device like this:

![Screenshot 2024-02-19 105156](https://github.com/AltoRobotics/knowledge-base/assets/32684998/727e1b36-2fd3-48e5-9a53-eb2d856841ba)

### Test 19/2/2024
The performed tests (a very simple check of the detection fields) have shown the device to be responsive fast enough for what we need, proving the LiDAR to be a better solution for safety than radar, as we expected.
