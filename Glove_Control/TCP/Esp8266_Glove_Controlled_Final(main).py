import requests
import machine
import time
from machine import I2C
import ssd1306





esp_ip = "192.168.4.2"
esp_port = 80
url = f"http://{esp_ip}:{esp_port}/"

def send_command(command):
    try:
        response = requests.post(url, data=command)
        if response.status_code == 200:
            response_text = response.text
            #print(f"Command '{command}' sent successfully. Response: {response_text}")
        else:
            #print(f"Failed to send command '{command}'. Status code: {response.status_code}")
            pass
    except requests.RequestException as e:
        #print(f"Error sending command '{command}': {e}")
        pass

def control_left_motor(rotation=1, speed=100):
    command = f"LEFT,{rotation},{speed}"
    #print(f"Sending command: {command}")
    send_command(command)

def control_right_motor(rotation=1, speed=100):
    command = f"RIGHT,{rotation},{speed}"
    #print(f"Sending command: {command}")
    send_command(command)

def back_and_forth(rotation=1, speed=100):
    command = f"BackAndForth,{rotation},{speed}"
    #print(f"Sending command: {command}")
    send_command(command)

def g_turn(rotation=1, speed=200):
    command = f"G_Turn,{rotation},{speed}"
    #print(f"Sending command: {command}")
    send_command(command)

def control_upper_motor(rotation=1, speed=200):
    command = f"Upper,{rotation},{speed}"
    #print(f"Sending command: {command}")
    send_command(command)

def control_right_left_motor(right_motor_pwm=100, left_motor_pwm=100, rotation=1):
    command = f"2BackAndForth,{right_motor_pwm},{left_motor_pwm},{rotation}"
    #print(f"Sending command: {command}")
    send_command(command)

def control_right_left_motor_with_rotations(right_motor_pwm=100, left_motor_pwm=100, RightRotation=1, LeftRotation=1):
    command = f"3BackAndForth,{right_motor_pwm},{left_motor_pwm},{RightRotation},{LeftRotation}"
    #print(f"Sending command: {command}")
    send_command(command)

def measure_distance():
    command = "MEASURE"
    #print(f"Sending command: {command}")
    send_command(command)

def play_buzzer():
    command = "BUZZER"
    #print(f"Sending command: {command}")
    send_command(command)










# I2C ayarları
i2c = I2C(scl=machine.Pin(12), sda=machine.Pin(14), freq=400000)

# SSD1306 ekran ayarları
WIDTH = 128
HEIGHT = 64
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Ekranı temizle
oled.fill(0)


def write_centered_text(text):
    text_width = len(text) * 8  # 8, yazı boyutudur (genelde 8 piksel)
    x = (WIDTH - text_width) // 2
    oled.text(text, x, 0, 1)  # text, x konumu, y konumu, 1 (renk)

def draw_right_arrow():
    oled.fill(0)
    # Dikey gövde
    oled.fill_rect(60, 27, 6, 20, 1)
    # oled.fill_rect(X,Y,WIDTH,HIGHT,RENKLI iSE 1 DEGIL ISE 0)
    x1 ,y1 ,x2 ,y2 = 52 ,27 ,72 ,27
    # ucgenin kafasinin icini doldurma
    for i in range (11):
        oled.line(x1, y1, x2, y2, 1)
        y1-=1
        y2-=1
        x2-=1
        x1+=1
    write_centered_text("SAGA")
    oled.show()

def draw_left_arrow():
    oled.fill(0)
    # Dikey gövde
    oled.fill_rect(60, 21, 6, 20, 1)  # Ok gövdesi (dikey dikdörtgen)
    # Ok başı (üçgen)
    x1, y1 = 52, 41  # Ok başının sol noktası
    x2, y2 = 72, 41  # Ok başının sağ noktası
    # Ok başı üçgenini doldurmak için
    for i in range (11):
            oled.line(x1, y1, x2, y2, 1)
            y1+=1
            y2+=1
            x2-=1
            x1+=1
    write_centered_text("SOLA")
    oled.show()

def draw_down_arrow():
    oled.fill(0)
    # Dikey gövde
    oled.fill_rect(50, 32, 20, 6, 1)  # Ok gövdesi (yatay dikdörtgen)

    # Ok başı (üçgen)
    x1, y1 = 70, 25  # Ok başının üst noktası
    x2, y2 = 70, 45  # Ok başının alt noktası

    # Ok başı üçgenini doldurmak için
    for i in range(11):
        oled.line(x1, y1, x2, y2, 1)  # Üçgenin kenarlarını çiz
        x1 += 1  # Sol kenarın X koordinatını artır
        x2 += 1  # Sağ kenarın X koordinatını artır
        y1 += 1  # Üst kenarın Y koordinatını artır
        y2 -= 1  # Alt kenarın Y koordinatını azalt
    write_centered_text("GERI")
    oled.show()

