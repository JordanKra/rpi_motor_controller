#Tutorial main to demonstrate using user created libraries onboard the pi pico

import max_10
from time import sleep
from machine import Pin, PWM
def main():
    led = Pin(25, Pin.OUT)
    # Max10(throttle control pin num, servo control pin num, freq)
    esc = max_10.Max10(4, 5, 50)
    #esc.arm_esc()
    while True:
        #esc.motor_test()
        led.value(1)
        esc.set_steering(0)
        led.value(0)
        sleep(2.0)
        esc.set_steering(60)
        led.value(1)
        sleep(2.0)
        esc.set_steering(180)
        led.value(0)
        sleep(2.0)

if __name__ == '__main__':
    main()
