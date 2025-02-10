import numpy as np
import matplotlib.pyplot as plt


class Phasor:
    def __init__(self, name, magnitude, angle, start_x, start_y):
        self.name = name
        self.magnitude = magnitude
        self.angle_deg = angle
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = start_x + magnitude * np.cos(np.deg2rad(angle))
        self.end_y = start_y + magnitude * np.sin(np.deg2rad(angle))


class PhasorManager:
    def __init__(self, figsize=(10, 10)):
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.phasors = {}
        self.setup_plot()

    def setup_plot(self):
        self.ax.set_aspect("equal")
        self.ax.grid(True)
        self.ax.axhline(y=0, color="k", linestyle="-", linewidth=0.5)
        self.ax.axvline(x=0, color="k", linestyle="-", linewidth=0.5)

    def draw_phasor(
        self,
        name,
        magnitude=None,
        angle=None,
        start_ref="abs",
        start_x=0,
        start_y=0,
        end_x=None,
        end_y=None,
        ref_point="start",
        phasor_type="voltage",
        color=None,
        label_offset=0.1,
    ):
        if end_x is None and end_y is None:
            # Convert angle to radians
            angle_rad = np.radians(angle)
            # Calculate end points
            end_x = start_x + magnitude * np.cos(angle_rad)
            end_y = start_y + magnitude * np.sin(angle_rad)

        if start_ref != "abs":
            ref_phasor = self.phasors[start_ref]
            if ref_point == "end":
                start_x = ref_phasor["end_x"]
                start_y = ref_phasor["end_y"]

        # Set default colors based on phasor type
        if color is None:
            color = "blue" if phasor_type == "voltage" else "red"

        # Draw the phasor
        self.ax.quiver(
            start_x,
            start_y,
            end_x - start_x,
            end_y - start_y,
            angles="xy",
            scale_units="xy",
            scale=1,
            color=color,
            width=0.005,
        )

        # Add label
        label_x = start_x + (end_x - start_x) / 2 + label_offset
        label_y = start_y + (end_y - start_y) / 2 + label_offset
        self.ax.text(label_x, label_y, name)

        # Store phasor information
        self.phasors[name] = {
            "magnitude": np.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2),
            "angle": np.degrees(np.arctan2(end_y - start_y, end_x - start_x)),
            "start_x": start_x,
            "start_y": start_y,
            "end_x": end_x,
            "end_y": end_y,
            "type": phasor_type,
        }

    def get_phasor(self, name):
        return self.phasors.get(name)

    def show(self):
        plt.show()

    def save(self, filename):
        plt.savefig(filename)
