#!/bin/bash
cd ~/Downloads/MECH307/Testing/serialInterfacing
arduino-cli compile -v --fqbn arduino:megaavr:nona4809 &&
arduino-cli upload -vp /dev/ttyACM0 --fqbn arduino:megaavr:nona4809 &&
sudo python3 RPiSerialInterfacing.py
