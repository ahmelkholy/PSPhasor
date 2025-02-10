# Ultimate Phasor Diagram Tool

A powerful and flexible Python tool for creating phasor diagrams commonly used in electrical engineering and power systems analysis.

## Features

- Draw phasors with specified magnitude and angle
- Reference existing phasors for start/end points
- Automatic plot scaling and formatting
- Customizable colors and labels
- Support for absolute and relative positioning
- Save diagrams to files

## Installation

```bash
pip install numpy matplotlib
```

## Quick Start

```python
from phasor_system import PhasorManager

# Create a new diagram
pm = PhasorManager()

# Draw source voltage (10∠0°)
pm.draw_phasor("Vs", magnitude=10, angle=0, start_ref="abs", start_x=0, start_y=0)

# Draw line voltage drop (2∠30°) from end of Vs
pm.draw_phasor("Vl", magnitude=2, angle=30, start_ref="Vs", ref_point="end")

# Draw load voltage from start of Vs
pm.draw_phasor("Vr", magnitude=8.5, angle=-15, start_ref="Vs", ref_point="start")

# Show the diagram
pm.show()
```

## Advanced Usage

### Three-Phase System Example

```python
pm = PhasorManager()

# Draw three-phase voltages
pm.draw_phasor("Va", 10, 0)
pm.draw_phasor("Vb", 10, -120)
pm.draw_phasor("Vc", 10, 120)

pm.show()
```

### Power Triangle Example

```python
pm = PhasorManager()

# Draw apparent power
pm.draw_phasor("S", 10, 30, color='blue')
# Draw real power from start of S
pm.draw_phasor("P", 8.66, 0, start_ref="S", ref_point="start", color='green')
# Draw reactive power
pm.draw_phasor("Q", 5, 90, start_ref="S", ref_point="start", color='red')

pm.show()
```

## API Reference

### PhasorManager Methods

- `draw_phasor(name, magnitude, angle, start_ref='abs', start_x=0, start_y=0, ref_point='end', color='red')`
- `get_phasor(name)` - Get phasor by name
- `clear()` - Clear all phasors
- `show()` - Display the diagram
- `save(filename)` - Save diagram to file

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
