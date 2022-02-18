#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python vers. 3.7.0 ###########################################################
# Libraries ####################################################################
from assign_dirs import *
import os
import re
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
from Bio.Seq import Seq



################################################################################
# Base-level Functions #########################################################
################################################################################


################################################################################
# Task-specific Functions ######################################################
################################################################################
def test_bca(record):
    """
    Do a basic regex test to see if the SeqRecord Seq contains,
    both canonical beta-carbonic anhydrase sequences.
    """

    aa_seq = str(record.seq).upper()
    bothmotif = False
    match_1 = re.search(r'C[A-Z]D[A-Z]R', aa_seq)
    match_2 = re.search(r'H[A-Z][A-Z]C', aa_seq)

    if match_1 and match_2:
        bothmotif = True
        
    return bothmotif


def muscle_run(fasta_fn):
    """
    Send a muscle run to the system (command line).
    """
    muscle_loc = "./muscle5.1.linux_intel64"

    aligned_name = fasta_fn + ".muscle_aligned"
    runs_str = " ". join([muscle_loc, "-align", fasta_fn, "-output", aligned_name])
    print(runs_str)
    os.system(runs_str)
    

def filter_BCAs():
    """
    Filter list of BCAs based on presence of BCA canonical motifs.
    """
    beta_CAs = []

    if len(fasta_records)>0:
        for record in fasta_records:
            if test_bca(record):
                prot_id = re.findall(r'(?<=\|).+(?=\|)', record.description)[0]
                record.id = prot_id
                record.description = ""
                beta_CAs.append(record)

            else:
                print(record)
                
    SeqIO.write(beta_CAs, seq_BCAs_ofn, 'fasta')

    
################################################################################
# Initiating Variables #########################################################
################################################################################
gsalaris_fn = os.path.join(data_raw_dn, "Gsalaris_novelBCA.fasta")
seqs_fn = os.path.join(data_dn, "UniProt_BLAST_results.centroids.fasta")
seq_BCAs_ofn = seqs_fn.replace(".fasta",".BCAs.fasta")

################################################################################
# Execution ####################################################################
################################################################################
# load seq records
gsalaris_records = list(SeqIO.parse(gsalaris_fn, 'fasta'))
fasta_records = list(SeqIO.parse(seqs_fn, 'fasta'))
fasta_records = gsalaris_records+fasta_records

# filter to seqs with BCA motifs
filter_BCAs()

# do alignment
muscle_run(seq_BCAs_ofn)

































