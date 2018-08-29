#!/usr/bin/python


def unbind(api, net_id):
    uri = "/networks/{}/unbind".format(net_id)
    return api.post(uri)


def bind(api, net_id, data):
    uri = "/networks/{}/bind".format(net_id)
    return api.post(uri, data=data)
