import os
import shutil

import pytest

from absolufy_imports.__main__ import main


def test_main(tmpdir) -> None:
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
            (os.path.join("mypackage", "mysubpackage", "bar.py"),),
        )
    finally:
        os.chdir(cwd)

    with open(tmp_file) as fd:
        result = fd.read()

    expected = (
        "from mypackage.mysubpackage import B\n"
        "from mypackage.mysubpackage.bar import baz\n"
        "from mypackage.foo import T\n"
        "from .bar import D\n"
        "from . import O\n"
        "from datetime import datetime\n"
        "\n"
        "print(T)\n"
        "print(D)\n"
    )
    assert result == expected


def test_main_src(tmpdir) -> None:
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
                tmp_file,
            ),
        )
    finally:
        os.chdir(cwd)

    with open(tmp_file) as fd:
        result = fd.read()

    expected = (
        "from mypackage.mysubpackage import B\n"
        "from mypackage.mysubpackage.bar import baz\n"
        "from mypackage.foo import T\n"
        "from .bar import D\n"
        "from . import O\n"
        "from datetime import datetime\n"
        "\n"
        "print(T)\n"
        "print(D)\n"
    )
    assert result == expected


def test_noop(tmpdir) -> None:
    os.mkdir(os.path.join(str(tmpdir), "mypackage"))
    os.mkdir(os.path.join(str(tmpdir), "mypackage", "mysubpackage"))
    tmp_file = os.path.join(
        str(tmpdir),
        "mypackage",
        "mysubpackage",
        "baz.py",
    )
    shutil.copy(
        os.path.join(os.getcwd(), "tests", "test_files", "baz.py"),
        tmp_file,
    )

    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        main(
            (
                "--application-directories",
                ".",
                tmp_file,
            ),
        )
    finally:
        os.chdir(cwd)

    with open(tmp_file) as fd:
        result = fd.read()

    with open(os.path.join(os.getcwd(), "tests", "test_files", "baz.py")) as fd:
        expected = fd.read()

    assert result == expected


def test_bom_file() -> None:
    main(
        (
            "--application-directories",
            ".",
            os.path.join(os.getcwd(), "tests", "test_files", "bom.py"),
        ),
    )


def test_unresolvable_dir(tmpdir) -> None:
    f = tmpdir.join("f.py")
    f.write_binary("# -*- coding: cp1252 -*-\nx = €\n".encode("cp1252"))
    with pytest.raises(ValueError, match=r".*f.py.*"):
        main((f.strpath,))
