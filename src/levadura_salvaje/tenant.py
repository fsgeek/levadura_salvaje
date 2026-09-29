"""The corpus index's tenant on arango-ayllu (docs/plumbing-design.md, Ownership).

Yanantin's convention: one database and one user per tenant, a separate `_test`
database with its own user, no root and no `_system` at runtime, no databases
created at runtime. `scripts/tenant_setup.py` creates both once with the admin
credential; everything else connects through `connect()` with a tenant user.

Credentials live in ~/.levadura/config/db.ini (0600), never in the repository.
"""

import configparser
from pathlib import Path

from arango.client import ArangoClient
from arango.database import StandardDatabase

CONFIG = Path.home() / ".levadura" / "config" / "db.ini"
HOSTS = "http://localhost:8531"  # arango-ayllu
TIERS = ("app", "test")


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
