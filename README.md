# v-a_mp4.py

映像ファイルと音声ファイルを合わせてmp4を生成するスクリプトです。libfdk_aacが使えるffmpegが必要です。InquirerPy が必要です。WindowsのPython 3.10で動作確認しています。
```
pip install InquirerPy
```

## 使い方
```
python v-a_mp4.py
```

1. 動画ファイルのパスをきいてくるので入力もしくはドラッグ＆ドロップ。変換が必要な場合はx264、x265どちらを使うかきいてくるので選択してください。  
1. 音声ファイルのパスをきいてくるので入力もしくはドラッグ＆ドロップ。変換が必要な場合はビットレートをきいてくるで選択してください。  
1. 動画ファイルと同じ場所に「ファイル名.out.mp4」として書き出されます。

- 対応動画ファイルはmp4、ts、mkv、mov、jpg、pngです。mp4、ts、mkvの場合はコピーします。mov、jpg、pngの場合は変換します。
- 対応音声ファイルはmp4、m4a、wavです。mp4、m4aの場合はコピーします。wavの場合は変換します。
- aac変換はlibfdk_aacで行います。変更したい場合はスクリプトを直接編集してください
- videoがtsかmkvでaudioを入力しない場合、mp4にコピー変換します
- videoがjpgかpngの場合、音声の長さに合わせます

ffmpegのパスや変換プリセットはスクリプトを直接編集してください。
libfdk_aacが使えるffmpegは [ここ](https://github.com/AnimMouse/ffmpeg-stable-autobuild) などで入手できます。
