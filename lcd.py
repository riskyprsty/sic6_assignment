import ssd1306
import machine as m
i2c = m.SoftI2C(scl=m.Pin(22), sda=m.Pin(21))


def lcd(text,baris,kolom):
    oled_width = 128
    oled_height = 64
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    oled.text(text, kolom, baris)
    oled.show()