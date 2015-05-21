#! /usr/bin/python

import os
import subprocess


Src_dir = '/root/mp3'
Dst_dir = '/tmp/mp3'
FFMPEG = '/root/ffmpeg2.2'

current_files = os.listdir(Src_dir)

for one_file in current_files:
    #print one_file
    full_src_name = os.path.join(Src_dir, one_file)
    #print full_src_name
    full_dest_name = os.path.join(Dst_dir, one_file)

    # do transcode
    cmd = "%s -i '%s' -vn -acodec libmp3lame -ab 48k -ar 44100 -ac 1 -y '%s'" %(FFMPEG, full_src_name, full_dest_name)
    print cmd
    os.system(cmd)

