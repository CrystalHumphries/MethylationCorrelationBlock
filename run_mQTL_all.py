import os

file_length = 7850
file_start = 0
beta_file_name = "Meth_101_batchCellCorrected.txt"
#beta_file_name = "CorrectedRegressedValues.All.txt"
snp_pos= "MethPos_all_regular.txt"
#snp_pos        = "MethPos_all_regular.reg.txt"

def copy_file_cmdline(old, new):
    import os
    cmd = "cp " + old + " " + new
    os.system(cmd)

def sed_replace_value_inplace(old, new, file):
    import os
    cmd =  "sed -i 's/" + old + "/" + new +'/g\' ' + file
    os.system(cmd)

for run in xrange(1,21):
    output_file_name = "MQTL_CIS_" + str(run)+ ".txt"
    new_beta_file_name = "Meth_101_batchCellCorrected_" + str(run) + ".txt"
    new_beta_pos= "MethPos_all_regular_" + str(run) + ".txt"
    
    #divide file
    file_end = run*file_length
    print ("start: " + str(file_start))
    print ("stop: " + str(file_end))

    import itertools
    dir = "tempMQTL1/"
    beta_file = dir + new_beta_file_name
    pos_file  = dir + new_beta_pos

    with open(beta_file_name, 'r') as old_b, open(beta_file, 'w') as new_b:
        for line in itertools.islice(old_b, file_start, file_end):
            print ('*'),
            new_b.write(line)
    
    #get snp info
    with open(snp_pos, "r") as old_pos_file:
        with open(pos_file, "a") as fh:
            for line in itertools.islice(old_pos_file, file_start, file_end):
                fh.write(line)
    
    #create new R script file
    old_Rscript="matrixMQTL.1mb.cc.R"
    new_Rscript = dir + "matrixMQTL.1mb." + str(run) + ".R"
    copy_file_cmdline (old_Rscript, new_Rscript)

    sed_replace_value_inplace(beta_file_name, new_beta_file_name, new_Rscript)
    sed_replace_value_inplace(snp_pos, new_beta_pos, new_Rscript)
    sed_replace_value_inplace("NUMNUM", str(run), new_Rscript)

    #run the qsub file
    orig_pbs = "run.cc.pbs"
    pbs_file = dir + "run." + str(run) + ".pbs"

    copy_file_cmdline(orig_pbs, pbs_file)
    sed_replace_value_inplace("cc", str(run), pbs_file)
    final_cmd = "qsub " + pbs_file
    os.system(final_cmd)
    print (final_cmd)
    file_start = file_end + 1
    
