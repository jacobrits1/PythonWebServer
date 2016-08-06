from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi
import gevent
from cStringIO import StringIO
from PIL import Image
import os
# Debug with Visual Studio on Windows
import sys
import platform
import ptvsd
import exceptions
from exceptions import IOError, Exception, KeyboardInterrupt

platform_system=platform.system()

if len(sys.argv)>1:
    ptvsd.enable_attach('test') #tcp://test@raspberrypi/
    if platform_system != 'Windows':
        print "Waiting for Attach"
        ptvsd.wait_for_attach()
        print "Process Attached From Visual Studio"
# Debug end
from Good_w1_get_DS18B20_Temperature import *
from led_cont import *
from usb_camera_capture import *

chat_clients = set()


def get_temp():
    return 25

def handle_chat(ws):
    while True:
        message = ws.receive()
        if message is None:
            break
        for client in chat_clients:
            client.send("Echo:"+message)
    chat_clients.remove(ws)
def handle_command(ws):
    while True:
        message = ws.receive()
        if message is None:
            break;
        index = message.find(":")
        if((index >=1)and(index<30)):
            command= message[0:index]
            arg = message[index+1:]
            if(command=="GET_IMAGE"):
                try:
                    fp = StringIO()
                    try:
                        img = Image.open("./images/"+arg)
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
                    temps = read_temp()
                    ws.send("RET_TEMP:"+str(temps[0]))
            elif(command=="SET_LED"):
                if(platform_system ==  'Windows'):
                    if (arg.lower()=="true") or (arg=="1") :
                        print "LED=ON\n"
                    else:
                        print "LED=OFF\n"
                else:
                    if (arg.lower()=="true") or (arg=="1") :
                        set_led(True)
                        ws.send("RET_LED:True")
                    else:
                        set_led(False)
                        ws.send("RET_LED:False")
            elif(command=="GET_USB_IMAGE"):
                img=usb_camera_capture()
                fp = StringIO()
                img.save(fp,'JPEG')
                ws.send("RET_USB_IMAGE:"+fp.getvalue().encode("base64"))
            else:
                ws.send(command+": is not supported")
        else:
            ws.send("Format is COMMAND:ARG")
            ws.send("Echo:"+message)
            
def app(environ, start_response):
    path = environ["PATH_INFO"]
    if path == "/":
        start_response("200 OK", [("Content-Type", "text/html")])
        return open("index.html").readlines()
    elif path == "/chat":
        handle_chat(environ["wsgi.websocket"])
    elif path == "/command":
        try:
            handle_command(environ["wsgi.websocket"])
        except:
            pass
    else:
        filename = path[1:] #remove /
        try:
            result = open(filename).readlines()
            if(len(result)>0):
                start_response("200 OK",[("Content-Type", "text/html")])
                return result
            else:
                start_response("404 Not Founds",[])
                return []
        except IOError as e:
            start_response("404 Not Found", [])
            return []

if __name__ == "__main__":
    init_led()
    try :
        server = pywsgi.WSGIServer(("0.0.0.0",5000), app, handler_class=WebSocketHandler)
        server.serve_forever()
    except KeyboardInterrupt :
        pass
