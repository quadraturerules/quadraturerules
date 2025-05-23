import os

from webtools.tools import join


def test_numbering():
    folder = join(
        os.path.dirname(os.path.realpath(__file__)),
        "..",
        "..",
        "rules",
    )
    qr_files = []
    folders = []
    for file in os.listdir(folder):
        if file.endswith(".qr"):
            assert os.path.isfile(os.path.join(folder, file))
            qr_files.append(file[:-3])
        else:
            assert os.path.isdir(os.path.join(folder, file))
            folders.append(file)

    assert set(qr_files) == set(folders)
    for i in range(1, len(qr_files) + 1):
        assert "Q" + f"000000{i}"[-6:] in qr_files


def test_version():
    folder = join(
        os.path.dirname(os.path.realpath(__file__)),
        "..",
        "..",
        "rules",
    )
    v = max(int(file[1:-3]) for file in os.listdir(folder) if file.endswith(".qr"))

    with open(join(
        os.path.dirname(os.path.realpath(__file__)),
        "..",
        "..",
        "VERSION",
    )) as f:
        assert int(f.read().split(".")[1]) == v
