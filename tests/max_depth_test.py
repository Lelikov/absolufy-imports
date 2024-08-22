import os
import shutil

import pytest

from absolufy_imports.__main__ import main


@pytest.mark.parametrize(
    ("max_depth", "imports"),
    [
        (0, "from mypackage.foo import T\nfrom mypackage.mysubpackage.bar import D"),
        (1, "from mypackage.foo import T\nfrom .bar import D"),
        (2, "from ..foo import T\nfrom .bar import D"),
    ],
)
def test_max_depth(tmpdir, max_depth: int, imports: str) -> None:
    os.mkdir(os.path.join(str(tmpdir), "mypackage"))
    os.mkdir(os.path.join(str(tmpdir), "mypackage", "mysubpackage"))
    tmp_file = os.path.join(
        str(tmpdir),
        "mypackage",
        "mysubpackage",
        "bar.py",
    )
    shutil.copy(
        os.path.join(os.getcwd(), "tests", "test_files", "bar.py"),
        tmp_file,
    )

    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        main(
            (
                "--application-directories",
                ".",
                f"--max-depth={max_depth}",
                tmp_file,
            ),
        )
    finally:
        os.chdir(cwd)

    with open(tmp_file) as fd:
        result = fd.read()

    expected = f"""from mypackage.mysubpackage import B
from mypackage.mysubpackage.bar import baz
{imports}
from . import O
from datetime import datetime

print(T)
print(D)
"""
    assert result == expected
