#!/bin/bash

# Activate virtual environment
source venv/Scripts/Activate

# Run FastAPI server
uvicorn main:app --reload --log-level debug
