import random
from numpy import *
import numpy as np

"""
    以下4个方法目的为从4个矩阵获得大矩阵U
    1.getDisVector():通过删除lnc(mi)_dis数组中的0，获得每个Lnc(mi)RNA有关联的每个疾病
    2.getArray():通过lnc(mi)-dis和dis-dis数组计算lnc-lnc矩阵（应是对称阵）
    3.getFinalMatrix():将所有数据拼接成完整的矩阵U
    4.getU()为将以上上个方法打包
"""


def getDisVector(ld_array):
    res = []
    for eachLnc in ld_array:
        eachLncRes = []
        for disID, eachDis in enumerate(eachLnc):
            if eachDis != 0:
                eachLncRes.append(disID)
        res.append(eachLncRes)
    return res


def getArray(ld_array, dd_array):
    res = []
    for eachLnc in ld_array:#每个LncRNA l1
        eachres = []
        for anotherLnc in ld_array:#与每个LncRNA对比的LncRNA l2
            if len(eachLnc) == 0 or len(anotherLnc) == 0:#若l1或l2和所有疾病都没有关系
                eachres.append(0)
            else:#l1-l2-sim为与l1和l2关联的所有疾病与其他疾病的相似度最大值的和/与l1和l2关联的疾病的个数
                simMaxSum = 0#相似度最大值的和
                cnt = 0#与l1和l2关联的疾病总数
                for eachDis in eachLnc:#每个与Lnc（l1）关联的Dis的编号
                    simMax = 0#当前疾病相似度最大值
                    cnt += 1
                    for anotherDis in anotherLnc:#每个与l2关联的Dis编号
                        if dd_array[eachDis][anotherDis] > simMax:
                            simMax = dd_array[eachDis][anotherDis]
                    simMaxSum += simMax
                for eachDis in anotherLnc:#每个与Lnc（l1）关联的Dis的编号
                    simMax = 0#当前疾病相似度最大值
                    cnt += 1
                    for anotherDis in eachLnc:#每个与l2关联的Dis编号
                        if dd_array[eachDis][anotherDis] > simMax:
                            simMax = dd_array[eachDis][anotherDis]
                    simMaxSum += simMax
                sim = simMaxSum/cnt
                eachres.append(sim)
        res.append(eachres)
    return res


def getFinalMatrix(lnc_sim, lnc_dis, lnc_mi, dis_sim, mi_dis, mi_sim):
    first_row = np.hstack((lnc_sim, lnc_dis, lnc_mi))
    second_row = np.hstack((np.transpose(lnc_dis), dis_sim, np.transpose(mi_dis)))
    third_row = np.hstack((np.transpose(lnc_mi), mi_dis, mi_sim))
    U = np.vstack((first_row, second_row, third_row))
    return U


"""
    mi_sim可重复使用，故单独拿出来计算

"""


def getU(ds_array, ld_array, lm_array, md_array, mi_sim):
    lnc_sim = getDisVector(ld_array)
    lnc_sim = getArray(lnc_sim, ds_array)
    lnc_sim = np.array(lnc_sim)

    U = getFinalMatrix(lnc_sim, ld_array, lm_array, ds_array, md_array, mi_sim)
    return U


"""
    输入：
        1.处理过的大矩阵U
        2.当前折的测试集（当前折中被当作测试数据的正例）
        3.lnc的总个数， 用于在U中定位表示dis的行
        4.dis的总个数， 用于给U shuffle然后获取反例
        5.原始的lnc-dis，用于获取反例
    输出：
        train_data_group:
        训练数据集， 由k个大小为（k-1）* lnc_size * dis_size/k的list构成 
        train_target_group：
        训练数据集， 由k个大小为（k-1）* lnc_size * dis_size/k的list构成，每个list由0-1构成， 位置与train_data_group对应 
        test_data_group：
        测试数据机， 由k个大小为lnc_size * dis_size/k的list构成
        test_target_group
"""


