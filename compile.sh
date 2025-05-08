#!/bin/bash
cd ./lcd 
export DISPLAY=:0
arduino-cli compile -v --fqbn arduino:megaavr:nona4809
arduino-cli upload -vp /dev/ttyACM0 --fqbn arduino:megaavr:nona4809
cp -r /home/giden/Downloads/MECH* /home/giden/Downloads/.backup/
sudo python3 ../game.py
