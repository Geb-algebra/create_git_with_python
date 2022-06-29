from __future__ import annotations
import hashlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Union

from .util import GIT_DIR_PATH


def create_object_from_hash(hash_: str):
    try:
        obj: Union[Blob, Tree, Commit] = Blob(hash_=hash_)
    except ValueError:  # object type and file type does not match
        try:
            obj = Tree(hash_=hash_)
        except ValueError:  # object type and file type does not match
            obj = Commit(hash_=hash_)
    return obj


class GitObject(ABC):
    """Abstract class for all git objects.

    Note:
        This object holds only the SHA-1 hash made from the object content
        (i.e., does not hold the content of the object)
        There are two reasons for this implementation:
        (1) Eliminate inconsistency between the object's content and
        the content in the database by having the object not have a content.
        (2) Low memory usage.

    Attributes:
        type_: The object type. One of "blob", "tree" or "commit"
        hash_: The SHA-1 hash made from the stringified object content.
    """

    type_ = ""

    @classmethod
    @abstractmethod
    def stringify_parsed_content(cls, content) -> str:
        return ""

    @classmethod
    @abstractmethod
    def parse_str_content(cls, content: str):
        return ""

    @classmethod
    @abstractmethod
    def instantiate_from_content(cls, content):
        str_content: str = cls.stringify_parsed_content(content)
        hash_ = hashlib.sha1(str_content.encode()).hexdigest()
        path = cls._get_file_path(hash_)
        path.parent.mkdir(exist_ok=True)
        path.touch()
        cls._get_file_path(hash_).write_text(str_content)
        return cls(hash_)

    @staticmethod
    def _get_file_path(hash_: str):
        dir_name, file_name = hash_[:2], hash_[2:]
        return GIT_DIR_PATH / f"objects/{dir_name}/{file_name}"

    def __init__(self, hash_: str) -> None:
        self.hash_ = hash_
        with self.file_path.open() as f:
            if f.readline().strip() != self.type_:
                raise ValueError("object type and file type does not match")
        if not self.file_path.exists():
            raise FileNotFoundError("object file does not exist")

    @property
    def file_path(self) -> Path:
        return self._get_file_path(self.hash_)

    @property
    def string_content(self) -> str:
        return self.file_path.read_text()

    @property
    def parsed_content(self):
        return self.parse_str_content(self.string_content)

    def __str__(self) -> str:
        return self.string_content


class Blob(GitObject):
    type_ = "blob"

    @classmethod
    def parse_str_content(cls, content: str) -> str:
        # cut off the first line which tells the object type
        return "".join(content.split("\n\n")[1:])

    @classmethod
    def stringify_parsed_content(cls, parsed_content) -> str:
        # add a line which tells the object type
        return cls.type_ + "\n\n" + parsed_content

    @classmethod
    def instantiate_from_content(cls, content: str):
        return super().instantiate_from_content(content)

    @classmethod
    def instantiate_from_file(cls, path: Path):
        content = path.read_text()
        return cls.instantiate_from_content(content)


class Tree(GitObject):
    type_ = "tree"

    @classmethod
    def parse_str_content(cls, content: str) -> dict:
        parsed_content: dict = {}
        # skip two lines (object type and a blank line)
        for line in content.split("\n")[2:]:
            _, hash_, name = line.split(" ")
            parsed_content[name] = create_object_from_hash(hash_)
        return parsed_content

    @classmethod
    def stringify_parsed_content(
        cls, parsed_content: Dict[str, GitObject]
    ) -> str:
        content = f"{cls.type_}\n\n"
        for name, obj in parsed_content.items():
            content += f"{obj.type_} {obj.hash_} {name}\n"
        return content.strip()

    @classmethod
    def instantiate_from_content(cls, content: Dict[str, Union[Blob, Tree]]):
        return super().instantiate_from_content(content)


class Commit(GitObject):
    type_ = "commit"

    @classmethod
    def parse_str_content(self, content: str) -> dict:
        parsed_content = {}
        # skip two lines (object type and a blank line)
        for line in content.split("\n")[2:]:
            name, hash_ = line.split(" ")
            if not hash_:
                parsed_content[name] = None
            else:
                parsed_content[name] = create_object_from_hash(hash_)
        return parsed_content

    @classmethod
    def stringify_parsed_content(
        cls, parsed_content: Dict[str, GitObject]
    ) -> str:
        content = f"{cls.type_}\n\n"
        for name, obj in parsed_content.items():
            content += f"{name} {obj.hash_ if obj else ''}\n"
        return content[:-1]  # remove the last \n

    @classmethod
    def instantiate_from_content(
        cls, content: Dict[str, Union[Tree, Commit, None]]
    ):
        if (
            content["parent"] is not None
            and content["tree"].hash_ == content["parent"].tree.hash_
        ):
            raise ValueError("No changes to commit.")
        else:
            return super().instantiate_from_content(content)

    @property
    def parent_commit(self) -> Commit:
        return self.parsed_content["parent"]

    @property
    def tree(self) -> Tree:
        return self.parsed_content["tree"]

