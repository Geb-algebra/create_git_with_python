import os
import hashlib
import glob
from util import *

# 複数回コミットを禁止する
# 以前のコミットのtreeのハッシュとindexのハッシュが等しかったら禁止
# def get_hash_content(hash, obj_type):
#     with open(f"git/objects/{hash}", mode="r") as f:
#         content = f.read()
#     return content


# treeを保存
text = read_file("git/index")
tree_hash = generate_hash(text)
# last_commit_hash = get_hash_content(get_ref())
# if tree_hash == last_commit_hash:

save_file(tree_hash, text)

commit_object = f"tree {tree_hash}\nparent {get_ref()}"

# commit objectを保存
commit_hash = generate_hash(commit_object)
set_ref(commit_hash)

save_file(commit_hash, commit_object)
