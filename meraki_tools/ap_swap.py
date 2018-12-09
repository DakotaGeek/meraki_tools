#!/usr/bin/python


# Built-In Libraries
import sys
import json


# Meraki Tools Libraries
from . import common
from . import __version__


def find_device(api, org_id, serial):
    devices = common.get.device_statuses(api, org_id)
    if not serial:
        print(json.dumps(devices, indent=4))
        sys.exit()
    else:
        for device in devices:
            if device["serial"].lower() == serial.lower():
                device_info = common.get.device(api, device["networkId"], device["serial"])
                return device_info


def remove_old_ap(api, old_ap):
    response = common.post.remove_device(api, old_ap["networkId"], old_ap["serial"])
    print(response)


def add_new_ap(api, old_ap, new_ap_serial):
    data = {"serial": new_ap_serial}
    response = common.post.claim_to_net(api, old_ap["networkId"], data)
    print(response)
    # print(response.text)


def update_old_ap(api, old_ap):
    new_name = "OLD_"+old_ap["name"]
    data = {
        "name": new_name
    }
    response = common.put.update_device(api, old_ap["networkId"], old_ap["serial"], data)
    print(response)


def update_new_ap(api, old_ap, new_ap_serial):
    move_atts = [
        "name",
        "tags",
        "lat",
        "lng",
        "address"
    ]
    data = {
        "moveMapMarker": True,
    }
    for attrib in move_atts:
        if old_ap[attrib]:
            data.update({attrib: old_ap[attrib]})
    print("Updating...")
    print(json.dumps(data, indent=4))
    response = common.put.update_device(api, old_ap["networkId"], new_ap_serial, data)
    print(response)


def start():
    parser, misc, required, optional = common.parser.parser(
                                            __version__.version,
                                            "AP Swap")
    optional.add_argument(
                        '-i', "--org_id",
                        help="Organization ID",
                        metavar='ORG',
                        dest="org_id")
    optional.add_argument(
                        '-o', "--old_ap_serial",
                        help="Serial number of old access point",
                        metavar='SERIAL',
                        dest="old_ap_serial")
    optional.add_argument(
                        '-n', "--new_ap_serial",
                        help="Serial number of new access point",
                        metavar='SERIAL',
                        dest="new_ap_serial")
    args = parser.parse_args()
    common.misc.check_args(parser, args)
    api = common.api.api(args.api_key)
    old_ap = find_device(api, args.org_id, args.old_ap_serial)
    print(json.dumps(old_ap, indent=4))
    # inv = common.get.inventory(api, args.org_id)
    # print(json.dumps(inv, indent=4))
    add_new_ap(api, old_ap, args.new_ap_serial)
    update_old_ap(api, old_ap)
    remove_old_ap(api, old_ap)
    update_new_ap(api, old_ap, args.new_ap_serial)


if __name__ == "__main__":
    start()
