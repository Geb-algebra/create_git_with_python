import os
import hashlib
import glob
from util import *
import argparse


def branch(branch_name):
    with open(f"git/refs/{branch_name}", mode="w") as f:
        f.write(get_ref())
    set_branch(branch_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("branch_name", type=str, help="branch name")
    args = parser.parse_args()
    branch(args.branch_name)