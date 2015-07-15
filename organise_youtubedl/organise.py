import os
import shutil
import subprocess
import json
import youtube_dl



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
                    result = ydl.extract_info("https://www.youtube.com/watch?v="+file[-15:-4], download=False)
                    uploader_id = result['uploader_id']
                    #json_data = json.loads(subprocess.check_output(["youtube-dl","-j", "https://www.youtube.com/watch?v="+file[-15:-4]]).decode("utf-8"))
                except youtube_dl.utils.DownloadError:
                    continue
                print(uploader_id, "/", file)

                create_dir(uploader_id)
                shutil.move(file, conf['organised_files_dir'] + "/" + uploader_id)
