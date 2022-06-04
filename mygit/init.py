import os

if os.path.exists("git"):
    raise Exception("git already exists")
os.mkdir("git")
os.mkdir("git/refs")
with open("git/refs/main", mode="w") as f:
    f.write("")

with open("git/HEAD", "w") as f:
    f.write("git/refs/main")
