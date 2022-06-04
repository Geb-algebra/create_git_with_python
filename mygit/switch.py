import argparse

from util import set_current_branch


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("branch_name", type=str, help="branch name")
    args = parser.parse_args()
    set_current_branch(args.branch_name)
