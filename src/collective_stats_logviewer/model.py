from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy import func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stats.db'

db = SQLAlchemy(app)
Base = declarative_base()


def init_db():
    db.create_all()


class Log(db.Model):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    access_time = Column(DateTime)
    publisher_time = Column(Float)
    traverse_time = Column(Float)
    commit_time = Column(Float)
    transform_time = Column(Float)
    setstate_time = Column(Float)
    total_object_loads = Column(Integer)
    object_loads_from_cache = Column(Integer)
    objects_modified = Column(Integer)
    action = Column(String)
    url = Column(String)
    start_RSS = Column(Float)
    end_RSS = Column(Float)

    def __init__(self, access_time, publisher_time, traverse_time, commit_time, transform_time, setstate_time, total_object_loads, object_loads_from_cache, objects_modified, action, url, start_RSS, end_RSS):
        self.access_time = access_time
        self.publisher_time = publisher_time
        self.traverse_time = traverse_time
        self.commit_time = commit_time
        self.transform_time = transform_time
        self.setstate_time = setstate_time
        self.total_object_loads = total_object_loads
        self.object_loads_from_cache = object_loads_from_cache
        self.objects_modified = objects_modified
        self.action = action
        self.url = url
        self.start_RSS = start_RSS
        self.end_RSS = end_RSS


def query_number_of_requests():
    # Number of requests
    rows = db.session.query(Log)
    num_requests = rows.count()
    return num_requests


def query_access_time():
    # Total access time of the server
    access_time = db.session.query(Log.access_time).order_by('access_time')
    total_time = 0
    if access_time.count():
        first, last = access_time[0], access_time[-1]
        difference = last[0] - first[0]
        total_time = difference.seconds
    return total_time


def query_reqs_sec():
    # Total access time
    total_time = query_access_time()
    if not total_time:
        return 0
    num_requests = query_number_of_requests()

    #Converts to float if result will be less than 1
    if num_requests < total_time:
        num_requests = float(num_requests)
        total_time = float(total_time)

    # Number of requests made to the server per second
    reqs_sec = num_requests / total_time

    return reqs_sec


def query_time_per_request():
    # Summates rendering time
    rendering_time = db.session.query(func.sum(Log.publisher_time))
    total_rendering_time = rendering_time[0][0]
    if not total_rendering_time:
        return 0

    num_requests = query_number_of_requests()

    #Converts to float if result will be less than 1
    if total_rendering_time < num_requests:
        total_rendering_time = float(total_rendering_time)
        num_requests = float(num_requests)
    # Total time per request
    time_per_request = total_rendering_time / num_requests
    return time_per_request


def query_optimal_requests():
    # Time per request
    time_per_request = query_time_per_request()
    if not time_per_request:
        return 0
    # Total access time
    total_time = query_access_time()
    # Optimal requests
    optimal_capacity = total_time * (1 / time_per_request)
    optimal_requests = optimal_capacity / total_time
    return optimal_requests


def query_current_capacity():
    # Current capacity
    optimal_requests = query_optimal_requests()
    if not optimal_requests:
        return 0
    return (query_reqs_sec() / optimal_requests) * 100


def get_average_render_time():
    """Takes the webpages and returns average time rendered
        from the datbase"""
    average = db.session.query(func.avg(Log.publisher_time).label("average"), Log.url).group_by(Log.url).order_by("-average").limit(10).all()
    return average


def get_response_time_details(url):
    """Takes the url from the webpage and returns timestamp and render time"""
    dict_list = []
    response_time = db.session.query(Log.access_time.label("timestamp"), Log.publisher_time).filter(Log.url == url).order_by("timestamp").all()
    for row in response_time:
        time = row[0].ctime()
        rt = row[1]
        new_dict = dict(zip(('timestamp', 'render_time'), (time, rt)))
        dict_list.append(new_dict)
    return dict_list


def get_overall_time(url):
    """Gets the overall time needed for the url to be called"""
    overall = db.session.query(func.sum(Log.publisher_time)).filter(Log.url == url).all()
    return overall
    

def get_total_hits(url):
    """Gets the total hits based the url recieved"""
    num_rows = db.session.query(Log).filter(Log.url == url).count()
    return num_rows

