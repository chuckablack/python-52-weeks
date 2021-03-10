class Device:

    def __init__(self, name, device_type, hostname):
        self.name = name
        self.hostname = hostname
        self.device_type = device_type

        self.mac = None
        self.ip = None
        self.connection = None

        self.username = None
        self.password = None
        self.port = None

    def set_credentials(self, username, password):
        self.username = username
        self.password = password

    def set_port(self, port):
        self.port = port

    def connect(self):
        raise NotImplementedError("Please implement the connect() method")

    def get_facts(self):
        raise NotImplementedError("Please implement the get_facts() method")

    def disconnect(self):
        raise NotImplementedError("Please implement the disconnect() method")
