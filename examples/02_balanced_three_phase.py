"""Balanced three-phase voltage and current phasor diagram."""

from _common import output_path

from PSPhasor import DiagramStyle, PhasorManager


def main() -> None:
    """Draw balanced positive-sequence voltage and current phasors."""

    manager = PhasorManager(
        figsize=(7, 7),
        title="Balanced Three-Phase System",
        xlabel="Real component",
        ylabel="Reactive component",
        style=DiagramStyle(arrow_line_width=2.8, arrow_head_size=19.0),
    )

    manager.draw_three_phase(
        "V",
        magnitude=1.0,
        angle=0,
        labels=(r"$V_a$", r"$V_b$", r"$V_c$"),
        phasor_type="voltage",
    )
    manager.draw_three_phase(
        "I",
        magnitude=0.65,
        angle=-32,
        names=("Ia", "Ib", "Ic"),
        labels=(r"$I_a$", r"$I_b$", r"$I_c$"),
        phasor_type="current",
        colors=("#8c1d18", "#c0392b", "#e67e22"),
    )

    manager.save(output_path("02_balanced_three_phase.png"))


if __name__ == "__main__":
    main()
