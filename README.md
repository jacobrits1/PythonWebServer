# PythonWebServer
Python Web Server for Raspberry Pi

I tested on Raspberry Pi 3

Server : gevent pywsgi.WSGIServer  
Client : javascript with jquery-1.11.3.min  
Protocol : WebSocket  
Debugging : ptvsd (and attach to Visual Studio 2015 Community on Windows10)  

Hardware control  
* Temperature : sensor DS18B20 with w1-gpio and w1-therm  
* LED ON/OFF : with RPi.GPIO  
* USB Camera Capture

Image Trasfer  
*  string transfer using base64 encoding/decoding  
