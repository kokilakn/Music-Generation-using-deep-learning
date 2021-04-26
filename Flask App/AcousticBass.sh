rm "./Static/AcousticBass.mp3"
timidity Acoustic\ Bass.mid -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k /Users/kokilareddy/flask_todo/Static/AcousticBass.mp3