#!/usr/bin/env python3

import hashlib
import os, os.path
from functools import reduce
import sys

BLOCKSIZE=2**20 # 1M
NUM_BLOCKS=3

def dwhash_file(in_file):
    #print("Hash of file: "+in_file)
    hasher = hashlib.sha512()
    n=0
    with open(in_file, 'rb') as infile:
        #_print_pos(infile)
        buf = infile.read(BLOCKSIZE)
        while len(buf) > 0 and n<NUM_BLOCKS-1:
            hasher.update(buf)
            buf = infile.read(BLOCKSIZE)
            n = n+1

        #_print_pos(infile)

        last_pos = infile.seek(0,2)

        #_print_pos(infile)
        if last_pos>(NUM_BLOCKS*BLOCKSIZE):
            infile.seek(-(NUM_BLOCKS*BLOCKSIZE),2)
            #_print_pos(infile)
        else:
            infile.seek(0,0)
            #_print_pos(infile)

        while len(buf) > 0 and n<NUM_BLOCKS:
            hasher.update(buf)
            n = n+1

    size=os.stat(in_file).st_size
    hasher.update(str(size).encode("utf-8"))

    return hasher.hexdigest()

def generic_walk(path):
    if(os.path.isfile(path)):
        return [dwhash_file(path)]
    elif(os.path.isdir(path)):
        items = [os.path.join(path,i) for i in os.listdir(path)]
        one_list=[]
        it=map(generic_walk,items) # items are now all lists. collect lists into one
        for i in it:
            one_list.extend(i)
        # add the hash of the dir too!
        # concatenate sort one_list, concatenate, calculate the hash of the resulting string
        one_list=list(set(one_list)) # remove duplicates
        one_list.sort()
        s = ""
        for i in one_list:
            s = s+i

        hasher = hashlib.sha512()
        hasher.update(s.encode('utf-8'))
        one_list.append(hasher.hexdigest())

        return one_list
    else:
        raise ValueError

import argparse

if __name__=="__main__":
    pass
