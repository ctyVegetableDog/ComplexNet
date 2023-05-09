from services.data import load as dld
from services.oper import fivecross as fc

#病405， miRNA495, LncRNA240， 正例数2687， 反例数94513， 总数据97200
ds_array, ld_array, lm_array, md_array = dld.dataLoad("./././data/dis_sim_matrix_process.txt", ' ',
                                                   "./././data/lnc_dis_association.txt", ' ',
                                                   "./././data/lnc_mi.txt", '\t',
                                                   "./././data/mi_dis.txt", '\t')

ave_roc = fc.crossVerify(ds_array, ld_array, lm_array, md_array, 5, 0)
print(ave_roc)
