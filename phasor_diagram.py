#!/usr/bin/env python3
"""
Phasor Diagram Drawer

This script draws a phasor diagram using matplotlib. The phasor is drawn based on
parameters provided by the user via command-line arguments:
- Magnitude (absolute value)
- Angle (in degrees)
- Starting point (x, y coordinates)

Usage:
    python phasor_diagram.py --magnitude 2.0 --angle 45 --start_x 1 --start_y 1
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse


def draw_phasor(magnitude: float, angle_deg: float, start_x: float, start_y: float):
    """
    Draws a phasor diagram where the phasor starts at (start_x, start_y) and extends
    with a given magnitude and angle.

    Parameters:
    - magnitude: The length of the phasor.
    - angle_deg: The angle in degrees from the positive real axis.
    - start_x: The x-coordinate of the start point.
    - start_y: The y-coordinate of the start point.
    """
    angle_rad = np.deg2rad(angle_deg)

    # Calculate end point of the phasor vector
    end_x = start_x + magnitude * np.cos(angle_rad)
    end_y = start_y + magnitude * np.sin(angle_rad)

    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw a circle centered at the start point with radius equal to magnitude (for reference)
    circle = plt.Circle(
        (start_x, start_y), magnitude, fill=False, color="gray", linestyle="dashed"
    )
    ax.add_artist(circle)

    # Draw horizontal and vertical axes through the start point
    xlims = [start_x - magnitude - 1, start_x + magnitude + 1]
    ylims = [start_y - magnitude - 1, start_y + magnitude + 1]
    ax.plot([xlims[0], xlims[1]], [start_y, start_y], color="black", linewidth=0.5)
    ax.plot([start_x, start_x], [ylims[0], ylims[1]], color="black", linewidth=0.5)

    # Draw the phasor as an arrow from the start point to the end point
    ax.annotate(
        "",
        xy=(end_x, end_y),
        xytext=(start_x, start_y),
        arrowprops=dict(arrowstyle="->", color="red", lw=2),
    )

    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.set_aspect("equal")

    # Title and labels
    plt.title(
        "Phasor Diagram (Magnitude = {}, Angle = {}°)".format(magnitude, angle_deg)
    )
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(True)
    plt.show()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Draw a phasor diagram with a given magnitude, angle, and starting point."
    )
    parser.add_argument(
        "--magnitude",
        type=float,
        required=True,
        help="The magnitude (absolute value) of the phasor",
    )
    parser.add_argument(
        "--angle", type=float, required=True, help="The angle of the phasor in degrees"
    )
    parser.add_argument(
        "--start_x",
        type=float,
        default=0.0,
        help="The x-coordinate of the starting point (default: 0)",
    )
    parser.add_argument(
        "--start_y",
        type=float,
        default=0.0,
        help="The y-coordinate of the starting point (default: 0)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    draw_phasor(args.magnitude, args.angle, args.start_x, args.start_y)
