# Resnet18 transfer learning

In this task we will forcus on using transfer learning technique to classify EMNIST Letters dataset, Resnet18 Architechure will be used and the performance of the model we be evaluated.

Resnet18 model first created in 2015 by Kaiming He, is a special type of convolutional neural network that makes building really deep neural networks without the worries of vanishing Gradient possible. 
This is because of the skip connection method built and embedded in its architecture.

The skip connection enables information/weights from previous blocks/layers to be added to the current block, meaning that residual weights from previous forward pass are then gathered and used to aid learning of the current block resulting to a more stabilized deep neural networks.


There are various Resnet models since first created, and the number after its name tell use how deep the model is. therefore resnet18 are 18 layers deep.


### Update after 10 Epochs

<img width="512" alt="Screenshot 2023-01-21 at 23 56 52" src="https://user-images.githubusercontent.com/111536571/213894970-ae75e2e1-0ded-4126-8605-e730aea9a94b.png">


<img width="662" alt="Screenshot 2023-01-21 at 23 57 23" src="https://user-images.githubusercontent.com/111536571/213894890-1da2359f-c2fa-444d-8a76-2be7cebfd9f7.png">


Training was stopped after 10 epochs, the graph shows that the model had not reached its global minimum, and with more training or fine tuning a better inference score could be achieved.
