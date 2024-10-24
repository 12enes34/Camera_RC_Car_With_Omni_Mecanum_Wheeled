import requests
import keyboard
from threading import Thread
import pygame
import time


# Mesajları saklamak için bir liste
messages = []

esp_ip = "192.168.137.158"
esp_port = 80
url = f"http://{esp_ip}:{esp_port}/"

def send_command(command):
    try:
        response = requests.post(url, data=command)
        if response.status_code == 200:
            response_text = response.text
            print(f"Command '{command}' sent successfully. Response: {response_text}")
        else:
            print(f"Failed to send command '{command}'. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending command '{command}': {e}")


def controll(FrontLeft,FrontLeftRotation,FrontRight,FrontRightRotation,BehindLeft,BehindLeftRotation,BehindRight,BehindRightRotation):
    command = f"controll,{FrontLeft},{FrontLeftRotation},{FrontRight},{FrontRightRotation},{BehindLeft},{BehindLeftRotation},{BehindRight},{BehindRightRotation}"
    print(f"Sending command: {command}")
    send_command(command)


# Motorları kontrol etme fonksiyonları
def control_left_motor(rotation=1, speed=100):
    command = f"LEFT,{rotation},{speed}"
    print(f"Sending command: {command}")
    send_command(command)

def control_right_motor(rotation=1, speed=100):
    command = f"RIGHT,{rotation},{speed}"
    print(f"Sending command: {command}")
    send_command(command)

def back_and_forth(rotation=1, speed=100):
    command = f"BackAndForth,{rotation},{speed}"
    print(f"Sending command: {command}")
    send_command(command)

def g_turn(rotation=1, speed=200):
    command = f"G_Turn,{rotation},{speed}"
    print(f"Sending command: {command}")
    send_command(command)

def control_upper_motor(rotation=1, speed=200):
    command = f"Upper,{rotation},{speed}"
    print(f"Sending command: {command}")
    '''TEST'''
    for i in range(10):#duruma gore uzatilacak TEST gerekli 
        send_command(command)
    # 2 saniye boyunca komutu çalıştır
    #start_time = time.time()
    #duration = 2  # 2 saniye

    #while time.time() - start_time < duration:
        #send_command(command)
        #time.sleep(0.1)  # 0.1 saniye aralıklarla tekrar ediyor, isteğe göre değiştirilebilir


def control_right_left_motor(right_motor_pwm=100, left_motor_pwm=100, rotation=1):
    command = f"2BackAndForth,{right_motor_pwm},{left_motor_pwm},{rotation}"
    print(f"Sending command: {command}")
    send_command(command)

def control_right_left_motor_with_rotations(right_motor_pwm=100, left_motor_pwm=100, RightRotation=1, LeftRotation=1):
    command = f"3BackAndForth,{right_motor_pwm},{left_motor_pwm},{RightRotation},{LeftRotation}"
    print(f"Sending command: {command}")
    send_command(command)

# Mesafe ölçümü
def measure_distance():
    command = "MEASURE"
    print(f"Sending command: {command}")
    send_command(command)

# Buzzer melodisini çaldırma
def play_buzzer():
    command = "BUZZER"
    print(f"Sending command: {command}")
    send_command(command)

def control_motors_with_keyboard():
    while True:
        if keyboard.is_pressed('t'):
            back_and_forth(0, 100)  # İleri hareket
        elif keyboard.is_pressed('s'):
            #back_and_forth(1, 100)  # Geri hareket
            back_and_forth(1, 255)  # Geri hareket

        elif keyboard.is_pressed('d'):
            #g_turn(1, 100)  # Sol dönüş
            g_turn(1, 255)  # Sol dönüş
        elif keyboard.is_pressed('a'):
            #g_turn(0, 100)  # Sağ dönüş
            g_turn(0, 255)  # Sağ dönüş
        elif keyboard.is_pressed('e'):
            control_right_motor(0, 100)
        elif keyboard.is_pressed('q'):
            control_left_motor(0, 100)  # WORK
        elif keyboard.is_pressed('m'):
            measure_distance()  # Mesafe ölçümü yap
        elif keyboard.is_pressed('b'):
            play_buzzer()  # Buzzer melodisini çaldır
        elif keyboard.is_pressed('r'):
            back_and_forth(0, 150)
        elif keyboard.is_pressed('f'):
            back_and_forth(0, 0)
        elif keyboard.is_pressed('y'):
            control_right_left_motor(80, 120, 1)
        elif keyboard.is_pressed('h'):
            control_right_left_motor(100, 100, 1)
        elif keyboard.is_pressed('w'):
            #control_right_left_motor_with_rotations(80, 100, 0, 0)  # Her iki motorun hem yönünü hem rotasyonunu ayrı ayrı ayarlayabiliriz
            control_right_left_motor_with_rotations(255, 255, 0, 0)  # Her iki motorun hem yönünü hem rotasyonunu ayrı ayrı ayarlayabiliriz

        elif keyboard.is_pressed("n"):
            for i in range(8):
                g_turn(1, 80)
            for i in range(4):
                back_and_forth(1, 80)
            for i in range(4):
                g_turn(0, 80)
            for i in range(4):
                back_and_forth(1, 80)
            for i in range(4):
                g_turn(0, 150)
            for i in range(4):
                back_and_forth(1, 80)
            for i in range(4):
                g_turn(1, 80)
        elif keyboard.is_pressed('u'):
            control_upper_motor(1, 255)
        elif keyboard.is_pressed('j'):
            control_upper_motor(0, 255)
        elif keyboard.is_pressed('z'):
            print("Exiting...")
            break




