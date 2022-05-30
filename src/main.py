# Tutorial main to demonstrate using user created libraries onboard the pi pico

import max_10
from time import sleep
from machine import Pin, PWM


def main():
    led = Pin(25, Pin.OUT)
    # Max10(throttle control pin num, servo control pin num, freq)
    esc = max_10.Max10(4, 5, 50)
    esc.arm_esc()
    control_test(esc)


def control_test(esc):
    esc.set_steering(90)
    sleep(3.0)
    esc.set_forward(0.15)
    sleep(0.5)
    esc.set_steering(85)
    sleep(2.0)
    esc.set_forward(0.2)
    sleep(0.5)
    esc.set_steering(100)
    sleep(1.0)
    esc.set_forward(0.1)
    sleep(1.0)
    esc.set_steering(70)
    sleep(2.0)
    esc.set_neutral()
    sleep(1.0)
    esc.set_steering(90)


if __name__ == '__main__':
    main()
