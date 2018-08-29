#!/usr/bin/python


# Built-In Libraries
import re
import sys


# Meraki Tools Libraries
from . import get


def confirm(message):
    confirm = raw_input("{} [N] ".format(message))
    if confirm.lower() == "y" or confirm.lower() == "yes":
        return True
    else:
        return False


def get_changes(current, saved, attribs, id_key, addkeys=None):
    changes = []
    for current_item in current:
        item_changes = {}
        item_id = current_item[id_key]
        saved_item = None
        for each in saved:
            if each[id_key] == item_id:
                saved_item = each
                break
        for attrib in attribs:
            if saved_item[attrib] != current_item[attrib]:
                item_changes.update({attrib: {"current": current_item[attrib], "new": saved_item[attrib]}})
        if item_changes:
            item_changes.update({id_key: item_id})
            if addkeys:
                for key in addkeys:
                    item_changes.update({key: current_item[key]})
            changes.append(item_changes)
    return changes


def get_switches(api, net_id):
    devices = get.devices(api, net_id)
    switches = []
    for device in devices:
        if device["model"][:2] == "MS":
            switches.append(device)
    return switches


def check_args(parser, args):
    """
    check_args checks for the existence of at least one argument
    from the command-line. If there are no arguments provided, we will print
    the help menu.
    """
    for key in args.__dict__:
        # If there is a value
        if args.__dict__[key]:
            # Then return back to start()
            return None
    # If we didn't return, then print help and quit
    parser.print_help()
    sys.exit()


def select_net(api):
    sel_org = selector(get.orgs(api))
    sel_net = selector(normalize_dict_list(get.networks(api, sel_org["id"])))
    return sel_net


def selector(list_of_dicts):
    # Make a copy so we don't modify the original
    list_of_dicts_copy = []
    for d in list_of_dicts:
        list_of_dicts_copy.append(dict(d))
    finder = {}
    index = 1
    for d in list_of_dicts_copy:
        finder.update({str(index): d.copy()})
        d.update({"#": str(index)})
        index += 1
    print(make_table(list(list_of_dicts_copy[0]), list_of_dicts_copy))
    picked = input("Select a # > ")
    return finder[str(picked)]


def normalize_dict_list(list_of_dicts):
    all_keys = []
    for d in list_of_dicts:
        for key in d:
            if key not in all_keys:
                all_keys.append(key)
    for d in list_of_dicts:
        for key in all_keys:
            if key not in d:
                d.update({key: None})
    return list_of_dicts


def make_table(columnorder, tabledata):
    ##### Check and fix input type #####
    if type(tabledata) != type([]): # If tabledata is not a list
        tabledata = [tabledata] # Nest it in a list
    ##### Set seperators and spacers #####
    tablewrap = "#" # The character used to wrap the table
    headsep = "=" # The character used to seperate the headers from the table values
    columnsep = "|" # The character used to seperate each value in the table
    columnspace = "  " # The amount of space between the largest value and its column seperator
    ##### Generate a dictionary which contains the length of the longest value or head in each column #####
    datalengthdict = {} # Create the dictionary for storing the longest values
    for columnhead in columnorder: # For each column in the columnorder input
        datalengthdict.update({columnhead: len(columnhead)}) # Create a key in the length dict with a value which is the length of the header
    for row in tabledata: # For each row entry in the tabledata list of dicts
        for item in columnorder: # For column entry in that row
            if len(re.sub(r'\x1b[^m]*m', "",  str(row[item]))) > datalengthdict[item]: # If the length of this column entry is longer than the current longest entry
                datalengthdict[item] = len(str(row[item])) # Then change the value of entry
    ##### Calculate total table width #####
    totalwidth = 0 # Initialize at 0
    for columnwidth in datalengthdict: # For each of the longest column values
        totalwidth += datalengthdict[columnwidth] # Add them all up into the totalwidth variable
    totalwidth += len(columnorder) * len(columnspace) * 2 # Account for double spaces on each side of each column value
    totalwidth += len(columnorder) - 1 # Account for seperators for each row entry minus 1
    totalwidth += 2 # Account for start and end characters for each row
    ##### Build Header #####
    result = tablewrap * totalwidth + "\n" + tablewrap # Initialize the result with the top header, line break, and beginning of header line
    columnqty = len(columnorder) # Count number of columns
    for columnhead in columnorder: # For each column header value
        spacing = {"before": 0, "after": 0} # Initialize the before and after spacing for that header value before the columnsep
        spacing["before"] = int((datalengthdict[columnhead] - len(columnhead)) / 2) # Calculate the before spacing
        spacing["after"] = int((datalengthdict[columnhead] - len(columnhead)) - spacing["before"]) # Calculate the after spacing
        result += columnspace + spacing["before"] * " " + columnhead + spacing["after"] * " " + columnspace # Add the header entry with spacing
        if columnqty > 1: # If this is not the last entry
            result += columnsep # Append a column seperator
        del spacing # Remove the spacing variable so it can be used again
        columnqty -= 1 # Remove 1 from the counter to keep track of when we hit the last column
    del columnqty # Remove the column spacing variable so it can be used again
    result += tablewrap + "\n" + tablewrap + headsep * (totalwidth - 2) + tablewrap + "\n" # Add bottom wrapper to header
    ##### Build table contents #####
    result += tablewrap # Add the first wrapper of the value table
    for row in tabledata: # For each row (dict) in the tabledata input
        columnqty = len(columnorder) # Set a column counter so we can detect the last entry in this row
        for column in columnorder: # For each value in this row, but using the correct order from column order
            spacing = {"before": 0, "after": 0} # Initialize the before and after spacing for that header value before the columnsep
            spacing["before"] = int((datalengthdict[column] - len(re.sub(r'\x1b[^m]*m', "",  str(row[column])))) / 2) # Calculate the before spacing
            spacing["after"] = int((datalengthdict[column] - len(re.sub(r'\x1b[^m]*m', "",  str(row[column])))) - spacing["before"]) # Calculate the after spacing
            result += columnspace + spacing["before"] * " " + str(row[column]) + spacing["after"] * " " + columnspace # Add the entry to the row with spacing
            if columnqty == 1: # If this is the last entry in this row
                result += tablewrap + "\n" + tablewrap # Add the wrapper, a line break, and start the next row
            else: # If this is not the last entry in the row
                result += columnsep # Add a column seperator
            del spacing # Remove the spacing settings for this entry
            columnqty -= 1 # Keep count of how many row values are left so we know when we hit the last one
    result += tablewrap * (totalwidth - 1) # When all rows are complete, wrap the table with a trailer
    return result
