from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
db = SQLAlchemy(app)
db.create_all()


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    ip_address = db.Column(db.Text, unique=True, nullable=False)
    vendor = db.Column(db.Text)
    os = db.Column(db.Text)
    ssh_username = db.Column(db.Text)
    ssh_password = db.Column(db.Text)

    def __repr__(self):
        return '<Device %r>' % self.name


device_csr = Device(
    id=1,
    name="ios-xe-mgmt-latest.cisco.com",
    ip_address="10.1.1.1",
    vendor="Cisco",
    os="IOS",
    ssh_username="developer",
    ssh_password="C1sco12345",
)
device_nxos = Device(
    id=2,
    name="sbx-nxos-mgmt.cisco.com",
    ip_address="10.1.2.1",
    vendor="Cisco",
    os="NXOS",
    ssh_username="admin",
    ssh_password="Admin_1234!",
)

db.create_all()

db.session.add(device_csr)
db.session.add(device_nxos)
db.session.commit()

all_devices = Device.query.all()
print("\n----- all devices ----------")
for device in all_devices:
    pprint(vars(device))

csr = Device.query.filter_by(id=1).first()
print("\n----- csr device ----------")
pprint(vars(csr))

csr = Device.query.filter_by(name="no name will match this").first()
print("\n----- csr device not found ----------")
pprint(csr)

db.session.delete(device_csr)
db.session.delete(device_nxos)
db.session.commit()

all_devices = Device.query.all()
print("\n----- all devices after delete ----------")
pprint(all_devices)

