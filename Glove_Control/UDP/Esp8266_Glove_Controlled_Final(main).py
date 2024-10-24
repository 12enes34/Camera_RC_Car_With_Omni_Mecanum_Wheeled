import socket
import machine
import time
from machine import I2C
import ssd1306
import framebuf

# UDP ayarları
UDP_IP = "192.168.4.2"  # ESP32'nin IP adresi
UDP_PORT = 8888  # Kullanacağınız UDP portu

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP soketi oluştur

def send_command(command):
    try:
        sock.sendto(command.encode(), (UDP_IP, UDP_PORT))  # Komutu UDP ile gönder
        #print(f"Command '{command}' sent successfully.")
    except Exception as e:
        #print(f"Error sending command '{command}': {e}")
        pass

def controll(FrontLeft, FrontLeftRotation, FrontRight, FrontRightRotation, BehindLeft, BehindLeftRotation, BehindRight, BehindRightRotation):
    command = f"controll,{FrontLeft},{FrontLeftRotation},{FrontRight},{FrontRightRotation},{BehindLeft},{BehindLeftRotation},{BehindRight},{BehindRightRotation}"
    print(f"Sending command: {command}")
    send_command(command)

def play_buzzer():
    command = "BUZZER"
    send_command(command)

# Set Process time (for hand controller)
def SetProcessTime(delayTime):
    command = f"TIME,{delayTime}"
    print(f"Sending command: {command}")
    send_command(command)

# I2C ayarları
i2c = I2C(scl=machine.Pin(12), sda=machine.Pin(14), freq=400000)

# SSD1306 ekran ayarları
WIDTH = 128
HEIGHT = 64
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Ekranı temizle
oled.fill(0)



def write_rotated_text(text):
    

    for i, char in enumerate(text):
        # Her karakteri framebuffer kullanarak çiz
        buf = bytearray(8 * 8 // 8)  # 8x8 boyutunda bir buffer oluştur
        fbuf = framebuf.FrameBuffer(buf, 8, 8, framebuf.MONO_HLSB)
        fbuf.text(char, 0, 0)  # Metni buffer üzerine yaz

        # Buffer'i -90 derece döndür ve OLED ekrana bas
        for x in range(8):
            for y in range(8):
                if fbuf.pixel(x, y):
                    # Pikseli -90 derece döndürerek ekrana yaz
                    oled.pixel(y, 63 - (i * 10 + x), 1)

    oled.show()



def write_centered_text(text):
    text_width = len(text) * 8  # 8, yazı boyutudur (genelde 8 piksel)
    x = (WIDTH - text_width) // 2
    oled.text(text, x, 0, 1)  # text, x konumu, y konumu, 1 (renk)

def draw_right_arrow():
    oled.fill(0)
    oled.fill_rect(60, 27, 6, 20, 1)
    x1, y1, x2, y2 = 52, 27, 72, 27
    for i in range(11):
        oled.line(x1, y1, x2, y2, 1)
        y1 -= 1
        y2 -= 1
        x2 -= 1
        x1 += 1
    write_rotated_text(' SAGA ')
    oled.show()

def draw_left_arrow():
    oled.fill(0)
    oled.fill_rect(60, 21, 6, 20, 1)
    x1, y1 = 52, 41
    x2, y2 = 72, 41
    for i in range(11):
        oled.line(x1, y1, x2, y2, 1)
        y1 += 1
        y2 += 1
        x2 -= 1
        x1 += 1
    write_rotated_text(' SOLA ')
    oled.show()

def draw_down_arrow():
    oled.fill(0)
    oled.fill_rect(50, 32, 20, 6, 1)
    x1, y1 = 70, 25
    x2, y2 = 70, 45
    for i in range(11):
        oled.line(x1, y1, x2, y2, 1)
        x1 += 1
        x2 += 1
        y1 += 1
        y2 -= 1
    write_rotated_text(' GERI ')
    oled.show()

def draw_up_arrow():
    oled.fill(0)
    oled.fill_rect(55, 32, 20, 6, 1)
    x1, y1 = 55, 25
    x2, y2 = 55, 45
    for i in range(11):
        oled.line(x1, y1, x2, y2, 1)
        x1 -= 1
        x2 -= 1
        y1 += 1
        y2 -= 1
    write_rotated_text(' ILERI')
    oled.show()

def arrow():
    for i in range(5):
        draw_left_arrow()
        oled.show()
        time.sleep(1)
        oled.fill(0)

        draw_right_arrow()
        oled.show()
        time.sleep(1)
        oled.fill(0)

        draw_down_arrow()
        oled.show()
        time.sleep(1)
        oled.fill(0)

        draw_up_arrow()
        oled.show()
        time.sleep(1)
        oled.fill(0)

oled.text('AKTIF', 0, 0, 1)
oled.show()


VehicleMaxSpeed = 255
i2c = I2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)

