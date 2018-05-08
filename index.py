#!/usr/bin/env python3

import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import sys

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
def generate_file(detail_data, seq_name):
    data = pd.DataFrame([[i[0], i[1], i[2]] for i in detail_data], columns=['k-mers', 'observed', 'possible'])    
    data.to_csv('output/data/'+seq_name+'.csv', index=False)
    #return data

#function to generate a linguistic complexity graph of all sequence name
def generate_complexity_graph(file_name, seq_name_list, linguistic_complexity_list):    
    plt.plot(seq_name_list, linguistic_complexity_list, 'ro')
    plt.xlabel('Sequence Name')
    plt.ylabel('Linguistic Complexity')
    #plt.show()
    graph_name = file_name + '_complexity.png'
    plt.savefig('output/image/'+graph_name)
    #return data

#function to generate comparison of possible and observed kmers of all sequence name
def generate_kmers_graph(file_name, seq_name_list, possible_total_list, observed_total_list):
    fig, ax = plt.subplots()
    index = np.arange(len(seq_name_list))
    bar_width = 0.35
    opacity = 0.8
    rects1 = plt.bar(index, possible_total_list, bar_width,
                     alpha=opacity,
                     color='b',
                     label='Possible Kmers')
    rects2 = plt.bar(index + bar_width, observed_total_list, bar_width,
                     alpha=opacity,
                     color='g',
                     label='Observed Kmers')
    plt.xlabel('Sequence Names')
    plt.ylabel('Kmers')
    plt.title('Kmers per each Sequence Name')
    plt.xticks(index + bar_width, seq_name_list)
    plt.legend()
    plt.tight_layout()
    #plt.show()
    graph_name = file_name + '_kmers.png'
    plt.savefig('output/image/'+graph_name)

#main function
if __name__ == "__main__":
    #get a input variable as a file name
    file_name=sys.argv[1]    
    if file_name in glob.glob('*.fasta'):
        f = open(file_name,'r')
        seq = f.readlines()
        seq_name_list = []
        observed_total_list = []
        possible_total_list = []
        linguistic_complexity_list = []
        for line_num, line in enumerate(seq[0:len(seq)]):
            if len(line) > 1 :
                if '>' in line :
                    line = line.replace(">", "")
                    seq_name = line.rstrip()
                    seq_name_list.append(seq_name)
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
                            #print(counts)
                            #get the observed kmers                            
                            observed = len(counts)
                            k_list.append(k);
                            possible_list.append(possible)                          
                            observed_list.append(observed)
                        #get the total possible kmers                        
                        possible_total = sum(possible_list)  
                        possible_list.append(possible_total)
                        possible_total_list.append(possible_total)
                        #get the total observed kmers
                        observed_total = sum(observed_list)
                        observed_list.append(observed_total)
                        observed_total_list.append(observed_total)
                        k_list.append('Total'); 
                        #merge kmers-data per each sequence name
                        detail_data = list(zip(k_list, observed_list, possible_list))
                        #generate file per each sequence name            
                        detail = generate_file(detail_data, seq_name)
                        #get the linguistic complexity
                        linguistic_complexity = observed_total/possible_total
                        linguistic_complexity_list.append(linguistic_complexity) 
        summary_linguistic_complexity = generate_complexity_graph(file_name, seq_name_list, linguistic_complexity_list)
        summary_kmers = generate_kmers_graph(file_name, seq_name_list, possible_total_list, observed_total_list)
        print('succeed to generate files and graphs for ', seq_name_list) 
    else:
        print('file should be in fasta format')