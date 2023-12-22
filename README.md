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


## Adding new productions

1. Each production should live in separate module: `src/production/production_<production_number>.py`.
2. After implementing the production please reexport it in [main module file](./src/production/__init__.py), so it can be imported straight from it.
3. Unittests live inside `__test__` module.
4. Each production should have its own dedicated test module `__test__/test_production_<production_number>.py`.
5. Unittests should ideally test whether a production can be applied in various case, but also how does the graph look like after applying the production.
6. Visual examples do live in `example` module.
7. Each production should have its own dedicated visual example in module `example/production_<production_number>.py`
8. Visual example modules **must** define `main` method so that it can be called from `main` module (see how few examples are already implemented).


In case of any changes to this structure please remember to edit readme & put these changes in compact, **dedicated** PR.

## Running examples

Run examples with visualisation:

```bash
# Running all examples
python src/main.py


# Running selected example
python src/main.py --name <example_name_without_dot_py_suffix>

# E.g.
python src/main.py --name production_1
```

For available example names inspect [`example` module](./src/example/)

