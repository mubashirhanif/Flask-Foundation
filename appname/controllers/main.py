from flask import Blueprint, render_template, flash, request, redirect, url_for

from appname.extensions import cache
from appname.forms import IPRegistrationForm
from appname.models import Interface, Node, db
import json

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route("/register_ip", methods=["POST", "GET"])
def register_ip():
    form = IPRegistrationForm()
    if form.validate_on_submit():
        host = Node.query.filter_by(username=form.username.data, hostname=form.hostname.data).first()
        if not host:
            host = Node(username=form.username.data, hostname=form.hostname.data)
            db.session.add(host)
            db.session.commit()
        iface = Interface.query.filter_by(name=form.interface_name.data, node_id=host.get_id()).first()
        if not iface:
            iface = Interface(ip=form.ip.data, name=form.interface_name.data, node = host)
            host.interfaces.append(iface)
            db.session.add(host)
        else:
            iface.ip = form.ip.data
        db.session.add(iface)
        db.session.commit()
        
        flash("IP registered successfully.", "success")
        return redirect(request.args.get("next") or url_for(".home"))
    return render_template("ipregistration.html", form=form)

@main.route("/register_ips", methods=["POST"])
def register_ips():
    _json =  request.get_json(force=True)
    host = Node.query.filter_by(username=_json["username"], hostname=_json["hostname"]).first()
    if not host:
        host = Node(username=_json["username"], hostname=_json["hostname"])
        db.session.add(host)
        db.session.commit()
    for _iface in _json["interfaces"]:
        iface = Interface.query.filter_by(name=_iface["name"], node_id=host.get_id()).first()
        if not iface:
            iface = Interface(ip=_iface["ip"], name=_iface["name"], node = host)
            host.interfaces.append(iface)
            db.session.add(host)
        else:
            iface.ip = _iface["ip"]
        db.session.add(iface)
    db.session.commit()

    return "Success", 200
    

@main.route("/ip_addresses", methods=["GET"])
def ip_addresses():
    hosts = Node.query.all()
    # [
    #     {
    #         "username": 'mubashir',
    #         "hostname": 'hostname',
    #         "interfaces": [
    #             {
    #                 "name": 'xda',
    #                 "ip": '192.168.0.100'
    #             }, 
    #             {
    #                 "name": 'xda2',
    #                 "ip": '192.168.1.100'
    #             } 
    #         ]
    #     },
    #     {
    #         "username": 'mubashir2',
    #         "hostname": 'hostname2',
    #         "interfaces": [
    #             {
    #                 "name": 'xdg',
    #                 "ip": '10.10.0.100'
    #             },
    #             {
    #                 "name": 'xdg2',
    #                 "ip": '10.10.1.100'
    #             } 
    #         ]
    #     },
    # ]
    return render_template("ipaddresses.html", hosts=enumerate(hosts))


# @login_required
@main.route("/restricted")
def restricted():
    return "You can only see this if you are logged in!", 200
