# PSPhasor

PSPhasor is a small Python package for drawing phasor diagrams with Matplotlib.
It supports polar input, Cartesian input, and phasors referenced from previously
drawn phasors.

![Example phasor diagram](examples/output/01_basic_load.png)

## Features

- Draw phasors from magnitude/angle or explicit start/end coordinates.
- Start a phasor from the start or end of another phasor.
- Store each phasor as a typed `Phasor` object with magnitude, angle, and
  component properties.
- Preserve older dictionary-style reads such as `phasor["magnitude"]`.
- Draw directly from complex numbers.
- Generate balanced positive- or negative-sequence three-phase phasor sets.
- Use engineering-style plots with major/minor grids, heavier axes, arrowheads,
  and automatic label placement.
- Fit plots without the excessive blank canvas that can happen with equal
  aspect Matplotlib axes.
- Save diagrams directly to image files.

## Installation

Install from PyPI:

```bash
python -m pip install PSPhasor
```

For local development:

```bash
python -m pip install -e ".[dev]"
```

## Quick Start

```python
from PSPhasor import DiagramStyle, PhasorManager

manager = PhasorManager(
    figsize=(9, 5),
    title="Single-phase load phasor diagram",
    xlabel="Real component",
    ylabel="Reactive component",
    style=DiagramStyle(arrow_line_width=3.0, arrow_head_size=20.0),
)

source = manager.draw_phasor(
    "Vs",
    magnitude=10,
    angle=0,
    label=r"$V_s$",
)
manager.draw_phasor(
    "Vdrop",
    magnitude=2,
    angle=150,
    start_ref="Vs",
    color="#9467bd",
    label=r"$V_{drop}$",
)
manager.draw_phasor(
    "Vr",
    start_x=0,
    start_y=0,
    end_x=8.27,
    end_y=1.0,
    color="#2ca02c",
    label=r"$V_R$",
)
manager.draw_phasor(
    "Iload",
    magnitude=4,
    angle=-30,
    phasor_type="current",
    label=r"$I_L$",
)

print(f"{source.name}: {source.magnitude:.2f} at {source.angle_deg:.1f} deg")
manager.save("examples/output/01_basic_load.png")
```

## Examples

All examples live under `examples/`.

```bash
python examples/run_all.py
```

The example set includes:

- `00_minimal.py`: minimal voltage/current diagram.
- `01_basic_load.py`: source voltage, line drop, receiving voltage, and current.
- `02_balanced_three_phase.py`: balanced voltage and current phasors.
- `03_unbalanced_three_phase_load.py`: unbalanced currents and neutral current.
- `04_feeder_voltage_drop.py`: feeder `IR` and `jIX` voltage-drop components.
- `05_fault_current_sequence_components.py`: sequence and phase fault currents.
- `06_power_triangle.py`: real, reactive, and apparent power triangle.

## API

### `PhasorManager`

```python
PhasorManager(
    figsize=(9.0, 5.0),
    title="Phasor Diagram",
    xlabel="Real axis",
    ylabel="Imaginary axis",
)
```

Main methods:

- `draw_phasor(...) -> Phasor`: draw and store a phasor.
- `draw_complex(...) -> Phasor`: draw a phasor from a complex value.
- `draw_three_phase(...) -> list[Phasor]`: draw a balanced three-phase set.
- `get_phasor(name) -> Phasor | None`: return a stored phasor.
- `fit(margin=0.15, equal_aspect=True)`: fit axes around all phasors.
- `save(filename, dpi=300) -> Path`: save the current diagram.
- `show()`: display the current diagram.
- `clear()`: remove all stored phasors and reset the plot.

### `draw_phasor`

```python
manager.draw_phasor(
    name,
    magnitude=None,
    angle=None,
    *,
    start_ref="abs",
    start_x=0.0,
    start_y=0.0,
    end_x=None,
    end_y=None,
    ref_point="end",
    phasor_type="voltage",
    color=None,
    label_offset=None,
    arrow_width=None,
    line_width=None,
    label=None,
    alpha=1.0,
    linestyle="-",
    metadata=None,
)
```

Use exactly one geometry mode:

- Polar: provide `magnitude` and `angle`.
- Cartesian: provide `end_x` and `end_y`.

Set `start_ref` to the name of an existing phasor to start from that phasor.
Use `ref_point="start"` or `ref_point="end"` to choose the reference point.

### Complex and Three-Phase Helpers

```python
manager.draw_complex("V", 3 + 4j, label=r"$V$")
manager.draw_three_phase(
    "V",
    magnitude=1.0,
    angle=0.0,
    sequence="abc",
    labels=(r"$V_a$", r"$V_b$", r"$V_c$"),
)
```

These helpers are intended for power-system workflows where phasors are already
represented as complex quantities or balanced phase sets.

### `Phasor`

`draw_phasor` returns a `Phasor` object:

```python
phasor = manager.draw_phasor("Vs", magnitude=10, angle=0)

phasor.magnitude
phasor.angle_deg
phasor.start
phasor.end
phasor.dx
phasor.dy
```

Dictionary-style access is also supported for compatibility:

```python
phasor["magnitude"]
phasor["angle_deg"]
phasor["end_x"]
```

## Development

Run the test suite:

```bash
python -m pytest
```

Run lint checks:

```bash
ruff check .
```

## License

This project is licensed under the MIT License. See `LICENSE` for details.
