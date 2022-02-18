#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python vers. 3.7.0 ###########################################################
# Libraries ####################################################################
from assign_dirs import *
import string
import os
import re

from ete3 import Tree, TreeStyle, NodeStyle, faces, AttrFace
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
################################################################################
# Functions ####################################################################
################################################################################
def my_palplot(pal, size=1, ax=None):
    """
    Make plot of color palette for manual legend.
    """

    import numpy as np
    import matplotlib as mpl
    import matplotlib.ticker as ticker

    # color palette of leaves
    sns_color_pal = "RdYlBu"
    # all phyla
    unique_obs_count = len(phyla)
    obs_colors = sns.color_palette(sns_color_pal, unique_obs_count).as_hex()
    
    n = len(pal)
    
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(n * size, size))
    ax.imshow(np.arange(n).reshape(1, n),
              cmap=mpl.colors.ListedColormap(list(pal)),
              interpolation="nearest", aspect="auto")
    ax.set_xticks(np.arange(n) - .5)
    ax.set_yticks([-.5, .5])
    ax.set_xticklabels(phyla, rotation=90)
    ax.yaxis.set_major_locator(ticker.NullLocator())
    plt.savefig(os.path.join(output_dn, ".".join([sns_color_pal, "legend", "svg"])))

    
def pretty_colors(sns_color_pal):
    """
    Generate colors using observation (phyla) and Seaborn color pal name
    """
    
    unique_obs_count = len(phyla)
    obs_colors = sns.color_palette(sns_color_pal, unique_obs_count).as_hex()
    obs_colors_d = {phylum:obs_color for phylum,obs_color in zip(phyla, obs_colors)}

    return obs_colors_d, obs_colors


def layout(node):

    # set tiered support value 
    support_val = node.support
    tiered_support_val=0
    if support_val >= 50:
        tiered_support_val=50
    if support_val >= 70:
        tiered_support_val=70
    if support_val >= 90:
        tiered_support_val=90
        
    # change the style of the node based on tiered support value
    nstyle = NodeStyle()
    nstyle["shape"] = "sphere"
    nstyle["shape"] = "circle"
    nstyle["size"] = tiered_support_val
    nstyle["fgcolor"] = "black"
    node.set_style(nstyle)

    # tree branch aesthetics
    nstyle["vt_line_width"] = 8
    nstyle["hz_line_width"] = 8
    nstyle["vt_line_type"] = 0 # 0 solid, 1 dashed, 2 dotted
    nstyle["hz_line_type"] = 1

    # modify leaf coloration by phyla
    if node.is_leaf():
        node_name = node.name
        N = AttrFace("name", fsize=100)
        faces.add_face_to_node(N, node, 0, position="aligned")
        org_id = node_name[node_name.find("(")+1:node_name.find(")")]
        org_data = anno_df[anno_df['Entry'] == org_id]
        org_phylum = org_data['Taxonomic lineage (PHYLUM)'].tolist()[0]
        
        obs_color = obs_colors_d[org_phylum]
        node.img_style["bgcolor"] = obs_color
        node.img_style["size"] = 10

    else:
        """https://groups.google.com/forum/#!topic/etetoolkit/bwM12m9c2y4"""
        support_loc_options = ['branch-top', 'float', 'branch-bottom', 'aligned', 'branch-right', 'float-behind']
        support = faces.TextFace(str(int(node.support)),fsize=20, fgcolor="")
        # add a support value to node
        # node.add_face(support, column=0, position=support_loc_options[5])
        # S = AttrFace("support", fsize=45, text_prefix="")
        # faces.add_face_to_node(S, node, 0, position="aligned")
    

def rename_leaves():
    """
    Rename leaves with 
    """

    # iterate through leaves
    for leaf in t:

        leaf_name = leaf.name

        # get organism/seq data for each leaf from BLAST annotation data table
        org_data = anno_df[anno_df['Entry'] == leaf_name]
        org_name = org_data['Taxonomic lineage (SPECIES)'].tolist()[0]

        # extract common name
        if "(" in org_name:
            org_common_name = org_name[org_name.find("(")+1:org_name.find(")")]
        else:
            org_common_name = org_name

        # set new leaf name
        leaf.name = org_common_name+"("+leaf_name+")"


def get_example_tree():

    # Gray dashed branch lines
    for n in t.traverse():
        n.dist = 0.3

    # apply layout
    ts.layout_fn = layout
    ts.show_branch_support = False
    ts.show_leaf_name = False

    # circular layout
    ts.mode = "c"
    ts.root_opening_factor = .25
    return t, ts


################################################################################
# Initiating Variables #########################################################
################################################################################
# phyla have been pseudo-ordered to have bacteria phyla at end, otherwise
# the order is alphabetical
phyla = ['Annelida',
         'Arthropoda',
         'Brachiopoda (lampshells)',         
         'Cnidaria',
         'Echinodermata',         
         'Mollusca',
         'Nematoda (roundworms)',
         'Placozoa (placozoans)',
         'Platyhelminthes',
         'Rotifera (rotifers)',
         'Tardigrada (water bears)',
         'Actinobacteria',
         'Armatimonadetes',
         'Chlamydiae',
         'Cyanobacteria',
         'Firmicutes',
         'Proteobacteria']

# IQ-TREE output consensus file
tree_file = os.path.join(data_dn, "UniProt_BLAST_results.centroids.BCAs.fasta.muscle_aligned-gb.contree")
t = Tree(tree_file)
ts = TreeStyle()

# BLAST annotations
anno_fn = os.path.join(data_raw_dn, "UniProt_BLAST_results.tab")
anno_df = pd.read_csv(anno_fn, sep="\t")

sns_color_pal = "RdYlBu"
################################################################################
# Execution ####################################################################
################################################################################
# generate colors
obs_colors_d, obs_colors = pretty_colors(sns_color_pal)
my_palplot(obs_colors)

rename_leaves() 
t, ts = get_example_tree()
t.ladderize()
t.render(os.path.join(output_dn, "Gsalaris_BCA_phylogram.svg"), tree_style=ts)
























