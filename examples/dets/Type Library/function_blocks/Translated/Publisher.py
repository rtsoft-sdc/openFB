import cv2
import numpy as np
from time import sleep
from shared_memory_dict import SharedMemoryDict
import subprocess as sp

fps = 60
width = 640
height = 480
rtsp_url = 'rtsp://localhost:8554/live'
command = ['ffmpeg',
           '-re',
           '-f', 'rawvideo',
           '-s', f'{width}x{height}',
           '-pixel_format', 'bgr24',
           '-r', f'{fps}',
           '-i', '-',
           '-pix_fmt', 'yuv420p',
           '-c:v', 'libx264',
           '-bufsize', '64M',
           '-maxrate', '4M',
           '-rtsp_transport', 'tcp',
           '-f', 'rtsp',
           #'-muxdelay', '0.1',
           rtsp_url]
p = sp.Popen(command, stdin=sp.PIPE)


class Publisher:
    def __init__(self) -> None:
        image_shape = 1080  # max width, height parametr
        container_size = 15  # number of images that could be stored
        self.max_size = container_size*image_shape**2
        self.QUEUE_ID = ""
        self.fps = 30
        self.width = 640
        self.height = 480
        self.writer = ""

    def schedule(self, event_input_name, event_input_value, Enc_type: str = "x264enc", SpeedPreset: str = "ultrafast",
                 Bitrate: int = 600, KeyIntMax: int = 40, location: str = None, QUEUE_ID: str = None, IMG_ID: int = 0, QI: bool = False):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            sleep(1)
            self.smd = SharedMemoryDict(name=QUEUE_ID, size=self.max_size)
            self.writer = cv2.VideoWriter('appsrc ! videoconvert' +
                                          f' ! {Enc_type} speed-preset={SpeedPreset} bitrate={Bitrate} key-int-max={KeyIntMax}' +
                                          f' ! rtspclientsink location={location}',
                                          cv2.CAP_GSTREAMER, 0, self.fps, (self.width, self.height), True)
            return event_input_value, None, QI, "Init publisher"
        if event_input_name == 'REQ':
            "Write your handler for current event here."
            if self.writer.isOpened():
                return None, event_input_value, QI, "Can't open video writer!"
            elif not QI:
                return None, event_input_value, QI, "Source is closed!"
            else:
                frame = self.smd[str(IMG_ID)]
                self.writer.write(frame)
                return None, event_input_value, QI, "Frame  was sended to server"
