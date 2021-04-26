rm "./static/Piano.mp3"
timidity Piano.mid -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k /Users/kokilareddy/flask_todo/Static/Piano.mp3