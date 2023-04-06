import cv2
import driver
import logging
import numpy as np
import dataLoader as dl
import matplotlib.pyplot as plt
import imgProcessor as ip


if __name__ == '__main__':
    test_img_path = '../Faceware/ROM_fwt/video/ROM_full/ROM.0000.jpg'

    logging.getLogger().setLevel(logging.INFO)
    test_df = driver.load_csv(driver.TRAIN_CSV_PATH)
    test_df.info(verbose=True)

    print(f'Len of train csv: {len(np.array(test_df.Image))}')

    train_df, val_df = dl.getTrainValidationDataSet(test_df, 0.75)
    # print(type((np.array(train_df.Image))[0]))
    # print(((np.array(train_df.Image))[0]))
    # test_img_str = np.array(train_df.Image)[0]
    # test_img = np.fromstring(test_img_str[1:-1], sep=', ')

    # img_arr, pose_df = dl.getImgArrAndPoseDf(train_df)
    # print(test_img)
    # plt.imshow(test_img.reshape(90, 160), cmap='gray')
    # plt.show()

    # resized_img = ip.resize_img(test_img_path)
    # print(resized_img)
    # plt.imshow(resized_img.reshape(160, 90), cmap='gray')
    # plt.show()

    train_dataset = dl.FacialPoseDataSet(train_df)
    val_dataset = dl.FacialPoseDataSet(val_df)

    print('Size of training set: {}'.format(len(train_dataset)))
    print('Size of validation set: {}'.format(len(val_dataset)))

    img, pose = train_dataset[0]
    print(img.shape)
    print(img)

    plt.imshow(img.reshape(160, 90), cmap='gray')
    plt.show()
