# Library Management Software KitabuSoft

## How to build

```bash
pyinstaller --noconsole --onefile --icon="src/assets/icon.ico" --add-data="src/assets;src/assets" --add-data="src/db;src/db" --add-data="src/settings;src/settings" .\start.py
```

## How To contribute

- Fork The projet
- Clone into your local computer

```bash
git clone 'htttps://github.com/nom-utilisateur/nom-du-repo'
cd nom-du-repo
```

- Create a virtual environment

```bash
python -m venv venv
```

- Activate the virtual environment

```bash
venv/Scripts/activate
```

- Install dependancies

```bash
pip install -r requirements.txt
```

- Make your changes
- Commit the changes
- Push the Changes
- Create a pull request
