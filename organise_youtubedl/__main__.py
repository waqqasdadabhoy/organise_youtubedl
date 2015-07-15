import sys

import organise_youtubedl.organise

config = {
    'organised_files_dir': "Youtube"
}


def download():
    print('Download called')
    pass


def createlist():
    print('List called')
    pass

commands = {
    'download': download,
    'organise': organise_youtubedl.organise.organise(),
    'createlist': createlist
}

if __name__ == '__main__':
    if len(sys.argv) == 1 or (not sys.argv[1] in commands):
        print("Please specify an action: " + ", ".join(commands))
        exit()
    commands[sys.argv[1]](config)
