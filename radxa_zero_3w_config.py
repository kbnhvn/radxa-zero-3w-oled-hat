import time
import spidev
import gpiod

# Pin definition for Radxa Zero 3W
RST_PIN = (3, 17)  # gpiochip3, line 17
DC_PIN = (3, 10)   # gpiochip3, line 10
CS_PIN = (4, 22)   # gpiochip4, line 22

# GPIO pin definitions for joystick and buttons
KEY1_PIN = (3, 5)      # gpiochip3, line 5
KEY2_PIN = (3, 6)      # gpiochip3, line 6
KEY3_PIN = (3, 7)      # gpiochip3, line 7
JOY_UP_PIN = (3, 12)   # gpiochip3, line 12
JOY_DOWN_PIN = (3, 4)  # gpiochip3, line 4
JOY_LEFT_PIN = (3, 11) # gpiochip3, line 11
JOY_RIGHT_PIN = (1, 4) # gpiochip1, line 4
JOY_PRESS_PIN = (3, 19)# gpiochip3, line 19

LINE_REQ_DIR_IN = gpiod.LINE_REQ_DIR_IN
LINE_REQ_FLAG_BIAS_PULL_UP = gpiod.LINE_REQ_FLAG_BIAS_PULL_UP

class RadxaZero3W:
    def __init__(self, spi=spidev.SpiDev(3, 0), spi_freq=40000000):
        self.spi = spi
        self.spi.max_speed_hz = spi_freq
        self.spi.mode = 0b11

        # Initialize GPIO chips
        self.chips = {
            1: gpiod.Chip('gpiochip1'),
            3: gpiod.Chip('gpiochip3'),
            4: gpiod.Chip('gpiochip4')
        }

        # Setup GPIO lines
        self.rst_line = self.setup_line(RST_PIN, 1)  # 1 for output
        self.dc_line = self.setup_line(DC_PIN, 1)    # 1 for output
        self.cs_line = self.setup_line(CS_PIN, 1)    # 1 for output

        # Setup input lines
        # Configuration des boutons
        self.key1_line = self.setup_input(KEY1_PIN)
        self.key2_line = self.setup_input(KEY2_PIN)
        self.key3_line = self.setup_input(KEY3_PIN)
        self.joy_up_line = self.setup_input(JOY_UP_PIN)
        self.joy_down_line = self.setup_input(JOY_DOWN_PIN)
        self.joy_left_line = self.setup_input(JOY_LEFT_PIN)
        self.joy_right_line = self.setup_input(JOY_RIGHT_PIN)
        self.joy_press_line = self.setup_input(JOY_PRESS_PIN)

    def setup_line(self, pin, direction):
        chip_num, line_offset = pin
        chip = self.chips[chip_num]
        line = chip.get_line(line_offset)
        if direction:
            line.request(consumer="RadxaZero3W", type=gpiod.LINE_REQ_DIR_OUT)
        else:
            line.request(consumer="RadxaZero3W", type=gpiod.LINE_REQ_DIR_IN)
        return line
    
    def setup_input(self, pin):
        chip_num, line_offset = pin
        chip = self.chips[chip_num]
        line = chip.get_line(line_offset)
        line.request(consumer="RadxaZero3W", 
                    type=gpiod.LINE_REQ_DIR_IN)
        return line

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def digital_write(self, line, value):
        line.set_value(value)

    def digital_read(self, line):
        return line.get_value()

    def spi_writebyte(self, data):
        self.spi.writebytes([data[0]])

    def module_init(self):
        self.digital_write(self.rst_line, 0)
        self.digital_write(self.dc_line, 0)
        self.digital_write(self.cs_line, 1)  # CS high (inactive)
        return 0

    def module_exit(self):
        self.spi.close()
        self.digital_write(self.rst_line, 0)
        self.digital_write(self.dc_line, 0)
        self.digital_write(self.cs_line, 1)  # CS high (inactive)

        # Release all GPIO lines
        for chip in self.chips.values():
            chip.close()