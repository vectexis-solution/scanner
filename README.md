<div align="center">

# 🔍 Vectexis Scanner

**A lightweight command-line toolkit for network port scanning and web page crawling.**

*Powered by [Vectexis Solution](https://linkedin.com/company/vectexis-solution)*

![Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white)
![Nmap](https://img.shields.io/badge/requires-nmap-green)
![Interface](https://img.shields.io/badge/interface-CLI-lightgrey)
![Status](https://img.shields.io/badge/status-active-brightgreen)

[LinkedIn](https://linkedin.com/company/vectexis-solution) · [GitHub](https://github.com/vectexis-solution)

</div>

---

## 📖 Overview

Vectexis Scanner is a Python CLI tool that bundles two reconnaissance utilities behind a clean, colorized terminal interface built with [Rich](https://github.com/Textualize/rich):

- **Scan**: a wrapper around [Nmap](https://nmap.org) for port, service, and OS detection.
- **Crawl**: a quick web page crawler that extracts the page title and every link found on the page.

Both modes can save their results to a report file for later review.

## ✨ Features

- 🎨 Polished terminal output with a branded banner, colors, and panels (via Rich)
- 🔌 Nmap integration with configurable target and port selection
- ⚡ Two scan profiles: **aggressive** (`-A`) by default, or **fast** (`-F`) with a flag
- 🌐 Web crawler that reports the page title, content size, and link count
- 💾 Optional report export, with parent directories created automatically
- 🛡️ Graceful error handling: missing Nmap, scan timeouts (600s), and network errors
- 🧾 Reports include target, ports, timestamp, and the exact command executed

## 📋 Requirements

| Requirement | Purpose |
|---|---|
| Python 3.8+ | Runtime |
| [Nmap](https://nmap.org/download.html) | Required for the `scan` command (must be on your `PATH`) |
| `requests` | HTTP requests for the crawler |
| `beautifulsoup4` | HTML parsing |
| `rich` | Terminal UI |

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/vectexis-solution/vectexis-scanner.git
cd vectexis-scanner

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install requests beautifulsoup4 rich

# 4. Install Nmap
sudo apt install nmap           # Debian/Ubuntu
sudo pacman -S nmap             # Arch
brew install nmap               # macOS
# Windows: https://nmap.org/download.html
```

Verify Nmap is available:

```bash
nmap --version
```

## 🛠️ Usage

```bash
python vectexis_scanner.py <command> [options]
```

### `scan`: Port scanning with Nmap

```bash
python vectexis_scanner.py scan -t <target> [-p <ports>] [-o <file>] [--fast]
```

| Option | Description | Default |
|---|---|---|
| `-t`, `--target` | Target IP address or hostname **(required)** | – |
| `-p`, `--port` | Port(s) to scan, e.g. `80`, `22,80,443`, `1-1000` | `1-1000` |
| `-o`, `--output` | Save results to a file, e.g. `report.txt` | – |
| `--fast` | Use fast scan (`-F`) instead of aggressive scan (`-A`) | off |

**Examples**

```bash
# Aggressive scan of port 80, saved to a report
python vectexis_scanner.py scan -t 44.238.29.244 -p 80 -o test_results.txt

# Fast scan of the default port range
python vectexis_scanner.py scan -t scanme.nmap.org --fast

# Scan multiple specific ports
python vectexis_scanner.py scan -t 192.168.1.10 -p 22,80,443
```

Under the hood, the tool runs `nmap -v -A -p <ports> <target>` (or `-F` with `--fast`) and prints the exact command before executing it.

### `crawl`: Web page crawler

```bash
python vectexis_scanner.py crawl <url> [-o <file>]
```

| Option | Description |
|---|---|
| `url` | URL of the page to crawl **(required)** |
| `-o`, `--output` | Save the title and full link list to a file |

**Example**

```bash
python vectexis_scanner.py crawl http://testaspnet.vulnweb.com/ -o test_results.txt
```

The crawler fetches the page, prints its title, content length, and the number of links found, and displays the first 50 links in the terminal. When `-o` is used, **all** links are written to the report.

## 📸 Example Output

### Scan

```text
$ python vectexis_scanner.py scan -t 44.238.29.244 -p 80 -o test_results.txt

[*] Scanning... 44.238.29.244 on port(s) 80
$ nmap -v -A -p 80 44.238.29.244
Starting Nmap 7.991 ( https://nmap.org ) at 2026-10-02 14:30 +0500
...
Discovered open port 80/tcp on 44.238.29.244
```

### Crawl

```text
$ python vectexis_scanner.py crawl http://testaspnet.vulnweb.com/ -o test_results.txt

[*] Crawling... http://testaspnet.vulnweb.com/
[+] Title: acublog news
[+] Fetched 14044 chars, Found 60 links
 - https://www.acunetix.com/
 - about.aspx
 - login.aspx
 ...
```

## 📄 Report Format

**Scan report**

```text
--- Vectexis Scanner ---
Target: 44.238.29.244
Ports: 80
Date: 2026-10-02 14:30:00.000000
Command: nmap -v -A -p 80 44.238.29.244

<nmap output>
```

**Crawl report**

```text
--- Vectexis Crawler ---
URL: http://testaspnet.vulnweb.com/
Date: 2026-10-02 15:00:00.000000
Title: acublog news

Links:
https://www.acunetix.com/
about.aspx
...
```

## 📁 Project Structure

```text
vectexis-scanner/
├── vectexis_scanner.py   # Main CLI application
└── README.md
```

## ⚠️ Legal Disclaimer

> **Use this tool only on systems you own or have explicit, written permission to test.**

Port scanning and crawling without authorization may be illegal in your jurisdiction and may violate the terms of service of the target. Vectexis Solution and the contributors accept **no liability** for misuse or damage caused by this tool. You are solely responsible for your actions.

The examples above use targets intended for security testing (such as Acunetix's deliberately vulnerable test site, `testaspnet.vulnweb.com`).

## 🗺️ Roadmap

- [ ] Configurable scan timeout
- [ ] JSON / HTML report formats
- [ ] Recursive crawling with depth control
- [ ] Absolute URL resolution for relative links
- [ ] Multi-target scanning from a file

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## 📬 Contact

**Vectexis Solution**

- LinkedIn: [linkedin.com/company/vectexis-solution](https://linkedin.com/company/vectexis-solution)
- GitHub: [github.com/vectexis-solution](https://github.com/vectexis-solution)

---

<div align="center">

Made with ❤️ by **Vectexis Solution**

</div>
