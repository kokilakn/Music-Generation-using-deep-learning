rm "./static/StringInstrument.mp3"
timidity StringInstrument.mid -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k ./Static/StringInstrument.mp3