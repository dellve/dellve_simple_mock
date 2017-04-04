from flask import Flask, render_template, json, jsonify, request, Response
import requests
import os
from conf import *
import time

class Benchmark():
    def __init__(self):
        self.progress = 0
        self.id = None
        self.name = None
        self.running = False
        self.run_detail = None
    def start(self, b_id):
        self.id = b_id
        self.progress = 0
        self.running = True
        #self.owner = owner
    def stop(self):
        self.running = False # stop progress update
        self.run_detail = None
        #self.owner = None

app = Flask(__name__)
CURRENT_BENCH = Benchmark()

@app.route('/benchmark')
def get_benchmarks():
    bench = [{"name": "Mock0", "id": "0"}, {"name": "Mock1", "id": "1"}]
    return Response( json.dumps(bench), status=200 )

@app.route('/benchmark/<int:b_id>/start', methods=['GET'] )
def start_benchmark(b_id):
    global CURRENT_BENCH
    if CURRENT_BENCH.running != True:
        CURRENT_BENCH.start(b_id)
    return Response( json.dumps(CURRENT_BENCH.__dict__), status=200 )

@app.route('/benchmark/<int:b_id>/stop', methods=['GET'])
def stop_benchmark(b_id):
    global CURRENT_BENCH
    #owner = request.headers.get('Owner')
    # Do not allow benchmark stop
    #if owner == CURRENT_BENCH.owner:
    if CURRENT_BENCH.running == True and CURRENT_BENCH.id == b_id :
        CURRENT_BENCH.stop()
    return Response( json.dumps(CURRENT_BENCH.__dict__), status=200 )

@app.route('/benchmark/progress', methods=['GET'])
def get_progress():
    global CURRENT_BENCH
    #owner = request.headers.get('Owner')
    #{"progress": 26, "id": 0}
    if CURRENT_BENCH.running == True:
        if CURRENT_BENCH.progress != 100:
            CURRENT_BENCH.progress += 1
        if CURRENT_BENCH.progress == 100:
            CURRENT_BENCH.running = False
            CURRENT_BENCH.run_detail = 'example run detail'
    return Response( json.dumps(CURRENT_BENCH.__dict__), status=200 )

# Fakes presence of netdata dependencies
@app.route('/api/v1/charts/data', methods=['GET'])
def get_netdata():
    return Response( status = 200 )

if __name__ == "__main__":
    app.run(port=DEFAULT_PORT, debug=True, threaded=True)
