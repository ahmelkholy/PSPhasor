# PSPhasor Examples

Run any example from the repository root:

```bash
python examples/00_minimal.py
python examples/01_basic_load.py
python examples/02_balanced_three_phase.py
python examples/03_unbalanced_three_phase_load.py
python examples/04_feeder_voltage_drop.py
python examples/05_fault_current_sequence_components.py
python examples/06_power_triangle.py
python examples/run_all.py
```

Each script writes a PNG to `examples/output/`.

## Example Set

- `00_minimal.py`: Minimal voltage/current diagram.
- `01_basic_load.py`: Single-phase source, receiving-end voltage, line drop, and
  lagging load current.
- `02_balanced_three_phase.py`: Balanced positive-sequence voltage and current
  phasors.
- `03_unbalanced_three_phase_load.py`: Unbalanced three-phase load current set
  with neutral current from vector sum.
- `04_feeder_voltage_drop.py`: Sending-end voltage, current, impedance drop,
  resistive/reactive drop components, and receiving-end voltage.
- `05_fault_current_sequence_components.py`: Positive, negative, and zero
  sequence current components plus reconstructed phase currents.
- `06_power_triangle.py`: Apparent, real, and reactive power phasors for a
  lagging power-factor load.
