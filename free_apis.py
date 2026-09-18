#!/usr/bin/env python3
"""
Free APIs Hub & Query Engine
A curated directory of 1,870+ categorized free public APIs, with built-in
live execution for zero-auth public data (weather, crypto, forex, news, IP, etc.).
"""

import sys
import os
import json
import re
from pathlib import Path
from typing import Optional, Any

import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()
DATA_FILE = Path(__file__).resolve().parent / "apis.json"

# In-memory cached database
_DB = None

def load_database() -> dict:
    global _DB
    if _DB is None:
        if DATA_FILE.exists():
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                _DB = json.load(f)
        else:
            _DB = {}
    return _DB


def get_categories() -> list[tuple[str, int]]:
    """Return all categories with API counts."""
    db = load_database()
    return sorted([(cat, len(apis)) for cat, apis in db.items()], key=lambda x: x[0].lower())


def search_apis(query: str, limit: int = 15, no_auth_only: bool = False) -> list[dict]:
    """Search APIs across name, description, category."""
    db = load_database()
    q = query.lower().strip()
    results = []

    for cat, apis in db.items():
        for item in apis:
            if no_auth_only and item.get("auth", "").lower() not in ("no", "none", ""):
                continue
            name = item.get("name", "").lower()
            desc = item.get("description", "").lower()
            cat_l = cat.lower()

            if q in name or q in desc or q in cat_l:
                res = dict(item)
                res["category"] = cat
                results.append(res)
                if len(results) >= limit:
                    return results

    return results


# ── Live API Callers (Zero-Auth Instant Execution) ───────────────────────────
def call_weather(location: str = "") -> str:
    """Fetch live weather from wttr.in."""
    loc = location.strip().replace(" ", "+") if location else ""
    url = f"https://wttr.in/{loc}?format=3"
    try:
        with httpx.Client(timeout=6.0) as client:
            resp = client.get(url, headers={"User-Agent": "curl/7.68.0"})
            if resp.status_code == 200:
                return resp.text.strip()
    except Exception as e:
        return f"Weather unavailable: {e}"
    return "Weather service did not return data."


def call_crypto(coin: str = "bitcoin") -> str:
    """Fetch live cryptocurrency prices via CoinGecko."""
    c = coin.lower().strip()
    mapping = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "sol": "solana",
        "doge": "dogecoin",
        "xrp": "ripple"
    }
    coin_id = mapping.get(c, c)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd,eur&include_24hr_change=true"
    try:
        with httpx.Client(timeout=6.0) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json().get(coin_id, {})
                usd = data.get("usd")
                change = data.get("usd_24h_change", 0.0)
                if usd is not None:
                    ch_str = f"+{change:.2f}%" if change >= 0 else f"{change:.2f}%"
                    return f"{coin_id.upper()}: ${usd:,.2f} USD (24h: {ch_str})"
    except Exception as e:
        return f"Crypto price error: {e}"
    return f"Unable to fetch price for {coin}."


def call_ip() -> str:
    """Fetch public IP geolocation info via ipapi."""
    try:
        with httpx.Client(timeout=6.0) as client:
            resp = client.get("https://ipapi.co/json/")
            if resp.status_code == 200:
                d = resp.json()
                return f"IP: {d.get('ip')} | Location: {d.get('city')}, {d.get('region')}, {d.get('country_name')} | ISP: {d.get('org')}"
    except Exception as e:
        return f"IP lookup error: {e}"
    return "Unable to determine public IP."


def call_joke() -> str:
    """Fetch a random programmer or general joke."""
    try:
        with httpx.Client(timeout=6.0) as client:
            resp = client.get("https://official-joke-api.appspot.com/random_joke")
            if resp.status_code == 200:
                d = resp.json()
                return f"{d.get('setup')} — {d.get('punchline')}"
    except Exception:
        pass
    return "Why do programmers prefer dark mode? Because light attracts bugs."


def call_quote() -> str:
    """Fetch daily inspirational quote."""
    try:
        with httpx.Client(timeout=6.0) as client:
            resp = client.get("https://zenquotes.io/api/random")
            if resp.status_code == 200:
                d = resp.json()[0]
                return f"\"{d.get('q')}\" — {d.get('a')}"
    except Exception:
        pass
    return "\"Simplicity is prerequisite for reliability.\" — Edsger W. Dijkstra"


def call_forex(from_cur: str = "USD", to_cur: str = "EUR", amount: float = 1.0) -> str:
    """Convert foreign exchange currencies via open.er-api.com."""
    base = from_cur.upper().strip()
    target = to_cur.upper().strip()
    url = f"https://open.er-api.com/v6/latest/{base}"
    try:
        with httpx.Client(timeout=6.0) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                rates = resp.json().get("rates", {})
                if target in rates:
                    rate = rates[target]
                    converted = amount * rate
                    return f"{amount:,.2f} {base} = {converted:,.2f} {target} (Rate: {rate:.4f})"
    except Exception as e:
        return f"Forex error: {e}"
    return f"Unable to convert {base} to {target}."


def call_news(limit: int = 5) -> str:
    """Fetch top headlines from HackerNews."""
    try:
        with httpx.Client(timeout=6.0) as client:
            top_ids = client.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()[:limit]
            headlines = []
            for i, tid in enumerate(top_ids, 1):
                item = client.get(f"https://hacker-news.firebaseio.com/v0/item/{tid}.json").json()
                headlines.append(f"{i}. {item.get('title')} ({item.get('score')} pts)")
            return "\n".join(headlines)
    except Exception as e:
        return f"News error: {e}"


