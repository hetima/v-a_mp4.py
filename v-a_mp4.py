import os
from InquirerPy import inquirer

import subprocess

# videoがtsでaudioを入力しない場合、単純にts->mp4変換する
# videoがjpgかpngの場合、音声の長さに合わせる

FFMPEG_PATH = "ffmpeg"
AUDIO_CODEC = "libfdk_aac"
VIDEO_PRESETS = {
    "x264": ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-g", "90", "-preset", "slow", "-crf", "23", "-tune", "film"],
    "x265": ["-c:v", "libx265", "-pix_fmt", "yuv420p", "-g", "90", "-preset", "medium", "-crf", "26", "-tune", "ssim", "-tag:v", "hvc1"]
}
IMAGE_PRESET = ["-c:v", "libx264", "-preset", "fast", "-crf", "24", "-tune", "stillimage", "-pix_fmt", "yuv420p", "-shortest"]

def input_file_path(mess) -> str:
    v_path = inquirer.filepath(message=mess).execute()
    if len(v_path) == 0:
        return ""
    if v_path[0] == '"' or v_path[0] == "'":
        v_path = v_path[1:-1]
    if not os.path.exists(v_path):
        return ""
    return v_path

def select_bit_rate() -> str:
    dirs = ["256k", "192k", "128k"]
    slct = inquirer.rawlist(message="Select bit rate:", choices=dirs, multiselect=False).execute()
    return slct

def select_video_codec() -> list:
    dirs = list(VIDEO_PRESETS.keys())  # ["x264", "x265"]
    slct = inquirer.rawlist(message="Select video codec:", choices=dirs, multiselect=False).execute()
    return VIDEO_PRESETS[slct]

def do_wav_to_m4a(v_path):
    out_path = os.path.splitext(v_path)[0] + ".out.m4a"
    args = [FFMPEG_PATH, '-hide_banner']
    args.extend(["-i", v_path])
    a_args = ["-c:a", AUDIO_CODEC, "-ab", select_bit_rate()]
    args.extend(a_args)
    args.append(out_path)
    subprocess.run(args)

if __name__ == "__main__":
    v_path = input_file_path("video file path:")
    pre_args = []

    if v_path.endswith(".mp4") or v_path.endswith(".ts") or v_path.endswith(".mkv"):
        v_args = ["-c:v", "copy"]
    elif v_path.endswith(".mov"):
        v_args = select_video_codec()
    elif v_path.endswith(".jpg") or v_path.endswith(".jpeg") or v_path.endswith(".png"):
        pre_args = ["-loop", "1", "-r", "24"]
        v_args = IMAGE_PRESET
    elif v_path.endswith(".wav"):
        do_wav_to_m4a(v_path)
        exit(0)
    else:
        print("invalid video file")
        exit(0)

    a_path = input_file_path("audio file path:")
    if a_path.endswith(".mp4") or a_path.endswith(".m4a"):
        a_args = ["-c:a", "copy"]
    elif a_path.endswith(".wav"):
        a_args = ["-c:a", AUDIO_CODEC, "-ab", select_bit_rate()]
    else:
        if a_path == "" and (v_path.endswith(".ts") or v_path.endswith(".mkv")):
            a_path = v_path
            a_args = ["-c:a", "copy"]
        else:
            print("invalid aidio file")
            exit(0)

    out_path = os.path.splitext(v_path)[0]
    out_path = out_path + ".out.mp4"

    args = [FFMPEG_PATH, '-hide_banner']
    args.extend(pre_args)
    args.extend(["-i", v_path, "-i", a_path, "-map", "0:v", "-map", "1:a"])
    args.extend(v_args)
    args.extend(a_args)
    args.append(out_path)
    # print(args)
    subprocess.run(args)