# ADXL345 I2C adresi
ADXL345_ADDRESS = 0x53

def write_register(reg, value):
    i2c.writeto(ADXL345_ADDRESS, bytearray([reg, value]))

def read_registers(reg, num):
    return i2c.readfrom_mem(ADXL345_ADDRESS, reg, num)

def setup_adxl345():
    # ADXL345'i başlat
    write_register(0x2D, 0x08)  # Power control register (ölçüm modunu etkinleştir)
    write_register(0x31, 0x0B)  # Data format register (full resolution, ±4g)

setup_adxl345()

mapLambda = lambda InputSpeedValue, InputValue: InputValue * InputSpeedValue
previous_direction = None

def controlls():
    global previous_direction
    toleranceX = 0.30
    toleranceY = 0.30
    toleranceZ = 0.10
    while True:
        data = read_registers(0x32, 6)

        x = (data[1] << 8) | data[0]
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]

        if x & 0x8000:
            x -= 0x10000
        if y & 0x8000:
            y -= 0x10000
        if z & 0x8000:
            z -= 0x10000

        x /= 256
        y /= 256
        z /= 256
        
        if z > (0 - toleranceZ):
            current_direction = None
            
            if x > (0 + toleranceX):
                speed = mapLambda(VehicleMaxSpeed, x)
                controll(FrontLeft=speed, FrontLeftRotation=1, FrontRight=speed, FrontRightRotation=1, BehindLeft=speed, BehindLeftRotation=1, BehindRight=speed, BehindRightRotation=1)
                current_direction = "UP"

            elif x < (0 - toleranceX):
                speed = mapLambda(VehicleMaxSpeed, x)
                speed = speed * -1
                controll(FrontLeft=speed, FrontLeftRotation=0, FrontRight=speed, FrontRightRotation=0, BehindLeft=speed, BehindLeftRotation=0, BehindRight=speed, BehindRightRotation=0)
                current_direction = "DOWN"

            elif y > (0 + toleranceY):
                speed = mapLambda(VehicleMaxSpeed, y)
                controll(FrontLeft=speed, FrontLeftRotation=0, FrontRight=speed, FrontRightRotation=1, BehindLeft=speed, BehindLeftRotation=0, BehindRight=speed, BehindRightRotation=1)
                current_direction = "LEFT"

            elif y < (0 - toleranceY):
                speed = mapLambda(VehicleMaxSpeed, y)
                controll(FrontLeft=speed, FrontLeftRotation=1, FrontRight=speed, FrontRightRotation=0, BehindLeft=speed, BehindLeftRotation=1, BehindRight=speed, BehindRightRotation=0)
                current_direction = "RIGHT"

            print(mapLambda(VehicleMaxSpeed, x))
        
            if current_direction != previous_direction:
                previous_direction = current_direction
                if current_direction == "UP":
                    draw_up_arrow()
                elif current_direction == "DOWN":
                    draw_down_arrow()
                elif current_direction == "LEFT":
                    draw_left_arrow()
                elif current_direction == "RIGHT":
                    draw_right_arrow()
        else:
            previous_direction = None

            if x < (0 - toleranceX):
                speed = mapLambda(VehicleMaxSpeed, x)
                speed = speed * -1
                controll(FrontLeft=speed, FrontLeftRotation=1, FrontRight=speed, FrontRightRotation=0, BehindLeft=speed, BehindLeftRotation=0, BehindRight=speed, BehindRightRotation=1)
                current_direction = "RIGHT"#Belki saga donus
            elif y < (0 - toleranceY):
                speed = mapLambda(VehicleMaxSpeed, y)
                speed = speed * -1
                controll(FrontLeft=speed, FrontLeftRotation=0, FrontRight=speed, FrontRightRotation=1, BehindLeft=speed, BehindLeftRotation=1, BehindRight=speed, BehindRightRotation=0)
                current_direction = "LEFT"



#SetProcessTime(500)
time.sleep(5)
controlls()



