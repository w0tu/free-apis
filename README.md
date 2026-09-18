# 🌐 Free Public APIs — Curated Directory & Live Client

<div align="center">

![License](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)
![APIs](https://img.shields.io/badge/Indexed%20APIs-1%2C870%2B-brightgreen.svg?style=for-the-badge)
![Categories](https://img.shields.io/badge/Categories-52-orange.svg?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![Zero Auth](https://img.shields.io/badge/Auth-Zero--Config%20Live%20Queries-purple.svg?style=for-the-badge)

**A comprehensive, curated repository and Python toolkit indexing 1,870+ free public APIs across 52 categories, featuring an interactive terminal client and instant live zero-auth callers.**

</div>

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
free-apis call weather "London"
free-apis call crypto btc
free-apis call forex USD EUR
free-apis call ip
free-apis call news
free-apis call joke
free-apis call quote
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
    print(f"{api['API']} — {api['Description']} ({api['Link']})")

# Instant live execution without API keys
temp = query_live_api("weather", "Tokyo")
btc_price = query_live_api("crypto", "bitcoin")
joke = query_live_api("joke")
```

---

## 📜 License

MIT License. Maintained by [w0tu](https://github.com/w0tu).
Contributions and new API submissions are welcome!
