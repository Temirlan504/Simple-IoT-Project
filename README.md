# Simple-IoT-Project

The project is a simple **IoT** project that uses a *Raspberry Pi Pico W* and a *TMP36* sensor to measure temperature. Video Tutorial on TMP36 sensor can be found [here](https://youtu.be/y_RuKoYqlJ4?si=VVFExP5LfA2FrHx7). The data is displayed on a webpage using simple html text and some in-line css. The webpage is hosted on the Pico W and can be accessed by any device on the same network as the Pico W. The project also includes a simple button that allows the user to turn ON and OFF an onboard LED on the Pico W.

The code uses MicroPython and the network and socket modules to create a simple web server on the Pico W. The server listens for incoming requests and sends the webpage to the client (device with a web browser). The network module is used to connect the Pico W to the local network and the socket module is used to create a socket object that allows the Pico W to accept connections from any client.

### Hardware
- Raspberry Pi Pico W
- TMP36 Temperature Sensor
- Breadboard
- Jumper Wires

### Software
- Thonny IDE
- MicroPython
- network module
- socket module

### Circuit Diagram
![Circuit Diagram](circuit_diagram.png)

### Code
[main.py](main.py)
