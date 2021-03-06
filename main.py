#!/usr/bin/env python3
#Unsure- About two parts (1) & (2).

import evdev
import ev3dev.auto as ev3
import threading
import time
from time import sleep

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def scale(val, src, dst):
    return (float(val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

def scale_stick(value):
    return scale(value,(0,255),(-1000,1000))

def dc_clamp(value):
    return clamp(value,-1000,1000)

#To find the PS4 controller
#Don't forget to connect to PS4 controller before running main.py
ev3.Sound.speak("Finding a PS4 controller to connect to...").wait()
print("Finding a PS4 controller to connect to...")
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
ps4dev = devices[0].fn

gamepad = evdev.InputDevice(ps4dev)

forward_speed = 0
side_speed = 0
running = True


#For the writing/drawing on the LCD screen
screen = ev3.Screen()

smile = True

while True:
    screen.clear()

    #Screen.draw returns a PIL.ImageDraw handle
    screen.draw.ellipse(( 20, 20, 60, 60))
    screen.draw.ellipse((118, 20, 158, 60))

    if smile:
        #This is for a happy face
        screen.draw.arc((20, 80, 158, 100), 0, 180)
    else:
        #This is for a sad face
        screen.draw.arc((20, 80, 158, 100), 180, 360)
    
    smile = not smile
    
    #update lcd display
    screen.update()

    break

'''
#For the sound
for event in gamepad.read_loop(): 
#Once EV3 code starts running, it will play Megalovania from Undertale.
    if event.type == 3:
        if event.code == 310:
'''

ev3.Sound.speak("Battle has commenced, Megalovania shall play now...").wait() #Once EV3 has started it will play Megalovoania song.
ev3.Sound.tone([(1174, 100, 100),
(1174, 100, 100),
(2349, 150, 100),
(1760, 150, 100),
(1661, 100, 100),
(1567, 150, 100),
(1396, 150, 100),
(1174, 150, 100),
(1396, 100, 100),
(1567, 100, 100),
(1046, 100, 100),
(1046, 100, 100),
(2349, 100, 100),
(1760, 150, 150),
(1661, 150, 100),
(1567, 150, 100),
(1396, 150, 100),
(1174, 100, 100),
(1396, 100, 100),
(1576, 100, 100),
(1975, 100, 100),
(1975, 100, 100),
(2349, 150, 100),
(1760, 150, 150),
(1661, 150, 100),
(1567, 150, 100),
(1396, 150, 100),
(1174, 100, 100),
(1396, 100, 100),
(1567, 100, 100),
(1174, 100, 100),
(1174, 100, 100),
(2349, 150, 100),
(1760, 150, 100),
(1661, 100, 100),
(1567, 150, 100),
(1396, 150, 100),
(1174, 150, 100),
(1396, 100, 100),
(1567, 100, 100),
(1046, 100, 100),
(1046, 100, 100),
(2349, 100, 100)
]).wait()

#For the motor
class MotorThread(threading.Thread):
    def __init__(self):
        #Right motor is connected to output C
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        #Left motor is connected to output B
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        #Front motor (which is the wire stealer) is connected to output A (!WORK IN PROGRESS!)
        self.front_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        threading.Thread.__init__(self)

    def run(self):
        ev3.Sound.speak("Engine should be running...")
        print("Engine should be running...")
        while running:
            self.right_motor.run_forever(speed_sp=dc_clamp(forward_speed+side_speed))
            self.left_motor.run_forever(speed_sp=dc_clamp(-forward_speed+side_speed))
            #Front motor is still a work in progress, need to figure out the code
            self.front_motor.run_forever(speed_sp=dc_clamp(forward_speed+side_speed))
        self.right_motor.stop()
        self.left_motor.stop()
        self.front_motor.stop()

motor_thread = MotorThread()
motor_thread.setDaemon(True)
motor_thread.start()

#For PS4 joysticks effects and what the code does in return
for event in gamepad.read_loop():   #This loops infinitely when running = True
    if event.type == 3:             #Event.type 3 is when a joy stick is moved
        if event.code == 0:         #The X-axis on left joy stick
            forward_speed = -scale_stick(event.value)
        if event.code == 1:         #The Y-axis on left joy stick
            side_speed = -scale_stick(event.value)
        if side_speed < 100 and side_speed > -100:
            side_speed = 0
        if forward_speed < 100 and forward_speed > -100:
            forward_speed = 0
    elif event.type == 1: #Event.type 1 is when a button is pressed
        if event.value == 1: #I think event.value 1 is when EV3 is on
            if event.code == 304: #Press the X button for the EV3 to say "Bruh"
                ev3.Sound.speak("Bruh").wait()
            if event.code == 307: #Press the triangle button for the EV3 to say "GG, Eazy clap noob"
                ev3.Sound.speak("GG, Easy clap noob").wait()
            if event.code == 308: #Press the square button for the EV3 to say "This is rigged"
                ev3.Sound.speak("This is rigged").wait()
            if event.code == 305 and event.value == 1: #Press Circle button to turn of engine
                ev3.Sound.speak("You have pressed the Circle button, the engine is now turning off...").wait()
                print("You have pressed the Circle button, the engine is now turning off...") 
                running = False 
                time.sleep(0.5) #Wait for the motor thread to finish
                break
    




