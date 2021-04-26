rm "./static/AcousticGuitar.mp3"
timidity Acoustic\ Guitar.mid -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k /Users/kokilareddy/flask_todo/Static/AcousticGuitar.mp3