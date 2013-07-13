import json
import logging
from flask import render_template
from flask import Flask
from flask import jsonify
from flask import request
import logs
from model import db
from model import query_reqs_sec, query_time_per_request, query_optimal_requests, \
    query_current_capacity, get_average_render_time, get_response_time_details, \
    get_overall_time, get_total_hits, get_server_chokers, get_memory_hogs

logging.basicConfig(level=logging.INFO)

class _DefaultSettings(object):
    USERNAME = 'world'
    SECRET_KEY = 'development key'
    DEBUG = True

# create the application
app = Flask(__name__)
app.config.from_object(_DefaultSettings)
del _DefaultSettings

def init_db():
    """ Initialize the database """
    db.create_all()

@app.route('/')
@app.route('/index/')
def index():
    """Renders the index pages of collective stats. Queries the db to pull
    overall server load stats, as well as basic stats for each offending url.
    More detailed stats for each url are queried and served by
    response_time_details() using an ajax request."""
    # Assignment
    reqs_sec = query_reqs_sec()
    time_per_request = query_time_per_request()
    optimal_requests = query_optimal_requests()
    current_capacity = query_current_capacity()
    average_render_time = get_average_render_time()

    data_store = {}
    data_store['instance_stats'] = {'reqs_sec': reqs_sec, 'time_per_request': time_per_request, 'optimal_requests': optimal_requests, 'cc_percentage': current_capacity}
    data_store['slow_pages'] = average_render_time
    data_store['server_chokers'] = get_server_chokers()
    data_store['memory_hogs'] = get_memory_hogs()
    return render_template("index.html", data=data_store)


@app.route('/response_time_details/', methods=['GET'])
def response_time_details():
    """Queries db for detailed stats for a specific url. This function is
    called from an ajax request (logview.js), which sends the url as a GET request
    and returns a json object with details about rendering time, num hits, etc
    for that url. This also returns the data necessary to render the graph for
    that url."""

    url = request.args.get('url', '')
    response_time_details = get_response_time_details(url)
    overall_time = get_overall_time(url)
    total_hits = get_total_hits(url)

    graph_data = response_time_details

    stats_data = {'overall': overall_time, 'num_hits': total_hits, 'cached_benefit': 1.0003, 'avg': 2.3}
    return jsonify(url=url, graph_data=graph_data, stats_data=stats_data)

@app.route('/super_url', methods=['POST'])
def super_url():
    log_lines = json.loads(request.data)
    logging.info('views.py -- Received request from file_upload.py, sending to database')
    commited_logs = logs.do_it(log_lines)
    return "%s lines commited to the database" % commited_logs

