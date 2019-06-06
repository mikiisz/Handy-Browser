# Handy-Browser
Version 1.0.1

## Table of contents
* [General info](#general-info)
* [Getting started](#getting-started)
* [Manual](#manual)
* [Contact](#contact)
* [Comming soon features](#comming-soon-features)

## General info
Handy Browser is a small tool that help users to operate Internet Browsers with thairs hands.
Progeram was designed by Michał Szkarłat and Dominik Mondzik.
The orgin of this project was to complete and pass the python course.
Feel free to use and edit the code.
The way you can reach us is described in the 'contact' section.
	
## Getting started
### Project is linux friendly
Project is created with python3, using:
* Pillow==5.1.0
* opencv-python==4.0.0.21
* selenium==3.141.0
* numpy==1.16.2
* tkinter==8.6
* webbrowser>=1.0

After installing the required dependecies you have to make sure to install geckodriver.
This issue is well descirebed here: https://python-forum.io/Thread-Getting-error-geckodriver-executable-needs-to-be-in-PATH
Make sure to follow the instructions correctly
	
## Manual
The program can work in 2 modes: static and dynamic. <br>
To change between the modes click <b>s</b> <br>
To reset the background sample click <b>r</b> <br>
To quit tha application click <b>q</b> 

### Navigation

![Demo mode](https://raw.githubusercontent.com/mikiisz/Handy-Browser/master/Screenshot%20from%202019-06-06%2009-58-34.png)

There are 7 commands available:
#### Dynamic Mode
* Swipe hand in right direction - <b>open new card</b>
* Swipe hand in left direction - <b>close current card</b>
* Put forward two fingers from right edge of camera window - <b>open webside</b>
* Put forward two fingers from left edge of camera window - <b>open webside</b>
* Move hand up / down - <b>change volume level </b>
#### Static Mode
* Two fingers - <b> take a picture </b>
* Three fingers - <b> make a screenshot </b>
```
$ cd Handy-Browser
$ pyhton3 my_gui.py
```

## Contact
We prefer to contact by email:
* Michał Szkarłat - mikiisz497@gmail.com
* Dominik Mondzik - mondzik.d@gmail.com

## Comming soon features
During our work we came into some new ideas, which would improve functionality of this project or just make it more usable.<br>
Below we present some of this ideas:<br>
* instalator which will automatically add geckodriver for all (or chosen) web browsers,
* more possible views in GUI,
* list all possible browsers, not only harcoded ones,
