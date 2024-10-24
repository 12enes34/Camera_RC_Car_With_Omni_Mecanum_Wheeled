import requests
import keyboard
from threading import Thread

# Mesajları saklamak için bir liste
messages = []

esp_ip = "192.168.137.87"
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

# islem süresini ayarlama (eldiven icin)
def SetProcessTime(delayTime):
    command = f"TIME,{delayTime}"
    print(f"Sending command: {command}")
    send_command(command)

# Motorları kontrol etme fonksiyonları
def controll(FrontLeft,FrontLeftRotation,FrontRight,FrontRightRotation,BehindLeft,BehindLeftRotation,BehindRight,BehindRightRotation):
    command = f"controll,{FrontLeft},{FrontLeftRotation},{FrontRight},{FrontRightRotation},{BehindLeft},{BehindLeftRotation},{BehindRight},{BehindRightRotation}"
    print(f"Sending command: {command}")
    send_command(command)

# Buzzer melodisini çaldırma
def play_buzzer():
    command = "BUZZER"
    print(f"Sending command: {command}")
    send_command(command)

def control_motors():
    while True:
#       Normal Control
        if keyboard.is_pressed('w'):
            controll(FrontLeft=250,FrontLeftRotation=1,FrontRight=250,FrontRightRotation=1,BehindLeft=250,BehindLeftRotation=1,BehindRight=250,BehindRightRotation=1)
        elif keyboard.is_pressed('a'):
            controll(FrontLeft=250,FrontLeftRotation=0,FrontRight=250,FrontRightRotation=1,BehindLeft=250,BehindLeftRotation=0,BehindRight=250,BehindRightRotation=1)
        elif keyboard.is_pressed('s'):
            controll(FrontLeft=250,FrontLeftRotation=0,FrontRight=250,FrontRightRotation=0,BehindLeft=250,BehindLeftRotation=0,BehindRight=250,BehindRightRotation=0)
        elif keyboard.is_pressed('d'):
            controll(FrontLeft=250,FrontLeftRotation=1,FrontRight=250,FrontRightRotation=0,BehindLeft=250,BehindLeftRotation=1,BehindRight=250,BehindRightRotation=0)


#       Side Way(yengec)
        elif keyboard.is_pressed('q'):
            controll(FrontLeft=250,FrontLeftRotation=0,FrontRight=250,FrontRightRotation=1,BehindLeft=250,BehindLeftRotation=1,BehindRight=250,BehindRightRotation=0)
        elif keyboard.is_pressed('e'):
            controll(FrontLeft=250,FrontLeftRotation=1,FrontRight=250,FrontRightRotation=0,BehindLeft=250,BehindLeftRotation=0,BehindRight=250,BehindRightRotation=1)


#       Diogonal(capraz)
        elif keyboard.is_pressed('r'):
            controll(FrontLeft=0,FrontLeftRotation=0,FrontRight=250,FrontRightRotation=1,BehindLeft=250,BehindLeftRotation=1,BehindRight=0,BehindRightRotation=0)
        elif keyboard.is_pressed('t'):
            controll(FrontLeft=250,FrontLeftRotation=1,FrontRight=0,FrontRightRotation=0,BehindLeft=0,BehindLeftRotation=0,BehindRight=250,BehindRightRotation=1)
        elif keyboard.is_pressed('f'):
            controll(FrontLeft=250,FrontLeftRotation=0,FrontRight=0,FrontRightRotation=1,BehindLeft=0,BehindLeftRotation=1,BehindRight=250,BehindRightRotation=0)
        elif keyboard.is_pressed('g'):
            controll(FrontLeft=0,FrontLeftRotation=1,FrontRight=250,FrontRightRotation=0,BehindLeft=250,BehindLeftRotation=0,BehindRight=0,BehindRightRotation=1)


#       Turn of rear axis(arka sabit donus)
        elif keyboard.is_pressed('u'):
            controll(FrontLeft=250,FrontLeftRotation=1,FrontRight=250,FrontRightRotation=0,BehindLeft=0,BehindLeftRotation=0,BehindRight=0,BehindRightRotation=0)
        elif keyboard.is_pressed('y'):
            controll(FrontLeft=250,FrontLeftRotation=0,FrontRight=250,FrontRightRotation=1,BehindLeft=0,BehindLeftRotation=0,BehindRight=0,BehindRightRotation=0)
#       Turn of front axis(on sabit donus)
        elif keyboard.is_pressed('h'):
            controll(FrontLeft=0,FrontLeftRotation=0,FrontRight=0,FrontRightRotation=0,BehindLeft=250,BehindLeftRotation=1,BehindRight=250,BehindRightRotation=0)
        elif keyboard.is_pressed('j'):
            controll(FrontLeft=0,FrontLeftRotation=0,FrontRight=0,FrontRightRotation=0,BehindLeft=250,BehindLeftRotation=0,BehindRight=250,BehindRightRotation=1)

#       Turn of right axis(sag sabit donus)
        elif keyboard.is_pressed('z'):
            controll(FrontLeft=0,FrontLeftRotation=0,FrontRight=250,FrontRightRotation=1,BehindLeft=0,BehindLeftRotation=0,BehindRight=250,BehindRightRotation=1)
        elif keyboard.is_pressed('x'):
            controll(FrontLeft=250,FrontLeftRotation=1,FrontRight=0,FrontRightRotation=0,BehindLeft=250,BehindLeftRotation=1,BehindRight=0,BehindRightRotation=0)

#       Turn of left axis(sol sabit donus)
        elif keyboard.is_pressed('c'):
            controll(FrontLeft=250,FrontLeftRotation=0,FrontRight=0,FrontRightRotation=0,BehindLeft=250,BehindLeftRotation=0,BehindRight=0,BehindRightRotation=0)
        elif keyboard.is_pressed('v'):
            controll(FrontLeft=0,FrontLeftRotation=0,FrontRight=250,FrontRightRotation=0,BehindLeft=0,BehindLeftRotation=0,BehindRight=250,BehindRightRotation=0)

        elif keyboard.is_pressed('b'):
            play_buzzer()  # Buzzer melodisini çaldır

        elif keyboard.is_pressed('y'):
            pass
        elif keyboard.is_pressed('h'):
            pass

        elif keyboard.is_pressed('j'):
            pass

        elif keyboard.is_pressed('1'):
            print("Exiting...")
            break

if __name__ == '__main__':
    # Motor kontrolünü ayrı bir thread'de çalıştır
    motor_thread = Thread(target=control_motors)
    motor_thread.start()

    # Ana thread'i açık tutmak için beklet
    motor_thread.join()
