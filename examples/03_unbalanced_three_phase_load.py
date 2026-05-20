"""Unbalanced three-phase load current phasor diagram."""

from _common import output_path

from PSPhasor import DiagramStyle, PhasorManager


def main() -> None:
    """Draw unbalanced phase currents and the resulting neutral current."""

    manager = PhasorManager(
        figsize=(8, 8),
        title="Unbalanced Three-Phase Load Currents",
        xlabel="Real current component",
        ylabel="Reactive current component",
        style=DiagramStyle(arrow_line_width=2.9, arrow_head_size=19.0),
    )

    currents = {
        "Ia": (95.0, -18.0, "#1f77b4", r"$I_a$"),
        "Ib": (72.0, -138.0, "#d62728", r"$I_b$"),
        "Ic": (58.0, 104.0, "#2ca02c", r"$I_c$"),
    }
    total = 0j
    for name, (magnitude, angle, color, label) in currents.items():
        phasor = manager.draw_phasor(
            name,
            magnitude=magnitude,
            angle=angle,
            phasor_type="current",
            color=color,
            label=label,
        )
        total += phasor.value

    manager.draw_complex(
        "In",
        -total,
        phasor_type="current",
        color="#111111",
        label=r"$I_n=-(I_a+I_b+I_c)$",
    )

    manager.save(output_path("03_unbalanced_three_phase_load.png"))


if __name__ == "__main__":
    main()
