rm "./Static/Trumpet.mp3"
timidity Trumpet.mid -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k ./Static/Trumpet.mp3