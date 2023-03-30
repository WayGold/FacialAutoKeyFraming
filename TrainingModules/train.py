import torch
import numpy as np
from torchvision import models


def RMSELoss(output, target):
    return torch.sqrt(torch.mean(torch.square(output - target)))


def train_model(model, optim, loader_train, loader_val, scheduler=None,
                loss_fn=RMSELoss, epochs=1, log_every=30):

    train_losses, val_losses = [], []
    min_val_loss = np.Inf

    USE_GPU, device = check_GPU()
    print('Using Device - {}'.format(device))
    model = model.to(device=device)  # move the model parameters to CPU/GPU

    for e in range(epochs):
        train_loss = 0

        print('Starting Epoch: {}/{} '.format(e + 1, epochs))
        model.float().train()
        print('Train Mode Set to True.')

        for i, (img, poses) in enumerate(loader_train):
            if i == 0:
                print('Starting the first batch...')

            if USE_GPU:
                img = img.type(torch.float32).cuda()
                poses = poses.type(torch.float32).cuda()

            # Zero your gradients for every batch!
            optim.zero_grad()

            # Make predictions for this batch
            prediction = model(img)
            loss = loss_fn(prediction, poses)

            # Compute the loss and its gradients
            loss.backward()
            optim.step()

            train_loss += loss.item()

            if i % log_every == 0:
                print('Iteration - {}: '.format(i + 1),
                      "Average Training Loss: {:.4f}".format(train_loss / (i + 1)))

        # We don't need gradients on to do reporting
        model.train(False)

        print('Evaluating..')
        val_loss = evaluate(model, loader_val, loss_fn)

        if scheduler is not None:
            scheduler.step(val_loss)

        train_losses.append(train_loss / len(loader_train))
        val_losses.append(val_loss / len(loader_val))

        print("Average Training Loss: {:.4f}".format(train_losses[-1]),
              "Average Val Loss: {:.4f}".format(val_losses[-1]))

        if val_loss < min_val_loss:
            min_val_loss = val_loss
            torch.save(model.state_dict(), './best_model.pt')
            print('Improvement Detected, Saving to ./best_model.pt')


def evaluate(model, val_loader, loss_fn):
    USE_GPU, device = check_GPU()
    val_loss = 0

    with torch.no_grad():
        model.eval()
        for img, poses in val_loader:

            if USE_GPU:
                img = img.cuda()
                poses = poses.cuda()

            prediction = model(img)
            loss = loss_fn(prediction, poses)
            val_loss += loss.item()

    return val_loss


def check_GPU():
    USE_GPU = False
    device = torch.device('cpu')

    if torch.cuda.is_available():
        USE_GPU = True
        device = torch.device('cuda')

    return USE_GPU, device
