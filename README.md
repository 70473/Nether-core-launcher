<div align="center">

```
███╗   ██╗███████╗████████╗██╗  ██╗███████╗██████╗      ██████╗ ██████╗ ██████╗ ███████╗
████╗  ██║██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗    ██╔════╝██╔═══██╗██╔══██╗██╔════╝
██╔██╗ ██║█████╗     ██║   ███████║█████╗  ██████╔╝    ██║     ██║   ██║██████╔╝█████╗  
██║╚██╗██║██╔══╝     ██║   ██╔══██║██╔══╝  ██╔══██╗    ██║     ██║   ██║██╔══██╗██╔══╝  
██║ ╚████║███████╗   ██║   ██║  ██║███████╗██║  ██║    ╚██████╗╚██████╔╝██║  ██║███████╗
╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
```

**Ultra-premium Minecraft Instance Lifecycle Manager & Automation Dashboard**

*Anarchy Cyberpunk · PyQt5 · Bazzite / Fedora Silverblue*

---

![Python](https://img.shields.io/badge/Python-3.10%2B-8A2BE2?style=flat-square&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15%2B-00FFFF?style=flat-square&logo=qt&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Bazzite%20%7C%20Fedora%20Silverblue-39FF14?style=flat-square&logo=linux&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-FF3131?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active%20Development-FFD700?style=flat-square)

</div>

---

## What is Nether Core?

Nether Core is a fully isolated, high-performance Minecraft Instance Lifecycle Manager built for **immutable Linux environments** — specifically optimised for [Bazzite](https://bazzite.gg/) and Fedora Silverblue. It rivals tools like Prism Launcher while adding custom AI bot orchestration, a live coloured telemetry terminal, and a cyberpunk-grade desktop UI built entirely in PyQt5.

Everything runs in user-space. No root. No system modifications. Fully compatible with the immutable filesystem model.

---

## Features

### ⬡ Instance Matrix & Modpack Hub
- Visual card grid showing all sandboxed Minecraft installations
- Per-card display of version, mod loader (Fabric / Forge / NeoForge / Quilt), and last launch timestamp
- One-click modpack ingestion from **Modrinth**, **CurseForge**, **FTB**, and **Technic** manifest formats
- Instance cloning and ZIP export for sharing configurations

### ◈ Add-on Repository & Dependency Solver
- Multi-source search across Modrinth and CurseForge for Mods, Resource Packs, Shaders, and Data Packs
- Visual dependency auto-resolver that detects and queues missing prerequisites automatically

### ◉ Identity Control Center
- Hot-swap between multiple **Microsoft OAuth** accounts and local **offline personas**
- Active player skin preview with ASCII render and cape display
- Upload custom skin PNGs directly from the launcher

### ◫ System Tuning & Runtime Management
- Per-instance and global **JVM heap sliders** (`-Xmx` / `-Xms`) with live MB readout
- Java runtime detection matrix showing all installed JVM environments
- Auto-download pipeline for **OpenJDK 8, 17, and 21** into user-space (`~/.local/share/nethercore/`)
- Custom display resolution overrides and JVM optimisation flag input

### ◬ Engine Telemetry & Lifecycle Controls
- Live **colour-coded terminal** streaming real-time game process output
  - `INFO` → Cyber Cyan · `WARN` → Gold · `ERROR` → Neon Crimson
- One-click crash log export to **[mclo.gs](https://mclo.gs)**
- Emergency **KILL PROCESS** button wired to `subprocess.kill()` — stops frozen instances instantly without touching the parent app

### ◐ AI Bot Automation Deck
- Simulation dashboard for background bot automation runners
- **Initialize / Halt** toggle pipeline for execution state control
- Natural language directive input — submit tasks directly to the bot controller thread
- Visual **arc token gauge** with colour-threshold alerts for API consumption tracking

---

## Screenshots

> *UI renders in the Anarchy Cyberpunk theme — high-contrast dark luxury on a `#0A0A0C` canvas with Electric Neon Violet (`#8A2BE2`) accents.*

```
┌─────────────────────────────────────────────────────────────────┐
│  ⚡ NETHER CORE          │  ⬡  Instance Matrix                  │
│  Instance Manager v2.0   │                                       │
│  ─────────────────────   │  ┌──────────┐  ┌──────────┐          │
│  ⬡  Instance Matrix  ◀  │  │ ⬡ Survi- │  │ ◈ Create │          │
│  ◈  Add-on Repo          │  │ val Hard │  │ Automat- │          │
│  ◉  Identity Center      │  │ 1.21.1   │  │ 1.20.1   │          │
│  ◫  System Tuning        │  │ Fabric   │  │ Forge    │          │
│  ◬  Engine Telemetry     │  │ ▶  ⎘  ✕  │  │ ▶  ⎘  ✕  │          │
│  ◐  AI Bot Deck          │  └──────────┘  └──────────┘          │
│                           │                                       │
│  ◉ IDLE                  │  Modpack Ingest: [Modrinth ▾] [____]  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Requirements

| Dependency | Version | Notes |
|---|---|---|
| Python | 3.10+ | 3.11 / 3.12 recommended |
| PyQt5 | 5.15+ | Core UI framework |
| pip | Any | For installing PyQt5 |

No other third-party Python packages are required. All other dependencies (`subprocess`, `uuid`, `datetime`, etc.) are from the Python standard library.

---

## Installation

### Bazzite / Fedora Silverblue (Immutable OS)

The system root on Bazzite is read-only, so you have two clean options:

#### Option A — Toolbox (Recommended for development)

```bash
# Create a dedicated toolbox container
toolbox create nethercore

# Enter the container
toolbox enter nethercore

# Install Python and PyQt5 inside the container
sudo dnf install python3 python3-pyqt5 python3-pip git -y

# Clone the repo
git clone https://github.com/YOUR_USERNAME/nether-core.git
cd nether-core

# Launch
python3 ui/window.py
```

> Toolbox containers have full read-write access and share your home directory, so your instance data in `~/.local/share/nethercore/` persists across sessions.

#### Option B — User Virtual Environment (No root, no container)

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/nether-core.git
cd nether-core

# Create a venv in your home directory
python3 -m venv ~/.local/venvs/nethercore

# Activate it
source ~/.local/venvs/nethercore/bin/activate

# Install PyQt5
pip install PyQt5

# Launch
python3 ui/window.py
```

> Add `source ~/.local/venvs/nethercore/bin/activate` to a launcher script so you don't need to activate manually each time.

---

### Standard Linux (Ubuntu / Arch / Manjaro / Pop!_OS)

```bash
# Ubuntu / Debian
sudo apt install python3 python3-pyqt5 git

# Arch / Manjaro
sudo pacman -S python python-pyqt5 git

# Or universally via pip + venv
python3 -m venv venv
source venv/bin/activate
pip install PyQt5

git clone https://github.com/YOUR_USERNAME/nether-core.git
cd nether-core
python3 ui/window.py
```

---

### Windows (WSL2 or Native)

```powershell
# Native Windows — install Python from python.org first, then:
pip install PyQt5
git clone https://github.com/YOUR_USERNAME/nether-core.git
cd nether-core
python ui/window.py
```

> On WSL2 you'll need an X server (e.g. VcXsrv or WSLg on Windows 11) for the GUI to display.

---

## Project Structure

```
nether-core/
│
├── ui/
│   └── window.py          # ← Full application — all panels, workers, and theme
│
├── README.md
└── LICENSE
```

The entire UI lives in `ui/window.py`. It is intentionally self-contained so it can be dropped into any existing backend project as a single file. When you build out your service layer, connect it by importing into `window.py` and wiring calls to the worker threads and panels already defined.

---

## Architecture Overview

```
MainWindow
├── SidebarWidget          — Nav command deck (6 NavButton pills)
└── QStackedWidget
    ├── InstanceMatrixPanel
    │   ├── InstanceCard × N    — Per-instance cards (launch / clone / delete)
    │   └── Modpack ingest bar
    ├── AddonRepositoryPanel
    │   ├── Multi-source search
    │   └── Dependency resolver strip
    ├── IdentityCenterPanel
    │   ├── Account QListWidget
    │   └── Skin preview pane
    ├── SystemTuningPanel
    │   ├── RAM sliders (Xmx / Xms)
    │   ├── Java runtime list
    │   └── Resolution + JVM flags
    ├── TelemetryPanel
    │   ├── QTextEdit terminal (colour-coded)
    │   └── ProcessMonitorWorker (QThread)
    └── AiBotPanel
        ├── Bot status card
        ├── Directive input
        └── Arc token gauge (QPainter)

Workers (QThread)
├── DownloadWorker         — Generic async task runner (API calls, downloads)
└── ProcessMonitorWorker   — Live stdout/stderr stream from game process
```

All long-running operations are dispatched to `QThread` workers and communicate back to the UI via `pyqtSignal` — the main thread never blocks.

---

## Connecting Your Backend

The UI is built to be wired into your existing service layer. Here are the key integration points:

**Launching a real Minecraft process:**
```python
# In MainWindow._handle_instance_launch(), replace the simulation block with:
proc = subprocess.Popen(
    [java_path, *jvm_args, "net.minecraft.client.main.Main"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    cwd=instance_dir,
)
self._panel_telemetry.attach_process(proc, instance_name)
```

**Injecting log lines from any subsystem:**
```python
# Call from anywhere — it's thread-safe via the Qt signal queue
self._panel_telemetry.append_log("Fabric loader initialised.", "info")
self._panel_telemetry.append_log("Missing mod: sodium", "warn")
self._panel_telemetry.append_log("JVM crashed: OutOfMemoryError", "error")
```

**Wrapping an API download in the worker:**
```python
def my_modrinth_fetch(worker, slug):
    # worker.progress_signal.emit(pct) to update UI
    # worker.log_signal.emit(msg, level) for terminal output
    response = requests.get(f"https://api.modrinth.com/v2/project/{slug}")
    ...

task = DownloadWorker(my_modrinth_fetch, slug="sodium")
task.finished_signal.connect(lambda ok, msg: print(ok, msg))
task.start()
```

---

## Data Storage

All application data is written to user-space only — no system paths are ever touched:

| Data | Path |
|---|---|
| Instance configurations | `~/.local/share/nethercore/instances/` |
| Managed JDK runtimes | `~/.local/share/nethercore/jdks/` |
| Downloaded mods / assets | `~/.local/share/nethercore/assets/` |
| Account session cache | `~/.local/share/nethercore/accounts/` |

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Enter` in mod search | Trigger search |
| `Enter` in bot directive | Send directive to bot |
| `Enter` in new instance dialog | Confirm creation |

Full keybinding customisation is on the roadmap.

---

## Roadmap

- [ ] Live Modrinth / CurseForge API integration (replace search mocks)
- [ ] Real Microsoft OAuth2 / Xbox Live authentication flow
- [ ] Actual JVM process spawning with full argument chain builder
- [ ] mclo.gs HTTP POST integration for crash log export
- [ ] Instance data persistence (JSON → `~/.local/share/nethercore/`)
- [ ] Per-instance configuration overrides (RAM, Java, flags)
- [ ] Mod update checker with delta notifications
- [ ] Flatpak packaging for one-click Bazzite install
- [ ] Dark/light theme toggle

---

## Contributing

Pull requests are welcome. For major changes please open an issue first to discuss what you'd like to change.

```bash
# Fork the repo, then:
git clone https://github.com/YOUR_USERNAME/nether-core.git
cd nether-core
git checkout -b feature/your-feature-name
# make changes
git commit -m "feat: describe your change"
git push origin feature/your-feature-name
# open a PR
```

Please keep new UI code inside `ui/window.py` and follow the existing OOP patterns — one class per panel, signals for all cross-panel communication, worker threads for all I/O.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">

*Built with PyQt5 · Designed for Bazzite Linux · Anarchy Cyberpunk theme*

`#0A0A0C` `#8A2BE2` `#00FFFF` `#39FF14` `#FF3131`

</div>
