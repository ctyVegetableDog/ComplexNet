import numpy as np
import torch
from torch.autograd import Variable
from torch.utils.data import DataLoader, TensorDataset
from services.net import CNN
from torch import nn, optim
from services.net import GCN


"""
    训练网络
    input:大矩阵U， 原始的lnc_dis, 用于生成符合CNN格式数据的lnc数和dis数， 网络必须的参数
    return:
"""


def training_CNN(train_data, train_target, batch_size, learning_rate):
    #训练
    train_data = torch.from_numpy(np.array(train_data)).float()
    train_target = torch.from_numpy(np.array(train_target)).long()
    deal_dataset = TensorDataset(train_data, train_target)
    train_loader = DataLoader(dataset=deal_dataset, shuffle=True, batch_size=batch_size)

    model = CNN.CNN()
    if torch.cuda.is_available():
        model = model.cuda()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for epoch, (train_data, train_target) in enumerate(train_loader):
        if torch.cuda.is_available():
            inputs = Variable(train_data).cuda()
            outputs = Variable(train_target).cuda()
        else:
            inputs = Variable(train_data)
            outputs = Variable(train_target)

        out = model(inputs)
        loss = criterion(out, outputs)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 20 == 0:
            print('Epoch[{}], loss: {:6f}'.format(epoch + 1, loss.data))
    return model


"""
    测试网络， 输出为out和label
"""


def testing_Net(model, test_data, test_target, batch_size):
    test_data = torch.from_numpy(np.array(test_data)).float()
    test_target = torch.from_numpy(np.array(test_target)).long()
    test_dataset = TensorDataset(test_data, test_target)
    test_loader = DataLoader(dataset=test_dataset, shuffle=False, batch_size=batch_size)
    model.eval()
    outs = []
    labels = []
    for test_data in test_loader:
        data, label = test_data
        out = model(data)
        # _, pred = torch.max(out, 1)
        outs.append(out)
        labels.append(label)
    return outs, labels


"""
    训练GCN，每一折返回一个Z
    输入
        (1)u, x
        (2)学习率
        (3)权重矩阵的大小
"""


def training_GCN(u, x):
    model = GCN.GCNNet()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.3)
    loss_func = nn.MSELoss()

    for epoch in range(1600):
        decoded, encoded = model(u, x)
        loss = loss_func(decoded, x)  # 计算损失函数
        optimizer.zero_grad()  # 梯度清零
        loss.backward()  # 反向传播
        optimizer.step()  # 梯度优化
        print(epoch)
        print(loss.data)
    return encoded

"""
    每一折得到Z以后， 训练一个全连接来验证
    test_data为本折做为测试集的lnc-dis位置， 除test_data里元素以外全做为训练集
    ld_array中取label
"""


def training_Linear_GCN(train_data, train_target, batch_size, learning_rate):
    train_data = torch.from_numpy(np.array(train_data)).float()
    train_target = torch.from_numpy(np.array(train_target)).long()
    deal_dataset = TensorDataset(train_data, train_target)
    train_loader = DataLoader(dataset=deal_dataset, shuffle=True, batch_size=batch_size)

    model = GCN.finalNet(200, 64, 2)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    for epoch, (train_data, train_target) in enumerate(train_loader):
        if torch.cuda.is_available():
            inputs = Variable(train_data).cuda()
            outputs = Variable(train_target).cuda()
        else:
            inputs = Variable(train_data)
            outputs = Variable(train_target)

        out = model(inputs)
        loss = criterion(out, outputs)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (epoch + 1) % 20 == 0:
            print('Epoch[{}], loss: {:6f}'.format(epoch + 1, loss.data))
    return model
