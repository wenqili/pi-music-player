#!/user/bin/python

import os
import subprocess
import glob
f = glob.glob('*mp3')
pointer = 0

status = 1
volume = 8
os.chdir('/home/pi/music_player/')

playPath = "/home/pi/music_player/track.mp3"
if __name__ == '__main__':
    try:
        while True:
            if (status == 1):
                player = subprocess.Popen(["omxplayer", f[pointer]], stdin=subprocess.PIPE)
                status = 0;
                # print ["omxplayer",]
                
    except KeyboardInterrupt:
        print("Stopped by user") 