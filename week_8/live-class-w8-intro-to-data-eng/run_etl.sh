#!/bin/bash

echo "Start Luigi ETL Pipeline Process"

# Virtual Environment Path
VENV_PATH="/home/shandytp/course-intro-to-data-eng/venv/bin/activate"

# Activate venv
source "$VENV_PATH"

# set python script
PYTHON_SCRIPT="C:\Users\ihdarsyd\Documents\Pacmann\Simple DE\week_8\live-class-w8-intro-to-data-eng\main.py"

# run python script
python "$PYTHON_SCRIPT" >> /home/shandytp/course-intro-to-data-eng/log/logfile.log 2>&1

# logging simple
dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "Luigi Started at ${dt}" >> /home/shandytp/course-intro-to-data-eng/log/luigi-info.log

echo "End Luigi ETL Pipeline Process"