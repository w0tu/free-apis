# 🌐 Free Public APIs — Curated Directory & Live Client

A comprehensive, curated repository and Python toolkit indexing **1,870+ free public APIs** across 52 categories, complete with an interactive terminal client and zero-auth live execution for real-time data (weather, cryptocurrency, forex, public IP, tech news, jokes, and quotes).

---

## ⚡ Quick Start

```bash
# Search across 1,870+ APIs
free-apis search weather
free-apis search ai
free-apis search crypto

# Explore categories
free-apis categories
free-apis list Environment

# Live zero-auth instant queries
free-apis call weather "San Francisco"
free-apis call crypto btc
free-apis call forex USD EUR
free-apis call ip
free-apis call news
free-apis call joke
```

---

## 📚 Categories Indexed (52)

- **Animals** (Cats, Dogs, Birds, Wildlife)
- **Anime & Manga** (Jikan, AniList, Studio Ghibli)
- **Artificial Intelligence & ML** (Hugging Face, Open-source LLMs)
- **Blockchain & Cryptocurrency** (CoinGecko, CoinCap, Etherscan)
- **Books & Literature** (Open Library, Gutenberg)
- **Cloud Storage & File Sharing**
- **Currency Exchange & Finance** (Forex, Rates, Stocks)
- **Development & DevOps** (GitHub, GitLab, Docker Hub, Package Registries)
- **Dictionaries & Linguistics** (Definitions, Synonyms, Rhymes)
- **Entertainment & Gaming** (IGDB, Steam, Trivia, Chess)
- **Environment & Weather** (Open-Meteo, wttr.in, NOAA, AQI)
- **Geocoding & Maps** (OpenStreetMap, Nominatim, IP Geolocation)
- **Government & Open Data** (US, EU, World Bank, UN)
- **Health & Science** (COVID, Nutrition, Medical, Astronomy)
- **Jobs & Career** (Remote jobs, Job boards, GitHub Jobs)
- **News & Media** (HackerNews, Reddit, RSS)
- **Security & Authentication** (HaveIBeenPwned, Shodan, VirusTotal)
- **Transportation & Flights** (FlightAware, OpenSky, Transit)
- *...and 34 more categories.*

---

## 🛠️ Python SDK Usage

```python
from free_apis import search_apis, query_live_api, get_categories

# Search APIs programmatically
weather_apis = search_apis("weather", limit=5)
for api in weather_apis:
    print(f"{api['name']} ({api['auth']}): {api['url']}")

# Query real-time zero-auth endpoints
print(query_live_api("weather", "Tokyo"))
print(query_live_api("crypto", "ethereum"))
print(query_live_api("forex", "USD", "JPY", 100))
```

---

## 📄 License & Attribution

- Built from the collective open-source work of the community and `public-apis/public-apis`.
- Released under the [MIT License](LICENSE).
