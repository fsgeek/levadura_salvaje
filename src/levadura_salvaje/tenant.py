"""The corpus index's tenant on arango-ayllu (docs/plumbing-design.md, Ownership).

Yanantin's convention: one database and one user per tenant, a separate `_test`
database with its own user, no root and no `_system` at runtime, no databases
created at runtime. `scripts/tenant_setup.py` creates both once with the admin
credential; everything else connects through `connect()` with a tenant user.

Credentials live in ~/.levadura/config/db.ini (0600), never in the repository.

The sandbox's (arango-vector-sandbox) root is read by `sandbox_root()` from
~/.levadura/config/sandbox.ini (0600), which yanantin's owner writes when it rotates
that password, so the value never passes through an agent. It was read from the
container's environment until 2026-10-25, and a container's environment can't change
without recreating it, which blocked the rotation.
"""

import configparser
import stat
from pathlib import Path

from arango.client import ArangoClient
from arango.database import StandardDatabase

CONFIG = Path.home() / ".levadura" / "config" / "db.ini"
HOSTS = "http://localhost:8531"  # arango-ayllu
TIERS = ("app", "test")
SANDBOX = Path.home() / ".levadura" / "config" / "sandbox.ini"


def sandbox_root(path: Path = SANDBOX) -> str:
    """The sandbox's root password, from [root] password in a file only its owner can read."""
    if not path.exists():
        raise FileNotFoundError(f"{path}: written by yanantin's owner when it rotates the sandbox root "
                                "(yanantin docs/credentials.md)")
    if stat.S_IMODE(path.stat().st_mode) & 0o077:
        raise PermissionError(f"{path}: must be 0600 (owner only), is {stat.S_IMODE(path.stat().st_mode):04o}")
    c = configparser.ConfigParser()
    c.read(path)
    return c["root"]["password"]


def settings(path: Path = CONFIG) -> configparser.SectionProxy:
    c = configparser.ConfigParser()
    if not c.read(path):
        raise FileNotFoundError(f"{path}: run scripts/tenant_setup.py once")
    return c["database"]


def connect(tier: str = "test", path: Path = CONFIG) -> StandardDatabase:
    """A handle on the tenant's database for `tier` ("app" or "test")."""
    if tier not in TIERS:
        raise ValueError(f"tier must be one of {TIERS}")
    s = settings(path)
    return ArangoClient(hosts=s["hosts"]).db(s[f"{tier}_database"], username=s[f"{tier}_user"],
                                              password=s[f"{tier}_password"], verify=True)
