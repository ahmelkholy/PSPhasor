from phasor_chain import draw_phasor_chain
from phasor_diagram import draw_phasor

# Starting point coordinates
start_x = 2
start_y = 2

# Format: (label, magnitude, angle)
vectors = [
    ("Vs", 10.0, 0),  # Source voltage at 0 degrees
    ("Vl", 2.0, 0),  # Line voltage drop, starting from end of Vs
    ("Vr", 8.5, 30),  # Load voltage, connecting from start to Vl
]

# Draw the phasor diagram from specified starting point
draw_phasor_chain(start_x, start_y, vectors)
draw_phasor(10, 0, 0, 0)
