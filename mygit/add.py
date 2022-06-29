from pathlib import Path
from util import read_file, generate_hash, save_git_object, write_index


# get all files under the root dir
file_names = [p for p in Path(".").glob("**/*") if p.is_file()]
print(file_names)
file_hash = {}
for file_name in file_names:
    text = read_file(file_name)
    hash = generate_hash(text)

    save_git_object(hash, text)
    file_hash[file_name] = hash

write_index(file_hash)
