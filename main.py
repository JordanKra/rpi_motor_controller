#Tutorial main to demonstrate using user created libraries onboard the pi pico

import max_10
from time import sleep
from machine import Pin, PWM
def main():
    esc = max_10.Max10(4, 50)
    esc.arm_esc()
    while True:
        esc.motor_test()

if __name__ == '__main__':
    main()
