"""Engineering-style PSPhasor example."""

from PSPhasor import DiagramStyle, PhasorManager


def main() -> None:
    """Draw and save a power-system phasor diagram."""

    manager = PhasorManager(
        figsize=(9, 5),
        title="Single-phase load phasor diagram",
        xlabel="Real component",
        ylabel="Reactive component",
        style=DiagramStyle(arrow_line_width=3.0, arrow_head_size=20.0),
    )

    source = manager.draw_phasor(
        "Vs",
        magnitude=10,
        angle=0,
        label=r"$V_s$",
    )
    manager.draw_phasor(
        "Vdrop",
        magnitude=2,
        angle=150,
        start_ref="Vs",
        ref_point="end",
        phasor_type="voltage",
        color="#9467bd",
        label=r"$V_{drop}$",
    )
    manager.draw_phasor(
        "Vr",
        start_x=0,
        start_y=0,
        end_x=8.27,
        end_y=1.0,
        phasor_type="voltage",
        color="#2ca02c",
        label=r"$V_R$",
    )
    manager.draw_phasor(
        "Iload",
        magnitude=4,
        angle=-30,
        phasor_type="current",
        label=r"$I_L$",
    )

    print(f"{source.name}: {source.magnitude:.2f} at {source.angle_deg:.1f} deg")
    print(f"End point: ({source.end_x:.2f}, {source.end_y:.2f})")
    manager.save("phasor_diagram.png")
    manager.show()


if __name__ == "__main__":
    main()
