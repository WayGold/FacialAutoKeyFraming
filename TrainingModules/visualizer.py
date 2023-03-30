import numpy as np
import matplotlib.pyplot as plt


def vis_loss(train_losses, val_losses):
    """

    Args:
        train_losses:
        val_losses:

    Returns:

    """
    plt.tick_params(colors='black')
    plt.plot(train_losses, label='Training Loss')
    plt.plot(val_losses, label='Validation Loss')
    plt.legend(frameon=False)
    plt.show()
