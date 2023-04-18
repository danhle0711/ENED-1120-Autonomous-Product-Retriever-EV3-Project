#!/usr/bin/env micropython
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedPercent, MoveTank, MoveDifferential, SpeedRPM, follow_for_ms
from ev3dev2.wheel import EV3Tire
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import GyroSensor, ColorSensor, UltrasonicSensor
from ev3dev2.led import Leds
import time
import random

# Docs
# https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/motors.html?highlight=distance#move-differential

# Initialize constants
distance_between_wheels = 118
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_D)
lift_motor = MediumMotor(OUTPUT_B)
DA_diff = MoveDifferential(OUTPUT_D, OUTPUT_A, EV3Tire, distance_between_wheels)
DA_diff.gyro = GyroSensor()
DA_diff.gyro.reset()
DA_diff.gyro.calibrate()
# DA_diff.gyro.mode = 'GYRO-ANG'
DA_diff.cs = ColorSensor()
DA_diff.cs.mode = 'COL-COLOR'
DA_diff.ultrasonic = UltrasonicSensor()
DA_diff.ultrasonic.mode = 'US-DIST-CM'

standard_speed_percent = 20

distance_to_first_box = 0.8125 
box_length = 4 + (3/8)
distance_between_each_box = 6
shelf_length = 36
intersection_length = 12

# Functions
def go_straight_in(distance_in, speed_percent, target_angle_degree):
    # Description: drive forward {distance_in} inches with {speed_percent} percentage of max speed
    
    # distance_mm = float(input('Enter the distance: '))
    # speed_percent = float(input('Enter the speed: '))

    # distance_mm = distance_in * 25.4

    # Tinker with this coefficient
    # coefficient_of_distance = 1
    # coefficient_of_distance = (1 / 1.25)
    coefficient_of_distance = 261.54

    # DA_diff.on_for_distance(SpeedPercent(speed_percent), coefficient_of_distance * distance_mm)

    DA_diff.follow_gyro_angle(
        kp = 11.3, ki = 0.05, kd = 3.2,
        speed = SpeedPercent(speed_percent),
        target_angle = target_angle_degree,
        follow_for = follow_for_ms,
        ms = coefficient_of_distance * distance_in
    )

def turn_right_degrees(angle_degrees, speed_percent):
    # Description: turns {angle_degrees} degrees to the right
    DA_diff.turn_right(SpeedPercent(speed_percent), angle_degrees, brake = True, block = True, error_margin = 0.1, use_gyro = True)

def turn_left_degrees(angle_degrees, speed_percent):
    # Description: turns {angle_degrees} degrees to the left

    DA_diff.turn_left(SpeedPercent(speed_percent), angle_degrees, brake = True, block = True, error_margin = 0.1, use_gyro = True)

def instructions_to_list(input_list):
    shelf = input_list[0][:2]
    location_in_shelf = int(input_list[0][3])
    barcode_type = int(input_list[1])
    fulfillment_area = input_list[2]
    return [shelf, location_in_shelf, barcode_type, fulfillment_area]

def check_accuracy():
    print('Gyro value: {0}'.format(DA_diff.gyro.value()))
    print('Left motor: {0}'.format(left_motor.position))
    print('Right motor: {0}'.format(right_motor.position))
    print('Lift motor: {0}'.format(lift_motor.position))
    # print('\n')

def reset_motors():
    left_motor.reset()
    right_motor.reset()
    lift_motor.reset()

def barcode_reader():
    code_list = [9, 9, 9, 9]
    for i in range(4):
        time.sleep(2)
        if (DA_diff.cs.color == 1):
            code_list[i] = 1
        else:
            code_list[i] = 0
        print(code_list)
        go_straight_in(0.80, 30, 0)
    return code_list

def barcode_type_identifier(code_list):
    if (code_list == [0, 0, 0, 1] or code_list == [1, 0, 0, 0]):
        result = 1
    elif (code_list == [0, 1, 0, 1] or code_list == [1, 0, 1, 0]):
        result = 2
    elif (code_list == [0, 0, 1, 1] or code_list == [1, 1, 0, 0]):
        result = 3
    elif (code_list == [1, 0, 0, 1]):
        result = 4
    else:
        print('Error, making random guess')
        result = random.randint(1, 4)
    print('Barcode type: {0}'.format(result))
    return result

def path_to_shelve(shelf):
    if any(shelf == x for x in ['A1', 'A2', 'C1', 'C2']):
    # if ((shelf == 'A1') or (shelf == 'A2') or (shelf == 'C1') or (shelf == 'C2')):
        return 0
    elif any(shelf == x for x in ['B1', 'B2', 'D1', 'D2']):
    # elif ((shelf == 'B1') or (shelf == 'B2') or (shelf == 'D1') or (shelf == 'D2')):
        return 0
    else:
        return 0

def path_to_fulfillment_area():
    return 0

def path_back_to_A(fulfillment_area):
    if (fulfillment_area == 'B'):
        print('Going fom B to A\n')
        go_straight_in(-96, 20) # Going backwards from Home B to Home A (-x direction)
    elif (fulfillment_area == 'C'):
        print('Going fom C to A\n')
        go_straight_in(-114, 20) # Going backwards from Home C to Home A (-y direction)
    elif (fulfillment_area == 'D'):
        print('Going fom D to C\n')
        go_straight_in(-96, 20) # Going backwards from Home D to Home C (-x direction)
        print('Reached Home C\n')
        print('Turning\n')
        DA_diff.odometry_start()
        turn_left_degrees(90, 20) # Turn left in place 90 degrees at Home C (now facing +y direction)
        DA_diff.odometry_stop()
        print('Going fom C to A\n')
        go_straight_in(-114, 20) # Going backwards from Home C to Home A (-y direction)
    print('Reached Home A')

# Input
shelf = input('Enter the shelf: ')
location_in_shelf = int(input('Enter the location of the item on the shelf: '))
barcode_type = int(input('Enter the barcode type: '))
fulfillment_area = input('Enter the fulfillment area: ')

# print(DA_diff.gyro.value())

# go_straight_in(20, 50)

# DA_diff.odometry_start()

# turn_right_degrees(90, 10)
# print(DA_diff.gyro.value())

# DA_diff.odometry_stop()

# go_straight_in(20, 50)

go_straight_in(30, 20, 0)

