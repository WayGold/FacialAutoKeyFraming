from torch.utils.data import Dataset
from torchvision import transforms

import numpy as np


class FacialPoseDataSet(Dataset):
    def __init__(self, i_df, transform_func=None, transform_param=None):
        self.img_arr, self.pose_df = getImgArrAndPoseDf(i_df)
        self.transform_func = transform_func
        self.transform_param = transform_param

        # Norm to [-1, 1]
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.5,), std=(0.5,))
        ])

    def __getitem__(self, index):
        img = self.img_arr[index].astype(np.uint8).reshape(96, 96)
        img = self.transform(img)

        # Extracting rows
        kpts = np.array(self.pose_df.iloc[index])

        if self.transform_func is not None:
            img, kpts = self.transform_func(img, kpts, self.transform_param)

        return img, kpts

    def __len__(self):
        return len(self.img_arr)


def getImgArrAndPoseDf(i_df):
    # Get img data
    img_arr = np.array(i_df.Image)
    # print(f'Size of Image Array - {len(img_arr)}')
    for i in range(len(img_arr)):
        img_arr[i] = np.fromstring(img_arr[i], sep=' ')

    # Get kpts data
    pose_df = i_df.drop(['Image'], axis=1)

    return img_arr, pose_df
