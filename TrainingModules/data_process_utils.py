import os
import glob
import json
import pandas as pd
import numpy as np

from dataLoader import getImgArrAndPoseDf
from imgProcessor import resize_img


def load_ctrl_config_file(data_path):
    # Read ctrl_config file
    with open(data_path) as f:
        ctrl_config = json.load(f)
    return ctrl_config


def load_ctrl_data(data_path):
    # Read ctrl_data file
    data_name, ext = os.path.splitext(os.path.basename(str(data_path)))
    with open(data_path) as f:
        ctrl_data = json.load(f)

    return ctrl_data, data_name


def load_img(data_path):
    # Read Img path
    img_folder_path = str(data_path)

    # iterable all folder
    img_list = glob.glob(os.path.join(img_folder_path, "*.jpg"))
    img_data_list = []

    return img_list, img_data_list


def data_process(out_path, img_path, config_path, data_path):
    ctrl_config = load_ctrl_config_file(config_path)
    ctrl_data, data_name = load_ctrl_data(data_path)
    # Pick "Ctrl_" str
    ctrl_keys = [k for k in ctrl_data["1"].keys() if "CTRL_" in k]

    # Combine Ctrl name and its channel
    ctrl = []
    # iterable the ctrls name in ctrl_config
    for i in ctrl_keys:
        if i in ctrl_config:
            for n in ctrl_config[i]:
                ctrl.append(f"{i}{n}")
    # print(ctrl_keys)

    # Switch to dataFrame
    df = pd.DataFrame([ctrl])
    img_list, img_data_list = load_img(img_path)

    for i in img_list:
        img_resize = pd.DataFrame(resize_img(i))
        img_data_list.append(img_resize)

    img = np.array(img_data_list)
    img = img.tolist()
    img_df = pd.DataFrame(img)
    # print(img_df)

    # Calculate Img Count
    data_dir = str(img_path)
    file_list = os.listdir(data_dir)
    file_count = len(file_list)
    # print(file_count)

    count = 0
    # Switch controllers data to df
    ctrl_values = []
    for k in ctrl_data.keys():
        # if int(k) == file_count:
        row = []
        for v in ctrl_data[k].values():
            row.extend(v)
        ctrl_values.append(row)
        count += 1
        if count >= file_count:
            break

    ctrl_df = pd.DataFrame(ctrl_values)

    # Combine df and ctrl_df, delete index row
    df = df.append(ctrl_df, ignore_index=True)
    df.columns = df.iloc[0]
    df = df.drop(df.index[0])

    # Add Image data
    df = df.reset_index(drop=True)
    df['Image'] = img_df[0]

    # Output as csv
    file_name = os.path.join(out_path, str(data_name) + '_withImg_data' + '.csv')
    df.to_csv(file_name, index=False)
    print('Row count is:', len(img_df.index))


def import_csv(data_path):
    # Read csv Path
    csv_path = (str(data_path))
    # Read All CSV Data
    all_csv_files = glob.glob(os.path.join(csv_path, '*.csv'))
    print(all_csv_files)
    return all_csv_files


def combine_csv(new_path, csv_path):
    all_csv_files = import_csv(csv_path)
    # Combine & export
    combine_df = pd.concat([pd.read_csv(f) for f in all_csv_files], ignore_index=True)
    new_csv = os.path.join(new_path, 'combined_data' + '.csv')
    combine_df.to_csv(new_csv, index=False)
    print(combine_df)
