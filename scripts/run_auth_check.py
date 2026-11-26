"""Exercise dormant account/session data isolation with disposable SQLite data."""
from __future__ import annotations

import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from trinity.hub.accounts import authenticate, create_user, get_session, issue_session, revoke_session
from trinity.hub.memory import create_conversation, create_ticket, list_tickets


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="staymate-auth-check-") as directory:
        database = Path(directory) / "isolated.sqlite3"
        first = create_user("guest-a@example.test", "Strong test password 1", "Gast A", path=database)
        second = create_user("guest-b@example.test", "Strong test password 2", "Gast B", path=database)
        assert first["role"] == second["role"] == "guest"
        assert authenticate(first["email"], "Strong test password 1", path=database)["id"] == first["id"]
        assert authenticate(first["email"], "wrong password", path=database) is None
        session, _ = issue_session(first["id"], path=database)
        assert get_session(session, path=database)["id"] == first["id"]
        assert create_conversation("conversation-a", first["id"], path=database)
        assert not create_conversation("conversation-a", second["id"], path=database)
        create_ticket("city-loft", "City Loft", "", "Question", "unknown", "normal", "Summary", "conversation-a", first["id"], path=database)
        assert len(list_tickets(owner_id=first["id"], path=database)) == 1
        assert list_tickets(owner_id=second["id"], path=database) == []
        revoke_session(session, path=database)
        assert get_session(session, path=database) is None
    print("PASS account password hashing, session revocation, chat ownership, and per-user ticket isolation.")


if __name__ == "__main__":
    main()