def getCNNPairs(U, each_k, lnc_size, dis_size, ld_array):
    test_data = []
    test_target = []
    train_data = []
    train_target = []
    all_negative_data = []
    lnc_array = U[:lnc_size]
    dis_array = U[lnc_size:lnc_size + dis_size]
    for i in range(lnc_size):
        for j in range(dis_size):
            #对每个lnc个dis获得一个data
            channel_layer = []
            # 增加一个维度 使之符合conv2d需要的4维即（batch_size, w, h, channel），此处channel为1
            channel_layer.append(np.vstack((lnc_array[i], dis_array[j])))
            if ld_array[i][j] == 0:#若当前是反例
                all_negative_data.append(channel_layer)
            else:#若是正例，则判断是否是测试集，若不是则加入训练集
                ok = False#是否是测试集
                for each in each_k:
                    if each.x == i and each.y == j:#若是测试集
                        ok = True
                        test_data.append(channel_layer)
                        test_target.append(1)
                        break
                if not ok:#若不是测试集
                    train_data.append(channel_layer)
                    train_target.append(1)
    random.shuffle(all_negative_data)#将所有反例洗牌，然后为每个正例配对一个反例
    test_len = len(test_data)
    train_len = len(train_data)
    for i in range(test_len):
        test_data.append(all_negative_data[i])
        test_target.append(0)
    for i in range(test_len, test_len + train_len):
        train_data.append(all_negative_data[i])
        train_target.append(0)
    test = list(zip(test_data, test_target))
    random.shuffle(test)
    test_data[:], test_target[:] = zip(*test)
    train = list(zip(train_data, train_target))
    random.shuffle(train)
    train_data[:], train_target[:] = zip(*train)
    return train_data, train_target, test_data, test_target


"""
    获取GCN最后全连接需要的pair
"""

def getGCNPair(z, each_k, lnc_size, dis_size, ld_array):
    z = z.data.numpy().tolist()
    test_data = []
    test_target = []
    train_data = []
    train_target = []
    all_negative_data = []
    lnc_array = z[:lnc_size]
    dis_array = z[lnc_size:lnc_size + dis_size]

    for i, each_lnc in enumerate(lnc_array):
        for j, each_dis in enumerate(dis_array):
            if ld_array[i][j] == 0:#若是反例
                all_negative_data.append(each_lnc + each_dis)
            else:
                ok = False  # 是否是测试集中元素
                for each in each_k:
                    if i == each.x and j == each.y:  # 是测试集d
                        test_data.append(each_lnc + each_dis)
                        test_target.append(1)
                        break
                if not ok:  # 不是测试集
                    train_data.append(each_lnc + each_dis)  # 将lnc行与dis行拼接得到一个data
                    train_target.append(1)  # 对应的lnc-dis关系为target

    random.shuffle(all_negative_data)  # 将所有反例洗牌，然后为每个正例配对一个反例
    test_len = len(test_data)
    train_len = len(train_data)
    for i in range(test_len):
        test_data.append(all_negative_data[i])
        test_target.append(0)
    for i in range(test_len, test_len + train_len):
        train_data.append(all_negative_data[i])
        train_target.append(0)
    test = list(zip(test_data, test_target))
    random.shuffle(test)
    test_data[:], test_target[:] = zip(*test)
    train = list(zip(train_data, train_target))
    random.shuffle(train)
    train_data[:], train_target[:] = zip(*train)
    return train_data, train_target, test_data, test_target



