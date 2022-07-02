from pathlib import Path
from util import read_file, generate_hash, save_git_object, write_index

# リポジトリ直下のファイル全て
file_names = [p for p in Path(".").glob("**/*") if p.is_file()]
file_hash = {}
for file_name in file_names:
    text = read_file(file_name)
    hash = generate_hash(text)  # ファイルの中身のhash生成
    save_git_object(hash, text)  # hashをファイル名にしてgit/objectsに保存
    file_hash[file_name] = hash

write_index(file_hash)  # 登録したファイルの情報をgit/indexに記述
