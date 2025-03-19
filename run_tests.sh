#!/bin/sh

# Run black to autoformat the code
black src

# Run bandit to perform security checks
bandit -r src

# Run pytest with coverage
pytest --disable-warnings --cov=src --cov-report=term