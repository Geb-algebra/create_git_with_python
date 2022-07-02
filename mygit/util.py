import os
import hashlib


def generate_hash(content: str):
    """ファイルの中身 (content) からhash生成"""
    m = hashlib.sha1()
    m.update(content.encode())
    hash_ = m.hexdigest()
    return hash_


def read_file(file_name):
    with open(file_name, "r") as f:
        text = f.read()
    return text


def save_git_object(file_name, content):
    """ファイル名file_name, 内容contentのファイルをgit/objectsに保存"""
    if not os.path.exists(file_name):
        os.makedirs("git/objects", exist_ok=True)
        with open("git/objects/" + file_name, "w") as f:
            f.write(content)


def write_index(tree_dict):
    """ファイル一覧をgit/indexに記述"""
    content = ""
    for name, hash_ in tree_dict.items():
        content += f"{name} {hash_}\n"
    # save_file(hash_tree, content)
    with open("git/" + "index", "w") as f:
        f.write(content)


def get_current_branch():
    """git/HEADから今のブランチ名を読んでくる"""
    with open("git/HEAD", "r") as f:
        branch_path = f.read()
    return branch_path


def set_current_branch(branch):
    """git/HEADにブランチ名を書いてブランチ設定"""
    branch_path = f"git/refs/{branch}"
    if not os.path.exists(branch_path):
        raise Exception(f"branch {branch} does not exist")
    with open("git/HEAD", "w") as f:
        f.write(branch_path)


def get_last_commit():
    """現ブランチの最新コミットを読んでくる"""
    branch_path = get_current_branch()
    with open(branch_path, mode="r") as f:
        last_commit_hash = f.read()
    return last_commit_hash


def set_last_commit(last_commit_hash):
    """現ブランチの最新コミットを設定"""
    branch_path = get_current_branch()
    with open(branch_path, mode="w") as f:
        f.write(last_commit_hash)
