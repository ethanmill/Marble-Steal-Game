#!/bin/bash
echo "Main code"
wc -l ./game.py
wc -l ./lib/sorter.py
wc -l ./lib/sound.py
wc -l ./lib/turntable.py
wc -l ./arduino/SlaveNEW/SlaveNEW.ino
wc -l ./arduino/MasterNEW/MasterNEW.ino

n1=$(< ./game.py wc -l)
n2=$(< ./lib/sorter.py wc -l)
n3=$(< ./lib/sound.py wc -l)
n4=$(< ./lib/turntable.py wc -l)
n5=$(< ./arduino/SlaveNEW/SlaveNEW.ino wc -l)
n6=$(< ./arduino/MasterNEW/MasterNEW.ino wc -l)

echo $((n1+n2+n3+n4+n5+n6))
echo
echo "Testing code"
wc -l ../Testing/lcd/lcd.ino
wc -l ../Testing/test/test.ino
wc -l ../Testing/interupts/interupts.ino
wc -l ../Testing/lcd/lcd.ino
wc -l ../Testing/threading/RPithreading.py
wc -l ../Testing/asyncTesting/async.py
wc -l ../Testing/servoTesting/servoTesting.ino
wc -l ../Testing/servoTesting/RPiservoTesting.py
wc -l ../Testing/solenoidTest/solenoidTest.py
wc -l ../Testing/elevatorMotor/elevatorMotor.ino
wc -l ../Testing/elevatorMotor/RPielevatorMotor.py
wc -l ../Testing/interupts/interupts.ino
wc -l ../Testing/fullSamplerun/fullSampleRun.py
wc -l ../Testing/serialInterfacing/serialInterfacing.ino
wc -l ../Testing/serialInterfacing/RPiSerialInterfacing.py
wc -l ../Testing/colorSensorTesting/RPiOnline.py
wc -l ../Testing/colorSensorTesting/simplePoll.py
wc -l ../Testing/colorSensorTesting/RPicolorSenor.py
wc -l ../Testing/colorSensorTesting/pigpioColorSensor.py
