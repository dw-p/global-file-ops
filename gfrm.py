#!/usr/bin/env python3

import gfo
import sys

MASTER_RM_DB_FN="master_rm_db.txt"
HASHES_TMP="hashes.tmp"
RM_SCRIPT_FN="rm-generated.bash"
RM_TMPL_s="rm -rf {path}"
RM_TMPL_f="""#!/bin/bash

set -e

{rm_cmds}

# append the hashes to the DB
cat {hashes_tmp} >> {rm_db}
"""

if __name__=="__main__":
    hashes = gfo.generic_walk(sys.argv[1])

    with open(HASHES_TMP, 'w') as tmpfile:
        list(map(lambda i: tmpfile.write(i+'\n'),hashes))

    rm_string=RM_TMPL_s.format(path=sys.argv[1])
    rm_generated_bash=RM_TMPL_f.format(rm_cmds=rm_string,hashes_tmp=HASHES_TMP,rm_db=MASTER_RM_DB_FN)

    print("Writing script for deletion of {s}... ".format(s=sys.argv[1]))
    with open(RM_SCRIPT_FN, 'w') as outfile:
        outfile.write(rm_generated_bash)

    print("Don't forget to invoke {s}!\n\n".format(s=RM_SCRIPT_FN))
