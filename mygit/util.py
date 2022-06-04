import os
import hashlib


def generate_hash(content):
    m = hashlib.sha256()
    m.update(content.encode())
    hash_ = m.hexdigest()
    return hash_


def read_file(file_name):
    with open(file_name, "r") as f:
        text = f.read()
    return text


def save_file(file_name, content):
    if not os.path.exists(file_name):
        os.makedirs("git/objects", exist_ok=True)
        with open("git/objects/" + file_name, "w") as f:
            f.write(content)


def save_index(tree_dict):
    content = ""
    for name, hash_ in tree_dict.items():
        content += f"{name} {hash_}\n"
    # save_file(hash_tree, content)
    with open("git/" + "index", "w") as f:
        f.write(content)


def get_branch():
    with open("git/HEAD", "r") as f:
        branch_path = f.read()
    return branch_path


def set_branch(branch):
    branch_path = f"git/refs/{branch}"
    if not os.path.exists(branch_path):
        raise Exception(f"branch {branch} does not exist")
    with open("git/HEAD", "w") as f:
        f.write(branch_path)


def get_ref():
    branch_path = get_branch()
    with open(branch_path, mode="r") as f:
        last_commit_hash = f.read()
    return last_commit_hash


def set_ref(content):
    branch_path = get_branch()
    with open(branch_path, mode="w") as f:
        f.write(content)
