import subprocess
from pydub import AudioSegment
from random import sample
def generate_all():
    subprocess.call(['python3', 'Piano.py'])
    subprocess.call(['python3', 'Electricguitar.py'])
    subprocess.call(['python3', 'StringInstrument.py'])
    subprocess.call(['python3', 'Trumpet.py'])
    subprocess.call(['python3', 'AcousticGuitar.py'])
    subprocess.call(['python3', 'AcousticBass.py'])
def Mix():
    #"AcousticBass.mp3","AcousticGuitar.mp3","ElectricGuitar.mp3","Piano.mp3","StringInstrument.mp3","Trumpet.mp3"
    sound1 = AudioSegment.from_mp3("./static/AcousticBass.mp3")
    sound2 = AudioSegment.from_mp3("./static/AcousticGuitar.mp3")
    sound3 = AudioSegment.from_mp3("./static/ElectricGuitar.mp3")
    sound4 = AudioSegment.from_mp3("./static/Piano.mp3")
    sound5 = AudioSegment.from_mp3("./static/StringInstrument.mp3")
    sound6 = AudioSegment.from_mp3("./static/Trumpet.mp3")
    output1 = sound1.overlay(sound2, position=2000)
    output2 = output1.overlay(sound3, position=4000)
    output3 = output2.overlay(sound4, position=6000)
    output4 = output3.overlay(sound5, position=8000)
    output5=  output4.overlay(sound6,  position=9000)
    output5.export("./static/All_sounds.mp3", format="mp3")
if __name__=='__main__':
    generate_all()
    Mix()
