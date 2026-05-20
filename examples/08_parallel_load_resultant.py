"""Parallel-load current resultant with power-factor angle marker."""

from _common import output_path

from PSPhasor import DiagramStyle, PhasorManager


def main() -> None:
    """Draw branch currents and their total current resultant."""

    manager = PhasorManager(
        figsize=(9, 6),
        title="Parallel Loads: Branch Currents and Resultant",
        xlabel="Current real component",
        ylabel="Current reactive component",
        style=DiagramStyle(arrow_line_width=2.8, arrow_head_size=19.0),
    )

    manager.draw_phasor(
        "Vref",
        magnitude=6.0,
        angle=0,
        phasor_type="voltage",
        color="#1f77b4",
        label=r"$V_{ref}$",
        alpha=0.55,
    )
    manager.draw_phasor(
        "I_motor",
        magnitude=3.4,
        angle=-38,
        phasor_type="current",
        color="#d62728",
        label=r"$I_{motor}$",
    )
    manager.draw_phasor(
        "I_lighting",
        magnitude=1.8,
        angle=-8,
        phasor_type="current",
        color="#ff7f0e",
        label=r"$I_{lighting}$",
    )
    manager.draw_phasor(
        "I_capacitor",
        magnitude=1.2,
        angle=90,
        phasor_type="current",
        color="#2ca02c",
        label=r"$I_C$",
    )
    manager.draw_resultant(
        "I_total",
        ["I_motor", "I_lighting", "I_capacitor"],
        phasor_type="current",
        color="#111111",
        label=r"$I_{total}$",
        line_width=3.8,
    )
    manager.add_angle_marker("Vref", "I_total", label=r"$\phi$", radius=1.1)
    manager.add_legend("upper right")
    manager.save(output_path("08_parallel_load_resultant.png"))
    manager.save_csv(output_path("08_parallel_load_resultant.csv"))


if __name__ == "__main__":
    main()
