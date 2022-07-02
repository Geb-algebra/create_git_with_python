import argparse

from util import get_last_commit, set_current_branch


def branch(branch_name):
    with open(f"git/refs/{branch_name}", mode="w") as f:
        f.write(get_last_commit())  # 現ブランチの最新コミットをgit/refs/{新ブランチ名}に書く
    set_current_branch(branch_name)  # git/HEADに新ブランチ名を記述


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("branch_name", type=str, help="branch name")
    args = parser.parse_args()
    branch(args.branch_name)
