"""Single-phase load phasor diagram."""

from _common import output_path

from PSPhasor import DiagramStyle, PhasorManager


def main() -> None:
    """Draw a source, load voltage, voltage drop, and lagging current."""

    manager = PhasorManager(
        figsize=(9, 5),
        title="Single-Phase Load Phasor Diagram",
        xlabel="Real component",
        ylabel="Reactive component",
        style=DiagramStyle(arrow_line_width=3.0, arrow_head_size=20.0),
    )

    manager.draw_phasor("Vs", magnitude=10, angle=0, label=r"$V_s$")
    manager.draw_phasor(
        "V_drop",
        magnitude=2,
        angle=150,
        start_ref="Vs",
        color="#9467bd",
        label=r"$V_{drop}$",
    )
    manager.draw_phasor(
        "Vr",
        start_x=0,
        start_y=0,
        end_x=8.27,
        end_y=1.0,
        color="#2ca02c",
        label=r"$V_R$",
    )
    manager.draw_phasor(
        "I_load",
        magnitude=4,
        angle=-30,
        phasor_type="current",
        label=r"$I_L$",
    )

    manager.save(output_path("01_basic_load.png"))


if __name__ == "__main__":
    main()
