#!/usr/bin/python


def unbind(api, net_id):
    uri = "networks/{}/unbind".format(net_id)
    return api.post(uri)


def bind(api, net_id, data):
    uri = "networks/{}/bind".format(net_id)
    return api.post(uri, data=data)


def remove_device(api, net_id, serial):
    uri = "networks/{}/devices/{}/remove".format(net_id, serial)
    return api.post(uri)


def claim_to_net(api, net_id, data):
    uri = "networks/{}/devices/claim".format(net_id)
    return api.post(uri, data=data)
