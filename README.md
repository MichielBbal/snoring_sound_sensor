# Sound Classifier using EdgeImpulse and a Raspberry Pi
A Raspberry Pi based Sound Sensor to classify sounds. 


## Snoring

## Hardware
For this tutorial I've used the following hardware:
- A Raspberry PI 4 with 2 Gb RAM. I've used Raspbian Buster for this tutorial.
- A microphone connected to the Pi. There are many different microphones available, both cheap and expensive. 

## Tutorial

### 1. Use the snoring sound samples provided here 

### 2. Record your own data (like silence)

A much simpler approach is to record your own data. This can be done with the following python script:

Alternatively, you can run this Jupyter Notebook:

I advice to record at least 10 samples of 10 seconds each.

### 3. Alternative: download (more) data from Google's AudioSet
Google's Audioset [link](https://research.google.com/audioset/index.html) is a large collection of audiosamples. AudioSet has 527 classes of audio that can be used to train Deep Learning models. Unfortunately the quality is not always good as one sample can contain multiple sound classes. (In our case we will see that samples can contain both snoring and other classes, such as music or silence). However this is still the best way to get (free) data in quantities large enough for training deep learning models. We also propose another mechanism of recording your own data in combination with data augmentation.     

To download the data I use the Jupyter Notebook: [here](https://github.com/aoifemcdonagh/audioset-processing/blob/master/demo.ipynb). You can open it in Google Colab. In Step 3 of the notebook you can change the Audio Class to '. A full ontology of the AudioSet classes can be found [here](https://research.google.com/audioset/ontology/index.html). I would also recommend to download classes such as white noise.  

### 4. Do data augmentation on the Audio Files
Data augmentation is an important part of creating Deep Learning datasets. With the script provided here you can create four augmented files based on one original file. 
Please find the script on my Github Gist [here](https://gist.github.com/MichielBbal/15b9081d41f858c3dcd2c4307e401f58#file-audio_data_augmentation-py)

### 5. Upload to EdgeImpulse & train your dataset. 

There are tons of tutorials on EdgeImpulse so I won't give a full tutorial here.

To train the model I've created the following three classes:
- Snoring
- Silence
- White noise

The class Snoring can be trained with the data provided in this repo (folder snoring_wavs).
The class Silence can be trained with the audio wav's you've trained and augmented yourself. 
The class White Noise can be trained with the data you've downloaded from AudioSet and/or recorded and augmented yourself.
 
In EdgeImpulse I've used the following settings:


### 6.Install EdgeImpulse and InfluxDb on the Raspberry Pi
* If you have already installed EdgeImpulse and InfluxDb on your Pi, you can skip this step*
* 
To install EdgeImpulse follow the tutorial [here](https://docs.edgeimpulse.com/docs/edge-impulse-for-linux)
To install InfluxDB follow the tutorial [here](https://simonhearne.com/2020/pi-influx-grafana/) 


### 7. Download the model to the Raspberry and use the provided script 

After training the model in EdgeImpulse, you can download it to your Raspberry using the following command:

`$ cd <to directory>

`$ edge-impulse-linux-runner --clean --download modelfile.eim

I've provided a script to store the data in a Influx database.

After starting the script, there will be some errormessages about ALSA, which you can ignore (November 2021). (The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI functionality to the Linux operating system). 

### 8. Connect Grafana to your Raspberry
I've installed Grafana [link](https://grafana.com/) on my laptop. With it you can easily create a connection to the InfluxDB on your pi. 

Use Grafana on your laptop to connect to the Raspberry and get the data and show the results. 

That's it! Enjoy building it. 


