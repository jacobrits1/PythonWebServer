#from subprocess import Popen, PIPE
from subprocess import check_call
from datetime import datetime
from PIL import Image


def usb_camera_capture():
    datetime_now=datetime.now().strftime('%Y%m%d_%H%M%S') # 20160805_130532
    filename="./images/"+datetime_now+".jpg"
    check_call(["shutter2.sh", filename ])
    #p = Popen(["shutter2.sh", filename ], stdout=PIPE)
    #p.wait()
    img = Image.open(filename)
    return img

