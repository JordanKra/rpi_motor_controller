# Class for controlling the Hobbywing EZRUN Max 10 ESC
from time import sleep
from machine import Pin, PWM
MAX_DUTY = 65535


def map_to_range(x, in_min, in_max, out_min, out_max):
    #Python implementation of the arduino map function: https://www.arduino.cc/reference/en/language/functions/math/map/
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


class Max10:
    def __init__(self, motor_pin, servo_pin, freq):
        #Setup motor PWM
        self.motor_pwm = PWM(Pin(motor_pin))
        self.motor_pwm.freq(freq)

        #Setup servo PWM
        self.servo_pwm = PWM(Pin(servo_pin))
        self.servo_pwm.freq(freq)

        #Status LED pin setup
        self.led = Pin(25, Pin.OUT)

    def arm_esc(self):
        #According to to the docs this should just be neutral, full forward, then full reverse
        #Calculating the duty cycle is just doing   (desired_width / period) * 100%
        #Netural
        self.set_netural()
        sleep((20*2)/1000)
        self.set_forward(1.0)
        sleep((20*2)/1000)
        self.set_reverse(1.0)
        sleep(3.0)

    def set_netural(self):
        #set pin to netural
        self.motor_pwm.duty_u16(int((1.5/20.0) * MAX_DUTY))

    def set_forward(self, percent):
        # set pin to a percentage of forward
        self.motor_pwm.duty_u16(int(((1.5 + (percent * 0.5)) / 20.0) * MAX_DUTY))

    def set_reverse(self, percent):
        # set the pin to a percentage of reverse
        self.motor_pwm.duty_u16(int(((1.5 - (0.1 * 0.5)) / 20.0) * MAX_DUTY))
        sleep(20*2/1000)
        self.set_netural()
        sleep(1.0)
        self.motor_pwm.duty_u16(int(((1.5 - (percent * 0.5)) / 20.0) * MAX_DUTY))

    def servo_test(self):
        self.servo_pwm.duty_u16(int((1.8/20.0) * MAX_DUTY))
        sleep(2.0)
        self.servo_pwm.duty_u16(int((1.0/20)*MAX_DUTY))
        sleep(2.0)
        self.servo_pwm.duty_u16(int((1.4/20.0) * MAX_DUTY))
        sleep(2.0)

    def set_steering(self, angle):
        #Set servo position based on given angle
        duty = int(map_to_range(angle, 0, 180, int(((1.0/20.0)*MAX_DUTY)), int(((2.0/20.0)*MAX_DUTY))))
        self.servo_pwm.duty_u16(duty)


    def motor_test(self):
        self.led.value(1)
        self.set_forward(0.10)
        sleep(2.0)
        self.set_netural()
        sleep(2.0)
        self.set_reverse(0.10)
        sleep(2.0)


