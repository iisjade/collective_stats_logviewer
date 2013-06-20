#! /usr/bin/python

import fileinput
import json
import logging
import requests

# Set logging level to info so logging in do_it() prints to
# console (default level is warning)
logging.basicConfig(level=logging.INFO)

class Loader(object):
    def __init__(self):
        self.name = "Ahmad"
        self.api_key = "sdhufuserhfhrjf"
        self.api = "http://127.0.0.1:5000/super_url"
        self.machine_name = "Terminator"

    def send_to_database(self):
        log_lines = []
        for line in fileinput.input():
            if line.count('INFO collective.stats'):
                log_lines.append(line)
                # Lines are being sent over in batches of 10000. This number is
                # largely arbitrary, feel free to change as needed.
                if len(log_lines) == 10000:
                    logging.info('file_upload.py -- Sending %s lines to super_url' % len(log_lines))
                    response = requests.post(self.api, data=json.dumps(log_lines))
                    log_lines = []
        # Upon exiting the for loop, there's a good chance there will be leftover
        # lines inside of log_lines. Check to make sure that's the case, and send
        # them over.
        if len(log_lines) != 0:
            logging.info('file_upload.py -- Sending %s lines to super_url' % len(log_lines))
            response = requests.post(self.api, data=json.dumps(log_lines))
        fileinput.close()

if __name__ == "__main__":
    load = Loader()
    load.send_to_database()
