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

5. Execute the test suite:

   ```bash
   python -m pytest
   ```

Warn the maintainer if solving sessions begin to consume unusually high token counts so we can adjust prompts before impacting the shared quota.

## TLS Certificates

If your environment lacks the Advent of Code certificate chain, install `certifi` in your virtualenv (`python -m pip install certifi`). The tooling automatically loads that CA bundle. Use `AOC_SKIP_TLS_VERIFY=1` only as a last resort for a single command.

## Submitting Answers

Submit a computed solution once you are confident in the result:

```bash
python automation/submit_answer.py 2015 1 138 --out .responses/day01-part1.html
```

Use `--dry-run` to preview the payload without sending it, and inspect the response for messages about rate limits or incorrect answers.
