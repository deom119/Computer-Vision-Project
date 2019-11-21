import cv2
import numpy
import argparse
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from src.detect_im import detect_digits


import torch
from sklearn.cluster import MiniBatchKMeans
from torchvision import datasets, transforms
from PIL import Image
import matplotlib.pyplot as plt


# gets webcam data and displays it
samplingRate = 10

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # 3 input image channel, 6 output channels, 3x3 square convolution
        # kernel
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 5 * 5, 120)  # 6*6 from image dimension
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        # Max pooling over a (2, 2) window
        x = self.pool(F.relu(self.conv1(x)))

        # If the size is a square you can only specify a single number
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16*5*5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
def colorQuantize(img, colors):

    image = img
    (h, w) = image.shape[:2]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    clt = MiniBatchKMeans(n_clusters=colors)
    labels = clt.fit_predict(image)
    quant = clt.cluster_centers_.astype("uint8")[labels]
    quant = quant.reshape((h, w, 3))
    quant = cv2.cvtColor(quant, cv2.COLOR_LAB2BGR)
    return quant


def preprocess(img):
    # convert to binary, segment image
    # or get multiple image segments with possible numbers
    # need blob detection or something to determine if number exists
    # then apply directly

    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (32,32))
    #cv2.imshow('sampling', img)
    #img = img.astype('float32')
    img = colorQuantize(img, 4);
    #img = img /255
    #img = 1 - img
    #img = img.reshape(28, 28, 1)

    #cv2.imshow('sampling', img)
    plt.figure(1)
    plt.imshow(img)
    #plt.show(block = False)
    plt.show()
    return img


def main():
    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    PATH = './svhn_net.pth'
    net = Net()
    net.load_state_dict(torch.load(PATH))
    cam = cv2.VideoCapture(0)
    counter = 0
    while True:
        ret_val, img = cam.read()
        # img is an rgb array
        #cv2.imshow('my webcam', img)
        #img = img[80:400, 100:540]     #cropping for my webcam
        #cv2.imshow('cropped', img)
        # add sampling rate
        if counter == samplingRate:
            # cv2.imshow('sampling', img)
            img_out = img

            # ADD each blob here
            images = detect_digits(img_out)
            # For EACH BLOB
            counter = 0
            for img_out in images:
                img_out = preprocess(img_out)
            
                img_out = transform(img_out)
                img_out = img_out[None]
                outputs = net(img_out)
                _, predicted = torch.max(outputs.data, 1)
                print(predicted)
        counter = counter + 1
        #outputs = net()
        #_, predicted = torch.max(outputs.data, 1)
        #print(predicted)



if __name__ == '__main__':
    main()