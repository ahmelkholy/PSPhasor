"""Power triangle phasor diagram."""

import math

from _common import output_path

from PSPhasor import DiagramStyle, PhasorManager


def main() -> None:
    """Draw real, reactive, and apparent power for a lagging load."""

    manager = PhasorManager(
        figsize=(8, 6),
        title="Power Triangle for Lagging Power-Factor Load",
        xlabel="Real power P",
        ylabel="Reactive power Q",
        style=DiagramStyle(arrow_line_width=3.0, arrow_head_size=20.0),
    )

    apparent_power = 100.0
    power_factor = 0.82
    phi = math.degrees(math.acos(power_factor))
    real_power = apparent_power * power_factor
    reactive_power = apparent_power * math.sin(math.radians(phi))

    manager.draw_phasor(
        "P",
        magnitude=real_power,
        angle=0,
        phasor_type="power",
        color="#2ca02c",
        label=r"$P$",
    )
    manager.draw_phasor(
        "Q",
        magnitude=reactive_power,
        angle=90,
        start_ref="P",
        phasor_type="power",
        color="#d62728",
        label=r"$Q$",
    )
    manager.draw_phasor(
        "S",
        magnitude=apparent_power,
        angle=phi,
        phasor_type="power",
        color="#1f77b4",
        label=rf"$S,\ \phi={phi:.1f}^\circ$",
    )

    manager.save(output_path("06_power_triangle.png"))


if __name__ == "__main__":
    main()
