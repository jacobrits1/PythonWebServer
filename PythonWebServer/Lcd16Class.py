import smbus
import time

class Lcd16Class:
    """Show Charactors on LCD16x2 module via smbus
    # SDA Pin 3 I2C_SDA1
    # SDC Pin 5 I2C_SCL1
    # For Checking __I2C_ADDRESS "sudo i2cdetect 1"
    """
    __I2C_ADDRESS  = 0x27 # I2C device address
    __LCD_WIDTH = 16   # Maximum characters per line
    # Hardware Delay for handshake
    __E_PULSE = 0.0005
    __E_DELAY = 0.0005
    # En bit
    __ENABLE = 0b00000100

    # Address of 1st, 2nd line
    __LCD_LINE_1 = 0x80
    __LCD_LINE_2 = 0xC0

    # Send Char or Command
    __LCD_CHAR = 1
    __LCD_COMMAND = 0

    # Backlight Control
    __LCD_BACKLIGHT_ON  = 0x08
    __LCD_BACKLIGHT_OFF = 0x00


    def __init__(self):
        self.__bus = smbus.SMBus(1) # Rev 2 Pi uses 1 and also 3
        self.__lcd_backlight = self.__LCD_BACKLIGHT_ON
        # Initialise display
        self.__lcd_byte(0x33,self.__LCD_COMMAND) # 110011 Initialise
        self.__lcd_byte(0x32,self.__LCD_COMMAND) # 110010 Initialise
        self.__lcd_byte(0x06,self.__LCD_COMMAND) # 000110 Cursor move direction
        self.__lcd_byte(0x0C,self.__LCD_COMMAND) # 001100 Display On,Cursor Off, Blink Off 
        self.__lcd_byte(0x28,self.__LCD_COMMAND) # 101000 Data length, number of lines, font size
        self.__lcd_byte(0x01,self.__LCD_COMMAND) # 000001 Clear display
        time.sleep(self.__E_DELAY)
    def clear(self):
        self.__lcd_byte(0x01, self.__LCD_COMMAND) #0x01 Clear Display

    def __lcd_toggle_enable(self, bits):
        # Toggle enable
        time.sleep(self.__E_DELAY)
        self.__bus.write_byte(self.__I2C_ADDRESS, (bits | self.__ENABLE))
        time.sleep(self.__E_PULSE)
        self.__bus.write_byte(self.__I2C_ADDRESS,(bits & ~self.__ENABLE))
        time.sleep(self.__E_DELAY)

    def __lcd_byte(self, bits, mode):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command

        bits_high = mode | (bits & 0xF0) | self.__lcd_backlight
        bits_low = mode | ((bits<<4) & 0xF0) | self.__lcd_backlight

        # High bits
        self.__bus.write_byte(self.__I2C_ADDRESS, bits_high)
        self.__lcd_toggle_enable(bits_high)

        # Low bits
        self.__bus.write_byte(self.__I2C_ADDRESS, bits_low)
        self.__lcd_toggle_enable(bits_low)


    def lcd_string1(self, message):
        line = self.__LCD_LINE_1           
        # Send string to display
        message = message.ljust(self.__LCD_WIDTH," ")
        self.__lcd_byte(line, self.__LCD_COMMAND)
        for i in range(self.__LCD_WIDTH):
            self.__lcd_byte(ord(message[i]),self.__LCD_CHAR)

    def lcd_string2(self, message):
        line = self.__LCD_LINE_2
           
        # Send string to display
        message = message.ljust(self.__LCD_WIDTH," ")
        self.__lcd_byte(line, self.__LCD_COMMAND)
        for i in range(self.__LCD_WIDTH):
            self.__lcd_byte(ord(message[i]),self.__LCD_CHAR)

    def string(self, message):
        w = self.__LCD_WIDTH
        if len(message) > w:
            message1 = message[0:w]
            message2 = message[w:]
        else:
            message1 = message;
            message2 = ""
        self.lcd_string1(message1)
        self.lcd_string2(message2)
