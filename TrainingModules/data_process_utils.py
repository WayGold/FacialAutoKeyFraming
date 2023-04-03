import os
import glob
import json
import pandas as pd
import numpy as np

from dataLoader import getImgArrAndPoseDf
from imgProcessor import resize_img

"""
data = {
    "0": {
        "CTRL_R_mouth_stickyInnerU": [0.0],
        "CTRL_neckCorrectivesMultiplyerU": [1.0],
        "CTRL_R_ear_up": [0.0],
        "CTRL_C_mouth_stickyD": [0.0],
        "CTRL_C_eye": [0.3556901919792986, -0.369528562826498]
    }
}

img = pd.DataFrame(resize_img('../Faceware/ROM_fwt/video/ROM_full/ROM.0000.jpg'))
img = np.array(img)
img = img.tolist()
print(img)

# Switch to DataFrame
df = pd.DataFrame.from_dict(data, orient='index')

# Add Img into column
df['Image'] = img

df.to_csv('output.csv', index=False)


# Read first json file
with open('../dataTools/DataCollector/out/10.json', 'r') as f1:
    data1 = json.load(f1)

# Read second json file
with open('../dataTools/DataCollector/ctrl_config.json', 'r') as f2:
    data2 = json.load(f2)
"""

# Read ctrl_config file
with open('../dataTools/DataCollector/ctrl_config.json') as f:
    ctrl_config = json.load(f)

# Read ctrl_data file
with open('../dataTools/DataCollector/out/10.json') as f:
    ctrl_data = json.load(f)

# Pick "Ctrl_" str
ctrl_keys = [k for k in ctrl_data["1"].keys() if "CTRL_" in k]

# Combine Ctrl name and its channel
ctrl = []
# 遍历 B 中的数据
for i in ctrl_keys:
    if i in ctrl_config:
        for n in ctrl_config[i]:
            ctrl.append(f"{i}{n}")

print(ctrl_keys)

# Switch to dataFrame
df = pd.DataFrame([ctrl])

# Set ctrl as column name
#df.columns = df.iloc[0]
#df = df.drop(df.index[0])

print(df)

# Import Image data
#img = pd.DataFrame(resize_img('../Faceware/ROM_fwt/video/ROM_full/ROM.0000.jpg'))
img_folder_path = "../Faceware/ROM_fwt/video/Test"

# 使用glob模块找到所有的jpg文件
img_list = glob.glob(os.path.join(img_folder_path, "*.jpg"))

img_data_list = []
# 遍历文件列表
for i in img_list:
    img_resize = pd.DataFrame(resize_img(i))
    img_data_list.append(img_resize)

img = np.array(img_data_list)
img = img.tolist()
#img = [x[0] for x in img] # delete the outest list
img_df = pd.DataFrame(img)
#print(img_df)



data_dir = "../Faceware/ROM_fwt/video/Test"
file_list = os.listdir(data_dir)
file_count = len(file_list)

print(file_count)

#img = np.array(img)
#img = img.tolist()

# 转换list为float
'''
unpacked_img = []
for sublist in img:
    for item in sublist:
        unpacked_img.append(item)

img = unpacked_img
print(img)
'''
count = 0
# Switch controllers data to df
ctrl_values = []
for k in ctrl_data.keys():
    #if int(k) == file_count:
    row = []
    for v in ctrl_data[k].values():
        row.extend(v)
    ctrl_values.append(row)
    count += 1
    if count >= file_count:
        break

ctrl_df = pd.DataFrame(ctrl_values)
print(ctrl_df)

#ctrl_df.columns = ctrl_df.iloc[0]
#ctrl_df = ctrl_df.drop(ctrl_df.index[0])

#df = df.loc[:,~df.columns.duplicated()].reset_index(drop=True)
#ctrl_df = ctrl_df.loc[:,~ctrl_df.columns.duplicated()].reset_index(drop=True)
#df = pd.concat([df, ctrl_df])

# Combine df and ctrl_df, delete index row
df = df.append(ctrl_df, ignore_index=True)
df.columns = df.iloc[0]
df = df.drop(df.index[0])

# Add Image data
df = df.reset_index(drop=True)
print(df)
print(img_df)
df['Image'] = img_df[0]


# Output as csv
df.to_csv('output.csv')

#getImgArrAndPoseDf(df)
#print(getImgArrAndPoseDf)

#df = pd.read_csv('../FacialAutoKeyFraming/TrainingModules/output.csv')

#print(df.info(verbose=True))
print('Row count is:', len(img_df.index))