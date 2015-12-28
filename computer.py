#!/usr/bin/env python
import logging
import pyjulius
import Queue
import subprocess as sp
import sys
import threading
import yaml

# Instantiate logger
logging.basicConfig(filename='COMPUTER.log', level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
# Initialize client and try to connect it to a running Julius module
client = pyjulius.Client('localhost', 10500)
try:
    client.connect()
    print '"You have successfully connected to me. Congrats, boss."'
except pyjulius.ConnectionError:
    print '"You will first need to start julius as a module."'
    sys.exit(1)

client.start()
logging.info('Client started')
q = Queue.Queue()
logging.info('Task queue instantiated')
# Global config yaml
cfile = open('config.yaml', 'r')
cconfig = yaml.load_all(cfile)
for data in cconfig:
    c = data
cc = c['applicaitons']
logging.info('Loaded global config from config.yaml')
# Magic words yaml
mfile = open('magic.yaml', 'r')
mconfig = yaml.load_all(mfile)
for data in mconfig:
    m = data
mm = m['magic_words']
logging.info('Loaded magic words config from magic.yaml')


def listen():
    "Listen to a connected Julius client and place its commands into a queue."
    from magic import magicWord
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
                            logging.info('Matched %s with %s', str(phr),
                                         str(result))
                            cmd = [app_key, cc[app_key]['phrases'][phr]]
                            q.put(cmd)  # Place command into task queue
                            logging.info('Added cmd %s to queue with %s tasks',
                                         cmd, q.qsize())
                            q.join()    # Await completion of all tasks
                            logging.info('Queue cleared')
                        else:
                            logging.info('Command %s yielded no match',
                                         str(result))
                            continue
            except Queue.Empty:
                continue
    except KeyboardInterrupt:
        logging.warning('Keyboard interrupt activated by the user!')
        print '"Good day to you."'
        client.stop()        # send the stop signal
        q.join()             # wait for the task queue to die
        client.join()        # wait for the Juluys thread to die
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
    for i in xrange(2):      # Two threads should do the trick
        t = ComputerTasks(q)
        t.setDaemon(True)    # Daemonize each threaded worker
        t.start()
    listen()

main()
