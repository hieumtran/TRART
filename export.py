import cx_Freeze
import os

executables = [cx_Freeze.Executable("main.py")]

all_files = []
for file in os.listdir('./data/building/'):
    all_files.append(('./data/building/', ['./data/building/'+file]))
for file in os.listdir('./font/'):
    all_files.append(('./font/', ['./font/'+file]))
for file in os.listdir('./ui_button/'):
    all_files.append(('./ui_button/', ['./ui_button/'+file]))
for file in os.listdir('./sounds/'):
    all_files.append(('./sounds/', ['./sounds/'+file]))
    ('', ['README.txt'])
all_files.append(('', ['menu.py']))
all_files.append(('', ['slide_puzzle.py']))

cx_Freeze.setup(
    name="DeSlicing",
    options={"build_exe": {"packages":["pygame"]}},
    data_files = all_files,
    executables = executables
    )