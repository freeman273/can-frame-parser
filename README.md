# CAN Frame Parser & Validator

A Python tool that parses and validates CAN (Controller Area Network) bus messages from a text log file, using the standard log format produced by real-world tools such as `candump` (Linux `can-utils`) and `python-can`.

## What it does

- **Parses** log lines in the format `(timestamp) interface ID#DATA` into structured `CANFrame` objects.
- **Validates** each frame against core CAN protocol rules:
  - CAN ID must be valid hexadecimal.
  - Standard (11-bit) IDs must be in range `0x000`–`0x7FF`.
  - Extended (29-bit) IDs must be in range `0x00000000`–`0x1FFFFFFF`.
  - Data payload must be valid hexadecimal with an even number of characters.
  - Data payload must not exceed 8 bytes (classic CAN).
- **Reports** results per frame, with a pass/fail summary.
- **Aggregates statistics** — message count per CAN ID.
- **Exports results to CSV** for further analysis (e.g. in Excel).

### A note on scope

This project validates the *logical* structure of a CAN frame (ID range, data length, hex formatting) as it appears in a text log. It does **not** recompute the physical-layer CRC, since that checksum is calculated over the raw bitstream (including bit-stuffing) and cannot be reconstructed from a text representation — the same limitation applies to most log-analysis tools working from `candump`-style output.

## Project structure
can-frame-parser/
├── CAN_Frame_Parser.py # parsing, validation, CLI, statistics, CSV export
├── test_CAN_Frame_Parser.py # automated tests (pytest)
├── sample_log.txt # example input log
├── results.csv # generated output (created after running)
└── README.md

## Requirements

- Python 3.8+
- pytest (for running tests): `pip install pytest`

## Usage

1. Place your CAN log lines in `sample_log.txt`, one per line, e.g.:1000000000.000001) vcan0 123#1122334455667788
(1000000000.300000) vcan0 XYZ#1122
2. Run the script: python CAN_Frame_Parser.py
3. Check the console output for a per-frame report and summary, and open `results.csv` for the exported data.

## Example output
ID=123| DATA=1122334455667788| VALID
ID=0C8| DATA=AABB| VALID
ID=456| DATA=11223344556677889900| INVALID:INVALID: too many bytes, the max is 8 bytes.
ID=XYZ| DATA=1122| INVALID:ID is not a valid hexadecimal

Summary:2 valid, 2 invalid

Statistics for each ID:
ID=123:1 messages
ID=0C8:1 messages
ID=456:1 messages
ID=XYZ:1 messages
## Running tests :pytest

Tests cover standard and extended valid IDs, invalid (non-hex) IDs, odd-length data, and oversized data payloads, using `pytest.mark.parametrize` to run the same checks across multiple input cases.

## What I learned building this

- Separating parsing from validation logic (single responsibility).
- Exception handling (`try`/`except`) for malformed input, instead of letting the program crash.
- Basic OOP: representing a parsed frame as a `CANFrame` object with its own `is_valid()` method.
- Writing parametrized automated tests with `pytest`.
- Aggregating data with dictionaries and exporting structured results to CSV.

## Possible future extensions

- Decode signal values from raw data using `.dbc` files (via [`cantools`](https://cantools.readthedocs.io/)).
- Capture live traffic from a virtual CAN bus using [`python-can`](https://python-can.readthedocs.io/).
- Filter report output by CAN ID or ID range.
