#!/usr/bin/env python
import pyjulius
import threading
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
q = Queue.Queue()  # Task queue

# Initialize and try to connect
client = pyjulius.Client('localhost', 10500)
try:
    client.connect()
except pyjulius.ConnectionError:
    print '"You will first need to start julius as a module."'
    sys.exit(1)

# Start listening to the server
client.start()


def listen():
    try:
        while 1:
            try:
                result = client.results.get(False)
                voca = str(result).split()
                app_key = magicWord(voca)
                if isinstance(app_key, basestring):
                    for phr in cc[app_key]['phrases']:
                        if str(result) in phr:
                            print '"I shall run ', phr, ' for you."'
                            cmd = [app_key, cc[app_key]['phrases'][phr]]
                            q.put(cmd)
                            # sp.check_call(cmd)
                            time.sleep(0.5)
                        else:
                            print '"I am unable to find that command for you."'
                            time.sleep(2)
            except Queue.Empty:
                time.sleep(0.85)
                continue
    except KeyboardInterrupt:
        print '"Good day to you."'
        client.stop()  # send the stop signal
        client.join()  # wait for the thread to die
        client.disconnect()  # disconnect from julius


class ComputerTasks(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while 1:
            try:
                task_cmd = self.queue.get()
                try:
                    sp.check_call(task_cmd)
                finally:
                    self.queue.task_done()
            except Queue.Empty:
                time.sleep(1)
                continue


def main():
    # spawn a pool of threads
    for i in xrange(4):
        t = ComputerTasks(q)
        t.setDaemon(True)
        t.start()
    listen()

main()
print '"Goodbye."'
