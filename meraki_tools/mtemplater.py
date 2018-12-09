#!/usr/bin/python


# Built-In Libraries
import json


# Meraki Tools Libraries
from . import common
from . import __version__


def print_vlan_changes(changes):
    table_data = []
    columns = ["id"]
    print(json.dumps(changes, indent=4))
    for vlan in changes:
        row = {"id": vlan["id"]}
        for attrib in vlan:
            if type(vlan[attrib]) == dict:
                if "current "+attrib not in columns:
                    columns.append("current "+attrib)
                    columns.append("new "+attrib)
                row.update({"current "+attrib: vlan[attrib]["current"]})
                row.update({"new "+attrib: vlan[attrib]["new"]})
        table_data.append(row)
    table_data = common.misc.normalize_dict_list(table_data)
    print(common.misc.make_table(columns, table_data))


def print_port_changes(changes):
    table_data = []
    columns = ["name", "port"]
    for switch in changes:
        for change in switch["changes"]:
            row = {"name": switch["name"]}
            row.update({"port": change["number"]})
            for attrib in change:
                if attrib != "number":
                    if "current "+attrib not in columns:
                        columns.append("current "+attrib)
                        columns.append("new "+attrib)
                    row.update({"current "+attrib: change[attrib]["current"]})
                    row.update({"new "+attrib: change[attrib]["new"]})
            table_data.append(row)
    table_data = common.misc.normalize_dict_list(table_data)
    print(common.misc.make_table(columns, table_data))


def rebind(api):
    org = common.misc.selector(common.get.orgs(api))
    net = common.misc.selector(common.misc.normalize_dict_list(common.get.networks(api, org["id"])))
    print(json.dumps(net, indent=4))
    if "configTemplateId" in net:
        if net["configTemplateId"]:
            if common.misc.confirm("Unbind Template?"):
                common.post.unbind(api, net["id"])
    new_template = common.misc.selector(common.get.templates(api, org["id"]))
    if common.misc.confirm("Bind New Template?"):
        data = {"configTemplateId": new_template["id"], "autoBind": True}
        resp = common.post.bind(api, net["id"], data)
        print(resp)


def save_config(api, filename):
    net = common.misc.select_net(api)
    print("Pulling VLAN Config")
    vlans = common.get.vlans(api, net["id"])
    switches = common.misc.get_switches(api, net["id"])
    index = 1
    for switch in switches:
        print("Pulling Switch ({}) ({})".format(
            switch["name"],
            "{}/{}".format(index, len(switches))
        ))
        ports = common.get.ports(api, switch["serial"])
        switch.update({"port_configs": ports})
        index += 1
    print("Saving to ({})".format(filename))
    f = open(filename, "w")
    data = {"vlans": vlans, "switches": switches}
    f.write(json.dumps(data, indent=4))
    f.close()
    print("Save to ({}) complete!".format(filename))


def write_config(api, filename):
    f = open(filename, "r")
    saved_data = json.loads(f.read())
    f.close()
    write_vlans(api, saved_data)
    write_ports(api, saved_data)


def write_vlans(api, saved_data):
    net_id = saved_data["vlans"][0]["networkId"]
    current_vlans = common.get.vlans(api, net_id)
    saved_vlans = saved_data["vlans"]
    changes = common.misc.get_changes(
        current_vlans,
        saved_vlans,
        ["subnet", "applianceIp"],
        "id",
        addkeys=["networkId"])
    print_vlan_changes(changes)
    confirm = raw_input("Make VLAN Changes? [N] ")
    if confirm.lower() == "y" or confirm.lower() == "yes":
        for vlan in changes:
            vlan_num = vlan["id"]
            net_id = vlan["networkId"]
            data = {}
            for attrib in vlan:
                if type(vlan[attrib]) == dict:
                    data.update({attrib: vlan[attrib]["new"]})
            print("Updating VLAN ({}) with: {}".format(vlan_num, data))
            response = common.put.vlan(api, net_id, vlan_num, data)
            if "errors" in response:
                print(response)


def write_ports(api, saved_data):
    index = 1
    changes = []
    for switch in saved_data["switches"]:
        print("Processing switch ({}) ({})".format(switch["name"], "{}/{}".format(index, len(saved_data["switches"]))))
        saved_ports = switch["port_configs"]
        # print(json.dumps(saved_ports, indent=4))
        current_ports = common.get.ports(api, switch["serial"])
        # print(json.dumps(current_ports, indent=4))
        switch_changes = common.misc.get_changes(
            current_ports,
            saved_ports,
            ["vlan", "type"],
            "number")
        print(switch_changes)
        if switch_changes:
            switch.update({"changes": switch_changes})
            changes.append(switch)
        index += 1
    print_port_changes(changes)
    confirm = raw_input("Make Port Changes? [N] ")
    if confirm.lower() == "y" or confirm.lower() == "yes":
        for switch in changes:
            for port in switch["changes"]:
                port_num = port["number"]
                data = {}
                for attrib in port:
                    if attrib != "number":
                        data.update({attrib: port[attrib]["new"]})
                print("Updating switch ({}) Port ({}) with: {}".format(switch["name"], port_num, data))
                response = common.put.port(api, switch["serial"], port_num, data)





def start():
    parser, misc, required, optional = common.parser.parser(
                                            __version__.version,
                                            "Templater")
    optional.add_argument(
                        '-r', "--rebind",
                        help="Bind to new configuration template",
                        dest="rebind",
                        action='store_true')
    optional.add_argument(
                        '-s', "--save_to_file",
                        help="Save port and VLAN configs to a JSON file",
                        metavar='FILENAME',
                        dest="save_to_file")
    optional.add_argument(
                        '-w', "--write_from_file",
                        help="Write port configs from a file",
                        metavar='FILENAME',
                        dest="write_from_file")
    args = parser.parse_args()
    common.misc.check_args(parser, args)
    api = common.api.api(args.api_key)
    if args.save_to_file:
        save_config(api, args.save_to_file)
    if args.rebind:
        rebind(api)
    if args.write_from_file:
        write_config(api, args.write_from_file)


if __name__ == "__main__":
    start()
