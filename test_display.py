import time
from PIL import Image, ImageDraw, ImageFont
from radxa_zero_3w_config import RadxaZero3W

class OLED:
    def __init__(self, board):
        self.board = board
        self.width = 128  # Ajustez si nécessaire
        self.height = 64  # Ajustez si nécessaire
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.load_default()
        
        self.init_display()

    def init_display(self):
        # Séquence d'initialisation pour SH1106
        self.board.digital_write(self.board.rst_line, 0)
        time.sleep(0.1)
        self.board.digital_write(self.board.rst_line, 1)
        time.sleep(0.1)
        
        self.write_cmd(0xAE)  # display off
        self.write_cmd(0xD5)  # set display clock divide ratio/oscillator frequency
        self.write_cmd(0x80)  # set divide ratio
        self.write_cmd(0xA8)  # set multiplex ratio
        self.write_cmd(0x3F)  # 1/64 duty
        self.write_cmd(0xD3)  # set display offset
        self.write_cmd(0x00)  # no offset
        self.write_cmd(0x40)  # set start line address
        self.write_cmd(0x8D)  # set charge pump
        self.write_cmd(0x14)  # enable charge pump
        self.write_cmd(0x20)  # set memory addressing mode
        self.write_cmd(0x00)  # horizontal addressing mode
        self.write_cmd(0xA1)  # set segment re-map
        self.write_cmd(0xC8)  # set COM output scan direction
        self.write_cmd(0xDA)  # set COM pins hardware configuration
        self.write_cmd(0x12)
        self.write_cmd(0x81)  # set contrast control
        self.write_cmd(0xCF)
        self.write_cmd(0xD9)  # set pre-charge period
        self.write_cmd(0xF1)
        self.write_cmd(0xDB)  # set VCOMH deselect level
        self.write_cmd(0x40)
        self.write_cmd(0xA4)  # entire display on
        self.write_cmd(0xA6)  # set normal display
        self.write_cmd(0xAF)  # display on

    def clear(self):
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

    def show(self):
        for page in range(0, 8):
            self.write_cmd(0xB0 + page)
            self.write_cmd(0x02)  # Lower column start address
            self.write_cmd(0x10)  # Higher column start address
            
            for x in range(self.width):
                byte = 0
                for bit in range(8):
                    y = page * 8 + bit
                    if y < self.height and self.image.getpixel((x, y)) == 255:
                        byte |= (1 << bit)
                self.write_data(byte)

    def write_cmd(self, cmd):
        self.board.digital_write(self.board.dc_line, 0)
        self.board.spi_writebyte([cmd])

    def write_data(self, data):
        self.board.digital_write(self.board.dc_line, 1)
        self.board.spi_writebyte([data])

def main():
    board = RadxaZero3W()
    board.module_init()
    oled = OLED(board)

    input_states = [
        ("Key 1", board.key1_line),
        ("Key 2", board.key2_line),
        ("Key 3", board.key3_line),
        ("Joy Up", board.joy_up_line),
        ("Joy Down", board.joy_down_line),
        ("Joy Left", board.joy_left_line),
        ("Joy Right", board.joy_right_line),
        ("Joy Press", board.joy_press_line)
    ]

    try:
        while True:
            oled.clear()
            oled.draw.text((0, 0), "Radxa Zero 3W Test", font=oled.font, fill=255)
            oled.draw.text((0, 10), "Input states:", font=oled.font, fill=255)

            y_offset = 20
            for label, line in input_states:
                value = board.digital_read(line)
                state = "Pressed" if value else "Released"
                oled.draw.text((0, y_offset), f"{label}: {state}", font=oled.font, fill=255)
                y_offset += 10
                print(f"{label}: {value}")

            oled.show()
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        board.module_exit()

if __name__ == "__main__":
    main()