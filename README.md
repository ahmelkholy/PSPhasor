# Phasor Chain Diagram Drawer

This open source project provides a Python script to draw a chain of phasor vectors. Each vector is drawn starting at the endpoint of the previous vector. This is useful for visualizing related phasors such as voltage and current in power engineering.

## Features

- Draw a chain of phasor vectors.
- Specify each vector with a label, magnitude (absolute value), and angle (in degrees).
- The phasors are chained sequentially (each new vector starts at the end of the previous one).
- Annotated with vector labels for clarity.

## Requirements

- Python 3.x
- [matplotlib](https://matplotlib.org/)
- [numpy](https://numpy.org/)

You can install the required packages using pip:

```bash
pip install matplotlib numpy