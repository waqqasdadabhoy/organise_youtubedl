import html
import sys
import os
import shutil
import subprocess
import json
import youtube_dl
import sqlite3
import glob
import pickle
import cgi

conf = {
    'organised_files_dir': "Youtube",
    'ydl_opts': {'proxy': '192.168.7.20:8118'},
    'list_filename': 'video_list',
    'debug': True,
}


def create_dir(uploader: str, conf):
    if not os.path.exists(conf['organised_files_dir'] + "/" + uploader):
        os.makedirs(conf['organised_files_dir'] + "/" + uploader)


def is_file_youtube_download(filename: str):
    if filename[-16:-15] == "-":
        if not (" " in filename[-15:-4]):
            return True
    return False


def organise(conf):
    ydl = youtube_dl.YoutubeDL(conf['ydl_opts'])

    for file in os.listdir("."):
        if file.endswith(".mp4") or file.endswith(".flv"):
            if is_file_youtube_download(file):
                try:
                    result = ydl.extract_info("https://www.youtube.com/watch?v=" + file[-15:-4], download=False)
                    uploader_id = result['uploader_id']
                    # json_data = json.loads(subprocess.check_output(["youtube-dl","-j", "https://www.youtube.com/watch?v="+file[-15:-4]]).decode("utf-8"))
                except youtube_dl.utils.DownloadError:
                    continue
                if conf['debug']: print(uploader_id, "/", file)

                create_dir(uploader_id)
                shutil.move(file, conf['organised_files_dir'] + "/" + uploader_id)


def createlist(conf):
    pickle_path = os.path.join(conf['organised_files_dir'], conf['list_filename'] + ".pickle")
    html_path = os.path.join(conf['organised_files_dir'], conf['list_filename'] + ".html")

    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as f:
            data = pickle.load(f)
    else:
        data = {}

    ydl = youtube_dl.YoutubeDL(conf['ydl_opts'])
    for path in glob.glob(conf['organised_files_dir'] + '/*/*'):
        try:
            assert isinstance(path, str)
            if conf['debug']: print(path.encode(sys.stdout.encoding, 'replace'))
            if '\\' in path:
                file = path.split('\\')[2]
                uploader_id = path.split('\\')[1]
            else:
                file = path.split('/')[2]
                uploader_id = path.split('/')[1]

            if file.endswith(".mp4") or file.endswith(".flv") and is_file_youtube_download(file):
                video_id = file[-15:-4]
                if not video_id in data:
                    try:
                        result = ydl.extract_info("https://www.youtube.com/watch?v=" + video_id, download=False)
                        title = result['title']
                        description = result['description']
                    except youtube_dl.utils.DownloadError:
                        title = ""
                        description = ""
                    data[video_id] = [uploader_id, title, description, path]
                    if conf['debug']: print(data[video_id][1].encode(sys.stdout.encoding, 'replace'))
        except KeyboardInterrupt:
            break

    with open(pickle_path, 'wb') as f:
        pickle.dump(data, f)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write('''<html>
            <head>
                <meta charset="utf-8">
                <title>Video List</title>
            </head>
            <body>
            <table border=1>''')
        f.write('<tr><th>Video ID</th><th>Uploader ID</th><th>Video Title</th><th>Description</th>')
        for video_id in data:
            f.write('<tr><td><a href="../' + data[video_id][3] + '">' + video_id + '</a></td>')
            f.write('<td>' + data[video_id][0] + '</td>')
            f.write('<td>' + html.escape(data[video_id][1]) + '</td>')
            f.write('<td>' + html.escape(data[video_id][2]).replace("\n","<br>") + '</td>')
            f.write('</tr>')
        f.write('</table></body></html>')


commands = {
    'organise': organise,
    'createlist': createlist
}
if __name__ == '__main__':
    if len(sys.argv) == 1 or (not sys.argv[1] in commands):
        print("Please specify an action: " + ", ".join(commands))
        exit()
    commands[sys.argv[1]](conf)
