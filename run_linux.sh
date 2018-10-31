#!/bin/bash
pypy main.py field_example
python plot_output.py field_example
pypy main.py xlm_calibrated
python plot_output.py xlm_calibrated