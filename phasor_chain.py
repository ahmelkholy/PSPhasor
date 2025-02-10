#!/usr/bin/env python3
"""
Phasor Chain Diagram Drawer

This script draws a chain of phasor vectors using matplotlib. Each vector
starts at the endpoint of the previous one. You can specify each vector via
the command-line using the --vector argument in the format:
    label,magnitude,angle

Where:
    - label: A string identifying the vector (e.g., 'V' for voltage, 'I' for current).
    - magnitude: The absolute value (length) of the vector.
    - angle: The angle in degrees measured from the positive x-axis.

Usage:
    python phasor_chain.py --start_x 0 --start_y 0 --vector "V,2.5,45" --vector "I,1.2,90"
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse


def draw_phasor_chain(start_x: float, start_y: float, vectors: list):
    """
    Draws a chain of phasor vectors.

    Parameters:
    - start_x: The starting x-coordinate.
    - start_y: The starting y-coordinate.
    - vectors: A list of tuples in the format (label, magnitude, angle_deg).
    """
    # Store the endpoints for plotting and boundaries for the axes
    x_points = [start_x]
    y_points = [start_y]

    current_x, current_y = start_x, start_y

    # Calculate endpoints for each vector in the chain
    endpoints = []  # list of tuples with vector start and end to annotate arrows
    for label, magnitude, angle in vectors:
        angle_rad = np.deg2rad(angle)
        end_x = current_x + magnitude * np.cos(angle_rad)
        end_y = current_y + magnitude * np.sin(angle_rad)
        endpoints.append((current_x, current_y, end_x, end_y, label))
        # Update current_x and current_y for next vector in the chain
        current_x, current_y = end_x, end_y
        x_points.append(end_x)
        y_points.append(end_y)

    # Setup plot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Draw arrows for each vector
    for sx, sy, ex, ey, label in endpoints:
        ax.annotate(
            "",
            xy=(ex, ey),
            xytext=(sx, sy),
            arrowprops=dict(arrowstyle="->", color="red", lw=2),
        )
        # Calculate the position for the label (midpoint offset slightly)
        mid_x = (sx + ex) / 2
        mid_y = (sy + ey) / 2
        ax.text(mid_x, mid_y, label, fontsize=12, color="blue", fontweight="bold")

    # Set limits dynamically with some buffer
    buffer = 1
    ax.set_xlim(min(x_points) - buffer, max(x_points) + buffer)
    ax.set_ylim(min(y_points) - buffer, max(y_points) + buffer)
    ax.set_aspect("equal")

    # Draw horizontal and vertical axes at the starting point for reference
    ax.axhline(y=start_y, color="gray", linewidth=0.5, linestyle="dashed")
    ax.axvline(x=start_x, color="gray", linewidth=0.5, linestyle="dashed")

    plt.title("Phasor Chain Diagram")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.grid(True)
    plt.show()


def parse_vector_argument(vector_str: str):
    """
    Parse a vector argument of the format 'label,magnitude,angle'
    and return a tuple: (label, magnitude, angle)
    """
    try:
        parts = vector_str.split(",")
        if len(parts) != 3:
            raise ValueError(
                "Each vector must have exactly 3 comma-separated values: label,magnitude,angle"
            )
        label = parts[0].strip()
        magnitude = float(parts[1].strip())
        angle = float(parts[2].strip())
        return (label, magnitude, angle)
    except Exception as e:
        raise argparse.ArgumentTypeError(f"Error parsing vector '{vector_str}': {e}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Draw a chain of phasor vectors (e.g., voltage and current) starting from a given point."
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
    parser.add_argument(
        "--vector",
        type=parse_vector_argument,
        action="append",
        required=True,
        help="Define a vector as 'label,magnitude,angle'. Can be used multiple times.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    draw_phasor_chain(args.start_x, args.start_y, args.vector)
