from torch import nn

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=(3, 11), padding=1),#2 1140 -> 2 1132
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True)
        )

        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=(3, 11), padding=1),#2 1132 -> 2 1124
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)#2 1124 -> 1 562
        )

        self.layer3 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=(1, 11)),#1 562 -> 1 552
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
        )

        self.layer4 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=(1, 11)),# 1 552 -> 1 542
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(1, 2), stride=2)#1 271
        )

        self.fc = nn.Sequential(
            nn.Linear(128 * 1 * 271, 2048),
            nn.ReLU(inplace=True),
            nn.Linear(2048, 512),
            nn.ReLU(inplace=True),
            nn.Linear(512, 64),
            nn.ReLU(inplace=True),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        x = x.view(x.size(0), -1)#将一个多行的tensor拼成一行
        x = self.fc(x)
        return x
