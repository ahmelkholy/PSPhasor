# ultimate-phasor

A powerful Python package for creating and manipulating phasor diagrams in electrical engineering.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/ultimate-phasor)](https://pypi.org/project/ultimate-phasor/)

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

```bash
pip install ultimate-phasor
```

## Quick Start

```python
from ultimate_phasor import PhasorManager

# Create a new phasor diagram
pm = PhasorManager()

# Draw source voltage
pm.draw_phasor("Vs", magnitude=10, angle=0)

# Draw load voltage
pm.draw_phasor("Vl", magnitude=2, angle=30, start_ref="Vs", ref_point="end")

# Show the diagram
pm.show()
```

## Advanced Usage

### Three-Phase System Example

```python
from ultimate_phasor import PhasorManager

pm = PhasorManager()

# Draw three-phase voltages
pm.draw_phasor("Va", 10, 0)
pm.draw_phasor("Vb", 10, -120)
pm.draw_phasor("Vc", 10, 120)

pm.show()
```

### Power Triangle Example

```python
from ultimate_phasor import PhasorManager

pm = PhasorManager()

# Draw apparent power
pm.draw_phasor("S", 10, 30, color='blue')
# Draw real power from start of S
pm.draw_phasor("P", 8.66, 0, start_ref="S", ref_point="start", color='green')
# Draw reactive power
pm.draw_phasor("Q", 5, 90, start_ref="S", ref_point="start", color='red')

pm.show()
```

### Mixed Voltage-Current System Example

```python
from ultimate_phasor import PhasorManager

pm = PhasorManager()

# Voltage source
pm.draw_phasor("V", magnitude=10, angle=0)

# Current through impedance
pm.draw_phasor("I", magnitude=2, angle=-30, phasor_type="current")

# Voltage drop across impedance
pm.draw_phasor("Vz", start_x=0, start_y=0, end_x=5, end_y=2)

pm.show()
```

## API Reference

### PhasorManager Methods

- `draw_phasor(name, magnitude=None, angle=None, start_ref='abs', start_x=0, start_y=0, end_x=None, end_y=None, ref_point='end', phasor_type='voltage', color=None)`
- `get_phasor(name)` - Get phasor by name
- `clear()` - Clear all phasors
- `show(grid=True, equal_aspect=True)` - Display the diagram with enhanced plotting
- `save(filename)` - Save diagram to file

### Parameters

- `magnitude`: Optional magnitude for angle-based phasors
- `angle`: Optional angle in degrees for angle-based phasors
- `start_x, start_y`: Starting coordinates
- `end_x, end_y`: Ending coordinates (alternative to magnitude/angle)
- `phasor_type`: 'voltage' or 'current' (affects color and style)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
