import os
import shutil

from absolufy_imports.__main__ import main


def test_main(tmpdir) -> None:
    os.mkdir(os.path.join(str(tmpdir), "mypackage"))
    os.mkdir(os.path.join(str(tmpdir), "mypackage", "mysubpackage"))
    tmp_file = os.path.join(str(tmpdir), "mypackage", "mysubpackage", "baf.py")
    shutil.copy(os.path.join(os.getcwd(), "tests", "test_files", "baf.py"), tmp_file)

    cwd = os.getcwd()
    os.chdir(str(tmpdir))
    try:
        main((os.path.join("mypackage", "mysubpackage", "baf.py"),))
    finally:
        os.chdir(cwd)

    with open(tmp_file) as fd:
        result = fd.read()

    expected = "from . import O\n\nprint(T)\nprint(D)\n"
    assert result == expected
