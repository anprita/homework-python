#!/usr/bin/env python3

from index import count_kmers
#check_seq_format
import pytest

#avoid repetition by loading data in advance 
@pytest.fixture 

def fastq():
	#f = open('sample.fastq','r')
	#fastq = f.readlines()
	fastq = 'AGGATGAATGG'
	return fastq

#test k = 2 produces 6 kmers 
def test_count_kmers(fastq):
	counts = count_kmers(fastq, 2)
	assert len(counts) == 6 

