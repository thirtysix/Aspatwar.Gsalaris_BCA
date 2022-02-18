

## Aspatwar et al. Gyrodactylus salaris BCA phylogenetic analysis

# 1. Background
This repository provides Python scripts used to perform analyses and generate images for the pre-print article found at [biorxiv](https://www.biorxiv.org/).

---
---
# 2. Instructions
We will give instructions to set up a miniconda environment to contain the dependencies needed and to run the manuscript's analysis scripts.

## 2.1 Install miniconda
Miniconda is the barebones version of the larger Conda package. We will use this so that we choose only the dependencies that are needed and therefore reduce the installation size and time. The Miniconda installation instructions are here: [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

## 2.2 Create environment and activate
```
    $ conda create -n gsalaris_phylo python=3.7
    $ conda activate gsalaris_phylo
```

## 2.3 Install analyses dependencies
```
    $ conda install -c etetoolkit ete3==3.1.2 ete_toolchain
    $ conda install -c anaconda seaborn
    $ conda install -c conda-forge biopython
    $ conda install -c bioconda iqtree
```

## 2.4 Download Muscle 5.1, USEARCH 11, and Gblocks 0.91b
```
    $ cd 00.src
    $ python3 000.get_data.py
```

## 2.5 Extract Gblocks
```
    $ uncompress ./Gblocks_Linux64_0.91b.tar.Z
    $ tar -xvf ./Gblocks_Linux64_0.91b.tar
```

## 2.6 Enable executing as a program: Muscle 5.1 and USEARCH
```
    $ chmod +x muscle5.1.linux_intel64
    $ chmod +x usearch11.0.667_i86linux32
```

## 2.7 Cluster BLAST results
```
    $ ./usearch11.0.667_i86linux32 -cluster_fast ../01.data_raw/UniProt_BLAST_results.fasta -id 0.80 -centroids ../02.data/UniProt_BLAST_results.centroids.fasta
```

## 2.8 Filter out entries which are not BCAs and align using Muscle5.1
```
    $ python3 001.clean_CAs.py
```

## 2.9 Filter alignment to conserved residues
```
    $ ./Gblocks_0.91b/Gblocks ../02.data/UniProt_BLAST_results.centroids.BCAs.fasta.muscle_aligned -t=p -b2=6 -b3=20 -b4=2 -b5=h -d=y -v=240
```

## 2.10 Run IQTree analysis
```
    $ iqtree -s ../02.data/UniProt_BLAST_results.centroids.BCAs.fasta.muscle_aligned-gb -st AA -alrt 100000 -bb 100000 -nt AUTO -m TESTNEW+LM
```

## 2.11 Generate tree figure
```
    $ python3 002.ete_tree.py
```



---
---
# 3. Script files
### __000.get_tools.py__
**DESCRIPTION:** 
Will download Muscle5.1, USEARCH 11, and Gblocks 0.91b to be used in the analysis.

__INPUTS:__ N/A

__OUTPUTS:__
* (/src) program executables downloaded here.


---
### __001.clean_CAs.py__
**DESCRIPTION:** 
Do a basic regex test to see if each of the BLAST results contain both canonical beta-carbonic anhydrase AA motifs (CxDxR & HxxC). Do a Muscle alignment of the passing sequences.

__INPUTS:__
- (/data_raw/Gsalaris_novelBCA.fasta) Novel G. salaris BCA seq.
- (/data_raw/UniProt_BLAST_results.centroids.fasta) Identified centroids determined by USEARCH cluster analysis of BLAST results.

__OUTPUTS:__
* (/data/UniProt_BLAST_results.centroids.BCAs.fasta) Sequences containing BCA AA motifs.
* (/data/UniProt_BLAST_results.centroids.BCAs.fasta.muscle_aligned) Muscle-aligned sequences containing BCA AA motifs, with novel G. salaris BCA added before alignment.

---
### __002.ete_tree.py__
**DESCRIPTION:** 
Run a transcription factor binding site (TFBS) prediction using tfbs_footprinter on the human version of the human vs. Neanderthal SNPs, which have been identified within 2,500 bp of a human protein-coding transcript transcription start site (TSS).

__INPUTS:__
* (/data/UniProt_BLAST_results.centroids.BCAs.fasta.muscle_aligned-gb.contree) Consensus tree generated by IQTree analysis.

__OUTPUTS:__
* (/output/Gsalaris_BCA_phylogram.svg) Phylogram of BCA sequences, colored by phylum.
* (/output/[color_pal].legend.svg) Legend pairing phyla and associated colors.