"""Create the corpus index's tenant on arango-ayllu. Run once; idempotent.

The only code that uses the admin (root) credential, which it reads from the
container rather than storing. It creates `levadura` and `levadura_test`, one
user per database with read-write on that database only, and writes the tenant
credentials to ~/.levadura/config/db.ini (0600). See src/levadura_salvaje/tenant.py.

    uv run python scripts/tenant_setup.py
"""

import configparser
import os
import secrets
import string
import subprocess

from arango.client import ArangoClient

from levadura_salvaje.tenant import CONFIG, HOSTS, TIERS

CONTAINER = "arango-ayllu"
DATABASES = {"app": "levadura", "test": "levadura_test"}
USERS = {"app": "levadura", "test": "levadura_test"}


def root_password() -> str:
    env = subprocess.run(["docker", "inspect", CONTAINER, "--format",
                          "{{range .Config.Env}}{{println .}}{{end}}"],
                         capture_output=True, text=True, check=True).stdout
    return next(v.split("=", 1)[1] for v in env.splitlines() if v.startswith("ARANGO_ROOT_PASSWORD="))


def password() -> str:
    return "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(24))


def save(c: configparser.ConfigParser) -> None:
    """Atomic and private from the first byte: a 0600 temporary file, then rename."""
    CONFIG.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(CONFIG.parent, 0o700)
    tmp = CONFIG.with_suffix(".tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        c.write(f)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, CONFIG)


def main() -> None:
    c = configparser.ConfigParser()
    c.read(CONFIG)
    if "database" not in c:
        c["database"] = {"hosts": HOSTS, "container": CONTAINER}
    s = c["database"]
    s.setdefault("cursor_secret", secrets.token_hex(32))  # signs drill cursors
    for tier in TIERS:
        s[f"{tier}_database"], s[f"{tier}_user"] = DATABASES[tier], USERS[tier]
        s.setdefault(f"{tier}_password", password())
    save(c)  # durable before any password changes on the server
    sys_db = ArangoClient(hosts=HOSTS).db("_system", username="root", password=root_password(), verify=True)
    for tier in TIERS:
        db, user = DATABASES[tier], USERS[tier]
        if not sys_db.has_database(db):
            sys_db.create_database(db)
        if sys_db.has_user(user):
            sys_db.replace_user(user, password=s[f"{tier}_password"], active=True)
        else:
            sys_db.create_user(user, password=s[f"{tier}_password"], active=True)
        for other in sys_db.permissions(user):
            if other not in (db, "*"):
                sys_db.update_permission(user, "none", other)
        sys_db.update_permission(user, "rw", db)
        sys_db.update_permission(user, "none", "_system")
        grants = {}
        for d, p in sys_db.permissions(user).items():
            if p.get("permission") not in ("none", "undefined", None):
                grants[d] = p["permission"]
            for coll, cp in p.get("collections", {}).items():
                if cp not in ("none", "undefined"):
                    grants[f"{d}/{coll}"] = cp
        if grants != {db: "rw"}:
            raise SystemExit(f"{user}: effective grants {grants}, expected {{{db!r}: 'rw'}}")
        print(f"{tier}: database {db}, user {user}, grants {grants}")
    os.chmod(CONFIG, 0o600)
    print(f"credentials: {CONFIG}")


if __name__ == "__main__":
    main()
