#! /usr/bin/python

import os
import socket
import fcntl
import struct
import json
import getpass
import requests

URL = "http://192.168.0.101:5000/register_ips"

class IpChangeNotifier():
    def __init__(self, filename="ip_addresses.json"):
        
        self.filename = filename
        self.update = False
        self.prev_ips = []
        file = None
        self.interfaces = self.get_interfaces()
        try:
            file = open(self.filename, "r")
            self.prev_ips = json.loads(file.read())
        except:
            self.prev_ips = []
            self.update = True
        updated_ips = self.get_updated_ips()
        if self.update:
            self.notify_updated_ips(updated_ips)

    def get_interfaces(self):
        self.interfaces = os.listdir('/sys/class/net')
        return self.interfaces

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])

    def get_updated_ips(self):
        current_ips = []
        for interface in self.interfaces:
            try:
                prev_ip = ""
                for iface in self.prev_ips:
                    if  iface["name"] == iface["name"]:
                        prev_ip = iface["ip"]
                current_ip = self.get_ip_address(interface)
                current_ips.append({"name": interface, "ip": current_ip})
                if not self.update:
                    self.update = current_ip != prev_ip
            except:
                self.update = True
                current_ips.append({"name": interface, "ip": current_ip})
                continue
        return current_ips

    def notify_updated_ips(self, updated_ips):
        text = "\n-----------New Ip addresses for {}@{}----------\n".format(getpass.getuser(), socket.gethostname())
        _header = ["interface", "ip"]
        row_format ="{:>15}" * (len(_header) + 1)
        text += row_format.format("", *_header) + "\n"
        _packet = {"username": getpass.getuser(), "hostname": socket.gethostname(), "interfaces": updated_ips}
        for iface in updated_ips:
            text += row_format.format("", *[iface["name"],iface["ip"]]) + "\n"
        # {"username":"json", "hostname":"jsonhost", "interfaces": [{"name": "xda", "ip": "192.168.0.100"}, {"name": "xda2", "ip": "192.168.0.200"}]}
        res = requests.post(URL, json=_packet)
        print(text)
        if res:
            json.dump(updated_ips, open(self.filename, "w"))
        else:
            print("\n----------error------------\n")


if __name__ == "__main__":
    ip_change_notifier = IpChangeNotifier()


# for iface in os.listdir('/sys/class/net'):
#     ip_dict[iface] = get_ip_address(ifaces)  # '192.168.0.110'