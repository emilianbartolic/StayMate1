"""Documented CLI input using the same FastAPI hub as the browser."""
import argparse
import http.client
import ipaddress
import json
from urllib.parse import urlparse

def chat(base_url, property_id, question, conversation_id=""):
    parsed = urlparse(base_url)
    if parsed.scheme != "http" or not parsed.hostname or parsed.username or parsed.password or parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
        raise ValueError("Der CLI-Adapter akzeptiert nur eine einfache lokale HTTP-Adresse.")
    try:
        local_host = parsed.hostname.lower() == "localhost" or ipaddress.ip_address(parsed.hostname).is_loopback
    except ValueError:
        local_host = False
    if not local_host:
        raise ValueError("Der CLI-Adapter darf nur den lokalen StayMate-Dienst ansprechen.")
    payload = {"property_id": property_id, "question": question, "conversation_id": conversation_id}
    connection = http.client.HTTPConnection(parsed.hostname, parsed.port or 80, timeout=100)
    try:
        origin = f"http://{parsed.hostname}:{parsed.port or 80}"
        connection.request("POST", "/api/cli/chat", body=json.dumps(payload).encode(), headers={"Content-Type": "application/json", "Origin": origin})
        response = connection.getresponse()
        content = response.read()
        if response.status < 200 or response.status >= 300:
            raise RuntimeError(f"StayMate antwortete mit HTTP {response.status}.")
        return json.loads(content)
    finally:
        connection.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="StayMate shared hub CLI adapter")
    parser.add_argument("question")
    parser.add_argument("--property", default="design-maisonette")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--conversation-id", default="", help="Stabile ID, wenn Host-Antworten später im gleichen CLI-Thread abgefragt werden sollen")
    args = parser.parse_args()
    print(json.dumps(chat(args.base_url, args.property, args.question, args.conversation_id), ensure_ascii=False, indent=2))
