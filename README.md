# ZFS Automatic Manager

ZAM is a python-based command-line tool for maintaining a ZFS file system.

ZAM is very much a work in progress, and the name is certainly not final.

Currently the only feature that ZAM supports is periodically taking snapshots
and replicating them to remote servers. ZAM is not even able to delete old
snapshots, although that feature is a top priority.


## Development Process

Run these commands from the root of the ZAM repository to setup the development
environment:

    python3 -m venv ".venv" --prompt "ZAM"
    source ".venv/bin/activate"
    .venv/bin/python3 -m pip install --upgrade pip
    pip install -e '.'
    pip install -r requirements_dev.txt

Before each commit, run these commands and fix any issues:

    black --line-length 80 src tests
    mypy src/zam/task.py
    flake8 src tests
    pytest

## Installation

To install zam itself, simply run these two commands:

    python setup.py build
    python setup.py install --optimize=1

To install Linux-specific files that may be useful (e.g. example config file,
systemd service), run this command:

    make install_utils
