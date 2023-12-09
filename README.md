# graph-grammars
Project for graph grammar classes on AGH UST 2023

# Installation instructions

## Native dependencies

Some of the libs used (`networkx`, `graphviz`, `pygraphviz`) require some native dependencies to be present in system.

Please follow installation instruction of these libs:

1. https://networkx.org/documentation/stable/install.html
2. https://graphviz.org/download/

I recommend using your system-wide package manager (apt / brew / yum depending on OS).

In my case on Linux Mint 21.1 (Debian -> Ubuntu distro) I had to run following cmds:

```bash
sudo apt install graphviz graphviz-dev
```

It is possible, with some effort, to install these native deps in local specific environment, please refer to official docs & your OS knowledge.


## Installing python deps

Setup virtual env (I'm using specific interpreter here, you can try other versions (3.12 is not working), however I did not track what is the minimum python version required):

```bash
python3.11 -m virtualenv .venv
source ./.venv/bin/activate
```

Install deps:

```bash
pip install -r requirements.txt
```

## Docs about P1, P2
https://docs.google.com/document/d/1aBiGuepeNUuPSGl8aK_Ilit3hJedHvKwng_xBeh43OY/edit

## Running

```bash
In order to run and see hardcoded tests please run:
cd src; make test
```
