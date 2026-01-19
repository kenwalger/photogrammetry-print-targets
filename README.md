# Photogrammetric Coded Target Generator

This repository contains a small, self-contained Python script for generating
printable photogrammetry targets with a built-in calibration reference.

The output is a **1:1 scale PDF** intended for physical printing and use in
photogrammetric capture workflows.

---

## Features

- Binary coded photogrammetry markers
- 6 mm solid center dots (design-space)
- Explicit millimeter-based geometry
- Sheet-level calibration reference (20.00 mm)
- Print-verifiable output (PDF)
- No surface contact or adhesive requirements

---

## Requirements

- Python 3.9+
- matplotlib

Minimal dependencies are intentional.

```txt
matplotlib>=3.7
