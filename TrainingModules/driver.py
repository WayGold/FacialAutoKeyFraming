import os
import torch
import train
import numpy as np
import dataLoader as dl
import torch.optim as optim
import torch.nn as nn
from torchvision import models
from torch.utils.data.sampler import SubsetRandomSampler, SequentialSampler


def start_training():
    lr = 1e-3

    train_csv = None
    print(f'Len of train csv: {len(np.array(train_csv.Image))}')


