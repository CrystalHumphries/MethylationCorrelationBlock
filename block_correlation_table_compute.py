import time
start = time.time()

def Correlation_CpGs(CpGMeth, flag, no_samples):
    import numpy as np
    from scipy import stats
    
    no_samples = CpGMeth.shape[1]-1
    if (flag == "True"):
        methPerm = CpGMeth[CpGMeth.columns[np.random.random_integers(0, no_samples, no_samples)]]
    else:
        assert isinstance(CpGMeth, object)
        methPerm = CpGMeth

    meth_t       = methPerm.transpose()
    corr         = meth_t.corr(method='spearman')
    j            = corr.values[np.triu_indices_from(corr.values, 1)]
    corr_above04 = len([i for i in j if i >= 0.4])
    result       = 0

    if corr_above04 >= (len(j) * 0.5):
        result = j.mean()

    return result


if __name__ == "__main__":
    import pandas as pd
    import itertools
    import sys

    Blocks     = sys.argv[1]
    methfile   = sys.argv[2]
    blockID    = pd.read_table(Blocks, sep="\t")
    methTable  = pd.read_table(methfile, sep="\t")

    B          = blockID.BlockID.unique()
    no_samples = methTable.shape[1]-1
    new_file   = "/isb/chumphri/Meth_" + str(len(B)) + "_Block_Correlation_" + str(no_samples)+ "_samples.tsv"

    with open(new_file, "w") as f:

        for block in B:
            BlockCpGSites = blockID[blockID['BlockID'] == block].CpGSites
            CpGMeth       = methTable.loc[methTable.index.isin(BlockCpGSites)]
            corr_results  = []

            #determine the original correlation
            result = Correlation_CpGs(CpGMeth=CpGMeth, flag="False", no_samples = no_samples)
            corr_results.append(result)

            #do 1000 permutations of the block correlation
            for i in xrange(1000):
                result = Correlation_CpGs(CpGMeth=CpGMeth, flag="True", no_samples = no_samples)
                corr_results.append(result)

            corr_results.insert(0, block)
            f.write('\t'.join(map(str, corr_results)))
            f.write("\n")

print "Process time: " + str(time.time() - start)
