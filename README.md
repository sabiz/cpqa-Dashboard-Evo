# cpqa-Dashboard

Dashboard app for [CP9A](https://en.wikipedia.org/wiki/Mitsubishi_Lancer_Evolution).
(9 is pronounced like "q" in Japanese)

Displays car information using the MUT protocol via the OBD (OnBoard Diagnostic) connector.  
For Mitsubishi cars 1990s to 2000s.  

This app is inspired by "[Evoscan](https://evoscan.com/)".

## :sparkles:Features

- Display MUT values.

## :egg:Requirements

- [Tactrix](https://www.tactrix.com/) Openport 1.3 cable or compatible cable
- [FTDI Driver](https://www.ftdichip.com/FTDrivers.htm)
- Python 3.9 or later
- [uv](https://github.com/astral-sh/uv) (fast Python package manager)

git clone https://github.com/sabiz/cpqa-dashboard.git cpqa

cd cpqa

## :hatching_chick:Installation

```sh
git clone https://github.com/sabiz/cpqa-dashboard-evo.git
cd cpqa-dashboard-evo
uv sync
```


## :hatched_chick:Getting Started

1. Connect the Openport 1.3 cable to your Mitsubishi car.
2. Activate the virtual environment (on Windows: `./.venv/Scripts/activate`).
3. Start the dashboard:
   ```sh
   uv sync
   uv run -m cpqa
   ```
4. Follow the on-screen instructions.
## :wrench: Build (Native Extension)

On Windows, FTDI driver and Visual Studio Build Tools are required.
The native extension is usually built automatically with `uv pip install .`.

## :test_tube: Test

```sh
uv sync
pytest
```


## :chicken:FAQ

**Q. What is uv?**
A. [uv](https://github.com/astral-sh/uv) is a fast Python package manager. It can be used as a replacement for `pip` and `venv`.

## License

[MIT License](LICENSE) © [sAbIz](https://github.com/sabiz) :jp: