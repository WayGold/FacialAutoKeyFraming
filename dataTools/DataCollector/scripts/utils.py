import os
import json
import maya.cmds as cmds


def getCtrlValue():
    my_group = cmds.ls(selection=True, type="transform")[0]
    my_ctrl = cmds.listRelatives(my_group, children=True)
    channel_list = ['.translateX', '.translateY', '.translateZ',
                    '.rotateX', '.rotateY', '.rotateZ',
                    '.scaleX', '.scaleY', '.scaleZ']
    ctrl_confit_dict = {}

    for i, child in enumerate(my_ctrl):
        ctrl_confit_dict[child] = []
        for channelName in channel_list:
            if cmds.getAttr(child + channelName, k=True):
                ctrl_confit_dict[child].append(channelName)
