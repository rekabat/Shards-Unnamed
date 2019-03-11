# Running on Linux
If the system doesn't already have Python 3, install using the command

```
sudo apt install python3
sudo apt install python3-venv
sudo apt install python3-pip
```

Set up the virtual environment

```
python3 -m venv env
source env/bin/activate
```

Then install requirements

```
pip install -r requirements.txt
```