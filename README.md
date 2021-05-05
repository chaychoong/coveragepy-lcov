# coveragepy-lcov

This package provides a simple CLI for converting .coverage files to the LCOV format.

# Usage

```bash
pip install coveragepy-lcov

# If the .coverage file is in your current working directory
coveragepy-lcov

# Point to a different .coverage file path
coveragepy-lcov --data_file_path example/.coverage

# Write the output to a different file path
coveragepy-lcov --output_file_path build/lcov.info

# Use relative paths in the LCOV output
coveragepy-lcov --relative_path
```

# Configuration

```text
Usage: coveragepy-lcov [OPTIONS]

Options:
  --data_file_path TEXT    Path to .coverage file
  --output_file_path TEXT  lcov.info output file path
  --config_file TEXT       Path to .coveragerc file
  --relative_path          Use relative path in LCOV output
  --preview                Preview LCOV output
  --help                   Show this message and exit.
```
