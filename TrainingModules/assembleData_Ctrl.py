import json
import numpy as np


def assemble_data(img_data, json_out):
    with open('F:/Homework/FacialAutoFraming/FacialAutoKeyFraming/dataTools/DataCollector/ctrl_config.json') as f:
        ctrl_config = json.load(f)

    with open('F:/Homework/FacialAutoFraming/FacialAutoKeyFraming/dataTools/DataCollector/out/10.json') as f:
        ctrl_data = json.load(f)
    ctrl_keys = [k for k in ctrl_data["1"].keys() if "CTRL_" in k]

    # Combine Ctrl name and its channel
    ctrl = []
    # iterable the ctrls name in ctrl_config
    for i in ctrl_keys:
        if i in ctrl_config:
            for n in ctrl_config[i]:
                ctrl.append(f"{i}{n}")

    pred = list(img_data)
    pred = pred[0]
    data = {}

    print(len(ctrl), len(pred))
    print(ctrl)

    for i in range(len(ctrl)):
        data[ctrl[i]] = [pred[i]]

    print(len(data))
    with open(json_out, 'w') as f:
        json.dump(data, f, default=lambda o: o.tolist() if isinstance(o, np.ndarray) else float(o))

    return data


# Use ctrl_config to reassemble controller name
'''
with open('F:/Homework/FacialAutoFraming/FacialAutoKeyFraming/dataTools/DataCollector/ctrl_config.json') as f:
    ctrl_config = json.load(f)

ctrl = []
for key, channel in ctrl_config.items():
    for i in channel:
        ctrl.append(key + i)

print(ctrl)
'''


