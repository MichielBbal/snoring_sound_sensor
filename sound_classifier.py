#script by EdgeImpulse and Michiel Bontenbal
import os
import sys, getopt
import signal
import time
from edge_impulse_linux.audio import AudioImpulseRunner
from influxdb import InfluxDBClient
from datetime import datetime

#EI runner
runner = None

#setting up InfluxDB client
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('SNORING')
print(client)

def signal_handler(sig, frame):
    print('Interrupted')
    if (runner):
        runner.stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def help():
    print('python classify.py <path_to_model.eim> <audio_device_ID, optional>' )

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["--help"])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()

    if len(args) == 0:
        help()
        sys.exit(2)

    model = args[0]

    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model)

    json_body =[]
    my_dict= {"measurement": "my_snoring"}
    with AudioImpulseRunner(modelfile) as runner:
        try:
            model_info = runner.init()
            labels = model_info['model_parameters']['labels']
            print('Loaded runner for "' + model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')

            #Let the library choose an audio interface suitable for this model, or pass device ID parameter to manually select a specific audio interface
            selected_device_id = None
            if len(args) >= 2:
                selected_device_id=int(args[1])
                print("Device ID "+ str(selected_device_id) + " has been provided as an argument.")

            for res, audio in runner.classifier(device_id=selected_device_id):
                #print(res['timing'])
                my_dict["fields"]={}
                
                time.sleep(0.5)
                #print('Result (%d ms.) ' % (res['timing']['dsp'] + res['timing']['classification']), end='')
                
                for label in labels:
                    score = res['result']['classification'][label]
                    #print('%s: %.2f\t' % (label, score), end='')
                    my_dict["fields"][label]=score 
                #print(my_dict)
                json_body.append(my_dict)
                print(json_body)
                client.write_points(json_body)
                del my_dict["fields"]
                del json_body[0]
                #print('', flush=True)
                
        finally:
            if (runner):
                runner.stop()
    
if __name__ == '__main__':
    main(sys.argv[1:])
