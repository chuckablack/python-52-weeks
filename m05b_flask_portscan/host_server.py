import json
import yaml
import csv
from flask import Flask, request
import napalm


app = Flask(__name__)

# READ THIS: Don't do this. By that I mean, don't use global variables in a flask application.
#            The reason: flask is by nature, multi-threaded. Each REST request will operate on
#            it's own thread. So you could have multiple threads attempting to write global data.
#            That's a bad, bad idea.
#            In the next lessons, we'll be replacing this data with an SQL database. And reads
#            and writes to the database are safe.

# DON'T DO THIS # DON'T DO THIS # DON'T DO THIS !!!
global_hosts = dict()  # not thread-safe (flask)


@app.route("/hosts", methods=["GET", "POST", "PUT", "DELETE"])
def hosts():
    global global_hosts  # Remember, don't do this (use globals in Flask)

    if request.method == "GET":
        return global_hosts

    elif request.method == "POST":
        global_hosts = request.get_json()
        return {}, 204

    elif request.method == "PUT":
        hostname = request.args.get("hostname")
        if not hostname:
            return "must provide hostname on PUT", 400

        host = request.get_json()
        global_hosts[hostname] = host
        return {}, 204

    elif request.method == "DELETE":
        hostname = request.args.get("hostname")
        if not hostname:
            return "must provide hostname on DELETE", 400

        del global_hosts[hostname]
        return {}, 204


if __name__ == "__main__":
    app.run()
