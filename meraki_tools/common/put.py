#!/usr/bin/python


def port(api, serial, number, data):
    uri = "devices/{}/switchPorts/{}".format(serial, number)
    return api.put(uri, data)


def vlan(api, net_id, vlan_id, data):
    uri = "networks/{}/vlans/{}".format(net_id, vlan_id)
    return api.put(uri, data)


def update_device(api, net_id, serial, data):
    uri = "networks/{}/devices/{}".format(net_id, serial)
    return api.put(uri, data)
