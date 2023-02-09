import os
import json
import maya.cmds as cmds


def json_dump(dict_data, json_out):
    """

    Args:
        dict_data:
        json_out:

    Returns:

    """
    with open(json_out, 'w') as f:
        f.write(json.dumps(dict_data))
    json.dump(dict_data, json_out)


def json_load(data_path):
    """

    Args:
        data_path (str):

    Returns:

    """
    with open(data_path) as f:
        return json.load(f)


def paste_ctrl_value(ctrl_config_dict, data):
    """
    Paste the input data controller value to current frame.

    Args:
        ctrl_config_dict (Dict):    Dict[Controller Name]: List['channel name', '', ...]
        data (Dict):                Dict[Controller Name]: List[float, float, ...]

    Returns:                        None,  Paste the input data controller value to current frame.

    """
    for ctrl in ctrl_config_dict:
        for i, channel in enumerate(ctrl_config_dict[ctrl]):
            cmds.setAttr(ctrl + channel, float(data[ctrl][i]))
