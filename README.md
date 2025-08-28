# 🔍 PathFinder

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Zeeshan01001/pathfinder) [![Status](https://img.shields.io/badge/status-stable-green.svg)](https://github.com/Zeeshan01001/pathfinder) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A lightning-fast web reconnaissance tool that finds hidden directories and subdomains in seconds.

[Features](#-features) • [Requirements](#-requirements) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Examples](#-examples) • [Options](#%EF%B8%8F-options) • [Troubleshooting](#-troubleshooting)

## ⭐ Features

✨ **Super Simple**: Just one command - `pathfinder example.com`  
⚡ **Lightning Fast**: Multi-threaded scanning engine  
🔍 **Smart Detection**: Finds hidden paths and subdomains  
🎯 **Zero Config**: Works out of the box with 150+ common paths  
🎨 **Beautiful UI**: Clean, colorful progress bars with real-time results  
📊 **Multiple Formats**: Export results as TXT, JSON, or CSV  
🔄 **Progress Tracking**: Real-time scan progress and status updates

## 🛠️ Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

Required Python packages (automatically installed):
- aiohttp>=3.8.0 - For async HTTP requests
- rich>=12.0.0 - For beautiful terminal output
- requests>=2.28.0 - For HTTP requests
- dnspython>=2.2.0 - For DNS operations

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Zeeshan01001/pathfinder.git

# Change to project directory
cd pathfinder

# Install dependencies and the tool
pip install --user -e .

# Add ~/.local/bin to PATH (if not already added)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

After installation, PathFinder will be available globally as the `pathfinder` command.

Note: If you get a permission error during installation, try using:
```bash
pip install --user -e .
```

## 🚀 Quick Start

```bash
# Basic scan
pathfinder example.com

# Simple output mode (less verbose)
pathfinder example.com --simple

# Find subdomains
pathfinder -s example.com

# Save results
pathfinder example.com -o results.txt
```

## 💡 Examples

```bash
# Custom wordlist
pathfinder example.com -w wordlist.txt

# Scan specific extensions
pathfinder example.com --types php,html,js

# Thorough scan with more threads
pathfinder example.com --thorough --threads 30

# Export as JSON
pathfinder example.com --format json -o results.json

# Skip SSL verification
pathfinder example.com --no-ssl
```

## ⚙️ Options

| Option | Description |
|--------|-------------|
| `-s, --subdomains` | Search for subdomains |
| `-w, --wordlist` | Custom wordlist file |
| `-o, --out` | Save results to file |
| `--thorough` | Enable thorough scanning |
| `--types` | File extensions to check |
| `--threads` | Number of threads (default: 20) |
| `--timeout` | Request timeout in seconds |
| `--no-ssl` | Skip SSL verification |
| `--format` | Output format (txt/json/csv) |
| `--simple` | Simple output mode |

## 📝 Built-in Wordlists

PathFinder comes with 150+ common paths organized into categories:

- 🔑 Admin Panels & Dashboards
- 🔒 Authentication Endpoints
- 📁 Common Directories
- 🛠️ Development & Debug
- 🔌 CMS & Framework Paths
- 🌐 API & Service Endpoints
- 💾 Backup & Config Files
- 🛍️ E-commerce Paths
- 👥 User Content Areas
- 🔧 Utility Endpoints

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

[MIT License](LICENSE) © 2024 [Zeeshan01001](https://github.com/Zeeshan01001)

## ❓ Troubleshooting

1. **Command not found after installation**
   ```bash
   # Add this to your ~/.bashrc or ~/.zshrc
   export PATH="$HOME/.local/bin:$PATH"
   ```
   Then restart your terminal or run: `source ~/.bashrc`

2. **Permission error during installation**
   ```bash
   # Use the --user flag
   pip install --user -e .
   ```

3. **SSL Certificate Verification Failed**
   ```bash
   # Skip SSL verification
   pathfinder example.com --no-ssl
   ```

4. **Scan taking too long**
   ```bash
   # Use simple mode and increase threads
   pathfinder example.com --simple --threads 30
   ```

---

<div align="center">
Made with ❤️ by <a href="https://github.com/Zeeshan01001">Zeeshan01001</a>
</div> 