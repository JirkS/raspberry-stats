#!/usr/bin/python
# -*- coding:utf-8 -*-
import psutil
import sys
import os
import re, subprocess
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
import time
import traceback
from waveshare_OLED import OLED_1in5_rgb
from PIL import Image,ImageDraw,ImageFont
logging.basicConfig(level=logging.DEBUG)

try:
        disp = OLED_1in5_rgb.OLED_1in5_rgb()
        logging.info("\r 1.5inch rgb OLED ")
        # Initialize library.
        disp.Init()
        # Clear display.
        logging.info("clear display")
        disp.clear()

        # Create blank image for drawing.
        print("script is running!")
        image1 = Image.new('RGB', (disp.width, disp.height), 0)
        draw = ImageDraw.Draw(image1)
        font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
        font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        font2 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)


        def check_CPU_temp():
            err, msg = subprocess.getstatusoutput('vcgencmd measure_temp')
            return msg

        def get_CPU_use():
            load1, load5, load15 = psutil.getloadavg()
            return str(round((load15/os.cpu_count() * 100), 1))

        def get_RAM_info():
            p = os.popen('free')
            i = 0
            while True:
                i = i + 1
                line = p.readline()
                if i==2:
                    return(line.split()[1:4])

        def get_Ram_percent(r_u, r_t):
            return str(round(float(r_u) / (float(r_t) / 100), 1))

        def get_Disk_info():
            p = os.popen("df -h /")
            i = 0
            while 1:
                i = i +1
                line = p.readline()
                if i==2:
                    return(line.split()[1:5])

        def get_Disk_percent(d_u, d_t):
            return str(round(float(d_u) / (float(d_t) / 100), 1))

        num = 0
        while True:
            cpu_temp = check_CPU_temp()
            cpu_temp = cpu_temp[5:len(cpu_temp)]
            cpu_usage = get_CPU_use()
            ram_stats = get_RAM_info()
            ram_total = str(int(round(int(ram_stats[0]) / 1000,1)))
            ram_used = str(int(round(int(ram_stats[1]) / 1000,1)))
            ram_free = str(int(round(int(ram_stats[2]) / 1000,1)))
            disk_stats = get_Disk_info()
            disk_total = str(disk_stats[0])[0:len(str(disk_stats[0]))-1]
            disk_used = str(disk_stats[1])[0:len(str(disk_stats[1]))-1]
            disk_free = str(disk_stats[2])
            # logging.info("***draw CPU temp and usage")
            draw.text((5, 0), 'CPU: ' + cpu_temp + "   " + cpu_usage + "%", font = font, fill = "BLUE")
            draw.line([(0, 0), (100, 0)], fill=1)
            draw.text((5, 20), 'RAM:\n' + ram_used + " / " + ram_total + " MB   " + get_Ram_percent(ram_used, ram_total) + "%", font=font, fill="BLUE")
            draw.text((5, 60), 'DISK:\n' + disk_used + " / " + disk_total + " GB   " + get_Disk_percent(disk_used, disk_total) + "%", font=font, fill="BLUE")
            draw.text((5, 100), 'PUBLIC IP:\n89.176.120.30', font=font, fill="BLUE")
            image1 = image1.rotate(0)
            disp.ShowImage(disp.getbuffer(image1))
            time.sleep(5)
            image1 = Image.new('RGB', (disp.width, disp.height), 0)
            draw = ImageDraw.Draw(image1)
            num += 1

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    disp.module_exit()
    exit()