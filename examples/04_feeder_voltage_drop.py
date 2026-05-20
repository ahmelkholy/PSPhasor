"""Distribution feeder voltage-drop phasor diagram."""

from _common import output_path

from PSPhasor import DiagramStyle, PhasorManager


def main() -> None:
    """Draw voltage-drop components for a lagging load on an R+jX feeder."""

    manager = PhasorManager(
        figsize=(10, 6),
        title="Feeder Voltage Drop: Vs = Vr + I(R+jX)",
        xlabel="Voltage real component",
        ylabel="Voltage reactive component",
        style=DiagramStyle(arrow_line_width=3.0, arrow_head_size=20.0),
    )

    receiving_voltage = 11.0 + 0.0j
    current = 2.2 - 1.4j
    feeder_impedance = 0.45 + 0.75j
    resistive_drop = current * feeder_impedance.real
    reactive_drop = current * 1j * feeder_impedance.imag
    total_drop = resistive_drop + reactive_drop
    sending_voltage = receiving_voltage + total_drop

    manager.draw_complex(
        "Vr",
        receiving_voltage,
        phasor_type="voltage",
        color="#2ca02c",
        label=r"$V_R$",
    )
    manager.draw_complex(
        "IR",
        resistive_drop,
        start_ref="Vr",
        phasor_type="voltage",
        color="#ff7f0e",
        label=r"$IR$",
    )
    manager.draw_complex(
        "IX",
        reactive_drop,
        start_ref="IR",
        phasor_type="voltage",
        color="#9467bd",
        label=r"$jIX$",
    )
    manager.draw_complex(
        "Vs",
        sending_voltage,
        phasor_type="voltage",
        color="#1f77b4",
        label=r"$V_s$",
        alpha=0.88,
    )
    manager.draw_complex(
        "I",
        current,
        scale=1.2,
        phasor_type="current",
        color="#d62728",
        label=r"$I_{load}$",
    )

    manager.save(output_path("04_feeder_voltage_drop.png"))


if __name__ == "__main__":
    main()
