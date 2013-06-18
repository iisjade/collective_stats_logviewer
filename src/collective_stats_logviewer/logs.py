import datetime
import re
from collective_stats_logviewer.model import Log
from model import db
import logging

logging.basicConfig(level=logging.INFO)

def do_it(log_lines):
    pattern = re.compile("^(?P<access_time>\d+-\d+-\w+:\d+:\d+) INFO collective\.stats \| (?P<publisher_time>\d+\.\d+) (?P<traverse_time>\d+\.\d+) (?P<commit_time>\d+\.\d+) (?P<transform_time>\d+\.\d+) (?P<setstate_time>\d+\.\d+) (?P<total_object_loads>\d+) (?P<object_loads_from_cache>\d+) (?P<objects_modified>\d+) \| (?P<action>\w+:)(?P<url>.*) \| .* \| RSS\: (?P<start_RSS>\d+) - (?P<end_RSS>\d+)")
    matched_logs = []
    for line in log_lines:
        match_result = re.match(pattern, line)
        if match_result:
            result =  match_result.groupdict()
            request_time = datetime.datetime.strptime(result['access_time'],
                                                          "%Y-%m-%dT%H:%M:%S")
            l = Log(request_time, result['publisher_time'], result['traverse_time'], result['commit_time'], result['transform_time'],
                    result['setstate_time'], result['total_object_loads'], result['object_loads_from_cache'], result['objects_modified'],
                    result['action'], result['url'], result['start_RSS'], result['end_RSS'])
            matched_logs.append(l)
    # Commit all the log lines received in log_lines in a single SQL statement,
    # rather than 1 at a time. Based on the default batch number set in file_load.py
    # this should be 10000 lines.
    db.session.add_all(matched_logs)
    db.session.commit()
    logging.info('logs.py -- %s commited to database' % len(matched_logs))
    # return the number of logs commited to the database
    return len(matched_logs) 
