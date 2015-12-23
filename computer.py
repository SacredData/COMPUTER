#!/usr/bin/env python
import pyjulius
import threading
import Queue
import subprocess as sp
import sys
import yaml
from magic import magicWord

# Initialize and try to connect
client = pyjulius.Client('localhost', 10500)
try:
    client.connect()
    print '"You have successfully connected to me. Congrats, boss."'
except pyjulius.ConnectionError:
    print '"You will first need to start julius as a module."'
    sys.exit(1)

# Start listening to the server
client.start()
# Establish configs and queues
cfile = open('config.yaml', 'r')  # Global config YAML
cconfig = yaml.load_all(cfile)
mfile = open('magic.yaml', 'r')   # Magic words YAML
mconfig = yaml.load_all(mfile)
for data in cconfig:
    c = data
for data in mconfig:
    m = data
cc = c['applications']
mm = m['magic_words']
q = Queue.Queue()                 # Task queue


def listen():
    "Listen to a connected Julius client and place its commands into the queue."
    try:
        while 1:
            try:
                # Get voice match from the Julius client
                result = client.results.get(False)
                # Split the result so we can search substrings for magic words
                voca = str(result).split()
                # Use the key obtained to scan the config YAML for commands
                app_key = magicWord(voca)
                if isinstance(app_key, basestring):
                    for phr in cc[app_key]['phrases']:
                        if str(result) in phr:
                            print '"I shall run ', str(result), ' for you."'
                            cmd = [app_key, cc[app_key]['phrases'][phr]]
                            q.put(cmd)  # Place command into task queue
                            q.join()    # Await completion of all tasks
                        else:
                            continue
            except Queue.Empty:
                continue
    except KeyboardInterrupt:
        print '"A good day to you and a blessed \'morrow as well."'
        client.stop()  # send the stop signal
        client.join()  # wait for the thread to die
        client.disconnect()  # disconnect from julius


class ComputerTasks(threading.Thread):

    "A threaded worker class which seeks to clear out the task queue."

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        print '"Hello, my Lord! I have established a new task thread for you."'

    def run(self):
        print '"It would appear that the task thread is running."'
        while 1:
            try:
                task_cmd = self.queue.get()
                print '"I have taken a task out of the queue, my liege."'
                try:
                    sp.check_call(task_cmd)
                except sp.CalledProcessError:
                    print '"Oh my! An error has my jimmies very rustled."'
                finally:
                    self.queue.task_done()
            except Queue.Empty:
                continue


def main():
    # spawn worker threads
    for i in xrange(2):
        t = ComputerTasks(q)
        t.setDaemon(True)
        t.start()
    listen()

main()
