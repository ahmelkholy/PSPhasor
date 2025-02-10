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
    def __init__(self):
        self.phasors = {}
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.ax.set_aspect("equal")

    def draw_phasor(
        self,
        name,
        magnitude,
        angle,
        start_ref="abs",
        start_x=0,
        start_y=0,
        ref_point="end",
    ):
        """
        Draw a phasor with given parameters
        start_ref: 'abs' for absolute coordinates or name of reference phasor
        ref_point: 'start' or 'end' of reference phasor
        """
        if start_ref != "abs":
            if start_ref not in self.phasors:
                raise ValueError(f"Reference phasor {start_ref} not found")
            ref_phasor = self.phasors[start_ref]
            if ref_point == "end":
                start_x = ref_phasor.end_x
                start_y = ref_phasor.end_y
            else:
                start_x = ref_phasor.start_x
                start_y = ref_phasor.start_y

        phasor = Phasor(name, magnitude, angle, start_x, start_y)
        self.phasors[name] = phasor

        # Draw the phasor
        self.ax.annotate(
            "",
            xy=(phasor.end_x, phasor.end_y),
            xytext=(phasor.start_x, phasor.start_y),
            arrowprops=dict(arrowstyle="->", color="red", lw=2),
        )

        # Add label
        mid_x = (phasor.start_x + phasor.end_x) / 2
        mid_y = (phasor.start_y + phasor.end_y) / 2
        self.ax.text(mid_x, mid_y, name, fontsize=12, color="blue")

        self._update_plot()
        return phasor

    def _update_plot(self):
        """Update plot limits and styling"""
        all_x = []
        all_y = []
        for phasor in self.phasors.values():
            all_x.extend([phasor.start_x, phasor.end_x])
            all_y.extend([phasor.start_y, phasor.end_y])

        margin = max(1, 0.1 * (max(all_x) - min(all_x)))
        self.ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
        self.ax.set_ylim(min(all_y) - margin, max(all_y) + margin)

        self.ax.grid(True)
        self.ax.axhline(y=0, color="gray", linestyle="--", alpha=0.3)
        self.ax.axvline(x=0, color="gray", linestyle="--", alpha=0.3)
        plt.title("Phasor Diagram")

    def show(self):
        """Display the final diagram"""
        plt.show()
