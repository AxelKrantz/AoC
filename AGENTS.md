# Repository Guidelines

## Project Structure & Module Organization
Automation scripts live in `automation/` (bootstrap, run, sync). Solutions go to `solutions/y<year>/day_<day>.py` with zero-padded day numbers. Persist puzzle inputs under `inputs/y<year>/day_<day>.txt`; commit only example data while personal inputs stay `.gitignored`. Tests mirror solvers inside `tests/y<year>/test_day_<day>.py`, and shared helpers belong in `common/`.

## Build, Test, and Development Commands
Create a fresh env with `python -m venv .venv` and activate via `. .venv/bin/activate`. Install dependencies from `pip install -r requirements.txt` (pin versions for reproducibility). Fetch puzzle input with `python automation/fetch_input.py <year> <day>` and install `certifi` so TLS verification works out of the box. Run solutions using `python solutions/y<year>/day_<day>.py inputs/y<year>/day_<day>.txt --part=both` and finish with `python -m pytest` before pushing.

## Coding Style & Naming Conventions
Target Python 3.11+, four-space indents, and keep functions type-annotated. Name solver functions `solve_part1` and `solve_part2`; keep helpers snake_case modules. Format with `ruff check` and `black --check .` in CI or pre-push hooks. Limit runtime logic inside `if __name__ == "__main__":` blocks to pass args into pure solvers.

## Testing Guidelines
Use `pytest` with parametrized cases for sample and personal inputs. Store golden files beneath `tests/data/<year>/` and load them with pathlib so relative paths survive automation. Name tests `test_part1_example`, `test_part2_regression`, etc., and measure coverage via `pytest --cov=solutions --cov-report=term-missing` when touching shared utilities.

## Commit & Pull Request Guidelines
Write imperative commit subjects under 50 characters (e.g., `Add day 05 solver`) and mention the AoC year/day. Include brief bodies for tricky bugs or data shape changes. PRs should summarize the approach, list verification commands, and note any files added to `.gitignore` or `.env.example`; attach screenshots or console excerpts when behavior changes.

## Security & Configuration Tips
Keep the `AOC_SESSION` token in `.env` and load it through the automation scripts; never commit the raw cookie. Rotate the token yearly and redact puzzle answers in logs before sharing. When adding new config knobs, document defaults in `README.md` and reference them from the PR so agents stay aligned. Install `certifi` (or system roots) for trusted TLS and reserve `AOC_SKIP_TLS_VERIFY=1` for one-off emergencies.

## Agent Communication
Warn the maintainer if chat runs appear to consume excessive tokens so we can adjust prompts or split work before exhausting the shared allocation.
