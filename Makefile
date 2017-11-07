# make all runs main.py
PYTHON_LIBS="../league;../league/Models"

run_main_py:
	PYTHONPATH=${PYTHON_LIBS} python main.py

all: run_main_py

