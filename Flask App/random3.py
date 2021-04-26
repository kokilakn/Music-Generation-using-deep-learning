

import subprocess
from pydub import AudioSegment
from random import sample
def generate_all():
    subprocess.call(['python3', 'Piano.py'])
    subprocess.call(['python3', 'ElectricGuitar.py'])
    subprocess.call(['python3', 'StringInstrument.py'])
    subprocess.call(['python3', 'Trumpet.py'])
    subprocess.call(['python3', 'Acoustic Guitar.py'])
    subprocess.call(['python3', 'AcousticBass.py'])
def generate_random3():
    instruments=["AcousticGuitar.mp3","ElectricGuitar.mp3","Piano.mp3","StringInstrument.mp3"]
    sequence=[i for i in range(len(instruments))]
    randominstruments=sample(sequence,3)
    sound1 = AudioSegment.from_mp3("./Static/"+instruments[randominstruments[0]])
    sound2 = AudioSegment.from_mp3("./Static/"+instruments[randominstruments[1]])
    sound3 = AudioSegment.from_mp3("./Static/"+instruments[randominstruments[2]])
    # mix sound2 with sound1, starting at 5000ms into sound1)
    output = sound1.overlay(sound2, position=2000)
    output = output.overlay(sound3, position=4000)
    print("done")
    output.export("./Static/mixed_sounds.mp3", format="mp3")

if __name__=='__main__':
    generate_all()
    generate_random3()

