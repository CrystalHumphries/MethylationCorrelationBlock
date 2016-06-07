from sklearn.decomposition import PCA
from sklearn import decomposition
import numpy as np
import pandas as pd
import statsmodels.api as sm
import sys
from sklearn.preprocessing import Imputer
from multiprocessing import Process
import os

methPos = pd.read_csv("/isb/chumphri/MethylationPOP/temp_MethPos_file.txt", sep="\t")

def get_90_var(array):
    total = 0
    pos = 0
    for x in array:
         total += x
         pos   += 1
         if total>=0.95:
             return(pos)

def get_genotypes(CpG_location):
    import tabix
    import pandas as pd
    tb_file   = "/path/to/file/DF_meth_variants.gz"
    df        = pd.DataFrame(columns=xrange(0,782))
    tb        = tabix.open(tb_file)
#    print CpG_location
    records   = tb.querys(CpG_location)
    num       = 0
    for record in records:
        df.loc[num] = record[3:]
        num        += 1
    return(df)
        
def get_location(CpG):
    e = methPos.loc[ methPos['geneID']==CpG]
    e1 = map(list, e.values)
    if e1:
        e1 = e1[0]
        start = e1[2]-1000000
        if start < 0:
            start = 0
        start = str(start)
        stop  = str(e1[3]+1000000)
        tabix_loc = e1[1] +":" + start + "-" + stop
        flag = 'T'
        print CpG
        print tabix_loc
    else:
        flag='F'
        tabix_loc='x'
    return(flag, tabix_loc)

def run_pca(genotype_matrix):
    pca              = decomposition.PCA()
    pca.fit(genotype_matrix)
    top95percent_PC  = get_90_var(pca.explained_variance_ratio_)
    pca.n_components = top95percent_PC
    X_reduced        = pca.fit_transform(genotype_matrix)
    PCA_matrix       = pd.DataFrame(X_reduced)
    return(PCA_matrix)

def run_main(new_file, start, stop, dat):
    with open(new_file, 'a') as file:
        imp = Imputer(missing_values='NaN', strategy='most_frequent', axis=1)
        
        
        
        import itertools
        with open(dat, "r") as text_file:
            for line in itertools.islice(text_file, start, stop):
                line            = line.replace("NA", "NaN")
                content         = line.rstrip('\n').split('\t')
                CpG             = content.pop(0)
                
                CpG_location = get_location(CpG)
                genotype_matrix = get_genotypes(CpG_location)
                genotype_matrix = genotype_matrix.transpose()

                 #run PCA
                try:
                    PCA_matrix = run_pca(genotype_matrix)
                except ValueError:
                    continue

                #run linear regression
                meth_values = pd.Series(methylation_levels, name="meth_val", dtype=float)
                model = sm.OLS(meth_values, PCA_matrix)
                results = model.fit()
                
                
                
                
                MethValResids = results.resid
                final         = pd.Series(CpG)
                final         = final.append(MethValResids)
                fline         = final.tolist()
                fline         = '\t'.join(str(x) for x in fline)
                fline         = fline + "\n"
                file.write(fline)

if __name__ == '__main__':
    start     = sys.argv[1]
    stop      = sys.argv[2]
    file      = "/path/to/file/ten/iteration_" + str(start) + "_" + str(stop) + ".txt"
    dat       = "/path/to/file/ten/19K_meth_cellCorrected_101.txt" + str(stop)
    cmd       = "cp " +  "/path/to/file/19K_meth_cellCorrected_101.txt1 " +  dat
    os.system(cmd)
    run_main(file, int(start), int(stop), dat)

