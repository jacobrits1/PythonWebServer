from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi
import gevent
from cStringIO import StringIO
from PIL import Image
import os
import exceptions
from exceptions import IOError, Exception, KeyboardInterrupt
port_number=15328
pass_word="pass_word"

# Debug with Visual Studio on Windows
import sys
import platform
import ptvsd
platform_system=platform.system()
if len(sys.argv)>1:
    ptvsd.enable_attach('test') # tcp://test@raspberrypi/
    if platform_system != 'Windows':
        print "Waiting for Attach"
        ptvsd.wait_for_attach()
        print "Process Attached From Visual Studio"
# Debug end

from Good_w1_get_DS18B20_Temperature import TempratureSensor
from led_cont import LED
from usb_camera_capture import USBCamera
from led_pwm import LED_PWM
from Lcd16Class import Lcd16Class

led_pwm = []
def get_temp(): #dummy for windows debug
    return 25

def handle_command(env):
    isAuthed=False
    ws=env["wsgi.websocket"]
    while True:
        message = ws.receive()
        if message is None:
            break;
        index = message.find(":")
        if((index >=1)and(index<30)):
            command= message[0:index]
            arglist = message[index+1:]
            arg = arglist.split(',')
            if(command=="SET_AUTHENTICATION"):
                if arg[0]==pass_word:
                    isAuthed=True
                    ws.send("RET_AUTHENTICATION:True")
                else:
                    ws.send("RET_AUTHENTICATION:False")
            if isAuthed==True:
                if command=="GET_IMAGE":
                    try:
                        fp = StringIO()
                        try:
                            img = Image.open("./images/"+arg[0])
                        except IOError as e:
                            ws.send("ERROR :");
                            ws.send("< "+message+"");
                            ws.send("> "+e.strerror);                    
                        img.save(fp,'JPEG')
                        ws.send("RET_IMAGE:"+fp.getvalue().encode("base64"))
                    except Exception as e:
                        ws.send("ERROR :");
                        ws.send("< "+message+"");
                        ws.send("> "+e.strerror);
                elif(command=="GET_IMAGE_LIST"):
                    filelist=os.listdir('./images/')
                    filelist.sort()
                    filelist_str="`".join(filelist)
                    ws.send("RET_IMAGE_LIST:"+filelist_str)
                elif(command=="GET_SERVER_NAME"):
                    ws.send("RET_SERVER_NAME:"+ws.environ['SERVER_NAME'])
                elif(command=="GET_TEMP"):
                    if(platform_system ==  'Windows'):
                        ws.send("RET_TEMP:dummy 25.000")
                    else:
                        temps = tempsens.read_temp()
                        ws.send("RET_TEMP:"+str(temps[0]))
                elif(command=="SET_LED"):
                    if(platform_system ==  'Windows'):
                        if (arg[0].lower()=="true") or (arg[0]=="1") :
                            print "LED=ON\n"
                        else:
                            print "LED=OFF\n"
                    else:
                        if (arg[0].lower() == "true") or (arg[0] == "1") :
                            led.set(True)
                            ws.send("RET_LED:True")
                        else:
                            led.set(False)
                            ws.send("RET_LED:False")
                elif(command=="SET_LEDPWM"):
                    if len(arg) == 2:
                       led_pwm[int(arg[0])-1].lite(int(arg[1]))
                elif(command=="GET_USB_IMAGE"):
                    img=usbcamera.capture()
                    if img is not None:
                        fp = StringIO()
                        img.save(fp,'JPEG')
                        ws.send("RET_USB_IMAGE:"+fp.getvalue().encode("base64"))
                    else:
                        ws.send("RET_MESSAGE:[ERROR] USB Camera Capture ERROR")
                elif(command=="SET_LCD_MESSAGE"):
                    if len(arg)==1:
                        lcd16.string(arg[0])
                else:
                    ws.send(command+": is not supported")
            
        else:
            ws.send("Format is COMMAND:ARG")
            ws.send("Echo:"+message)
            
def app(environ, start_response):
    path = environ["PATH_INFO"]
    if path == "/":
        start_response("200 OK", [("Content-Type", "text/html")])
        return open("scripts/index.html").readlines()
    elif path == "/command":
        try:
            handle_command(environ)
        except:
            pass
    else:
        filename = path[1:] #remove /
        if filename.find("/") > -1 : #danger
            start_response("404 Not Found", [])
            return []
        try:
            result = open("scripts/"+filename).readlines()
            if(len(result)>0):
                start_response("200 OK",[("Content-Type", "text/html")])
                return result
            else:
                start_response("404 Not Founds",[])
                return []
        except IOError as e:
            start_response("404 Not Found", [])
            return []
def read_password(filename):
    if os.path.exists(filename):
        with open(filename) as f:
            lines=f.readlines()
            for line in lines:
                if line[0] != '#':
                    global pass_word
                    pass_word = line
                    break
if __name__ == "__main__":
    read_password("password.ini")
    usbcamera=USBCamera()
    tempsens=TempratureSensor()
    led=LED(12)
    led_pwm.append(LED_PWM(11))
    led_pwm.append(LED_PWM(15))
    led_pwm.append(LED_PWM(16))
    lcd16 = Lcd16Class()
    try :
        server = pywsgi.WSGIServer(("0.0.0.0",port_number), app, handler_class=WebSocketHandler)
        server.serve_forever()
    except KeyboardInterrupt :
        lcd16.clear()
