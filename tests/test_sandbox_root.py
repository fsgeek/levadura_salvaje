"""The sandbox's root credential is read from a private file, never from the container (2026-10-25)."""

import os

import pytest

from levadura_salvaje.tenant import sandbox_root


def write(path, mode, text="[root]\npassword = not-a-real-password\n"):
    path.write_text(text)
    os.chmod(path, mode)
    return path


def test_reads_a_private_file(tmp_path):
    assert sandbox_root(write(tmp_path / "sandbox.ini", 0o600)) == "not-a-real-password"


def test_refuses_a_file_others_can_read(tmp_path):
    with pytest.raises(PermissionError, match="0600"):
        sandbox_root(write(tmp_path / "sandbox.ini", 0o644))


def test_missing_file_says_who_writes_it(tmp_path):
    with pytest.raises(FileNotFoundError, match="yanantin"):
        sandbox_root(tmp_path / "sandbox.ini")
