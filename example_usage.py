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
print(f"End point: ({vs_phasor['end_x']:.2f}, {vs_phasor['end_y']:.2f})")

# Save the diagram
# pm.save("phasor_diagram.png")

# Show the complete diagram
pm.show()
