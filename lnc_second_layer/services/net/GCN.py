from numpy import *
import torch.nn.functional as F
import torch.nn as nn
from torch.nn.parameter import Parameter
import torch


"""
    得到Z以后
        (1)将每个lnc和dis拼接成一行
        (2)经过全连接得到关联的得分和非关联得分，进行验证
"""
class GCNNet(nn.Module):
    def __init__(self):
        super(GCNNet, self).__init__()
        self.H_1 = Parameter(torch.from_numpy(random.random((1140, 100))).float())#attention前的权重
        self.W0 = Parameter(torch.from_numpy(random.random((1140, 100))).float())#降维
        self.W1 = Parameter(torch.from_numpy(random.random((100, 1140))).float())#升维
        self.att_layer = nn.Sequential(
            nn.Linear(1140, 100, bias=True),
            nn.Tanh()
        )
        self.encoder = nn.Sequential(
            nn.Softmax()
        )
        self.decoder = nn.Sequential(
            nn.Sigmoid()
        )

    def forward(self, U, X):
        print(type(U))
        A2 = U / 1
        for i in range(U.shape[0]):
            K = self.att_layer(A2[i])
            K = torch.unsqueeze(K, dim=1).type(torch.FloatTensor)
            K = self.H_1.mm(K)
            score = F.softmax(K, dim=0)
            score = reshape(score.detach().numpy(), (score.shape[0],))
            score = torch.from_numpy(score)
            A2[i] = U[i] * score

        Z = self.encoder(A2.mm(X).mm(self.W0))
        X_p = self.decoder(U.mm(Z).mm(self.W1))
        return X_p, Z

class finalNet(nn.Module):
    def __init__(self, in_dim, n_hidden_1, out_dim):
        super(finalNet, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Linear(in_dim, n_hidden_1),
            nn.BatchNorm1d(n_hidden_1),
            nn.ReLU(inplace=True)
        )
        self.layer2 = nn.Sequential(
            nn.Linear(n_hidden_1, out_dim)
        )

    def forward(self, x):
        x = self.layer1(x)
        x = self.layer2(x)
        return x

