# homework-python
# Authors : Prita

The contents of the repository is that 


output/data: 

I created "data" folder inside the "output" folder where we export all kmers-table (kmers, number of observed kmers, number of possible kmers) per each sequence name in .csv file


output/image:

I created "image" folder inside the "output" folder where we generate all graphs (summary of complexity linguistic and sum of observed kmers per each sequence name) 


index.py:

I created index.py as a script using one input variable which is a filename in fasta format. If the sequence in fasta format is contain other than 'ACTG', it will not generate the table and graph, the script is considered it as wrong format of sequence.
Example : python index.py sample.fasta

test_index.py:
I created test_index.py as a testing script. 
Example : pytest

sample.fasta:

I created sample.fasta to simplify the testing of scripy

Type this to execute the script: python index.py sample.fasta

README.md

I created README.md as a read me file how to execute this file 

readme.png

I created readme.png to show how to execute this file


