# Sūrya‑Siddhānta Planetary Algorithm Re‑evaluation

This repository contains the code and data for the research paper:
**"Re‑evaluating Siddhāntic Planetary Algorithms through Modern Computational and Data‑Analytic Techniques"**  
by Ankita Banerjee, submitted to *Vakyartha Bharati
* (2026).

## Overview
We compare the planetary longitude formulas from the ancient Indian text *Sūrya‑Siddhānta* with NASA JPL’s DE441 ephemeris over the years 1900–2025. The analysis includes:
- Daily planetary position calculations using the *Sūrya‑Siddhānta* algorithm.
- Statistical error analysis (mean error, standard deviation, maximum error).
- Demonstration of the structural analogy between the *bīja* correction and a Kalman filter.

## Repository Structure
- `code/` – Python scripts that implement the *Sūrya‑Siddhānta* formulas, fetch JPL data, and compute residuals.
- `data/` – Downloaded JPL ephemerides (CSV format) for the period 1900‑2025.
- `results/` – Output tables and figures from the paper.
- `notebooks/` – Jupyter notebook for interactive exploration (optional).

## Requirements
Install the dependencies listed in `requirements.txt`:
