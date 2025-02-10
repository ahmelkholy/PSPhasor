#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PSPhasor - A powerful Python module for creating and manipulating phasor diagrams.

Features:
- Create complex phasor diagrams with voltage/current phasors
- Reference-based phasor positioning (start from absolute coordinates or another phasor's end)
- Customizable colors, arrow width, and label offset
- Methods to clear, save, and show the diagram
- Auto-scaling so that all phasors fit nicely in the figure
"""

import numpy as np
import matplotlib.pyplot as plt


class PhasorManager:
    """
    Manages the creation and display of phasor diagrams.
    """

    def __init__(self, figsize=(10, 10), title="Phasor Diagram"):
        """
        Initializes the PhasorManager.

        Args:
            figsize (tuple): The size of the figure (width, height) in inches.
            title (str): The title of the plot.
        """
        self.fig, self.ax = plt.subplots(figsize=figsize)
        self.phasors = {}
        self.title = title
        self.setup_plot()

    def setup_plot(self):
        """
        Sets up the plot with equal aspect, grid, and reference lines.
        """
        self.ax.set_aspect("equal", adjustable="datalim")
        self.ax.set_title(self.title)
        self.ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)
        # Draw x and y axes
        self.ax.axhline(y=0, color="k", linestyle="-", linewidth=0.8)
        self.ax.axvline(x=0, color="k", linestyle="-", linewidth=0.8)

    def draw_phasor(
        self,
        name,
        magnitude=None,
        angle=None,
        start_ref="abs",
        start_x=0.0,
        start_y=0.0,
        end_x=None,
        end_y=None,
        ref_point="end",
        phasor_type="voltage",
        color=None,
        label_offset=0.1,
        arrow_width=0.005,
    ):
        """
        Draws a phasor on the diagram.

        There are two main ways to specify the phasor:
        1) (magnitude, angle) + optional reference
        2) (start_x, start_y) & (end_x, end_y) directly

        Args:
            name (str): Unique identifier for the phasor.
            magnitude (float): The length of the phasor (used if end_x, end_y are not given).
            angle (float): The angle in degrees from the positive X-axis (used with magnitude).
            start_ref (str): Name of another phasor to reference for start point.
                             Use "abs" for absolute (0, 0) or user-specified start_x, start_y.
            start_x (float): The starting X coordinate (only used if start_ref="abs" or overriding).
            start_y (float): The starting Y coordinate (only used if start_ref="abs" or overriding).
            end_x (float): The ending X coordinate (optional; if provided, overrides magnitude/angle).
            end_y (float): The ending Y coordinate (optional; if provided, overrides magnitude/angle).
            ref_point (str): If referencing another phasor, use the 'start' or 'end' of that phasor.
            phasor_type (str): 'voltage' or 'current' (affects default color).
            color (str): Matplotlib-compatible color (optional).
            label_offset (float): Offset for the phasor name label.
            arrow_width (float): Width of the arrow (used in quiver).
        """

        # 1. If not referencing absolute coordinates, adjust start to reference phasor's start or end
        if start_ref != "abs":
            if start_ref not in self.phasors:
                raise ValueError(f"Phasor '{start_ref}' does not exist.")
            ref_phasor = self.phasors[start_ref]

            # Adjust the current phasor's start to the referenced phasor's start or end
            if ref_point == "end":
                start_x = ref_phasor["end_x"]
                start_y = ref_phasor["end_y"]
            else:  # ref_point == "start"
                start_x = ref_phasor["start_x"]
                start_y = ref_phasor["start_y"]

        # 2. Determine the end coordinates
        if end_x is None and end_y is None:
            # Must have magnitude and angle if end points aren't specified
            if magnitude is None or angle is None:
                raise ValueError(
                    "Either (end_x, end_y) or (magnitude, angle) must be provided."
                )
            # Convert angle to radians
            angle_rad = np.radians(angle)
            # Compute new end point from magnitude and angle
            end_x = start_x + magnitude * np.cos(angle_rad)
            end_y = start_y + magnitude * np.sin(angle_rad)

        # 3. Determine default color if none provided
        if color is None:
            color = "blue" if phasor_type.lower() == "voltage" else "red"

        # 4. Draw the phasor using quiver
        self.ax.quiver(
            start_x,
            start_y,
            end_x - start_x,
            end_y - start_y,
            angles="xy",
            scale_units="xy",
            scale=1,
            color=color,
            width=arrow_width,
        )

        # 5. Add text label near the midpoint of the arrow
        mid_x = (start_x + end_x) / 2.0
        mid_y = (start_y + end_y) / 2.0
        self.ax.text(mid_x + label_offset, mid_y + label_offset, name, color=color)

        # 6. Store phasor information for future reference
        self.phasors[name] = {
            "name": name,
            "type": phasor_type.lower(),
            "start_x": start_x,
            "start_y": start_y,
            "end_x": end_x,
            "end_y": end_y,
            "magnitude": np.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2),
            "angle_deg": np.degrees(np.arctan2(end_y - start_y, end_x - start_x)),
            "color": color,
        }

    def get_phasor(self, name):
        """
        Retrieves information about a previously drawn phasor.

        Args:
            name (str): The identifier of the phasor.

        Returns:
            dict: A dictionary with keys:
                  ['name', 'type', 'start_x', 'start_y', 'end_x', 'end_y',
                   'magnitude', 'angle_deg', 'color']
                  or None if the phasor doesn't exist.
        """
        return self.phasors.get(name, None)

    def clear(self):
        """
        Clears all phasors and resets the plot.
        """
        self.phasors.clear()
        self.ax.cla()
        self.setup_plot()

    def show(self, grid=True, equal_aspect=True):
        """
        Displays the diagram. Auto-scales so all phasors are visible.

        Args:
            grid (bool): Whether to show the grid.
            equal_aspect (bool): If True, enforce equal aspect ratio.
        """
        if grid:
            self.ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)

        if equal_aspect:
            self.ax.set_aspect("equal", adjustable="datalim")

        # Auto-scale to fit all phasors
        self.ax.autoscale(enable=True, axis="both", tight=True)

        plt.show()

    def save(self, filename):
        """
        Saves the current phasor diagram to an image file.

        Args:
            filename (str): The output file path (e.g. 'diagram.png').
        """
        self.fig.savefig(filename, bbox_inches="tight")
        print(f"Diagram saved to {filename}.")


def main():
    """
    Demonstration of using the PhasorManager for typical phasor diagrams.
    """

    # Create a new phasor diagram
    pm = PhasorManager(figsize=(12, 12), title="PSPhasor Demo")

    # 1. Draw a reference (source) voltage phasor
    pm.draw_phasor(
        name="Vs",
        magnitude=10,
        angle=0,
        start_ref="abs",  # absolute reference
        start_x=0,
        start_y=0,
        phasor_type="voltage",
        label_offset=0.2,
    )

    # 2. Draw a line voltage drop from the end of Vs
    pm.draw_phasor(
        name="Vl",
        magnitude=2,
        angle=150,
        start_ref="Vs",  # reference from "Vs"
        ref_point="end",  # start at Vs's end
        phasor_type="voltage",
        color="purple",
    )

    # 3. Draw a load voltage using explicit start/end coordinates
    pm.draw_phasor(
        name="Vr",
        start_x=0,
        start_y=0,
        end_x=8.5,
        end_y=2.2,
        phasor_type="voltage",
        color="green",
    )

    # 4. Draw a current phasor from an absolute point (2,2)
    pm.draw_phasor(
        name="I",
        magnitude=5,
        angle=-30,
        start_ref="abs",
        start_x=2,
        start_y=2,
        phasor_type="current",
    )

    # 5. Draw another current phasor from the end of I
    pm.draw_phasor(
        name="I2",
        magnitude=3,
        angle=45,
        start_ref="I",
        ref_point="end",
        phasor_type="current",
        color="cyan",
    )

    # Retrieve phasor properties for printing
    vs_phasor = pm.get_phasor("Vs")
    if vs_phasor:
        print("\n--- Vs Phasor properties ---")
        print(f"Name:      {vs_phasor['name']}")
        print(f"Magnitude: {vs_phasor['magnitude']:.2f}")
        print(f"Angle:     {vs_phasor['angle_deg']:.2f}°")
        print(f"End point: ({vs_phasor['end_x']:.2f}, {vs_phasor['end_y']:.2f})")

    # Save the diagram as an image
    pm.save("phasor_diagram.png")

    # Show the complete diagram
    pm.show()


if __name__ == "__main__":
    main()
