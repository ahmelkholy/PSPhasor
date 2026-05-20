"""Line-to-line voltage construction from phase voltages."""

from _common import output_path

from PSPhasor import DiagramStyle, PhasorManager


def main() -> None:
    """Draw phase and line-to-line voltages for a balanced system."""

    manager = PhasorManager(
        figsize=(8, 8),
        title="Phase and Line-to-Line Voltages",
        xlabel="Voltage real component",
        ylabel="Voltage reactive component",
        style=DiagramStyle(arrow_line_width=2.7, arrow_head_size=18.0),
    )

    manager.draw_three_phase(
        "V",
        magnitude=1.0,
        angle=0,
        labels=(r"$V_a$", r"$V_b$", r"$V_c$"),
        phasor_type="voltage",
    )
    manager.draw_line_to_line(
        "Vab",
        "Va",
        "Vb",
        color="#9467bd",
        label=r"$V_{ab}=V_a-V_b$",
        alpha=0.86,
    )
    manager.draw_line_to_line(
        "Vbc",
        "Vb",
        "Vc",
        color="#8c564b",
        label=r"$V_{bc}=V_b-V_c$",
        alpha=0.86,
    )
    manager.draw_line_to_line(
        "Vca",
        "Vc",
        "Va",
        color="#e377c2",
        label=r"$V_{ca}=V_c-V_a$",
        alpha=0.86,
    )
    manager.add_angle_marker("Va", "Vab", label=r"$30^\circ$", radius=0.42)
    manager.add_legend("upper right")
    manager.save(output_path("07_line_to_line_voltages.png"))
    manager.save_csv(output_path("07_line_to_line_voltages.csv"))


if __name__ == "__main__":
    main()
