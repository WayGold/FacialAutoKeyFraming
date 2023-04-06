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
        img = self.img_arr[index].astype(np.uint8).reshape(160, 90)
        img = self.transform(img)

        # Extracting rows
        poses = np.array(self.pose_df.iloc[index])

        if self.transform_func is not None:
            img, poses = self.transform_func(img, poses, self.transform_param)

        return img, poses

    def __len__(self):
        return len(self.img_arr)


def getImgArrAndPoseDf(i_df):
    """
        Split input df into img data array and poses data array.

        Args:
            i_df:       Input pd.Dataframe of all data to split

        Returns:        List    -   image data np array, poses data dataframe.

        """
    # Get img data
    img_arr = np.array(i_df.Image)
    # print(f'Size of Image Array - {len(img_arr)}')

    for i in range(len(img_arr)):
        img_arr[i] = np.fromstring(img_arr[i], sep=' ')

    # Get kpts data
    pose_df = i_df.drop(['Image'], axis=1)

    return img_arr, pose_df


def getTrainValidationDataSet(i_df, train_val_percentage):
    """

    Args:
        i_df (pandas.DataFrame):            Input DataFrame to split into training
                                            and validation set.
        train_val_percentage (float):       Percentage to split.

    Returns:    (pandas.DataFrame, pandas.DataFrame)   -    training set and
                                                            validation set

    """
    len_df = len(i_df)
    rand_idx = list(range(len_df))
    np.random.shuffle(rand_idx)

    split_idx = int(np.floor(len_df * train_val_percentage))
    train_idx, val_idx = rand_idx[:split_idx], rand_idx[split_idx:]

    train_df = i_df.iloc[train_idx]
    val_df = i_df.iloc[val_idx]

    return train_df, val_df
