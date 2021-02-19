#!/usr/bin/env python3
#Person who wrote this code was Artur Poznanski, I just edited it.
#Unsure- About two parts (1) & (2).
#Plan- To use connect front motor to right joy stick.

import evdev
import ev3dev.auto as ev3
import threading
import time

'''
#Naming some button variables (from code to button)
button_X == 305
button_O == 306
button_triangle == 307
button_square == 304
button_l1 == 308
button_l2 == 310
button_r1 == 309
button_r2 == 311
button_share == 312
button_options == 313
button_ps == 316
button_l3 == 314 #When you press the left joy stick.
button_r3 == 315 #When you press the right joy stick.
button_touchpad == 317
'''

#(1)Not sure what this does yet...
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
print("Finding a PS4 controller to connect to...")
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
ps4dev = devices[0].fn

gamepad = evdev.InputDevice(ps4dev)

forward_speed = 0
side_speed = 0
running = True

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
        print("Engine should be running...")
        while running:
            self.right_motor.run_forever(speed_sp=dc_clamp(forward_speed+side_speed))
            self.left_motor.run_forever(speed_sp=dc_clamp(-forward_speed+side_speed))
            #Front motor is still a work in progress, need to figure out the code
            self.front_motor.run_forever(speed_sp=dc_clamp(forward_speed+side_speed))
        self.right_motor.stop()
        self.left_motor.stop()
        self.front_motor.stop()

#(1)Not sure what this does yet...
motor_thread = MotorThread()
motor_thread.setDaemon(True)
motor_thread.start()

#For PS4 button effects and what the code does in return
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

#For the sound
for event in gamepad.read_loop(): 
#Megalovania code from Stephen, so if I press L2 on the PS4, it will play Megalovania from Undertale.
    if event.type == 3:
        if event.code == 310:
            Sound.speak("You have pressed L2, Megalovania shall play now...").wait() #Press L2 to play Megalovoania song.
            Sound.tone([(1174, 100, 100),
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
            (1567, 100, 100)
            ]).wait()

'''
if event.code == 305:
    print("You have pressed the X button, the engine is now turning off...") #Press X button to turn of engine
    running = False
    time.sleep(1) #Wait for the motor thread to finish
break 
'''
