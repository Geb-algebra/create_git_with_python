from util import (
    read_file,
    generate_hash,
    save_git_object,
    get_last_commit,
    set_last_commit,
)

# 複数回コミットを禁止する
# 以前のコミットのtreeのハッシュとindexのハッシュが等しかったら禁止
# def get_hash_content(hash, obj_type):
#     with open(f"git/objects/{hash}", mode="r") as f:
#         content = f.read()
#     return content


# treeを保存
text = read_file("git/index")
tree_hash = generate_hash(text)

save_git_object(tree_hash, text)

commit_object = f"tree {tree_hash}\nparent {get_last_commit()}"

# commit objectを保存
commit_hash = generate_hash(commit_object)
set_last_commit(commit_hash)

save_git_object(commit_hash, commit_object)
