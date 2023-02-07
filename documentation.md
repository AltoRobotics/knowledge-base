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
At the time of writing this, `nvidia-container-toolkit` is installed with `nvidia-docker2`. The [official guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#installation-guide) is good enough to get you started. In case you are running `Pop!OS`, make sure to [prioritize nvidia's apt repo over system76's](https://github.com/NVIDIA/nvidia-docker/issues/1388#issuecomment-1097326214).

## Setting up VSCode to auto-complete c++
We like VSCode and c++, we don't like not having auto-completion. 
We warmly suggest using [`clangd`](https://clangd.llvm.org/) instead of VSCode's own IntelliSense engine. In order to do this, the following are required:
- VSCode (extension-less. DO NOT install Microsoft's own C++ extensions)
- A working installation of `clangd` (e.g. installed via [binary distribution](https://clangd.llvm.org/installation#installing-clangd)). Make sure to `update-alternatives` if you're using Ubuntu
- Make sure `clangd` is looking for a `libstdc++-XX-dev` that is actually installed. Otherwise, [install it](https://stackoverflow.com/questions/74785927/clangd-doesnt-recognize-standard-headers/74787345)
- The `clangd` VSCode extension will look, by default, for a `compile_commands.json` file in the workspace root directory. You can generate one, for instance, via the cmake flag `-DCMAKE_EXPORT_COMPILE_COMMANDS=1` and link it from the workspace root directory
- (optional) You can generate the `compile_commands.json` when building a ROS2 workspace via `colcon build --cmake-args=-DCMAKE_EXPORT_COMPILE_COMMANDS=1`
- (optional) `clangd` will also auto-format your code if given a `.clang-format` file in the workspace root directory. You can find an example of such file [here](https://github.com/AltoRobotics/dotconfig/blob/main/.clang-format). Make sure you have the `Format On Save` option enabled in the VSCode settings, otherwise it won't work (and you'll be left wondering why).
