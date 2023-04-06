import torch
import torch.nn as nn
import numpy as np
import dataLoader as dl
import driver as dr

from torchvision import models
from torch.utils.data.sampler import SubsetRandomSampler, SequentialSampler


def loadModel(path, model_class):
    model = model_class
    model.load_state_dict(torch.load(path))
    model.eval()
    return model


def predict(model, imgs, kpts=None, vis=True, comp_kpts=None):
    with torch.no_grad():
        pred_poses = model(imgs)
    return pred_poses


if __name__ == '__main__':
    MODEL_PATH = 'best_model_0.0163.pt'

    train_csv = dr.load_csv(dr.TRAIN_CSV_PATH)
    print(f'Len of train csv: {len(np.array(train_csv.Image))}')

    _, val_df = dl.getTrainValidationDataSet(train_csv, 0.75)
    val_dataset = dl.FacialPoseDataSet(val_df)
    print('Size of validation set: {}'.format(len(val_dataset)))

    val_sampler = SequentialSampler(range(len(val_dataset)))
    val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=1, sampler=val_sampler, num_workers=4,
                                             pin_memory=True)
    print('Size of validation loader batches: {}'.format(len(val_loader)))

    NUM_CLASSES = 223
    resnet50 = models.resnet50(num_classes=NUM_CLASSES)
    resnet50.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    resnet50.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)

    resnet_model = loadModel(MODEL_PATH, resnet50)

    image, pose = next(iter(val_loader))
    pred = np.array(predict(resnet_model, image))
    print(pred)
    print(pose)
    print(pred.shape)
