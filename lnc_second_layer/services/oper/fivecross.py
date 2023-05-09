from services.data import pretreatment as dpt
import random
import copy
import numpy as np
from services.oper import training
from sklearn import metrics
from torch.autograd import Variable
import torch
import matplotlib.pyplot as plt

"""
    记录lnc-dis矩阵中每个元素的信息， x为lnc编号， y为dis编号， v为lnc-dis关系
    用于交叉验证,主要用于分片， 验证可用torch.max(a, 1)
"""

class LDLink():
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

"""
    分片
    输入：原始的lnc-dis矩阵和片数k
    输出：k个list， 每个list表示一片， 每一片包含分片后的lnc-dis对象，每个对象包含一个lnc-dis的位置
"""


def splitPositiveData(ld_array, k):
    data_group = []  # 用来保存所有正例的位置
    for i, each_line in enumerate(ld_array):  # 筛选出所有正例， 记录其正例
        for j, each_row in enumerate(each_line):
            if each_row == 1:
                data_group.append(LDLink(i, j))
    random.shuffle(data_group)
    #分割
    s = 0
    res = []
    length = int(len(data_group)/k)
    for i in range(k):
        res.append(data_group[s:s+length])
        s += length
    return res


"""
    1.将所有正例随机分为5份
    2.对每一份positive_data：
        （1）在本轮复制的ld_array中将其中所有lnc-dis置为0，计算lnc-sim，然后拼接为大矩阵U
        （2）CNN
            a.通过大矩阵U获得data和target
            b.对每一行lnc记录i和每一行dis记录j， 若i和j可以在positive_data中找到， 则将其加入测试集，否则则将其加入训练集
        （3）GCN
        （4）训练并验证，通过结果计算roc
    k为折数， s为GCN部分所占比例
"""


def crossVerify(ds_array, ld_array, lm_array, md_array, k, s):
    #计算miRNA的相似性， 可在整个验证过程中重复使用
    mi_sim = dpt.getDisVector(md_array)
    mi_sim = dpt.getArray(mi_sim, ds_array)
    mi_sim = np.array(mi_sim)
    positive_data_group = splitPositiveData(ld_array, k)
    total_roc = 0
    for each_group in positive_data_group:#每一组（每一折）
        temp_ld = copy.deepcopy(ld_array)#每一折临时的lnc_dis关系，用于将本折中测试的lnc_dis置为0，然后拼接成矩阵U
        for each_data in each_group:#每一组中的每一个lnc-dis的位置
            temp_ld[each_data.x][each_data.y] = 0
        U = dpt.getU(ds_array, temp_ld, lm_array, md_array, mi_sim)#获取该折的大矩阵U
        """
            开始进行GCN部分
        """
        u, x = dpt.getux(U)
        u = Variable(torch.from_numpy(np.array(u))).float()
        x = Variable(torch.from_numpy(np.array(x))).float()
        z = training.training_GCN(u, x)

        cnn_train_data, cnn_train_target, gcn_train_data, gcn_train_target, \
        cnn_test_data, gcn_test_data, test_target = dpt.getPairs(U, z, each_group, 240, 405, ld_array)

        gcn_model = training.training_Linear_GCN(gcn_train_data, gcn_train_target, 16, 0.01)
        gcn_outs, gcn_labels = training.testing_Net(gcn_model, gcn_test_data, test_target, 1)

        """
            开始进行CNN部分
        """
        model = training.training_CNN(cnn_train_data, cnn_train_target, 16, 0.001)
        cnn_outs, cnn_labels = training.testing_Net(model, cnn_test_data, test_target, 1)

        final_outs = []
        for i in range(len(gcn_outs)):
            final_score = (1 - s) * cnn_outs[i] + s * gcn_outs[i]
            _, pred = torch.max(final_score, 1)
            final_outs.append(pred)
        if cnn_labels == gcn_labels:
            print("true")
        else:
            print("false")
        roc = getROC(final_outs, gcn_labels)#gcn_labels和cnn_labels相同
        total_roc += roc
        print("final ROC", roc)

    return total_roc/k



"""
    从当前折测试数据的out和label获取ROC面积，该函数需执行K次，K为折数
    输入：1.测试数据的out
         2.测试数据的label
    输出：roc面积
"""


def getROC(outs, labels):
    y = np.array(labels)
    pred = np.array(outs)
    fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=1)
    ROC = metrics.auc(fpr, tpr)
    plt.plot(fpr, tpr,label = 'CNN-AUC:{0}'.format(ROC))
    plt.xlabel(u"fpr")
    plt.ylabel(u"tpr")
    plt.show()
    return ROC