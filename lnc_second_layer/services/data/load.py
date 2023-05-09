import numpy as np


def dataLoad(dis_sim, d1, lnc_dis, d2, lnc_mi, d3, mi_dis, d4):#先不加异常好不好 好呀
    dsArray = np.loadtxt(dis_sim, delimiter=d1)
    ldArray = np.loadtxt(lnc_dis, delimiter=d2)
    lmArray = np.loadtxt(lnc_mi, delimiter=d3)
    mdArray = np.loadtxt(mi_dis, delimiter=d4)

    return dsArray, ldArray, lmArray, mdArray