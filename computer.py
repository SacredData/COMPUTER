#!/usr/bin/env python
import pyjulius
import Queue
import subprocess as sp
import sys
import time
import yaml
from magic import magicWord

cfile = open('config.yaml', 'r')
cconfig = yaml.load_all(cfile)
mfile = open('magic.yaml', 'r')
mconfig = yaml.load_all(mfile)
for data in cconfig:
    c = data
for data in mconfig:
    m = data
cc = c['applications']
mm = m['magic_words']

# Initialize and try to connect
client = pyjulius.Client('localhost', 10500)
try:
    client.connect()
except pyjulius.ConnectionError:
    print 'Start julius as module first!'
    sys.exit(1)

# Start listening to the server
client.start()
try:
    while 1:
        try:
            result = client.results.get(False)
        except Queue.Empty:
            time.sleep(0.85)
            continue
        print repr(result)
        voca = str(result).split()
        app_key = magicWord(voca)
        time_str = str(time.time())
        selfie_save = 'selfies/' + time_str + '.jpeg'
        if isinstance(app_key, basestring):
            for phr in cc[app_key]['phrases']:
                if str(result) in phr:
                    print phr
                    cmd = [app_key, cc[app_key]['phrases'][phr]]
                    sp.check_call(cmd)
                    time.sleep(0.5)

except KeyboardInterrupt:
    print 'Exiting...'
    client.stop()  # send the stop signal
    client.join()  # wait for the thread to die
    client.disconnect()  # disconnect from julius
