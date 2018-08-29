#!/usr/bin/python


def orgs(api):
    uri = "organizations/"
    return api.get(uri)


def networks(api, org_id):
    uri = "organizations/{}/networks".format(org_id)
    return api.get(uri)


def devices(api, net_id):
    uri = "networks/{}/devices".format(net_id)
    return api.get(uri)


def vlans(api, net_id):
    uri = "networks/{}/vlans".format(net_id)
    return api.get(uri)


def ports(api, serial):
    uri = "devices/{}/switchPorts".format(serial)
    return api.get(uri)


def templates(api, org_id):
    uri = "/organizations/{}/configTemplates".format(org_id)
    return api.get(uri)
