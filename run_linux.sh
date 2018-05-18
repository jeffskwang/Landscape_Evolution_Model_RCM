#!/bin/bash

pypy main.py run_1
python plot_output.py run_1
pypy main.py run_2
python plot_output.py run_2
pypy main.py run_3
python plot_output.py run_3