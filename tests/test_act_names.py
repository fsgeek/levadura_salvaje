"""Act-name resolution through Yanantin's Jabberwock (parity lens v2)."""

import pytest

pytest.importorskip("yanantin", reason="needs uv run --with-editable ../yanantin")

from levadura_salvaje.act_names import ActNames, canonical, definitions


def test_canonical_long_names():
    assert canonical("the Bank Holding Company Act of 1956") == "bank holding company act"
    assert canonical("Bank Holding Company Act, as amended") == "bank holding company act"
    assert canonical("Home Owners' Loan Act") == "home owners' loan act"


def test_definitions_both_forms():
    d = definitions("BHC Act means the Bank Holding Company Act of 1956 (12 U.S.C. 1841 et seq.).")
    assert ("BHC Act", "Bank Holding Company Act of 1956") in d
    d = definitions("under the Federal Deposit Insurance Act (12 U.S.C. 1811 et seq.) (FDI Act), a")
    assert ("FDI Act", "Federal Deposit Insurance Act") in d
    d = definitions("the Financial Institutions Reform, Recovery, and Enforcement Act of 1989 (FIRREA)")
    assert ("FIRREA", "Financial Institutions Reform, Recovery, and Enforcement Act of 1989") in d
    d = definitions("Act means the Farm Credit Act of 1971, as amended.")
    assert ("Act", "Farm Credit Act of 1971") in d


@pytest.fixture
def names(tmp_path):
    n = ActNames(tmp_path / "j.duckdb")
    n.learn("12", "225", "the Bank Holding Company Act of 1956 (BHC Act) and the Act means the "
            "Bank Holding Company Act")
    n.learn("12", "1263", "Bank Act means the Federal Home Loan Bank Act")
    n.learn("12", "5", "the Bank Holding Company Act (BHC Act)")
    n.learn("12", "999", "the Bank Secrecy Act (Bank Act)")  # a conflicting short name
    return n


def test_long_names_and_short_names_resolve_to_one_act(names):
    bhc = names.resolve("Bank Holding Company Act of 1956", "12", "1")
    assert bhc is not None
    assert names.resolve("Bank Holding Company Act", "12", "1") == bhc
    assert names.resolve("BHC Act", "12", "7") == bhc  # consistent everywhere: global


def test_local_names_stay_local(names):
    bhc = names.resolve("Bank Holding Company Act", "12", "1")
    assert names.resolve("Act", "12", "225") == bhc
    assert names.resolve("Act", "12", "226") is None


def test_conflicting_short_names_resolve_only_where_defined(names):
    fhlb = names.resolve("Federal Home Loan Bank Act", "12", "1")
    assert names.resolve("Bank Act", "12", "1263") == fhlb
    assert names.resolve("Bank Act", "12", "999") == names.resolve("Bank Secrecy Act", "12", "1")
    assert names.resolve("Bank Act", "12", "7") is None  # two meanings: mome, not a guess
