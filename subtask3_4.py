#!/usr/bin/env micropython
from ev3dev2.motor import LargeMotor, MediumMotor, OUTPUT_A, OUTPUT_B, OUTPUT_D, SpeedPercent, MoveTank, MoveDifferential, SpeedRPM, follow_for_ms
from ev3dev2.wheel import EV3Tire
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import GyroSensor, ColorSensor, UltrasonicSensor
from ev3dev2.led import Leds
import time
import random

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
        # print('Error, making random guess')
        result = random.randint(1, 4)
    print('Barcode type: {0}'.format(result))
    return result


# while True:
#     print(DA_diff.ultrasonic.distance_centimeters)
#     time.sleep(0.2)


# while True:
#     print(DA_diff.cs.color)
#     time.sleep(0.2)

# Identifying the barcode
# barcode_type = barcode_type_identifier(barcode_reader())



# turn_left_degrees(90, 0)


# reset_motors()



# check_accuracy()
# lift_motor.on_to_position(20, lift_motor.position + 1800)


# check_accuracy()
# lift_motor.on_to_position(20, lift_motor.position - 1800)
# check_accuracy()
# lift_motor.on_to_position(20, 1800)
# go_straight_in(20,20,0)
# lift_motor.on_to_position(20, 0)
check_accuracy()
go_straight_in(14, 20, 0)
check_accuracy()
while (DA_diff.cs.color == 0):
    go_straight_in(0.3, 30, 0)
    
    # print('Hello')

go_straight_in(1, 20, 0)

# print(DA_diff.cs.color)
# check_accuracy()
# lift_motor.on_to_position(20, -1800)
# print(DA_diff.cs.color)
# check_accuracy()

barcode_type = barcode_type_identifier(barcode_reader())