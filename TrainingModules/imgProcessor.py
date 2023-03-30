import cv2


def resize_img(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print('Original Dimensions : ', img.shape)

    # scale_percent = 20  # percent of original size
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)
    dim = (90, 160)

    # resize image
    resized = cv2.resize(grey_img, dim, interpolation=cv2.INTER_AREA)

    print('Resized Dimensions : ', resized.shape)

    cv2.imshow("Resized image", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(resized.reshape(1, 90 * 160))


if __name__ == '__main__':
    test_img = '../Faceware/ROM_fwt/video/ROM_full/ROM.0000.jpg'
    resize_img(test_img)
