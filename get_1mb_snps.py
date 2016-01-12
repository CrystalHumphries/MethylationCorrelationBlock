def get_1mb_snps():
    import tabix 
    tb = tabix.open('snps_all.gz')

    fname = 'newMethPosFile.txt_2-3_col_1'
    snps = {}

    with open(fname) as f:
        for line in f:
            a = line.rstrip('\n').rsplit('\t')
            start = str(int(a[1]) - 1000000)
            stop  = str(int(a[1]) + 1000000)
            pos = a[0] + ":" + start + "-" + stop
            records = tb.querys(pos)
            for record in records:
                snps[record[3]] = 0
    return(snps)

def print_matching_items(keys, file):
    match_these = [line.rstrip() for line in open(keys)]
    
    with open(file) as f:
        for line in f:
            contents = line.rsplit('\t')
            if contents[0] in match_these:
                print line
            
    

if __name__ == "__main__":
   # snps = get_1mb_snps()
   # for key, value in snps.items() :
   #     print key
    
    print_matching_items('snps_to_keep', 'DF5_Merged_Mothers_noRepeats_AlleleCount.txt')
