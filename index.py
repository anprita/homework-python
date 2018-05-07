#!/usr/bin/env python3

import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import pathlib

#function to count the kmers
def count_kmers(seq, k):
    counts = {}
    for i in range(len(seq) - k + 1):
        kmer = seq[i:i+k]
        if kmer not in counts:
            counts[kmer] = 0
        counts[kmer] += 1
    return counts

#function to find the wrong DNA
def check_seq_format(seq):
    bad_chars = {}
    for l in seq:
        if l not in 'AGCT':
            if l in bad_chars: bad_chars[ l ] += 1
            else: bad_chars[ l ] = 1
    if bad_chars != {}: return bad_chars

#function to export a table(kmers, observed, possible) in .csv format per each sequence name
def generate_file(data, seq_name):
    data = pd.DataFrame([[i[0], i[1], i[2]] for i in data], columns=['k-mers', 'observed', 'possible'])    
    data.to_csv('output/data/'+seq_name+'.csv', index=False)
    #return data

#function to generate a graph
#def generate_graph
#not yet 

#main function
if __name__ == "__main__":
    #get a input variable as a file name
    filename=sys.argv[1]
    if filename in glob.glob('*.fasta'):
        f = open(filename,'r')
        seq = f.readlines()
        for line_num, line in enumerate(seq[0:len(seq)]):
            if len(line) > 1 :
                if '>' in line :
                    line = line.replace(">", "")
                    seq_name = line.rstrip()
                else:
                    seq = line.rstrip()
                    #check per each sequence name, the sequence format
                    seq_format = check_seq_format(seq)                    
                    if seq_format != None:
                        print('fail to generate kmers-table for ', seq_name, ' due to invalid sequence format, detail:', seq_format) 
                    else:
                        k_list = []
                        possible_list = []
                        observed_list = []
                        for k in range(1,len(seq)+1):
                            if k==1:
                                #exception only for k=1, possible kmers always 4 (A,C,T,G)
                                possible = 4
                            else:
                                #get the possible kmers
                                possible = len(seq) - k + 1
                            #get the kmers
                            counts = count_kmers(seq, k)
                            #get the observed kmers                            
                            observed = len(counts)
                            k_list.append(k);
                            possible_list.append(possible)                          
                            observed_list.append(observed)
                        #get the total possible kmers                        
                        possible_total = sum(possible_list)  
                        possible_list.append(possible_total)
                        #get the total observed kmers
                        observed_total = sum(observed_list)
                        observed_list.append(observed_total)
                        k_list.append('Total'); 
                        merge_list = zip(k_list, observed_list, possible_list)                     
                        data = list(merge_list)
                        #generate file per each sequence name            
                        table = generate_file(data, seq_name)
                        #get the linguistic complexity
                        linguistic_complexity = observed_total/possible_total    
                        print('linguistic_complexity for ',seq_name,' = ',linguistic_complexity)      
                        #generate graph -> not yet  
    else:
        print('file should be in fasta format')