from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)

def override_deliveries(deliveries_):
    deliverie = dict()
    deliverie["deliveries"] = deliveries_
    with open("deliveries.json", "w") as fo:
        fo.write(json.dumps(deliverie))

def get_deliveries_json():
    deliveries = []
    with open('deliveries.json') as json_file:
        deliveries = json.load(json_file)
    return deliveries

def override_workers(workers_):
    workers = dict()
    workers["workers"] = workers_
    with open("workers.json", "w") as fo:
        fo.write(json.dumps(workers))

def get_workers_json():
    workers = []
    with open('workers.json') as json_file:
        workers = json.load(json_file)
    return workers

@cross_origin()
@app.route('/addWorker')
def addWorker():
    if request.args.get('name') and request.args.get('id'):
        worker = create_worker(request.args.get('name'),request.args.get('id'),"FREE")
        workers = get_workers_json()
        workers["workers"].append(worker)
        override_workers(workers["workers"])
        return "granted"
    return "failed"


@cross_origin()
@app.route('/removeWorker')
def removeWorker():
    if  request.args.get('id'):
        workers = get_workers_json()
        workers["workers"] = list(filter(lambda x: x["id"] !=request.args.get('id') ,workers["workers"]))
        override_workers(workers["workers"])
        return "granted"
    return "failed"

@cross_origin()
@app.route('/addDelivery')
def addDelivery():
    if request.args.get('id'):
        delivery = create_delivery(request.args.get('id'),"ACTIVE")
        deliveries = get_deliveries_json()
        deliveries["deliveries"].append(delivery)
        override_deliveries(deliveries["deliveries"])
        return "granted"
    return "failed"

@cross_origin()
@app.route('/removeDelivery')
def removeDelivery():
    if  request.args.get('id'):
        deliveries = get_deliveries_json()
        deliveries["deliveries"] = list(filter(lambda x: x["id"] !=request.args.get('id') ,deliveries["deliveries"]))
        override_deliveries(deliveries["deliveries"])
        return "granted"
    return "failed"


def create_worker(name,id,status):
    worker = dict()
    worker["name"] = name
    worker["id"] = id
    worker["status"] = status
    return worker

def create_delivery(id,status):
    delivery = dict()
    delivery["id"] = id
    delivery["status"] = status
    delivery["completionTime"] = ""
    return delivery

@cross_origin()
@app.route('/init')
def initBabe():
    workers = []
    workers.append(create_worker("Sofia","8332","FREE"))
    workers.append(create_worker("Alba","8132","FREE"))
    workers.append(create_worker("Mateusz","8332","FREE"))
    workers.append(create_worker("Alba","8132","FREE"))
    override_workers(workers)
    deliveries = []
    deliveries.append(create_delivery("34123","ACTIVE"))
    deliveries.append(create_delivery("321","ACTIVE"))
    deliveries.append(create_delivery("654","ACTIVE"))
    override_deliveries(deliveries)
    return "done"

@cross_origin()
@app.route('/')
def index():
    return "done"

@cross_origin()
@app.route('/workers', methods=['GET'])
def get_workers():
    return get_workers_json()

@cross_origin()
@app.route('/deliveries', methods=['GET'])
def get_deliveries():
    return get_deliveries_json()

@cross_origin()
@app.route('/update_deliveries', methods=['POST'])
def update_deliveries():
    print(request.get_json())
    override_deliveries(request.get_json())
    return "updated del"

@cross_origin()
@app.route('/update_workers', methods=['POST'])
def update_workers():
    print(request.get_json())
    override_workers(request.get_json())
    return "updated"

if __name__== "__main__":
    app.run()