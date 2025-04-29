# UFW Parser

**UFW Parser** is a tool that remotely or locally fetches and parses UFW firewall rules from Linux servers, presenting them in a clean, tabular, and exportable format.

It supports various output formats such as:
- Console table
- CSV
- Excel
- Ansible-compatible YAML (`host_vars` style)

---

## ✨ Features

- Fetch UFW rules locally or via SSH (with `sudo` privileges)
- Group and consolidate firewall rules per server
- Export rules to:
  - CSV
  - Excel
  - Terminal table
  - Ansible host_vars YAML format (for easy automation)
- Structured logs with file rotation
- Fully modular and extensible design
- CLI-driven usage with debug support

---

## 🚀 Quick Start

### 1. Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/yourusername/ufw_parser.git
cd ufw_parser
pip install -e .
```

> You need Python 3.7+.

---

### 2. Usage

```bash
ufw_parser -c ~/.config/ufw_parser/hosts.yml -o ansible_yaml -of ~/exports/
```

| Option | Description |
|:-------|:------------|
| `-c`, `--config` | Path to hosts configuration file |
| `-o`, `--output` | Output format: `screen`, `csv`, `excel`, or `ansible_yaml` |
| `-of`, `--output_folder` | Destination folder for exports |
| `-l`, `--log` | Log files directory |
| `-d`, `--debug` | Enable debug logging |

---

### 3. Configuration Example

Example `hosts.yml`:

```yaml
servers:
  server1:
    hostname: 192.168.1.10
    processing: local
    rule_path: /etc/ufw
  server2:
    hostname: your.remote.server
    processing: remote
    ssh_user: your_ssh_user
    rule_path: /etc/ufw
    use_ssh_agent: true
```



---

## 📜 License

MIT License. See `LICENSE` for details.

---

## 🤝 Acknowledgments

Project by **qf3l3k** at [ChainTools](https://chaintools.tech).
