# Class for controlling the Hobbywing EZRUN Max 10 ESC
from time import sleep
from machine import Pin, PWM
MAX_DUTY = 65025

class Max10:
    def __init__(self, pin, freq):
        #Setup PWM
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
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

        return
    def set_netural(self):
        #set pin to netural
        self.pwm.duty_u16(int((1.5/20.0) * 65535))

    def set_forward(self, percent):
        # set pin to a percentage of forward
        self.pwm.duty_u16(int(((1.5 + (percent * 0.5)) / 20.0) * 65535))

    def set_reverse(self, percent):
        # set the pin to a percentage of reverse
        self.pwm.duty_u16(int(((1.5 - (0.1 * 0.5)) / 20.0) * 65535))
        sleep(20*2/1000)
        self.set_netural()
        sleep(20*4/1000)
        self.pwm.duty_u16(int(((1.5 - (percent * 0.5)) / 20.0) * 65535))

    def servo_test(self):
        for duty in range(31512, 65025):
            self.pwm.duty_u16(duty)
            sleep(0.5)
        self.pwm.duty_u16(31512)

    def motor_test(self):
        self.led.value(1)
        self.set_forward(0.10)
        sleep(2.0)
        self.set_netural()
        sleep(2.0)
        self.set_reverse(0.10)
        sleep(2.0)
        #self.pwm.duty_u16(65535)
        #self.led.value(0)



