import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
from svhn_nn.model import Net


transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = torchvision.datasets.SVHN(root='../../data', split='train', transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=5,
                                          shuffle=True, num_workers=2)


#def imshow(img, labels):
#    img = img / 2 + 0.5     # unnormalize
#    npimg = img.numpy()
#    plt.imshow(np.transpose(npimg, (1, 2, 0)))
#    classes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
#    i= []
#    for j in range(5):
#     i += classes[labels[j]]
#    plt.xlabel(i)
#    plt.show()
#

# get some random training images
#dataiter = iter(trainloader)
#images, labels = dataiter.next()


# show images
#imshow(torchvision.utils.make_grid(images),labels)
# print labels
#print(' '.join('%5s' % labels[j] for j in range(4)))







#warm start model with MNIST trained model
net = Net()
#PATH = "../src/mnist_cnn.pt"
#net.load_state_dict(torch.load(PATH), strict=False)

# Define a Loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
                                            
#Train the network
loss_epoch_array = np.zeros((1, 2))
for epoch in range(10):  # loop over the dataset multiple times

    running_loss = 0.0

    for i, data in enumerate(trainloader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
        if i % 2000  == 1999:    # print every 2000 mini-batches
            print('[%d, %5d] loss: %.3f' %
                  (epoch + 1, i + 1, running_loss / 2000))
            loss_epoch_array = np.concatenate((loss_epoch_array, np.array([[epoch + 1, running_loss/2000]])))
            running_loss = 0.0
np.save("loss_epoc_array", loss_epoch_array)

print('Finished Training')

#PATH = './svhn_net_2.pth'
#torch.save(net.state_dict(), PATH)

