import os
import hashlib
import glob
from util import *
import argparse


def switch(branch_name):
    set_branch(branch_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("branch_name", type=str, help="branch name")
    args = parser.parse_args()
    switch(args.branch_name)
