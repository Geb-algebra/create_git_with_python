from __future__ import annotations
from pathlib import Path
import argparse
import sys

from matplotlib.pyplot import ginput
from mygit_after.git_objects import Blob, Commit

from mygit_after.stage import Stage

from .util import GIT_DIR_PATH

commands = {
    "init": [],
    "add": ["path"],
    "commit": [],
    "checkout": ["branch"],
    "merge": ["branch"],
    "rebase": ["commit_hash"],
}

argparser = argparse.ArgumentParser(description="The stupid content tracker")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
for command, args in commands.items():
    sp = argsubparsers.add_parser(command)
    for arg in args:
        sp.add_argument(arg)
argsubparsers.required = True


def init(args):
    GIT_DIR_PATH.mkdir()
    (GIT_DIR_PATH / "objects").mkdir()
    (GIT_DIR_PATH / "refs").mkdir()
    (GIT_DIR_PATH / "refs" / "main").touch()
    (GIT_DIR_PATH / "HEAD").write_text("git/refs/main")


def add(args):
    def should_add(path):
        return (
            path.exists()
            and path.is_file()
            and "git" not in path.parts
            and path.name not in ["git.py", ".DS_Store"]
        )

    index = Stage()
    specified_path = Path(args.path)
    if should_add(specified_path):
        index.add(specified_path, Blob.instantiate_from_file(specified_path))
    else:
        for path in specified_path.glob("**/*"):
            if should_add(path):
                index.add(path, Blob.instantiate_from_file(path))


def commit(args):
    tree = Stage().generate_tree()
    branch_path = Path((GIT_DIR_PATH / "HEAD").read_text())
    last_commit_hash = branch_path.read_text()
    if not last_commit_hash:  # initial commit
        last_commit = None
    else:
        last_commit = Commit(last_commit_hash)
    commit = Commit.instantiate_from_content(
        {"tree": tree, "parent": last_commit}
    )
    branch_path.write_text(commit.hash_)


def switch():
    pass


def merge():
    pass


def restore():
    pass


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    if args.command == "add":
        add(args)
    elif args.command == "switch":
        switch(args)
    elif args.command == "commit":
        commit(args)
    elif args.command == "init":
        init(args)
    elif args.command == "merge":
        merge(args)
    elif args.command == "restore":
        restore(args)
