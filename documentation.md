# Documentation

## Setting up `docker`
Follow the [official docker engine docs](https://docs.docker.com/engine/install/). Do not install the `docker.io` package, install the docker engine packages listed in the official documentation. As a post-installation step, you can use 
```shell
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
$ newgrp docker
```
to avoid having to `sudo docker` all the time. 

## Setting up `nvidia-container-toolkit`
At the time of writing this, `nvidia-container-toolkit` is installed with `nvidia-docker2`. The [official guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#installation-guide) is good enough to get you started. In case you are running `Pop!OS`:
- force the `distribution` env variable to the ubuntu version your pop!OS is based on. For instance, in case of 22.04
```shell
distribution=ubuntu22.04 \
      && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
      && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
            sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
            sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```
- make sure to [prioritize nvidia's apt repo over system76's](https://github.com/NVIDIA/nvidia-docker/issues/1388#issuecomment-1097326214).

## Propagate gpus to Distrobox

If you use distrobox to handle the development containers be aware that in order to enable the GPU inside of it you need to add `-a "--gpus all --device /dev/dri"` to the distrobox command.
e.g.
```shell
$ distrobox create --image alto/ros:humble-dev --name dockHumble -a "--gpus all --device /dev/dri" 
```

## Setting up VSCode to auto-complete c++
We like VSCode and c++, we don't like not having auto-completion. 
We warmly suggest using [`clangd`](https://clangd.llvm.org/) instead of VSCode's own IntelliSense engine. In order to do this, the following are required:
- VSCode (extension-less. DO NOT install Microsoft's own C++ extensions)
- A working installation of `clangd` (e.g. installed via [binary distribution](https://clangd.llvm.org/installation#installing-clangd)). Make sure to `update-alternatives` if you're using Ubuntu
- Make sure `clangd` is looking for a `libstdc++-XX-dev` that is actually installed. Otherwise, [install it](https://stackoverflow.com/questions/74785927/clangd-doesnt-recognize-standard-headers/74787345)
- The `clangd` VSCode extension will look, by default, for a `compile_commands.json` file in the workspace root directory. You can generate one, for instance, via the cmake flag `-DCMAKE_EXPORT_COMPILE_COMMANDS=1` and link it from the workspace root directory
- (optional) You can generate the `compile_commands.json` when building a ROS2 workspace via `colcon build --cmake-args=-DCMAKE_EXPORT_COMPILE_COMMANDS=1`
- (optional) `clang-format` will also auto-format your code if given a `.clang-format` file in the workspace root directory. You can find an example of such file [here](https://github.com/AltoRobotics/dotconfig/blob/main/.clang-format). Make sure you have the `Format On Save` option enabled in the VSCode settings, otherwise it won't work (and you'll be left wondering why).

## Run tests on Arm architecture using qemu

```
  $ sudo apt install qemu-user-static qemu-utils gcc-arm-linux-gnueabihf libc6-dev-armhf-cross  g++-arm-linux-gnueabihf
  
  $ export CC=arm-linux-gnueabihf-gcc
  $ export CXX=arm-linux-gnueabihf-g++
  
  $ cd $PROJECT_HOME
  $ mkdir buildArm
  $ cd buildArm
  $ cmake ..
  $ make 
  
  $ qemu-arm-static -L /usr/arm-linux-gnueabihf/ test/tests

  ```
Same thing can be done for aarch64

```
 $ sudo apt install gcc-aarch64-linux-gnu  g++-aarch64-linux-gnu

 $ export CC=aarch64-linux-gnu-gcc
 $ export CXX=aarch64-linux-gnu-g++

  $ cd $PROJECT_HOME
  $ mkdir buildAarch64
  $ cd buildAarch64
  $ cmake ..
  $ make 

  $ qemu-aarch64-static -L /usr/aarch64-linux-gnu/ test/tests
  ```
  
## Cross build ROS2 Package

Cross building packages for a dockered Ros2 ARMv864 container is something needed but it is not clear on how to do in a blessed way.
I devised a way to do it in a way that seems to work at least in simple cases.

### Prerequisites

For an armv8 build you need

1- cross compilers and qemu: for simplicity you can install the ones given with Ubuntu

```
sudo apt install  qemu-user-static qemu-utils gcc-aarch64-linux-gnu  g++-aarch64-linux-gnu
```

A sysroot that is a root filesystem that contains the library you need to build against.

Otherwise you can copy it from the target with rsync, mount it with ssh-fs or extract from a docker I created it from a docker using

### Workaround &#128544;

It seems that rclcpp confuses cmake so you will need to add a symbolic link in 

```
/usr/lib/aarch64-linux-gnu $ sudo ln -s ${SYSROOT}/usr/lib/aarch64-linux-gnu/libpython3.10.so

```

### Proper crossbuilding

then you need a cmake toolchain file like this one in which 

https://github.com/peppedxAlto/simplepackage/blob/master/aarch64.cmake

please export a bash variable SYSROOT pointing to the sysroot like

```
$ export SYSROOT=/home/giellamo/roots
```

Then you can build

```
 $ colcon build --cmake-force-configure --cmake-args --no-warn-unused-cli   -DCMAKE_TOOLCHAIN_FILE=`pwd`/aarch64.cmake
 ```

 Then copy your workspace to your target (docker or not)

 e.g.
 ```
 $ rsync -avz  rostest jetson@192.168.1.202:
 ```

 ### How to extract a rootfs from a docker image

example

 ```
 $ docker run --rm arm64v8/ros:humble-perception-jammy
 $ export IMAGE_NAME=arm64v8/ros:humble-perception-jammy
 $ docker-squash -f $(($(docker history $IMAGE_NAME | wc -l | xargs)-1)) -t ${IMAGE_NAME}:squashed $IMAGE_NAME
 $ docker image save  arm64v8/ros:humble-perception-jammy -o ${PATH_TO_RFS}/arm64ros.tar
 $ cd ${PATH_TO_RFS}
 $ tar xvf arm64ros.tar
 $ tar xvf  b42329b86bd604ec09f30d2f9fda6f7c21c7d44cb7d3adab4285adbb664216b/layer.tar # it will be a different hash
 ``` 

ps docker-squash needs to be installed with pip.
