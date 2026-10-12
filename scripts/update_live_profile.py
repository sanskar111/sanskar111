"""Refresh profile sections using only the Python standard library."""
from datetime import datetime, timedelta, timezone
from html import escape
import json
from pathlib import Path
import re
from urllib.request import Request, urlopen

IST = timezone(timedelta(hours=5, minutes=30), "IST")
JOKE_URL = "https://v2.jokeapi.dev/joke/Programming?safe-mode&lang=en&blacklistFlags=nsfw,religious,political,racist,sexist,explicit"


def replace_section(text, start, end, body):
    pattern = re.escape(start) + r".*?" + re.escape(end)
    if len(re.findall(pattern, text, flags=re.S)) != 1:
        raise ValueError(f"Expected one section: {start}")
    return re.sub(pattern, lambda _: f"{start}\n{body}\n{end}", text, flags=re.S)


def joke_markup(data, date):
    if data.get("error") or data.get("category") != "Programming":
        raise ValueError("Unexpected joke response")
    if data.get("safe") is not True or any(data.get("flags", {}).values()):
        raise ValueError("Joke did not pass safe-mode checks")
    if data.get("type") == "single":
        lines = [data["joke"]]
    elif data.get("type") == "twopart":
        lines = [data["setup"], data["delivery"]]
    else:
        raise ValueError("Unsupported joke format")
    if not all(isinstance(line, str) and line.strip() for line in lines):
        raise ValueError("Empty joke")
    # External text is displayed as escaped HTML, never interpreted as markup.
    content = "<br />".join(escape(line).replace("\n", "<br />") for line in lines)
    return f"<!-- JOKE-DATE:{date} -->\n<blockquote>{content}</blockquote>\n\n<sub>Programming joke · {date} IST · <a href=\"https://jokeapi.dev/\">JokeAPI</a></sub>"


def show_populated_section(text, outer_start, outer_end, inner_start, inner_end, heading):
    pattern = re.escape(inner_start) + r"(.*?)" + re.escape(inner_end)
    match = re.search(pattern, text, flags=re.S)
    if match is None:
        raise ValueError(f"Missing marker: {inner_start}")
    body = match.group(1).strip()
    # Empty optional sections stay invisible until their source supplies data.
    inner = f"{inner_start}\n{body}\n{inner_end}"
    return replace_section(text, outer_start, outer_end, f"{heading}\n\n{inner}" if body else inner)


def update(text, now, fetch_joke):
    date = now.strftime("%Y-%m-%d")
    if f"<!-- JOKE-DATE:{date} -->" not in text:
        try:
            joke = joke_markup(fetch_joke(), date)
            text = replace_section(text, "<!-- DAILY-JOKE:START -->", "<!-- DAILY-JOKE:END -->", joke)
        except Exception as error:
            # Preserve the last successful joke and its original date on outages.
            print(f"::warning::Daily joke was not refreshed ({type(error).__name__}); retained previous content.")
    text = show_populated_section(text, "<!-- BLOG-SECTION:START -->", "<!-- BLOG-SECTION:END -->", "<!-- BLOG-POST-LIST:START -->", "<!-- BLOG-POST-LIST:END -->", "## 📝 Latest field notes")
    text = show_populated_section(text, "<!-- WAKA-SECTION:START -->", "<!-- WAKA-SECTION:END -->", "<!--START_SECTION:waka-->", "<!--END_SECTION:waka-->", "## ⏱️ Coding activity · last 7 days")
    stamp = now.strftime("%d %b %Y · %I:%M %p IST")
    return replace_section(text, "<!-- LAST-UPDATED:START -->", "<!-- LAST-UPDATED:END -->", f'<p align="center"><sub>Last updated: {stamp}</sub></p>')


def fetch_joke():
    request = Request(JOKE_URL, headers={"User-Agent": "sanskar111-profile/1.0", "Accept": "application/json"})
    with urlopen(request, timeout=20) as response:
        return json.load(response)


if __name__ == "__main__":
    path = Path(__file__).resolve().parents[1] / "README.md"
    original = path.read_text(encoding="utf-8")
    result = update(original, datetime.now(IST), fetch_joke)
    if result != original:
        path.write_text(result, encoding="utf-8")
    print("Live profile sync complete (IST).")
