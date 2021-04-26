from flask import Flask, render_template
import subprocess
app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/Piano')
def Piano():
    subprocess.call(['python3', 'Piano.py'])
    return render_template('Piano.html')

@app.route('/Electricguitar')
def Electricguitar():
    subprocess.call(['python3', 'Electricguitar.py'])
    return render_template('Electricguitar.html')

@app.route('/Stringinstrument')
def Stringinstrument():
    subprocess.call(['python3', 'StringInstrument.py'])
    return render_template('Stringinstrument.html')

@app.route('/Trumpet')
def Trumpet():
    subprocess.call(['python3', 'Trumpet.py'])
    return render_template('Trumpet.html')

@app.route('/Acousticguitar')
def Acousticguitar():
    subprocess.call(['python3', 'AcousticGuitar.py'])
    return render_template('Acousticguitar.html')

@app.route('/AcousticBass')
def AcousticBass():
    subprocess.call(['python3', 'AcousticBass.py'])
    return render_template('AcousticBass.html')

@app.route('/3')
def _3():
    return render_template('3.html')

@app.route('/6')
def _6():
   return render_template('6.html')
if __name__ == '__main__':
   app.run()
