import datetime
import re
from collective_stats_logviewer.model import Log
from model import db

def do_it(line):
    pattern = re.compile("^(?P<access_time>\d+-\d+-\w+:\d+:\d+) INFO collective\.stats \| (?P<publisher_time>\d+\.\d+) (?P<traverse_time>\d+\.\d+) (?P<commit_time>\d+\.\d+) (?P<transform_time>\d+\.\d+) (?P<setstate_time>\d+\.\d+) (?P<total_object_loads>\d+) (?P<object_loads_from_cache>\d+) (?P<objects_modified>\d+) \| (?P<action>\w+:)(?P<url>.*) \| .* \| RSS\: (?P<start_RSS>\d+) - (?P<end_RSS>\d+)")
    match_result = re.match(pattern, line)
    if match_result:
        result =  match_result.groupdict()
        request_time = datetime.datetime.strptime(result['access_time'], 
                                                      "%Y-%m-%dT%H:%M:%S")             
        l = Log(request_time, result['publisher_time'], result['traverse_time'], result['commit_time'], result['transform_time'],
                result['setstate_time'], result['total_object_loads'], result['object_loads_from_cache'], result['objects_modified'],
                result['action'], result['url'], result['start_RSS'], result['end_RSS'])
        db.session.add(l)
        db.session.commit()
        db.session.refresh(l)
        return l.id
    return None
    
