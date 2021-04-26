rm "./Static/ElectricGuitar.mp3"
timidity Electric\ Guitar.mid -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k /Users/kokilareddy/flask_todo/Static/ElectricGuitar.mp3