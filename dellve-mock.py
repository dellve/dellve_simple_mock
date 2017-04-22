from flask import Flask, render_template, json, jsonify, request, Response
import requests
import os
from conf import *
import time

class Benchmark():
    def __init__(self):
        self.progress = 0
        self.id = 0
        self.name = 'Mock0'
        self.running = False
        self.output = []
        self.config = {
                "GPU Devices": [ { "device_id": "0", "device_desc": "MockDevice0"} ,
                                { "device_id": "1", "device_desc": "MockDevice1"},
                                { "device_id": "2", "device_desc": "MockDevice2"} ],
                "run_time_min": 15,
                "mem_utilization": 123 }
    def start(self, b_id):
        self.id = b_id
        self.progress = 0
        self.running = True
        self.name= "Mock" + str(b_id)
        self.output = []

        #self.owner = owner
    def stop(self):
        self.running = False # stop progress update

app = Flask(__name__)
CURRENT_BENCH = Benchmark()

@app.route('/benchmark')
def get_benchmarks():
    global CURRENT_BENCH
    #return Response( json.dumps(CURRENT_BENCH.__dict__), status=200 )
    bench = [{ "name": "MockTool0", "id": "0", "config": {
                    "GPU Devices": [ { "device_id": "0", "device_desc": "MockDevice0"} ,
                            { "device_id": "1", "device_desc": "MockDevice1"},
                            { "device_id": "2", "device_desc": "MockDevice2"} ],
                    "run_time_min": 15,
                    "mem_utilization": 123
                    }
                },
                { "name": "MockTool1", "id": "1", "config": {
                    "GPU Devices": [ { "device_id": "0", "device_desc": "MockDevice0"} ,
                            { "device_id": "1", "device_desc": "MockDevice1"}],
                    "run_time_min": 15,
                    "mem_utilization": 123
                    }
                }]
    print(json.dumps(bench))
    return Response( json.dumps(bench), status=200 )


# TODO: integrate post/config
@app.route('/benchmark/<int:b_id>/start', methods=['GET', 'POST'] )
def start_benchmark(b_id):
    print(str(request.data))
    global CURRENT_BENCH
    if CURRENT_BENCH.running != True:
        CURRENT_BENCH.start(b_id)
    return Response( json.dumps(CURRENT_BENCH.__dict__), status=200 )

@app.route('/benchmark/<int:b_id>/stop', methods=['GET','POST'])
def stop_benchmark(b_id):
    print(str(request.data))
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
            CURRENT_BENCH.output.append('Running mock loop ' + str(CURRENT_BENCH.progress) + '...')
            CURRENT_BENCH.output.append('\n')
        if CURRENT_BENCH.progress == 100:
            CURRENT_BENCH.running = False
    return Response( json.dumps(CURRENT_BENCH.__dict__), status=200 )

# Fakes presence of netdata dependencies
@app.route('/api/v1/charts/data', methods=['GET'])
def get_netdata():
    return Response( status = 200 )

if __name__ == "__main__":
    app.run(port=DEFAULT_PORT, debug=True, threaded=True)