"""
    获取GCN和CNN所需的训练和测试数据
"""
def getPairs(U, z, each_k, lnc_size, dis_size, ld_array):
    test_target = []#cnn和gcn共用一个test_target并且test_label的元素顺序相同

    cnn_test_data = []
    cnn_train_data = []
    cnn_train_target = []

    z = z.data.numpy().tolist()
    gcn_test_data = []
    gcn_train_data = []
    gcn_train_target = []
    cnn_all_negative_data = []
    gcn_all_negative_data = []

    cnn_lnc_array = U[:lnc_size]
    cnn_dis_array = U[lnc_size:lnc_size + dis_size]

    gcn_lnc_array = z[:lnc_size]
    gcn_dis_array = z[lnc_size:lnc_size + dis_size]

    for i in range(lnc_size):
        for j in range(dis_size):
            #对每个lnc个dis获得一个data
            cnn_channel_layer = []
            # 增加一个维度 使之符合conv2d需要的4维即（batch_size, w, h, channel），此处channel为1
            cnn_channel_layer.append(np.vstack((cnn_lnc_array[i], cnn_dis_array[j])))
            if ld_array[i][j] == 0:#若当前是反例
                cnn_all_negative_data.append(cnn_channel_layer)
                gcn_all_negative_data.append(gcn_lnc_array[i] + gcn_dis_array[j])
            else:#若是正例，则判断是否是测试集，若不是则加入训练集
                ok = False#是否是测试集
                for each in each_k:
                    if each.x == i and each.y == j:#若是测试集
                        ok = True
                        cnn_test_data.append(cnn_channel_layer)
                        gcn_test_data.append(gcn_lnc_array[i] + gcn_dis_array[j])
                        test_target.append(1)
                        break
                if not ok:#若不是测试集
                    cnn_train_data.append(cnn_channel_layer)
                    cnn_train_target.append(1)
                    gcn_train_data.append(gcn_lnc_array[i] + gcn_dis_array[j])
                    gcn_train_target.append(1)

    """
        保证CNN和GCN的测试集数据顺序一致
        训练集可以不一致    
    """
    all_negative_data = list(zip(cnn_all_negative_data, gcn_all_negative_data))
    random.shuffle(all_negative_data)  # 将所有gcn,cnn反例按相同顺序洗牌，然后为每个正例配对一个反例
    cnn_all_negative_data[:], gcn_all_negative_data[:] = zip(*all_negative_data)
    cnn_test_len = len(cnn_test_data)#长度与gcn_test相同
    cnn_train_len = len(cnn_train_data)#长度与gcn_train相同
    for i in range(cnn_test_len):
        cnn_test_data.append(cnn_all_negative_data[i])
        gcn_test_data.append(gcn_all_negative_data[i])
        test_target.append(0)
    for i in range(cnn_test_len, cnn_test_len + cnn_train_len):
        cnn_train_data.append(cnn_all_negative_data[i])
        cnn_train_target.append(0)
        gcn_train_data.append(gcn_all_negative_data[i])
        gcn_train_target.append(0)

    test = list(zip(cnn_test_data, gcn_test_data, test_target))
    random.shuffle(test)
    cnn_test_data[:], gcn_test_data[:], test_target[:] = zip(*test)

    cnn_train = list(zip(cnn_train_data, cnn_train_target))
    random.shuffle(cnn_train)
    cnn_train_data[:], cnn_train_target[:] = zip(*cnn_train)

    gcn_train = list(zip(gcn_train_data, gcn_train_target))
    random.shuffle(gcn_train)
    gcn_train_data[:], gcn_train_target[:] = zip(*gcn_train)
    return cnn_train_data, cnn_train_target, gcn_train_data,\
           gcn_train_target, cnn_test_data, gcn_test_data, test_target

"""
    输入A计算A的度矩阵E
"""

def getE(A):
    m = A.sum(axis=1).tolist()
    """
        使用字符串
        将得到的A按行求和的结果列表降维
    """
    st = str(m)
    st = st.replace('[', '')
    st = st.replace(']', '')
    m = list(eval(st))
    E = mat(diag(m))
    return E

"""
    为矩阵A加上单位矩阵
"""
def plusIM(A):
    n, m = A.shape
    I = mat(eye(n, m, dtype=int))
    return A + I


"""
    对A进行对称拉普拉斯
    因为其中E为对角矩阵，计算E的负二分之一次方与二分之一次方等价于对矩阵中所有元素做相应对次方运算
    若为一般矩阵情况， 可使用代码计算负二分之一次方
    v, Q = la.eig(E)
    V = np.diag(v**(-0.5))
    L = Q * V * Q**-1
    E为输入， L为输出
"""


def symmetry_lp(A):
    M = plusIM(A)
    E = getE(A)
    x, y = E.shape
    L = mat(zeros((x, y)))
    for i in range(x):
        if E[i, i] == 0:
            L[i, i] = 0
        else:
            L[i, i] = E[i, i] ** (-0.5)
    return L * M * L



"""
    GCN
    处理U获得参与计算的U飘（u）和特折矩阵X(x)
"""


def getux(U):
    return symmetry_lp(U), plusIM(U)