def draw_up_arrow():
    oled.fill(0)
    # Dikey gövde
    oled.fill_rect(55, 32, 20, 6, 1)  # Ok gövdesi (yatay dikdörtgen)

    # Ok başı (üçgen)
    x1, y1 = 55, 25  # Ok başının üst noktası
    x2, y2 = 55, 45  # Ok başının alt noktası

    # Ok başı üçgenini doldurmak için
    for i in range(11):
        oled.line(x1, y1, x2, y2, 1)  # Üçgenin kenarlarını çiz
        x1 -= 1  # Sol kenarın X koordinatını azalt
        x2 -= 1  # Sağ kenarın X koordinatını azalt
        y1 += 1  # Üst kenarın Y koordinatını artır
        y2 -= 1  # Alt kenarın Y koordinatını azalt
    write_centered_text("ILERI")
    oled.show()

# Fonksiyonu çağırın
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

# Ekranı güncelle

oled.show()
# Sonsuz döngü (ekranda kalması için)



























VehicleMaxSpeed=255

# I2C ayarları
i2c = I2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=400000)

# ADXL345 I2C adresi
ADXL345_ADDRESS = 0x53

# ADXL345'ün veri sayfalarına göre ayarlama
def write_register(reg, value):
    i2c.writeto(ADXL345_ADDRESS, bytearray([reg, value]))

def read_registers(reg, num):
    """Belirli bir kayıttan num kadar veri oku."""
    return i2c.readfrom_mem(ADXL345_ADDRESS, reg, num)

def setup_adxl345():
    # ADXL345'i başlat
    write_register(0x2D, 0x08)  # Power control register (ölçüm modunu etkinleştir)
    write_register(0x31, 0x0B)  # Data format register (full resolution, ±4g)

setup_adxl345()


mapLambda = lambda InputSpeedValue,InputValue : InputValue * InputSpeedValue
previous_direction = None  # Global değişken olarak tanımlayın

# İvmeölçerden veri okuma
def  controll():
    global previous_direction
    toleranceX = 0.30
    toleranceY = 0.30
    toleranceZ = 0.10
    while True:
        # X, Y ve Z eksenleri için verileri oku
        data = read_registers(0x32, 6)  # 6 byte veri oku (X, Y, Z için 2 byte her biri)

        # Verileri birleştir
        x = (data[1] << 8) | data[0]  # X ekseni
        y = (data[3] << 8) | data[2]  # Y ekseni
        z = (data[5] << 8) | data[4]  # Z ekseni

        # Negatif değer kontrolü
        if x & 0x8000:  # X ekseni için MSB kontrolü
            x -= 0x10000
        if y & 0x8000:  # Y ekseni için MSB kontrolü
            y -= 0x10000
        if z & 0x8000:  # Z ekseni için MSB kontrolü
            z -= 0x10000

        # 256 ile bölerek -4g ile +4g aralığını elde et
        x /= 256
        y /= 256
        z /= 256

        #print("X: {:.2f}, Y: {:.2f}, Z: {:.2f}".format(x, y, z))
        # z ekseni pozitif iken 
        # El ileri arac ileri
        
        # z ekseni pozitif iken 
        if z > (0 - toleranceZ):
            current_direction = None  # Şu anki yönü tanımla

            if x > (0 + toleranceX):
                control_right_left_motor_with_rotations(mapLambda(VehicleMaxSpeed, x), mapLambda(VehicleMaxSpeed, x), 1, 1)
                current_direction = "UP"  # Yönü yukarı olarak ayarla
            
            elif x < (0 - toleranceX):
                control_right_left_motor_with_rotations(mapLambda(VehicleMaxSpeed, x), mapLambda(VehicleMaxSpeed, x), 1, 1)
                current_direction = "DOWN"  # Yönü aşağı olarak ayarla

            elif y > (0 + toleranceY):
                control_right_left_motor_with_rotations(mapLambda(VehicleMaxSpeed, x), mapLambda(VehicleMaxSpeed, x), 1, 1)
                current_direction = "LEFT"  # Yönü sola olarak ayarla
            
            elif y < (0 - toleranceY):
                control_right_left_motor_with_rotations(mapLambda(VehicleMaxSpeed, x), mapLambda(VehicleMaxSpeed, x), 1, 1)
                current_direction = "RIGHT"  # Yönü sağa olarak ayarla

            # Eğer yön değişmişse oku çiz
            if current_direction != previous_direction:
                previous_direction = current_direction  # Önceki yönü güncelle
                if current_direction == "UP":
                    draw_up_arrow()
                elif current_direction == "DOWN":
                    draw_down_arrow()
                elif current_direction == "LEFT":
                    draw_left_arrow()
                elif current_direction == "RIGHT":
                    draw_right_arrow()
        else:
            previous_direction = None  # Z negatifse yönü sıfırla
        # El saga arac saga


        #time.sleep(0.5) 
        



controll()





#z Ekseni negatif iken
# el sola arac sola
# el geri arac saga









