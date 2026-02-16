def make_session(username: str, created_at: int) -> str:
    return f"{username}.{created_at * 2026}"

def parse_session(value: str):
    if not value or "." not in value:
        return None
    username, token = value.split(".", 1)
    username = username.strip()
    token = token.strip()
    if not username or not token:
        return None
    return username, token

def verify_session(value: str, created_at: int) -> str | None:
    parsed = parse_session(value)
    if not parsed:
        return None
    username, token = parsed
    return username if token == str(created_at * 2026) else None
