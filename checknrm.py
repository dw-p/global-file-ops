#!/usr/bin/env python3

import gfo, sys


MASTER_RM_DB_FN="master_rm_db.txt"
RM_TMPL_s="rm -rf {path}"
RM_TMPL_f="""#!/bin/bash

{rm_cmds}
"""

if __name__=="__main__":
    #hashes = gfo.generic_walk(sys.argv[1])
    #hashes = set(hashes)

    with open(MASTER_RM_DB_FN, 'r') as infile:
        db = infile.readlines()
        db = set([l.strip() for l in db])

    print(str(db))
