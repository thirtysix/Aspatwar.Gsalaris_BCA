#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python vers. 3.7.0 ###########################################################
# Libraries ####################################################################
from assign_dirs import *
import os
from pathlib import Path


import pandas as pd
import gzip
import shutil
import tarfile

import ftplib
import urllib.request
import ssl

################################################################################
# Description/Notes ############################################################
################################################################################
"""
The current conda install process for Muscle 5.1 is imperfect.
We will download the executable directly from the project Github,
and call it directly.

USEARCH is only available from the DRIVE5 website.

"""

################################################################################
# Base-level Functions #########################################################
################################################################################


################################################################################
# Task-specific Functions ######################################################
################################################################################

def get_muscle():

    url = "https://github.com/rcedgar/muscle/releases/download/v5.1/muscle5.1.linux_intel64"
    ofn = os.path.join(data_raw_dn, os.path.basename(url))
    ofn = os.path.basename(url)

    # download archive file if it doesn't exist
    if not os.path.exists(ofn):
        try:
            ssl._create_default_https_context = ssl._create_unverified_context # avoid 'SSL: CERTIFICATE_VERIFY_FAILED' error
            urllib.request.urlretrieve(url, ofn)
            print("Download of {} was successful".format('Muscle'))
        except:
            print("Download of {} was unsuccessful".format('Muscle'))
    

def get_usearch():

    url = "https://drive5.com/downloads/usearch11.0.667_i86linux32.gz"
    ofn = os.path.join(data_raw_dn, os.path.basename(url))
    ofn = os.path.basename(url)

    # download file if it doesn't exist
    if not os.path.exists(ofn):
        try:
            ssl._create_default_https_context = ssl._create_unverified_context # avoid 'SSL: CERTIFICATE_VERIFY_FAILED' error
            urllib.request.urlretrieve(url, ofn)
            print("Download of {} was successful".format('USEARCH'))

        except:
            print("Download of {} was unsuccessful".format('USEARCH'))


    try:
        # extract file
        with gzip.open(ofn, 'rb') as f_in:
            unzipped_ofn = os.path.splitext(ofn)[0]
            with open(unzipped_ofn, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    except:
        print("Cannot extract {}".format(ofn))


def get_gblocks():

    url = "http://molevol.cmima.csic.es/castresana/Gblocks/Gblocks_Linux64_0.91b.tar.Z"
    ofn = os.path.join(data_raw_dn, os.path.basename(url))
    ofn = os.path.basename(url)

    # download archive file if it doesn't exist
    if not os.path.exists(ofn):
        try:
            ssl._create_default_https_context = ssl._create_unverified_context # avoid 'SSL: CERTIFICATE_VERIFY_FAILED' error
            urllib.request.urlretrieve(url, ofn)
            print("Download of {} was successful".format('GBlocks'))
        except:
            print("Download of {} was unsuccessful".format('GBlocks'))


################################################################################
# Initiating Variables #########################################################
################################################################################


################################################################################
# Execution ####################################################################
################################################################################
print("Will download Muscle 5.1 release from github.")
get_muscle()

print("""Will download 32-bit USearch release from Drive5.
      Terms of Use License at: https://drive5.com/usearch/license32.html""")
get_usearch()

print("Will download GBlocks 0.91b release from github.")
get_gblocks()






