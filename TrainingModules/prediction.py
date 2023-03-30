import torch


def loadModel(path, model_class):
    model = model_class
    model.load_state_dict(torch.load(path))
    model.eval()
    return model


def predict(model, imgs, kpts=None, vis=True, comp_kpts=None):

    with torch.no_grad():
        pred_poses = model(imgs)

    return pred_poses
