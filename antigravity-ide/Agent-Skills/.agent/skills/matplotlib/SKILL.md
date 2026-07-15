---
name: matplotlib
description: Generating customized plots and figures (such as Sine/Cosine comparison charts) using Matplotlib and NumPy.
---

# Matplotlib Plotting Skill

A skill for generating scientific, statistical, and custom data visualizations using Matplotlib.

## Setup
Before executing this skill, ensure that the dependencies are installed:
```bash
pip install -r requirements.txt
```

The plotting commands are run via the Python script:
`python3 scripts/plot.py`

## Commands and Arguments Schema

### 1. Sine and Cosine Comparison (`sine-cosine`)
Generates a highly-stylized comparison plot of Sine and Cosine curves.

**Arguments:**
- `output` (string, optional, default: `plot.png`): The file path where the resulting chart will be saved.
- `title` (string, optional, default: `Sine vs Cosine Wave Comparison`): The title of the plot.
- `xlabel` (string, optional, default: `Angle (radians)`): The label for the x-axis.
- `ylabel` (string, optional, default: `Amplitude`): The label for the y-axis.

**Example Command:**
```bash
python3 scripts/plot.py sine-cosine --output sine_cosine_comparison.png --title "Sine & Cosine Waves"
```
