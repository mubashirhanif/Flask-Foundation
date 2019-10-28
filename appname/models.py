from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Node(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(40))
    hostname = db.Column(db.String(40))
    interfaces = db.relationship('Interface', backref='node', lazy='joined')
    def __init__(self, username, hostname):
        self.username = username
        self.hostname = hostname

    def get_id(self):
        return self.id

    def __repr__(self):
        return f"<Node => {self.username}@{self.hostname}>"


class Interface(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(40))
    ip = db.Column(db.String(15))
    node_id = db.Column(db.Integer(), db.ForeignKey('node.id'), nullable=False)
    def __init__(self, name, ip, node):
        self.name = name
        self.ip = ip
        self.node_id = node.get_id()

    def get_id(self):
        return self.id

    def __repr__(self):
        return f"<Interface => {self.name}: {self.ip}>"
