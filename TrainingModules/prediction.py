import cv2
import torch
import torch.nn as nn
import numpy as np
import dataLoader as dl
import driver as dr
import assembleData_Ctrl as ac


from torchvision import models
from torchvision import transforms
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


def predict_raw(model, img_path):
    """

    Args:
        model:
        img_path:        Input image must be of size (1920, 1080)

    Returns:

    """

    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    dim = (90, 160)
    # resize image
    resized = cv2.resize(grey_img, dim, interpolation=cv2.INTER_AREA)
    resized = np.array(resized)

    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.ToTensor(),
        transforms.Normalize(mean=(0.5,), std=(0.5,))
    ])

    img = transform(resized.astype(np.uint8).reshape(160, 90))
    img = img[None, :]

    with torch.no_grad():
        pred_pose = model(img)

    return pred_pose


def test_loader():
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
    print(image.shape)
    pred = np.array(predict(resnet_model, image))
    print(pred)
    print(pose)
    print(pred.shape)


def test_single_img():
    MODEL_PATH = 'best_model_0.0077.pt'
    test_img = r'F:\Homework\FacialAutoFraming\FacialAutoKeyFraming\PerfomanceClips\GotTB_01_fwt\video\GotTB_01_full\GotTB_01.0650.jpg'

    NUM_CLASSES = 223
    resnet50 = models.resnet50(num_classes=NUM_CLASSES)
    resnet50.avgpool = nn.AdaptiveAvgPool2d((1, 1))
    resnet50.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)

    resnet_model = loadModel(MODEL_PATH, resnet50)

    pred = np.array(predict_raw(resnet_model, test_img))
    ac.assemble_data(pred, '../dataTools/DataCollector/out/ctrl_out.json')
    return pred


if __name__ == '__main__':
    # test_loader()

    print('Result - ', test_single_img())

