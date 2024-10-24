import network

ssid = 'Tulpar'
password = '12345687'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)

while ap.active() == False:
    pass

print('Bağlantı başarılı')
print(ap.ifconfig())
