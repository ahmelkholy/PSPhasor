"""Minimal PSPhasor example."""

from PSPhasor import PhasorManager


def main() -> None:
    """Create a two-phasor diagram."""

    manager = PhasorManager(figsize=(8, 4), title="Minimal phasor diagram")
    manager.draw_phasor("Vs", magnitude=10, angle=0, label=r"$V_s$")
    manager.draw_phasor(
        "Iload",
        magnitude=4,
        angle=-35,
        phasor_type="current",
        label=r"$I_L$",
    )
    manager.show()


if __name__ == "__main__":
    main()
