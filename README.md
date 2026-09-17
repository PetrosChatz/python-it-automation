# Python IT Automation Toolkit

Practical Python utilities for common IT support and system administration tasks. The project focuses on small, understandable scripts that automate routine checks and file-management work.

## Utilities

### `system_info.py`
Displays hostname, operating system, CPU information and memory usage.

```bash
python system_info.py
python system_info.py --json
```

### `network_check.py`
Checks DNS resolution, TCP connectivity to a selected port and basic reachability.

```bash
python network_check.py
python network_check.py example.com --port 443
```

The results are reported separately because different connectivity checks can succeed or fail independently.

### `disk_monitor.py`
Shows total, used and free disk space and compares usage against a configurable threshold.

```bash
python disk_monitor.py
python disk_monitor.py --threshold 90
```

### `file_organizer.py`
Groups files by type into categories such as Images, Documents, Archives, Audio, Video, Code and Other.

It runs as a dry run by default:

```bash
python file_organizer.py ~/Downloads
```

Use `--apply` only when you want to perform the planned file moves:

```bash
python file_organizer.py ~/Downloads --apply
```

The script avoids overwriting existing files by generating a unique destination name when needed.

## Project structure

```text
python-it-automation/
├── system_info.py
├── network_check.py
├── disk_monitor.py
├── file_organizer.py
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10+
- `psutil`

Install the dependency with:

```bash
python -m pip install -r requirements.txt
```

## Skills demonstrated

- Python scripting
- Command-line interfaces with `argparse`
- System information collection
- Basic connectivity checks
- Disk monitoring
- Filesystem operations
- Dry-run design for safer automation
- Error handling
- Cross-platform considerations
- Dependency management
- Git and GitHub

## Next improvements

- Unit tests and GitHub Actions CI
- JSON/CSV health reports
- Multiple-host checks
- Python logging
- Combined system health check

## Author

**Petros Chatzistefanou**  
BSc Applied Informatics — Information Systems, University of Macedonia  
[LinkedIn](https://www.linkedin.com/in/petros-chatzistefanou/)
