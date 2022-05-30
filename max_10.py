# Class for controlling the Hobbywing EZRUN Max 10 ESC
from time import sleep
from machine import Pin, PWM

MAX_DUTY = 65535
# Range of angles the steering wheels can achieve, assumes 90 degrees is the middle of travel
STEERING_RANGE = (65, 115)
MAX_SPEED_PERCENTAGE = 0.40


# Python implementation of the arduino map function:
# https://www.arduino.cc/reference/en/language/functions/math/map/
def map_to_range(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


# Why is this not a builtin function?
def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


class Max10:
    def __init__(self, motor_pin, servo_pin, freq):
        # Setup motor PWM
        self.motor_pwm = PWM(Pin(motor_pin))
        self.motor_pwm.freq(freq)

        # Setup servo PWM
        self.servo_pwm = PWM(Pin(servo_pin))
        self.servo_pwm.freq(freq)

        # TODO: Make this work for frequency values that are < 0.01 seconds
        self.period = (1 / freq) * 1000

        # Status LED pin setup
        self.led = Pin(25, Pin.OUT)

    def arm_esc(self):
        # Arm the esc by sending neutral, full forward, then full reverse
        self.set_neutral()
        sleep((20 * 2) / 1000)
        self.set_forward(1.0)
        sleep((20 * 2) / 1000)
        self.set_reverse(1.0)
        sleep(3.0)

    def set_neutral(self):
        # set pin to neutral
        self.motor_pwm.duty_u16(int((1.5 / self.period) * MAX_DUTY))

    def set_forward(self, percent):
        # set pin to a percentage of forward
        # Calculating the duty cycle is just doing (desired_width / period) * 100%
        self.motor_pwm.duty_u16(int(((1.5 + (clamp(percent, 0.0, MAX_SPEED_PERCENTAGE) * 0.5)) / self.period) * MAX_DUTY))

    def set_reverse(self, percent):
        # set the pin to a percentage of reverse
        # Calculating the duty cycle is just doing (desired_width / period) * 100%
        self.motor_pwm.duty_u16(int(((1.5 - (0.1 * 0.5)) / self.period) * MAX_DUTY))
        sleep(20 * 4 / 1000)
        self.set_neutral()
        sleep(4.0)
        self.motor_pwm.duty_u16(int(((1.5 - (clamp(percent, 0.0, MAX_SPEED_PERCENTAGE) * 0.5)) / self.period) * MAX_DUTY))

    def set_steering(self, angle):
        # Set servo position based on given angle, clamp steering angle to what the servo can achieve
        duty = map_to_range(clamp(angle, STEERING_RANGE[0], STEERING_RANGE[1]), STEERING_RANGE[0], STEERING_RANGE[1]
                            , int(((1.1 / self.period) * MAX_DUTY)), int(((1.9 / self.period) * MAX_DUTY)))
        self.servo_pwm.duty_u16(duty)