def control_motors_with_joystick():

    mapLambdaSpeed = lambda InputSpeedValue : (InputSpeedValue + 1) / 2 * 255
    mapLambda = lambda InputSpeedValue,InputValue : InputValue * InputSpeedValue
    pygame.init()
    pygame.joystick.init()
    speed = 0
    if pygame.joystick.get_count() == 0:
        print("Joystick bağlı değil!")
    else:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Joystick adı: {joystick.get_name()}")
        print(f"Eksen sayısı: {joystick.get_numaxes()}")
        print(f"Düğme sayısı: {joystick.get_numbuttons()}")

        treshold = 0.3
        UpperMotorUp = False
        UpperMotorDown = False
        running = True
        while running:
            #time.sleep(1) #Gecikme (Koyulma nedeni esp ye gereksiz fazla veri pompalanmamasi)
            for event in pygame.event.get():
                
                print(len(pygame.event.get()),pygame.event.get())
                
                if event.type == pygame.QUIT:
                    running = False
                
                # Joystick eksen verilerini al
                if event.type == pygame.JOYAXISMOTION:
                    # eksen 3 (gaz pedali)
                    speed = mapLambdaSpeed(-1*joystick.get_axis(3))

                
                    if abs(joystick.get_axis(1)) > treshold:
                        #eksen 1 ileri geri    
                        if -1*joystick.get_axis(1) > 0:
                            rotation = 1
                        elif -1*joystick.get_axis(1) < 0:
                            rotation = -1
                            
                        controll(rotation*mapLambda(speed,-1*joystick.get_axis(1)),rotation,rotation*mapLambda(speed,-1*joystick.get_axis(1)),rotation,rotation*mapLambda(speed,-1*joystick.get_axis(1)),rotation,rotation*mapLambda(speed,-1*joystick.get_axis(1)),rotation)

                    elif abs(joystick.get_axis(0)) > treshold:
                        #eksen 0 sag sol
                        if -1*joystick.get_axis(0) > 0:
                            
                            control_right_motor(0, speed)
                        elif -1*joystick.get_axis(0) < 0:
                            
                            control_left_motor(0, speed) #Test edilecek gerekiyorsa speed *-1 ile carpilacak
                        #g_turn(rotation,mapLambda(speed,-1*joystick.get_axis(0)))
                        # SAg sol kontrol
                        


                    elif abs(joystick.get_axis(2)) > treshold:
                        #eksen 2 G turn
                        if -1*joystick.get_axis(2) > 0:
                            rotation = 1
                        elif -1*joystick.get_axis(2) < 0:
                            rotation = -1
                            
                        g_turn(rotation,rotation*mapLambda(speed,-1*joystick.get_axis(2)))
                        #Gturn

            # Joystick düğme verilerini al
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 1:
                    print('1 e basıldı')
                    control_upper_motor(1, 255)

                if event.button == 0:
                    print('0 e basıldı')
                    control_upper_motor(0, 255)
            
                
                if event.button == 5:
                    print('5 e basıldı')
                    play_buzzer()
                
                if event.button == 3:
                    print('3 e basıldı')
                    measure_distance()
            
            if event.type == pygame.JOYBUTTONUP:
                if event.button == 1:
                    print('1 e bırakıldı')
                    UpperMotorUp = False

                if event.button == 0:
                    print('0 e bırakıldı')
                    UpperMotorDown = False
            # UpperMotorUp aktifken sürekli olarak bu işlemi yap
            
                # Joystick'ten çıkış yap
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
    # Pygame'den çık
    pygame.quit()






if __name__ == '__main__':
    # Motor kontrolünü ayrı bir thread'de çalıştır
    '''Klavye'''
    #motor_thread = Thread(target=control_motors_with_keyboard)
    motor_thread = Thread(target=control_motors_with_joystick)
    motor_thread.start()

    # Ana thread'i açık tutmak için beklet
    motor_thread.join()
