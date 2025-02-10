from PSPhasor.phasor_system import PhasorManager

pm = PhasorManager(figsize=(8, 6))

# Draw source voltage (reference phasor)
pm.draw_phasor(
    "Vs",
    magnitude=10,
    angle=0,
    start_ref="abs",
    start_x=0,
    start_y=0,
    phasor_type="voltage",
)

# Draw line voltage
pm.draw_phasor(
    "Vl",
    magnitude=2,
    angle=150,
    start_ref="Vs",
    ref_point="end",
    phasor_type="voltage",
    color="purple",
)

# Draw load voltage
pm.draw_phasor(
    "Vr",
    start_x=0,
    start_y=0,
    end_x=8.5,
    end_y=2.2,
    phasor_type="voltage",
    color="green",
)

pm.show()