def query_live_api(service: str, *args) -> str:
    """Universal dispatcher for built-in live free API endpoints."""
    s = service.lower().strip()
    if s in ("weather", "wttr"):
        loc = " ".join(args) if args else ""
        return call_weather(loc)
    elif s in ("crypto", "btc", "eth", "coin"):
        coin = args[0] if args else "bitcoin"
        return call_crypto(coin)
    elif s in ("ip", "myip", "geo"):
        return call_ip()
    elif s in ("joke", "jokes"):
        return call_joke()
    elif s in ("quote", "quotes", "inspire"):
        return call_quote()
    elif s in ("forex", "fx", "currency", "exchange"):
        f_cur = args[0] if len(args) > 0 else "USD"
        t_cur = args[1] if len(args) > 1 else "EUR"
        amt = float(args[2]) if len(args) > 2 else 1.0
        return call_forex(f_cur, t_cur, amt)
    elif s in ("news", "hn", "headlines"):
        return call_news()
    else:
        return f"Unknown live service '{service}'. Available: weather, crypto, ip, joke, quote, forex, news."


# ── Interactive CLI ──────────────────────────────────────────────────────────
def cli_main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        console.print(Panel(
            "[bold white]✦ FREE PUBLIC APIS DIRECTORY & LIVE CLIENT[/]\n"
            "[dim]A curated index of 1,870+ public APIs with built-in zero-auth callers.[/]\n\n"
            "[bold cyan]free-apis search <query>[/]       - Search APIs by keyword\n"
            "[bold cyan]free-apis categories[/]           - List all 52 API categories\n"
            "[bold cyan]free-apis list <category>[/]      - List APIs in a specific category\n"
            "[bold cyan]free-apis call weather [city][/]  - Real-time weather via wttr.in\n"
            "[bold cyan]free-apis call crypto [coin][/]   - Live cryptocurrency prices (CoinGecko)\n"
            "[bold cyan]free-apis call ip[/]              - Public IP geolocation details\n"
            "[bold cyan]free-apis call forex USD EUR[/]   - Live currency exchange rates\n"
            "[bold cyan]free-apis call news[/]            - Top HackerNews tech headlines\n"
            "[bold cyan]free-apis call joke | quote[/]    - Instant jokes or quotes",
            title="FREE APIS CLI",
            border_style="cyan"
        ))
        return

    cmd = args[0].lower()

    if cmd == "categories":
        cats = get_categories()
        table = Table(title="✦ FREE PUBLIC API CATEGORIES (52)", border_style="cyan")
        table.add_column("Category", style="bold white")
        table.add_column("APIs Count", justify="right", style="cyan")
        for cat, cnt in cats:
            table.add_row(cat, str(cnt))
        console.print(table)
        return

    if cmd in ("search", "find", "s"):
        if len(args) < 2:
            console.print("[yellow]Usage: free-apis search <keyword>[/]")
            return
        q = " ".join(args[1:])
        results = search_apis(q, limit=15)
        if not results:
            console.print(f"[dim]No APIs found matching '{q}'.[/]")
            return

        table = Table(title=f"✦ Results for '{q}' ({len(results)} found)", border_style="cyan")
        table.add_column("Name", style="bold white")
        table.add_column("Category", style="cyan")
        table.add_column("Description", style="dim")
        table.add_column("Auth", style="green")
        table.add_column("URL", style="blue")

        for r in results:
            table.add_row(r['name'], r['category'], r['description'][:45] + "...", r['auth'], r['url'][:35])
        console.print(table)
        return

    if cmd in ("list", "ls"):
        if len(args) < 2:
            console.print("[yellow]Usage: free-apis list <category>[/]")
            return
        cat_query = " ".join(args[1:]).lower()
        db = load_database()
        matched_cat = next((c for c in db if c.lower() == cat_query or cat_query in c.lower()), None)
        if not matched_cat:
            console.print(f"[red]Category '{cat_query}' not found. Run 'free-apis categories'.[/]")
            return

        apis = db[matched_cat]
        table = Table(title=f"✦ Category: {matched_cat} ({len(apis)} APIs)", border_style="cyan")
        table.add_column("Name", style="bold white")
        table.add_column("Description", style="dim")
        table.add_column("Auth", style="green")
        table.add_column("HTTPS", justify="center")
        table.add_column("URL", style="blue")

        for a in apis:
            table.add_row(a['name'], a['description'][:50], a['auth'], "✓" if a['https'] else "✗", a['url'])
        console.print(table)
        return

    if cmd in ("call", "run", "get"):
        if len(args) < 2:
            console.print("[yellow]Usage: free-apis call <service> [args...][/]")
            return
        service = args[1]
        extra_args = args[2:]
        res = query_live_api(service, *extra_args)
        console.print(Panel(res, title=f"LIVE API: {service.upper()}", border_style="bold cyan"))
        return

    # Default fallback: search
    results = search_apis(" ".join(args), limit=10)
    if results:
        table = Table(title=f"✦ APIs matching '{args[0]}'", border_style="cyan")
        table.add_column("Name", style="bold white")
        table.add_column("Category", style="cyan")
        table.add_column("Description", style="dim")
        table.add_column("URL", style="blue")
        for r in results:
            table.add_row(r['name'], r['category'], r['description'][:45] + "...", r['url'][:35])
        console.print(table)
    else:
        console.print(f"[yellow]Unknown command '{args[0]}'. Run 'free-apis --help'.[/]")


if __name__ == "__main__":
    cli_main()
