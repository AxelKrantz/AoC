# AoC

Tools and solutions for Advent of Code puzzles.

## Getting Started

1. Create a virtual environment and install tooling:

   ```bash
   python -m venv .venv
   . .venv/bin/activate
   python -m pip install -r requirements.txt  # if present
   python -m pip install pytest
   ```

2. Provide your Advent of Code session token by exporting `AOC_SESSION` or adding `AOC_SESSION=...` to `.env`.

3. Download puzzle input for Day 1, 2015:

   ```bash
   python automation/fetch_input.py 2015 1
   ```

4. Run the solver against the fetched input:

   ```bash
   python solutions/y2015/day_01.py inputs/y2015/day_01.txt
   ```
