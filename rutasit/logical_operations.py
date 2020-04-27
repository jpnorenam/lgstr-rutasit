import numpy as np

#def mult_operator(idx_orig, idx_dest, C):
#    N = C.shape[0]
#    if (idx_orig > N and idx_dest > N):
#        raise AttributeError("zone code out of bounds")
#    else:
#        arrO = C[idx_orig,:]
#        arrD = C[:,idx_dest]
#        arrC = np.clip(np.multiply(arrO, arrD), 0, 1)
#        arrR = [arrO[n] | arrD[n] for n in range(N)] * arrC
#        intR = 0
#        for n in range(N):
#            intR |= arrR[n]
#        return intR

def mult_operator(ArrO_N, ArrD_N, ArrO_L, ArrD_L):
    arrNC = np.clip(np.multiply(ArrO_N, ArrD_N), 0, 1)
    arrLG = np.array([ArrO_L[n] | ArrD_L[n] for n in range(len(ArrO_N))])
    arrR = arrLG * arrNC
    res = 0
    for n in range(len(ArrO_N)):
        res |= arrR[n]
    return res

def add_transfer_connections(direct_matrix, max_transfers):
    N = direct_matrix.shape[0]
    if (N != direct_matrix.shape[1]):
        raise AttributeError("Argument C must be a square matrix")
    else:
        logical_mm = direct_matrix
        logical_pp = np.zeros([N,N], dtype=int)
        numeric_mm = direct_matrix
        for transfer in range(max_transfers):
            numeric_pp = numeric_mm @ direct_matrix
            for i in range(N):
                for j in range(N):
                    if logical_mm[i, j] != 0:
                        logical_pp[i, j] = logical_mm[i, j]
                    elif numeric_pp[i,j] != 0 and numeric_mm[i,j] == 0:
                        logical_pp[i, j] = mult_operator(numeric_mm[i,:], numeric_mm[:,j], logical_mm[i,:], logical_mm[:,j])
            logical_mm = logical_pp
            numeric_mm = numeric_pp
        return logical_pp