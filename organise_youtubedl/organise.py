import os
import shutil
import subprocess
import json


def create_dir(uploader: str, config):
    if not os.path.exists(config['organised_files_dir'] + "/" + uploader):
        os.makedirs(config['organised_files_dir'] + "/" + uploader)


def check_if_file_is_youtube_download(filename: str):
    if filename[-16:-15] == "-":
        if not (" " in filename[-15:-4]):
            return True
    return False

def organise(config):
    for file in os.listdir("."):
        if file.endswith(".mp4") or file.endswith(".flv"):
            if check_if_file_is_youtube_download(file):
                try:
                    json_data = json.loads(subprocess.check_output(["youtube-dl","-j", "https://www.youtube.com/watch?v="+file[-15:-4]]).decode("utf-8"))
                except subprocess.CalledProcessError:
                    continue
                print(json_data["uploader_id"], "/", file)

                create_dir(json_data["uploader_id"])
                shutil.move(file, config['organised_files_dir'] + "/" + json_data["uploader_id"])
