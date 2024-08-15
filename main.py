"""
This code is for a simple IoT project using Pico W. 
The project consists of a web server running on Pico W,
which can be accessed by any device connected to the same network.

The web page has two buttons to turn on and off an onboard LED.
The web page also shows the temperature read by a TMP36 analog temperature
sensor connected to Pico on GP26 (ADC0).

The code was inspired by the following project:
https://projects.raspberrypi.org/en/projects/get-started-pico-w/0

Modified by: Temirlan Yergazy on 2024-08-14
"""

import network
import socket
from time import sleep
from picozero import pico_led
import machine

ssid = "your_wifi_name"
password = "your_wifi_password"

def calc_temperature(voltage):
    # y = mx + b, where y is temperature and x is voltage
    m = 104.1667 # Or same as k
    b = -54.1667
    temperature = m * voltage + b
    return round(temperature, 2)

def connect():
    #Connect to WLAN (Station interface STA_IF)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    # Try connecting to Wifi every second
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
        
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

# Open a socket on Pico, so that clients (devices w/ web browsers) can connect to it
# and access the web page
def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    
    return connection

def web_page(state, temperature):
    html = f"""
            <!DOCTYPE html>
            <html>
            <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; text-align: center; padding: 50px;">
                <h1>My First IoT Project</h1>

                <form action="/lighton" style="margin: 20px auto; display: inline-block;">
                    <input type="submit" value="Light on" style="background-color: #4CAF50; color: white; border: none; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 12px;">
                </form>
                <form action="/lightoff" style="margin: 20px auto; display: inline-block;">
                    <input type="submit" value="Light off" style="background-color: #4CAF50; color: white; border: none; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 12px;">
                </form>
                
                <p style="font-size: 18px; margin-top: 20px;">LED is {state}</p>
                <p style="font-size: 18px; margin-top: 20px;">Temperature is {temperature}</p>
            </body>
            </html>
            """
    return str(html)

def run_server(connection):
    state = 'OFF'
    pico_led.off()
    adc = machine.ADC(26)

    while True:
        try:
            adc_value = adc.read_u16()
            voltage = adc_value * (3.3 / 65535)
            temperature = calc_temperature(voltage)
            
            client = connection.accept()[0]
            request = client.recv(1024)
            request = str(request)
            print(request)
            
            try:
                request = request.split()[1]
            except IndexError:
                pass
            
            if request == '/lighton?':
                pico_led.on()
                state = 'ON'
            elif request == '/lightoff?':
                pico_led.off()
                state = 'OFF'

            html = web_page(state, temperature)
            client.send(html)
            client.close()
        except OSError as e:
            print(f"Error: {e}")
            client.close()


# Main part of the code
try:
    ip = connect()
    connection = open_socket(ip)
    run_server(connection)
except KeyboardInterrupt:
    machine.reset()
    