from phasor_system import PhasorManager

# Create a new phasor diagram
pm = PhasorManager()

# Draw source voltage starting from origin
pm.draw_phasor("Vs", magnitude=10, angle=0, start_ref="abs", start_x=0, start_y=0)

# Draw line voltage drop from end of Vs
pm.draw_phasor("Vl", magnitude=2, angle=30, start_ref="Vs", ref_point="end")

# Draw load voltage from start of Vs to end of Vl
pm.draw_phasor("Vr", magnitude=8.5, angle=-15, start_ref="Vs", ref_point="start")

# Show the complete diagram
pm.show()
