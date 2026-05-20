"""Complete PSPhasor example."""

from PSPhasor import PhasorManager


def main() -> None:
    """Draw and save a small referenced phasor diagram."""

    manager = PhasorManager(figsize=(9, 5), title="PSPhasor example")

    source = manager.draw_phasor(
        "Vs",
        magnitude=10,
        angle=0,
        label_offset=(0.0, 0.25),
    )
    manager.draw_phasor(
        "Vl",
        magnitude=2,
        angle=150,
        start_ref="Vs",
        ref_point="end",
        phasor_type="voltage",
        color="tab:purple",
    )
    manager.draw_phasor(
        "Vr",
        start_x=0,
        start_y=0,
        end_x=8.27,
        end_y=1.0,
        phasor_type="voltage",
        color="tab:green",
    )
    manager.draw_phasor(
        "I",
        magnitude=4,
        angle=-30,
        phasor_type="current",
        label="I (current)",
        label_offset=(0.65, 0.15),
    )

    print(f"{source.name}: {source.magnitude:.2f} at {source.angle_deg:.1f} deg")
    print(f"End point: ({source.end_x:.2f}, {source.end_y:.2f})")
    manager.save("phasor_diagram.png")
    manager.show()


if __name__ == "__main__":
    main()
