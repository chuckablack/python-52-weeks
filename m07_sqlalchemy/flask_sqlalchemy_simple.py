from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint
import yaml

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Device(db.Model):
    name = db.Column(db.Text, primary_key=True, nullable=False)
    hostname = db.Column(db.Text)
    ip_address = db.Column(db.Text, unique=True)
    vendor = db.Column(db.Text)
    os = db.Column(db.Text)

    def __repr__(self):
        return f"Device: {self.name}"


db.create_all()

with open("devices.yaml", "r") as yaml_in:
    yaml_devices = yaml_in.read()
    devices = yaml.safe_load(yaml_devices)

db.session.query(Device).delete()

for device in devices:
    db.session.add(Device(**device))

db.session.commit()

all_devices = Device.query.all()
print("\n----- all devices ----------")
for device in all_devices:
    pprint(vars(device))

csr = Device.query.filter_by(hostname="sbx-nxos-mgmt.cisco.com").first()
print("\n----- csr device ----------")
pprint(vars(csr))

csr = Device.query.filter_by(name="no name will match this").first()
print("\n----- csr device not found ----------")
print(f"--- device found should be None: {csr}")

all_devices = Device.query.order_by(Device.ip_address).all()
print("\n----- all devices, ordered by ip address ----------")
for device in all_devices:
    print(f"\nInformation for device: {device}\n")
    pprint(vars(device))

db.session.delete(Device.query.filter_by(ip_address="10.1.254.68").first())
db.session.delete(Device.query.filter_by(os="nxos-ssh").first())
db.session.commit()

all_devices = Device.query.all()
print("\n----- all devices after delete ----------")
pprint(all_devices)
