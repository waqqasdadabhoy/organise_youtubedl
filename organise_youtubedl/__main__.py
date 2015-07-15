import sys

from organise_youtubedl.organise import organise
from organise_youtubedl.createlist import createlist

conf = {
    'organised_files_dir': "Youtube",
    'ydl_opts': {'proxy':'192.168.7.20:8118'},
    'list_filename': 'video_list'
}

commands = {
    'organise': organise,
    'createlist': createlist
}

if __name__ == '__main__':
    if len(sys.argv) == 1 or (not sys.argv[1] in commands):
        print("Please specify an action: " + ", ".join(commands))
        exit()
    commands[sys.argv[1]](conf)
