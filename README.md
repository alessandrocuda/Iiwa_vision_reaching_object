# Vision-guided reaching movements with NN
<img src="https://media.giphy.com/media/aYjVNyRk9GPg3OqhGL/giphy.gif" />


## Introduction
This project aims: to solve the problem of inverse kinematics through the use of a neural network, locate the position of an object in space through a neural network and finally control the Iiwaa robotic arm to solve a reaching task.

This project was developed for the course of Robotics at the University of Pisa under the guide of [Prof. Egidio Falotico](https://www.santannapisa.it/it/egidio-falotico).

All details can be found in the presentation [here](https://docs.google.com/presentation/d/1NiAfCmL9spCaZ-xEjM6OpO3TFUCP8NwZ7ZqbdjWP4Ts/edit?usp=sharing).


## Table of Contents 
- [Usage](#usage)

- [Contributing](#contributing)
- [Contact](#contact)
- [License](#license)

## Usage
This code requires Python 3.8 or later and ROS noetic:
```bash
# install ROS noetic
sudo apt install ros-noetic-desktop-full

# Add the following line at the end of $HOME/.bashrc: 
source /opt/ros/noetic/setup.bash

#install other packages
sudo apt install ros-noetic-{urdfdom-py,kdl-parser-py,ros-control,ros-controllers,gazebo-ros-pkgs,gazebo-ros-control}

```

download the repository and copy the src/kuka_iiwa folder in your catkin workspace:

```bash
#download repo
git clone https://github.com/alessandrocuda/Iiwa_vision_reaching_object
cd Iiwa_vision_reaching_object

#copy and compile the project under the catkin workspace
cp ./src/kuka_iiwa <path to your catkin workspace folder>
cd <path to your catkin workspace folder>
catkin_make
. devel/setup.bash
```

Now you are ready to run the gazebo enviroment
```bash
roslaunch kuka_iiwa_gazebo kuka_iiwa.launch
```
Then, be sure to start the simulation in gazebo and finally, start all ros nodes needed for the vision-reaching object task
```bash
# first run the vision service
rosrun kuka_iiwa_utilities iiwa_camera_service.py
# then from other terminal
cd ~/<path to your catkin workspace folder>/src/kuka_iiwa_utilities/script
rosrun kuka_iiwa_utilities iiwa_move_to.py
```


## Contributing
 
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

<!-- CONTACT -->
## Contact

Alessandro Cudazzo - [@alessandrocuda](https://twitter.com/alessandrocuda) - alessandro@cudazzo.com

Giulia Volpi - giuliavolpi25.93@gmail.com

Nicola Ferella - n.farella@studenti.unipi.it

Project Link: [https://github.com/alessandrocuda/Iiwa_vision_reaching_object](https://github.com/alessandrocuda/Iiwa_vision_reaching_object)


<!-- LICENSE -->
## License
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

This library is free software; you can redistribute it and/or modify it under
the terms of the MIT license.

- **[MIT license](LICENSE)**
- Copyright 2021 ©  <a href="https://alessandrocudazzo.it" target="_blank">Alessandro Cudazzo</a> - <a href="mailto:giuliavolpi25.93@gmail.com">Giulia Volpi</a> - <a href="n.farella@studenti.unipi.it">Nicola Ferella</a>