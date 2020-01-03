# Mice Tracking Using The YOLO Algorithm

![Results Image](results/results_grid.png)

*Output examples of the YOLO network. (a)-(c) refer to [Ethological Evaluation](https://www.frontiersin.org/articles/10.3389/fnbeh.2015.00364/full), (d)-(f) refer to [Automated home-cage](https://www.nature.com/articles/ncomms1064) and (g)-(i) to [Crim](http://www.vision.caltech.edu/Video_Datasets/CRIM13/CRIM13/Main.html)*

This project **was developed and tested for Ubuntu 16.04 and 18.04.**

Knowledge in the darknet framework and YOLO object detector is required, further reading can be found [here](https://pjreddie.com/darknet/).

The darknet framework present here is a reimplementation based in [pjreddie](https://github.com/pjreddie/darknet) and [AlexeyAB](https://github.com/AlexeyAB/darknet/) work.

## Requirements

* Nvidia Drivers 390.87: [Install Guide](https://github.com/vanluwin/enviroment/#install-nvidia-gpu-drivers)

* CUDA 9.1: [Install Guide](https://github.com/vanluwin/enviroment#install-cuda)

* CuDNN 7.1: [Install Guide](https://github.com/vanluwin/enviroment#install-cudnn)

* GCC/G++ 5.5.0: [Install Guide](https://github.com/vanluwin/enviroment#change-gccg-version)

* OpenCV 3.3.0: [Install Guide](https://github.com/vanluwin/enviroment/#install-opencv)

## Installing Darknet

First clone the [repository](https://gitlab.com/helton.maia/proj-cnn-mice) and complie the source code. This can be accomplished by:

```console
user@computer:~$ git clone https://gitlab.com/helton.maia/proj-cnn-mice
user@computer:~$ cd proj-cnn-mice
user@computer:~/proj-cnn-mice$ make
```

## Weights

The latest weights used in the work can be downloaded here: [Full YOLO](https://drive.google.com/open?id=1GKVQipCa9q3Vk10yF78AR2Ip0GOe_2Ib), [Tiny YOLLO](https://drive.google.com/open?id=1ZtVNmLI9TfRYkLy4w_NxcCWPinpkuQ0u).

## Using the object detector

Clone the repository and enter the folder or add the darknet executabel to the path variable.

* To classify a single image do:

```console
user@computer:~/repo_folder$ sh image.sh .data .cfg .weight image
```

* To classify a video do:

```console
user@computer:~/repo_folder$ sh video.sh .data .cfg .weight video
```

* To save a video with the classifications do:

```console
user@computer:~/repo_folder$ sh videoOutput.sh .data .cfg .weight video output
```

* To calculate the mAP of a weight do:

```console
user@computer:~/repo_folder$ sh mAP.sh .data .cfg .weight
```

* To get the execution time spent in a file do:

```console
user@computer:~/repo_folder$ sh executionTime.sh .data .cfg .weights files output
```