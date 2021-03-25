from flask import Flask, request

app = Flask(__name__)

# READ THIS: Don't do this. By that I mean, don't use global variables in a flask application.
#            The reason: flask is by nature, multi-threaded. Each REST request will operate on
#            it's own thread. So you could have multiple threads attempting to write global data.
#            That's a bad, bad idea.
#            In the next lessons, we'll be replacing this data with an SQL database. And reads
#            and writes to the database are safe.

# DON'T DO THIS # DON'T DO THIS # DON'T DO THIS !!!
global_hosts = dict()  # not thread-safe (flask)
global_devices = dict()  # not thread-safe (flask)
global_services = dict()  # not thread-safe (flask)


@app.route("/hosts", methods=["GET", "POST", "PUT", "DELETE"])
def hosts():
    global global_hosts  # Remember, don't do this (don't use globals in Flask)

    if request.method == "GET":
        return global_hosts

    elif request.method == "PUT":
        hostname = request.args.get("hostname")
        if not hostname:
            return "must provide hostname on PUT", 400

        host = request.get_json()
        global_hosts[hostname] = host
        return {}, 204


@app.route("/devices", methods=["GET", "POST", "PUT", "DELETE"])
def devices():
    global global_devices  # Remember, don't do this (don't use globals in Flask)

    if request.method == "GET":
        return global_devices

    elif request.method == "POST":
        global_devices = request.get_json()
        return {}, 204

    elif request.method == "PUT":
        name = request.args.get("name")
        if not name:
            return "must provide name on PUT", 400

        device = request.get_json()
        global_devices[name] = device
        return {}, 204

    elif request.method == "DELETE":
        name = request.args.get("name")
        if not name:
            return "must provide name on DELETE", 400

        del global_devices[name]
        return {}, 204


@app.route("/services", methods=["GET", "POST", "PUT", "DELETE"])
def services():
    global global_services  # Remember, don't do this (don't use globals in Flask)

    if request.method == "GET":
        return global_services

    elif request.method == "POST":
        global_services = request.get_json()
        return {}, 204

    elif request.method == "PUT":
        name = request.args.get("name")
        if not name:
            return "must provide name on PUT", 400

        service = request.get_json()
        global_services[name] = service
        return {}, 204

    elif request.method == "DELETE":
        name = request.args.get("name")
        if not name:
            return "must provide name on DELETE", 400

        del global_services[name]
        return {}, 204
