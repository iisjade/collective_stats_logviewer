#! /usr/bin/python

import json
import fileinput
import requests
import logging


class Loader(object):
    def __init__(self):
        self.name = "Ahmad"
        self.api_key = "sdhufuserhfhrjf"
        self.api = "http://127.0.0.1:5000/super_url"
        self.machine_name = "Terminator"

    def send_log_to_database(self):
        results = []
        for line in fileinput.input():
            if line.count('INFO collective.stats'):
                result = requests.post(self.api, data={'line': line})
                result = json.loads(result.text)
                logging.info("Successfully added line with id %s" % result['item_id'])
                results.append(result)
        fileinput.close()
        print results
        return results


if __name__ == "__main__":
    load = Loader()
    load.send_log_to_database()
