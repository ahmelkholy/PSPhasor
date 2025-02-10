# PSPhasor

A powerful Python package for creating and manipulating phasor diagrams in electrical engineering.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/PSPhasor)](https://pypi.org/project/PSPhasor/)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Advanced Usage](#advanced-usage)
- [API Reference](#api-reference)
- [Contributing](#contributing)

## Features

- Create complex phasor diagrams
- Support for voltage and current phasors
- Reference-based phasor positioning
- Customizable colors and styles
- Export diagrams as images

## Installation

Install the package via pip:

```bash
pip install PSPhasor
```

````
## Quick Start

Below is an example of how to create a phasor diagram using PSPhasor:

```python
from PSPhasor.phasor_system import PhasorManager

# Create a new phasor diagram
pm = PhasorManager(figsize=(12, 12))

# Draw source voltage (reference phasor)
pm.draw_phasor(
    "Vs",
    magnitude=10,
    angle=0,
    start_ref="abs",
    start_x=0,
    start_y=0,
    phasor_type="voltage",
    label_offset=0.2,
)

# Draw line voltage drop using end reference
pm.draw_phasor(
    "Vl",
    magnitude=2,
    angle=150,
    start_ref="Vs",
    ref_point="end",
    phasor_type="voltage",
    color="purple",
)

# Draw load voltage using coordinate-based definition
pm.draw_phasor(
    "Vr",
    start_x=0,
    start_y=0,
    end_x=8.5,
    end_y=2.2,
    phasor_type="voltage",
    color="green",
)

# Draw current phasors
pm.draw_phasor(
    "I",
    magnitude=5,
    angle=-30,
    start_ref="abs",
    start_x=2,
    start_y=2,
    phasor_type="current",
)

# Draw another current phasor referenced from the end of I
pm.draw_phasor(
    "I2",
    magnitude=3,
    angle=45,
    start_ref="I",
    ref_point="end",
    phasor_type="current",
    color="cyan",
)

# Get a phasor and print its properties
vs_phasor = pm.get_phasor("Vs")
print("\nVs Phasor properties:")
print(f"Magnitude: {vs_phasor['magnitude']:.2f}")
print(f"Angle: {vs_phasor['angle']:.2f}°")
print(f"End point: ({vs_phasor['end_x']:.2f}, {vs_phasor['end_y']:.2f})")

# Save the diagram
pm.save("phasor_diagram.png")

# Show the complete diagram
pm.show()
```

## Advanced Usage

### Three-Phase System Example

```python
from PSPhasor.phasor_system import PhasorManager

pm = PhasorManager(figsize=(12, 12))

# Draw three-phase voltages
pm.draw_phasor("Va", magnitude=10, angle=0)
pm.draw_phasor("Vb", magnitude=10, angle=-120)
pm.draw_phasor("Vc", magnitude=10, angle=120)

pm.show()
```

### Power Triangle Example

```python
from PSPhasor.phasor_system import PhasorManager

pm = PhasorManager(figsize=(12, 12))

# Draw apparent power
pm.draw_phasor("S", magnitude=10, angle=30, color='blue')
# Draw real power from start of S
pm.draw_phasor("P", magnitude=8.66, angle=0, start_ref="S", ref_point="start", color='green')
# Draw reactive power
pm.draw_phasor("Q", magnitude=5, angle=90, start_ref="S", ref_point="start", color='red')

pm.show()
```

## API Reference

### PhasorManager Methods

- `draw_phasor(name, magnitude=None, angle=None, start_ref='abs', start_x=0, start_y=0, end_x=None, end_y=None, ref_point='end', phasor_type='voltage', color=None, label_offset=0)`
- `get_phasor(name)` - Get phasor by name
- `clear()` - Clear all phasors
- `show(grid=True, equal_aspect=True)` - Display the diagram
- `save(filename)` - Save diagram to file

### Parameters Explained

- **magnitude**: Magnitude (length) for phasors defined with an angle
- **angle**: Angle (in degrees) for phasors defined with a magnitude
- **start_x, start_y**: Starting coordinates (used when specifying coordinates)
- **end_x, end_y**: Ending coordinates (alternative to magnitude/angle)
- **phasor_type**: 'voltage' or 'current' to adjust style and color
- **label_offset**: Offset for the phasor label (optional)

## Contributing

Contributions are welcome! Feel free to fork the repository and submit Pull Requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
````
