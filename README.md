# snoring_sound_sensor
A Raspberry Pi based Sound Sensor to detect snoring (or create your own model using EdgeImpulse)

# Tutorial

## Steps

1. Download data from Google's AudioSet
Google's Audioset (link)[https://research.google.com/audioset/index.html] is a large collection of audiosamples. AudioSet has 527 classes of audio that can be used to train Deep Learning models. Unfortunately the quality is not always good as one sample can contain multiple sound classes. (In our case we will see that samples can contain both snoring and other classes, such as music or silence). However this is still the best way to get (free) data in quantities large enough for training deep learning models. We also propose another mechanism of recording your own data in combination with data augmentation.     

To download the data I use ... script. 

2. Record your own data (like silence)

A much simpler approach is to record your own data. This can be done with the following python script:

Alternatively, you can run this Jupyter Notebook:

I advice to record at least 10 samples of 10 seconds each.

3. Do data augmentation on the Audio Files
Data augmentation is an important part of creating Deep Learning datasets. With the script provided here you can create four augmented files based on one original file. 
Please find the script here: https://gist.github.com/MichielBbal/15b9081d41f858c3dcd2c4307e401f58#file-audio_data_augmentation-py


5. Upload to EdgeImpulse & train the model

There are tons of tutorials on EdgeImpulse so I won't give a full tutorial here.

7. Download to Raspberry and use InfluxDB to store the results

I've added an adapted script to store the data in a Influx database.

9. Connect Grafana to your Raspberry
Use Grafana on your laptop to connect to the Raspberry and get the data and show the results. 


