# DuckDB Installation Options

If you find yourself migrating environments, setting up a new machine, or moving to a production environment (Linux/Windows), refer to these standard installation commands. DuckDB has zero external dependencies, so it installs extremely quickly.

---

## 🐍 1. Python Environment (Universal)

If you are only interacting with DuckDB entirely within Python (e.g., in a Dagster, dbt, or Jupyter environment), installing via `pip` is usually sufficient:

```bash
# Basic installation (most common)
pip install duckdb

# If you need to install it with all optional dependencies (like for cloud storage extensions)
pip install "duckdb[all]"
```

If you use Conda:
```bash
conda install python-duckdb -c conda-forge
```

---

## 💻 2. DuckDB CLI (Standalone Terminal Tool)

If you want the standalone interactive command-line interface (CLI) to quickly query data without writing a Python script:

### **macOS**
The easiest approach is using Homebrew or the official install script.
```bash
# Using Homebrew (Recommended if you already use it)
brew install duckdb

# Alternative (Official Install Script)
curl https://install.duckdb.org | sh
```

### **Linux**
```bash
# Official Download/Install Script
curl https://install.duckdb.org | sh
```

### **Windows**
If you move to a Windows machine, you can use the Windows Package Manager (`winget`) or download the zip file directly.
```powershell
# Using Winget
winget install DuckDB.cli
```
*Note: Make sure the Microsoft Visual C++ Redistributable is installed on your Windows machine, as DuckDB relies on it.*

---

## ☁️ 3. Node.js Environment (Optional)
If you ever want to build a frontend or use DuckDB in a JavaScript environment:
```bash
npm install duckdb
```

## Adding Extentions
After opening the DuckDB CLI (`duckdb`) or setting up the connection in Python, you can easily install and load powerful extensions (like AWS, Postgres, or HTTP connections):
```sql
-- e.g., to query remote S3 files directly
INSTALL httpfs;
LOAD httpfs;

-- e.g., to attach a PostgreSQL database directly to DuckDB
INSTALL postgres;
LOAD postgres;
```
