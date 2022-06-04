import glob
from util import read_file, generate_hash, save_git_object, write_index


# file_names = ["test/file_in_test.txt"]
file_names = glob.glob("**/*.txt", recursive=True)
print(file_names)
file_hash = {}
for file_name in file_names:
    text = read_file(file_name)
    hash = generate_hash(text)

    save_git_object(hash, text)
    file_hash[file_name] = hash

write_index(file_hash)
