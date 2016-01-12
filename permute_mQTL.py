#!/isb/chumphri/anaconda/bin/python

import os
import sys
import random
import time

def add_dir(file):
    file_loc   = "/path/to/file/"
    new_file   = file_loc + file
    return(new_file)

start_time = time.time()
geno       = add_dir("DF5_Merged_Mothers_noRepeats_AlleleCount.txt")
meth       = add_dir('19K_meth_cellCorrected_101.txt1')


def permute_geno_meth_tables():
    start = ' awk \'BEGIN{OFS="\\t";} {print '
    end = '}\''
    a = random.sample(xrange(2,785),783)
    new_list = []

    for line in a:
        entry = "$" + str(line)
        new_list.append(entry)

    new_list[0]  = "$1"
    samples =  ", ".join(new_list)
    cmd = start +  samples +  end
    return(cmd)

def permute_Pos_file(file, file_2_3_col, final_temp_file, flag, p):
    with open(file) as f:
        content = f.readlines()
    
    if flag == "TRUE":
        start = content.pop(0)
        random.shuffle(content)
        content.insert(0, start)
    else:
        random.shuffle(content)
    
    write_file = add_dir("workfile." + str(p) + ".txt")
    meth_col = open(write_file, 'w')

    print len(content)
    
    for Snp in content:
        meth_col.write(Snp)

    meth_col.close()
    cmd = "paste " + write_file + " " + file_2_3_col + " > " + final_temp_file 
    os.system(cmd)
    print cmd

def SED_sub(orig, new):
    new = new.replace("/", "\/")
    temp = 's/' + orig + '/' + new + '/g;'
    return(temp)
        
def run_permutation(num, p):
    for permute in num:
        print "Currenly doing: " + str(permute)
        geno_perm  = add_dir ("temp.vcf." + str(p) + ".txt")
        cmd_g = permute_geno_meth_tables() + " " + geno  + " > " + geno_perm
        os.system(cmd_g)
        #print cmd_g
        meth_perm  = add_dir("temp.meth." + str(p) + ".txt")
        cmd_m = permute_geno_meth_tables() + " " +  meth + " > " + meth_perm
        os.system(cmd_m)                                                                                                                                                                                             
        #print cmd_m
        #permute genotypes
        snpFile  = geno_perm
        snpPos   = add_dir("temp_SnpPos_file." +str(p) + ".txt")
        methFile = meth_perm
        methPos  = add_dir("temp_MethPos_file." + str(p) + ".txt")
        permute_Pos_file(add_dir("newSnpPosFile.txt_first_col"), add_dir("newSnpPosFile.txt_2-3_col") ,  snpPos, "FALSE", p)
        permute_Pos_file(add_dir("newMethPosFile.txt_first_col"), add_dir("newMethPosFile.txt_2-3_col"), methPos, "TRUE", p)
        output_file = "mQTL_permute_file_" + str(permute) + "_" + p + ".txt"
        output_transcis = "mQTL_permute_transcis_" + str(permute) + "_" + p + ".txt"
        old_file = add_dir("matrixMQTL.1mb.permute.R")
        new_file = add_dir("matrixMQTL.1mb.temp." + p + ".new.R")
        replace_file = SED_sub("x_SNPFILE_x", snpFile) + SED_sub("x_SNPPOSFILE_x", snpPos) + SED_sub("x_METHFILE_x", methFile) + SED_sub("x_METHPOSFILE_x", methPos) + SED_sub("REPLACE_NEWFILE", output_transcis) + SED_sub("REPLACE_FILE" , output_file)
        cmd = "sed -e '" + replace_file + "' " + old_file + "  > " + new_file

        os.system(cmd)
        print cmd
        


if __name__ == "__main__":
    run_permutation(sys.argv[1],sys.argv[2])
#    permute_Pos_file(add_dir("newMethPosFile.txt_first_col"), add_dir("newMethPosFile.txt_2-3_col"), add_dir("temp_MethPos_file.TRY.txt"), "TRUE", 3)
    
