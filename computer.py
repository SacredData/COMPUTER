#!/usr/bin/env python
import logging
import pyjulius
import Queue
import subprocess as sp
import sys
import threading
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

client.start()                    # Start listening to the server
q = Queue.Queue()                 # Task queue
cfile = open('config.yaml', 'r')  # Global config YAML
mfile = open('magic.yaml', 'r')   # Magic words YAML
cconfig = yaml.load_all(cfile)
mconfig = yaml.load_all(mfile)
for data in cconfig:
    c = data
for data in mconfig:
    m = data
cc = c['applications']
mm = m['magic_words']
logging.basicConfig(filename='COMPUTER.log', level=logging.DEBUG,
                    format='%(asctime)s %(message)s')


def listen():
    "Listen to a connected Julius client and place its commands into the queue."
    logging.info('Beginning Julius listener module...')
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
                            logging.info('Matched %s with %s', str(phr), str(result))
                            cmd = [app_key, cc[app_key]['phrases'][phr]]
                            q.put(cmd)  # Place command into task queue
                            logging.info('Added cmd %s to queue with %s tasks',
                                         cmd, q.qsize())
                            q.join()    # Await completion of all tasks
                            logging.info('Queue cleared')
                        else:
                            continue
            except Queue.Empty:
                continue
    except KeyboardInterrupt:
        logging.warning('Keyboard interrupt activated by the user!')
        print '"Good day to you."'
        client.stop()        # send the stop signal
        client.join()        # wait for the thread to die
        client.disconnect()  # disconnect from julius


class ComputerTasks(threading.Thread):

    "A threaded worker class which seeks to clear out the COMPUTER task queue."

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        logging.info('New task thread established.')

    def run(self):
        logging.info('Task thread is running a command.')
        while 1:
            try:
                task_cmd = self.queue.get()
                try:
                    logging.info('Running command: %s', task_cmd)
                    sp.check_call(task_cmd)
                except sp.CalledProcessError:
                    logging.error('Command process error: %s', task_cmd)
                    print '"Oh my! An error has my jimmies very rustled."'
                    logging.warning('Skipping command: %s', task_cmd)
                    continue
                finally:
                    self.queue.task_done()
                    logging.info('Command cleaved from task queue: %s',
                                 task_cmd)
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
