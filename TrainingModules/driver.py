import os
import torch
import train
import logging
import pandas as pd
import numpy as np
import dataLoader as dl
import torch.optim as optim
import torch.nn as nn
from torchvision import models
from torch.utils.data.sampler import SubsetRandomSampler, SequentialSampler

TRAIN_CSV_PATH = '../TrainingData/combined_data.csv'


def load_csv(path):
    """
    Load the csv file from path into pd dataframe

    Args:
        path:       Path to the local csv data file

    Returns:        pd.DataFrame    -   pd dataframe of all data

    """
    _csv = pd.read_csv(path)
    logging.info(f'{path} has length - {len(_csv)}')
    return _csv


def start_training():
    lr = 6e-2

    train_csv = load_csv(TRAIN_CSV_PATH)
    print(f'Len of train csv: {len(np.array(train_csv.Image))}')

    train_df, val_df = dl.getTrainValidationDataSet(train_csv, 0.75)

    train_dataset = dl.FacialPoseDataSet(train_df)
    val_dataset = dl.FacialPoseDataSet(val_df)

    print('Size of training set: {}'.format(len(train_dataset)))
    print('Size of validation set: {}'.format(len(val_dataset)))

    print(train_dataset.img_arr.shape)

    # TODO:
    # Add Augmentation Modules Here

    # End TODO

    train_sampler = SubsetRandomSampler(range(len(train_dataset)))
    val_sampler = SequentialSampler(range(len(val_dataset)))

    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=128, sampler=train_sampler, num_workers=4,
                                               pin_memory=True)
    val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=128, sampler=val_sampler, num_workers=4,
                                             pin_memory=True)

    print('Size of training loader batches: {}\nSize of validation loader batches: {}'.format(len(train_loader),
                                                                                              len(val_loader)))

    # TODO: Load Model Here
    NUM_CLASSES = 223
    resnet50 = models.resnet50(num_classes=NUM_CLASSES)
    resnet50.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    resnet50.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)

    use_model = resnet50

    optimizer = optim.Adam(use_model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', verbose=True, patience=5)
    train.train_model(use_model, optimizer, train_loader, val_loader, scheduler=scheduler,
                      loss_fn=train.RMSELoss, epochs=250)


if __name__ == '__main__':
    start_training()
