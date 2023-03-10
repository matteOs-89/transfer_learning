
import torch
import torchvision
import torch.nn as nn

import torchvision.transforms as T
from torch.utils.data import DataLoader, TensorDataset


import sys

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import numpy as np
import matplotlib.pyplot as plt

"""In this task we will forcus on using transfer learning technique to classify EMNIST Letters dataset, Resnet18 Architechure will be used and the performance of the model we be evaluated. 

Resnet18 model first created in 2015 by Kaiming He, is a special type of convolutional neural network that makes building really deep neural networks without the worries of vanishing Gradient possible. This is because of the skip connection method built and embedded in its architecture.

The skip connection enables information/weights from previous blocks/layers to be added to the current block, meaning that residual weights from previous forward pass are then gathered and used to aid learning of the current block resulting to a more stabilized deep neural networks.

There are various Resnet models since first created, and the number after its name tell use how deep the model is. therefore
resnet18 are 18 layers deep.
"""

EmnistData = torchvision.datasets.EMNIST(root="emnist", 
                                    split="letters", 
                                    download=True)

EmnistData.class_to_idx

classindex = EmnistData.classes
print(classindex)

classindex = EmnistData.classes[1:]
print(classindex)

print(EmnistData.data.shape)

train_images = EmnistData.data.view(124800, 1, 28,28).float()

print(train_images.shape)

labels = EmnistData.targets
print(torch.sum(labels==0))

labels = (EmnistData.targets)-1
print(labels.shape)

print(torch.sum(labels==0))
torch.unique(labels)

train_images/= torch.max(train_images)

print(train_images.max())
print(train_images.min())

X_train, X_test, y_train, y_test = train_test_split(train_images, labels, test_size=0.2)
Val_data, X_test, Val_label, y_test = train_test_split(X_test, y_test, test_size=0.5)


train_data = TensorDataset(X_train, y_train)

val_data = TensorDataset(Val_data, Val_label)

test_data = TensorDataset(X_test, y_test)


batch_size = 128
train_loader = DataLoader(train_data,
                          shuffle=True,
                          batch_size=batch_size,
                          drop_last=True)


val_loader = DataLoader(val_data,
                          shuffle=False,
                          batch_size=test_data.tensors[0].shape[0],
                          )

test_loader = DataLoader(test_data,
                          shuffle=False,
                          batch_size=test_data.tensors[0].shape[0],
                          )

print(train_loader.dataset.tensors[0].shape[0]) 
print(val_loader.dataset.tensors[0].shape[0])  
print(test_loader.dataset.tensors[0].shape[0])

"""For this task i will freeze all layers, but fine tune the input later to accommodate our input shape, 
this means changing the number of channel input from three to one. 
This is because Resnet was created to classify colored images available on imagenet, however we are working on grayscale images for this task which 1 one channeled.

I will also change the output layer shape to accomodate inference for 26 image classes as provided in the MNIST Letter dataset, 
instead of the  1000 classes Resnet provides.
"""

resnet18 = torchvision.models.resnet18(weights=True)
for p in resnet18.parameters():

  p.requires_grad = False


resnet18.conv1 = nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False) # changing input shape from 3 channels to 1, in order to accept our dataset 

resnet18.fc = nn.Linear(512, 26) 

batch=torch.rand(32,1,64,64) # input random to noise image to test the model architecture

print(resnet18(batch).size)

loss_fun = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(resnet18.parameters(),lr=0.001,momentum=.9)


def trainCreatedModel(model,lossfun=loss_fun, optimizer=optimizer, 
                      train_loader=train_loader, val_loader=test_loader, 
                      epochs=10 ):

  """
  This function train and evaluate our model while also saving specified checkpoints
  """

  Trainloss= torch.zeros(epochs)
  Testloss = torch.zeros(epochs)
  TrainACC = torch.zeros(epochs)
  TestACC  = torch.zeros(epochs)


  for e in range(epochs):

    model.train()
    batchloss = []
    batchACC  = []


    for X,y in train_loader:

     
      yhat = model(X)
      loss = lossfun(yhat, y)

      optimizer.zero_grad()
      loss.backward()
      optimizer.step()

      batchloss.append(loss.item())
      batchACC.append(torch.mean((torch.argmax(yhat,axis=1) == y).float()).item() )

    Trainloss[e]=np.mean(batchloss)
    TrainACC[e] = 100*np.mean(batchACC)


    model.eval()
    with torch.no_grad():

      X,y = next(iter(val_loader))

      # validation prediction

      T_pred = model(X)
      loss = lossfun(T_pred, y)

      Testloss[e] = loss
      TestACC[e] = 100*torch.mean((torch.argmax(T_pred, axis=1)==y).float()).item()
      
  

    
    msg = f"Finished epoch {e +1}/{epochs} Train Accuracy: {batchACC[-1]} Train Loss: {batchloss[-1]}"
    sys.stdout.write("\r" + msg)
   

  return Trainloss, Testloss, TrainACC, TestACC

Trainloss, Testloss, TrainACC, TestACC = trainCreatedModel(resnet18, lossfun=loss_fun, optimizer=optimizer, 
                    train_loader=train_loader, val_loader=val_loader, 
                      epochs=10)

