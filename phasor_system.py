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
        """Initialize a new phasor diagram"""
        self.phasors = {}
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.ax.set_aspect("equal")
        self._setup_plot()

    def _setup_plot(self):
        """Setup initial plot styling"""
        self.ax.grid(True)
        self.ax.axhline(y=0, color="gray", linestyle="--", alpha=0.3)
        self.ax.axvline(x=0, color="gray", linestyle="--", alpha=0.3)
        plt.title("Phasor Diagram")
        plt.xlabel("Real")
        plt.ylabel("Imaginary")

    def draw_phasor(
        self,
        name,
        magnitude,
        angle,
        start_ref="abs",
        start_x=0,
        start_y=0,
        ref_point="end",
        color="red",
        label_offset=0.1,
    ):
        """
        Draw a phasor with specified parameters

        Parameters:
        -----------
        name : str
            Name/label of the phasor
        magnitude : float
            Length of the phasor
        angle : float
            Angle in degrees from positive real axis
        start_ref : str
            'abs' for absolute coordinates or name of reference phasor
        start_x, start_y : float
            Starting coordinates (used if start_ref is 'abs')
        ref_point : str
            'start' or 'end' of reference phasor
        color : str
            Color of the phasor arrow
        label_offset : float
            Offset distance for the label from the phasor
        """
        if start_ref != "abs":
            if start_ref not in self.phasors:
                raise ValueError(f"Reference phasor '{start_ref}' not found")
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
            arrowprops=dict(arrowstyle="->", color=color, lw=2),
        )

        # Add label with offset
        angle_rad = np.deg2rad(angle)
        label_x = (phasor.start_x + phasor.end_x) / 2 + label_offset * np.sin(angle_rad)
        label_y = (phasor.start_y + phasor.end_y) / 2 + label_offset * np.cos(angle_rad)
        self.ax.text(
            label_x, label_y, name, fontsize=12, color=color, ha="center", va="center"
        )

        self._update_plot()
        return phasor

    def get_phasor(self, name):
        """Get a phasor by name"""
        return self.phasors.get(name)

    def clear(self):
        """Clear all phasors from the diagram"""
        self.phasors.clear()
        self.ax.clear()
        self._setup_plot()

    def _update_plot(self):
        """Update plot limits and styling"""
        if not self.phasors:
            return

        all_x = []
        all_y = []
        for phasor in self.phasors.values():
            all_x.extend([phasor.start_x, phasor.end_x])
            all_y.extend([phasor.start_y, phasor.end_y])

        margin = max(1, 0.1 * (max(all_x) - min(all_x)))
        self.ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
        self.ax.set_ylim(min(all_y) - margin, max(all_y) + margin)

    def show(self):
        """Display the final diagram"""
        plt.show()

    def save(self, filename):
        """Save the diagram to a file"""
        plt.savefig(filename, bbox_inches="tight", dpi=300)
