from subprocess import Popen, PIPE
#from subprocess import check_call
from datetime import datetime
from PIL import Image

class USBCamera:
    def __init__(self):
        pass
    def capture(self):
        datetime_now=datetime.now().strftime('%Y%m%d_%H%M%S') # 20160805_130532
        filename="./images/"+datetime_now+".jpg"
        try:
            p = Popen(["/usr/bin/fswebcam","-S", "3",filename], stdout=PIPE, stderr=PIPE)
            p.wait()
            #check_call(["/usr/bin/fswebcam","-S", "3",filename])
        except OSError as e:
            print str(e)
        img = Image.open(filename)
        return img

