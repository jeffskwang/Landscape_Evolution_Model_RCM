#!/bin/bash
pypy main.py field_example_test
python plot_output.py field_example_test
pypy main.py field_example_test_lateral
python plot_output.py field_example_test_lateral