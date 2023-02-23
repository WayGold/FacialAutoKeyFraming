import os
import json
import maya.cmds as cmds


def get_ctrl_config():
    my_select = cmds.ls(selection=True)
    select_ctrl = cmds.listRelatives(my_select, ad=True, type='transform')
    my_ctrl = []

    channel_list = ['.translateX', '.translateY', '.translateZ',
                    '.rotateX', '.rotateY', '.rotateZ',
                    '.scaleX', '.scaleY', '.scaleZ']

    for ctrl_name in select_ctrl:
        if ctrl_name in ['CTRL_L_mouth_lipsPressD', 'CTRL_R_mouth_lipsPressD']:
            continue
        if "CTRL_" in ctrl_name:
            my_ctrl.append(ctrl_name)

    '''
    for i, ctrl_name in enumerate(my_ctrl):
        ctrl_name = str(ctrl_name).split('Shape')[0]
        my_ctrl[i] = ctrl_name
    '''
    ctrl_config_dict = {}

    for i, child in enumerate(my_ctrl):
        ctrl_config_dict[child] = []
        for channelName in channel_list:
            if cmds.getAttr(child + channelName, k=True):
                ctrl_config_dict[child].append(channelName)

    print 'Len of config ' + str(len(ctrl_config_dict))

    return ctrl_config_dict


def write_ctrl_config(out_path):
    ctrl_config_dict = get_ctrl_config()
    json_dump(ctrl_config_dict, out_path)


def export_ctrl_value(out_path):
    ctrl_config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), u"ctrl_config.json")
    ctrl_config_dict = json_load(str(ctrl_config_path))

    data_dict = {}

    final_frame = cmds.findKeyframe(ctrl_config_dict, which='last')
    for frame in range(0, int(final_frame) + 1):
        cmds.currentTime(frame)
        frame_data = {}
        for ctrl in ctrl_config_dict:
            frame_data[ctrl] = []
            for channel_name in ctrl_config_dict[ctrl]:
                frame_data[ctrl].append(cmds.getAttr(ctrl + channel_name))
        data_dict[frame] = frame_data

    '''
    for ctrl in ctrl_config_dict:
        data_dict[ctrl] = []
        for channel_name in ctrl_config_dict[ctrl]:
            data_dict[ctrl].append(cmds.getAttr(ctrl + channel_name))
    '''
    
    print 'Len of data ' + str(len(data_dict))

    file_name = os.path.join(out_path, str(int(cmds.currentTime(query=True))) + '.json')
    json_dump(data_dict, file_name)


def json_dump(dict_data, json_out):
    """

    Args:
        dict_data:
        json_out:

    Returns:

    """
    with open(json_out, 'w') as f:
        f.write(json.dumps(dict_data))


def json_load(data_path):
    """

    Args:
        data_path (str):

    Returns:

    """
    with open(data_path) as f:
        return json.load(f)


def load_data_file(data_path):
    """

    Args:
        data_path:

    Returns:

    """
    ctrl_config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), u"ctrl_config.json")
    ctrl_config_dict = json_load(str(ctrl_config_path))
    data_dict = json_load(str(data_path))

    paste_ctrl_value(ctrl_config_dict, data_dict)


def paste_ctrl_value(ctrl_config_dict, data):
    """
    Paste the input data controller value to current frame.

    Args:
        ctrl_config_dict (Dict):    Dict[Controller Name]: List['channel name', '', ...]
        data (Dict):                Dict[Controller Name]: List[float, float, ...]

    Returns:                        None,  Paste the input data controller value to current frame.

    """
    print 'Len of config ' + str(len(ctrl_config_dict))
    print 'Len of data ' + str(len(data))

    for frame in data:
        for ctrl in ctrl_config_dict:
            for i, channel in enumerate(ctrl_config_dict[ctrl]):
                if not cmds.getAttr(ctrl + channel, lock=True):
                    cmds.setAttr(ctrl + channel, float(data[frame][ctrl][i]))
                    cmds.setKeyframe(ctrl + channel, time=frame)

    '''
    for ctrl in ctrl_config_dict:
        for i, channel in enumerate(ctrl_config_dict[ctrl]):
            if not cmds.getAttr(ctrl + channel, lock=True):
                cmds.setAttr(ctrl + channel, float(data[ctrl][i]))
    '''


if __name__ == '__main__':
    export_ctrl_value(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), u"out"))
