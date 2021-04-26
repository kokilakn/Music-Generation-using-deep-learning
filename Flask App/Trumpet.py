#!/usr/bin/env python
# coding: utf-8

# In[1]:


from music21 import *
import csv
import numpy as np


# In[2]:


def read_midi(file):
    
    notes=[]
    notes_to_parse = None
    
    #parsing a midi file
    midi = converter.parse(file)
  
    #grouping based on different instruments
    s2 = instrument.partitionByInstrument(midi)

    #Looping over all the instruments
    for part in s2.parts:
    
        #select elements of only piano
        if 'Trumpet' in str(part): 
            notes_to_parse = part.recurse() 
      
            #finding whether a particular element is note or a chord
            for element in notes_to_parse:
                
                #note
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                
                #chord
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))

    return np.array(notes)

import os
import os.path
if (os.path.isfile("Trumpet.csv") == False):
    path='/Users/kokilareddy/Downloads/midis/Guitar_midkar.com_MIDIRip/jazz/'

    #read all the filenames
    files=[i for i in os.listdir(path) if i.endswith(".mid")]

    #reading each midi file
    notes_array = np.array([read_midi(path+i) for i in files])
    
    import csv
    with open("Trumpet.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(notes_array)
else:
    data_2d = []
    with open('Trumpet.csv', newline='\n') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            data_2d.append([x for x in row])
    i=0;
    for music in data_2d:
        if (music):
            data_2d[i] = music[0].split(",")
        i+=1
    notes_array = data_2d
    


# In[3]:


#converting 2D array into 1D array
notes_ = [element for note_ in notes_array for element in note_]

#No. of unique notes
unique_notes = list(set(notes_))
print(len(unique_notes))


# In[4]:


#importing library
from collections import Counter

#computing frequency of each note
freq = dict(Counter(notes_))

#library for visualiation
import matplotlib.pyplot as plt

#consider only the frequencies
no=[count for _,count in freq.items()]


# In[5]:


frequent_notes = [note_ for note_, count in freq.items() if count>=50]
print(len(frequent_notes))


# In[6]:


new_music=[]

for notes in notes_array:
    temp=[]
    for note_ in notes:
        if note_ in frequent_notes:
            temp.append(note_)            
    new_music.append(temp)
    
new_music = np.array(new_music)


# In[7]:


no_of_timesteps = 32
x = []
y = []

for note_ in new_music:
    for i in range(0, len(note_) - no_of_timesteps, 1):
        
        #preparing input and output sequences
        input_ = note_[i:i + no_of_timesteps]
        output = note_[i + no_of_timesteps]
        
        x.append(input_)
        y.append(output)
        
x=np.array(x)
y=np.array(y)


# In[8]:


unique_x = list(set(x.ravel()))
x_note_to_int = dict((note_, number) for number, note_ in enumerate(unique_x))
#preparing input sequences
x_seq=[]
for i in x:
    temp=[]
    for j in i:
        #assigning unique integer to every note
        temp.append(x_note_to_int[j])
    x_seq.append(temp)
    
x_seq = np.array(x_seq)


# In[9]:


unique_y = list(set(y))
y_note_to_int = dict((note_, number) for number, note_ in enumerate(unique_y)) 
y_seq=np.array([y_note_to_int[i] for i in y])


# In[10]:


from sklearn.model_selection import train_test_split
x_tr, x_val, y_tr, y_val = train_test_split(x_seq,y_seq,test_size=0.2,random_state=0)
x_tr = np.reshape(x_tr, (x_tr.shape[0], no_of_timesteps, 1))
x_val = np.reshape(x_val, (x_val.shape[0], no_of_timesteps, 1))


# In[11]:


def lstm():
    model = Sequential()
    model.add(LSTM(128,return_sequences=True, input_shape = (x_tr.shape[1], 1)))
    model.add(LSTM(128))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dense(len(unique_y)))
    model.add(Activation('softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')
    return model


# In[12]:


from keras.layers import *
from keras.models import *
from keras.callbacks import *
import keras.backend as K
import os

K.clear_session()
if(os.path.isfile("Trumpet.h5") == False):
    model=lstm()
    mc=ModelCheckpoint('Trumpet.h5', monitor='val_loss', mode='min', save_best_only=True,verbose=1)
    history = model.fit(np.array(x_tr),np.array(y_tr),batch_size=128,
                        epochs=30, validation_data=(np.array(x_val),np.array(y_val)),
                        verbose=1, callbacks=[mc])


# In[13]:


#loading best model
from keras.models import load_model
model = load_model('Trumpet.h5')


# In[14]:


def prediction():
    import random
    ind = np.random.randint(0,len(x_val)-1)

    random_music = x_val[ind]

    predictions=[]
    for i in range(30):

        random_music = random_music.reshape(1,no_of_timesteps,1)

        prob  = model.predict(random_music)[0]
        y_pred= np.argmax(prob,axis=0)
        predictions.append(y_pred)

        random_music = np.insert(random_music[0],len(random_music[0]),y_pred)
        random_music = random_music[1:]

    print(predictions)

    x_int_to_note = dict((number, note_) for number, note_ in enumerate(unique_x)) 
    predicted_notes = [x_int_to_note[i] for i in predictions]
    return predicted_notes


# In[15]:


def convert_to_midi(prediction_output):
   
    offset = 0
    output_notes = []

    # create note and chord objects based on the values generated by the model
    for pattern in prediction_output:
        
        # pattern is a chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                
                cn=int(current_note)
                new_note = note.Note(cn)
                new_note.storedInstrument = instrument.Trumpet()
                notes.append(new_note)
                
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
            
        # pattern is a note
        else:
            
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Trumpet()
            output_notes.append(new_note)

        # increase offset each iteration so that notes do not stack
        offset += 0.5
    output_notes.append(instrument.Trumpet())
    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp='Trumpet.mid')


# In[16]:


predicted_notes=prediction()
convert_to_midi(predicted_notes)


# In[17]:


import subprocess
subprocess.call(['sh', 'Trumpet.sh'])


# In[ ]:




