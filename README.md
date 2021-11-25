# Sound Classifier using EdgeImpulse and a Raspberry Pi
A Raspberry Pi based Sound Sensor to classify sounds. With the Jupyter Notebooks, Python scripts and EdgeImpulse you can train any sound classfier you want. For example, why don't train a model to detect planes flying over your house? In my case, I have chosen to build a model for snoring. 
 
## Background: Sleep and snoring
Sleep is one of the most important but least understood aspects of our life, wellness, and longevity. Until recently, science had no answer to the question of why we sleep, or what good it served, or why we suffer such devastating health consequences when we don't sleep. 

While there are many excellent consumer devices on the market to track your sleep (such as the Oura Ring or Apple Watch) they have no capability to record the sound of snoring. 
With this tutorial you can record your snoring and visualise it using Grafana Dashboards. 

With this sound classfier to detect snoring, you can better understand your sleep. For example, is snoring worse after drinking alcohol? Would snoring be less if you do breathing exercises before going to bed?

As sleep is a highly personal activity, with this 'privacy by design' sound sensor you don't have to share your data with anyone. Also, as the machine learning inference is done on the device (or 'on the edge') there is no recording of (sensitive) sounds. You just store the results of the inference on your local device. 

## Hardware
For this tutorial I've used the following hardware:
- A Raspberry PI 4 with 2 Gb RAM. I've used Raspbian Buster for this tutorial.
- A microphone connected to the Pi. There are many different microphones available, both cheap and expensive. 

On the raspberry make sure you've enabled SSH. 

## Tutorial
This tutorial assumes you've some experience with Python, Machine Learning etc. It's not written for the absolute beginner.

### 1. Three options of collecting raw data

There are three options of collecting your data:
1. Use the samples provided in this repo. These is clean data of high quality. There is only snoring, no other sounds, no silence. 
2. Record your own data using the script 'sound_record.py'. It uses the soundfile package.  I advice to record at least 10 samples of 10 seconds each.
3. Download from Google's AudioSet.  

Google's Audioset [link](https://research.google.com/audioset/index.html) is a large collection of audiosamples. AudioSet has 527 classes of audio that can be used to train Deep Learning models. Unfortunately the quality is not always good as one sample can contain multiple sound classes. (In our case we will see that samples can contain both snoring and other classes, such as music or silence). However this is still the best way to get (free) data in quantities large enough for training deep learning models. 

To download the data I use a Jupyter Notebook [provided here](https://github.com/aoifemcdonagh/audioset-processing/blob/master/demo.ipynb). You can open it in Google Colab. In Step 3 of the notebook you can change the Audio Class. A full ontology of the AudioSet classes can be found [here](https://research.google.com/audioset/ontology/index.html). I would recommend to download the Class white noise. You can also download the Class snoring, but do keep in mind that the 10s samples of Snoring in AudioSet also contain other sounds such as music, talking or silence. 

### 2. Do data augmentation on the Audio Files
Data augmentation is an important part of creating Deep Learning datasets. With the script provided here you can create four augmented files based on one original file. 
Please find the script on my Github Gist [here](https://gist.github.com/MichielBbal/15b9081d41f858c3dcd2c4307e401f58#file-audio_data_augmentation-py)

### 3. Upload to EdgeImpulse & train your dataset. 

[EdgeImpulse](www.edgeimpulse.com) is a low code platform to train machine learning models used on microcontrollers (eg. Arduino) and single board computers such as the Raspberry Pi. 

There are tons of tutorials on EdgeImpulse so I won't give a full tutorial here.

To train the model I've created the following three classes:
- Snoring
- Silence
- White noise

The class Snoring can be trained with the data provided in this repo (folder snoring_wavs).
The class Silence can be trained with the audio wav's you've trained and augmented yourself. 
The class White Noise can be trained with the data you've downloaded from AudioSet and/or recorded and augmented yourself.
 
In EdgeImpulse go to the 'data acquisition' tab. With the built in function you can see a soundwave and listen to the audio. You can use the 'crop' function to do data cleaning. (This is a time consuming but a necessary step!) Only with high quality, non-polluted data samples you can create a model with a high accuracy.

In EdgeImpulse I've used the following settings: 

* Under tab 'Create Impulse' I've used: 'Time Series data', 'Spectogram' and 'Classification (Keras).
* Under tab 'Spectogram' keep settings as provided
* Under tab 'NN Classifier' set 'Number of training cycles' to 100. 

With these settings I was able to achieve a model result of 92.7%. 

As we will use a Raspberry Pi (Linux) there is no need to use EdgeImpulse's EON Tuner.

### 4.Install EdgeImpulse and InfluxDb on the Raspberry Pi
<i>If you have already installed EdgeImpulse and InfluxDb on your Pi, you can skip this step </i>

* To install EdgeImpulse follow the tutorial [here](https://docs.edgeimpulse.com/docs/edge-impulse-for-linux)
* To install InfluxDB follow the tutorial [here](https://simonhearne.com/2020/pi-influx-grafana/) 

After installing InfluxDB create a database called 'SNORING'

### 5. Download the model to the Raspberry and use the provided script 

After training the model in EdgeImpulse, you can download it to your Raspberry using the following command:

`$ cd <to directory>` <br>
`$ edge-impulse-linux-runner --clean --download modelfile.eim`

I've provided a script sound_classifier.py to store the data in a Influx database.

When starting the script, there will be some errormessages about ALSA, which you can ignore (November 2021). (The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI functionality to the Linux operating system.). 

### 6. Connect Grafana to your Raspberry
I've installed Grafana ([link](https://grafana.com/)) on my laptop. With it you can easily create a connection to the InfluxDB on your pi. 

Use Grafana on your laptop to connect to the Raspberry and get the data and show the results. 
* Go to Grafana and select 'data sources' under 'configuration'
* Select 'add data source' and search for InfluxDB
* Change the name, add an url: http://<my_raspberry_ip>:8086
* Under Database use <SNORING> (or the name of your database)
* Create dashboard panels by selecting the right datafields.

### 7. Conclusion and next steps
That's it! The most important is that you have fun while building it.
 
What could be possible next steps?
 - Train a sensor with an accelerometer to detect your sleeping position (back, belly or side) or do this with an image classfier on a infrared webcam. 
 - Combine the snoring data with data from your Oura Ring (https://ouraring.com/)
 - Get "haptic feedback" when snoring using the Neosensory Buzz (https://neosensory.com/) 
 

