# uflix


![image](images/header.png)


uflix is a *very* lightweight home video sharing solution

## The problem 

You have a bunch of movies and videos, (some .avi) on a computer or on a hard drive at home. You want to watch a particular video on your tablet on your WiFi, or on a differnet computer, perhaps running a different OS. You want to allow anyone on your WiFi to watch any of these videos, without messy drive mounting, NAS or FTP. 

## The Solution

uflix assumes a webserver is running on the computer that has all the videos. For some specififed folder, uflix

1. finds all video files recursively and makes a list of them
2. if necessary, it transcodes them to HTML5-compatible .mp4s using VLC
3. it builds and links small webpages in each folder that allows web plays of that video file
4. it builds a "master" webpage from which you can find and navigate to all your files -- in the browser!

## installation

## usage

```
uflix -c 
```



## Roadmap

1. Test a script that coverts a .avi into a HTML5-supported .mp4 video
2. Build a script that finds and converts all video files in a folder
2. Build a script that builds webapges in each folder for each file
3. Build a script that builds the master webpage
4. Wrap up: setting up the server. 