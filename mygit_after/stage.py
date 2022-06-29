from __future__ import annotations
from pathlib import Path
from typing import Dict, Union

from mygit_after.git_objects import Blob, Tree
from mygit_after.util import GIT_DIR_PATH


class Stage:
    file_path = GIT_DIR_PATH / "index"

    def __init__(self) -> None:
        if not self.file_path.exists():
            self.file_path.touch()
        self.content: Dict[Path, Blob] = {}
        for line in self.file_path.read_text().strip().split("\n"):
            if " " in line:
                hash_, path = line.split(" ")
                self.content[Path(path)] = Blob(hash_)

    def _save(self) -> None:
        str_content = ""
        for path, blob in self.content.items():
            str_content += f"{blob.hash_} {path}\n"
        self.file_path.write_text(str_content)

    def add(self, file_path: Path, blob: Blob) -> None:
        self.content[file_path] = blob
        self._save()

    def generate_tree(self) -> Tree:
        def create_tree(index: Dict[Path, Blob]) -> Tree:
            gathered_items: Dict[str, Dict[Path, Blob]] = {}
            for path, blob in index.items():
                relative_root = path.parts[0]
                path_from_rel_root = Path("/".join(path.parts[1:]))
                if relative_root not in gathered_items:
                    gathered_items[relative_root] = {path_from_rel_root: blob}
                else:
                    gathered_items[relative_root][path_from_rel_root] = blob
            tree_content: Dict[str, Union[Blob, Tree]] = {}
            for root, children in gathered_items.items():
                if Path(".") in children:  # if root is a file
                    tree_content[root] = children[Path(".")]
                else:
                    tree_content[root] = create_tree(children)
            return Tree.instantiate_from_content(tree_content)

        return create_tree(self.content)
