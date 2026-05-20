"""Fault-current sequence-component phasor diagram."""

from _common import output_path

from PSPhasor import DiagramStyle, PhasorManager

A = complex(-0.5, 0.8660254037844386)


def main() -> None:
    """Draw sequence components and reconstructed phase fault currents."""

    manager = PhasorManager(
        figsize=(8, 8),
        title="Fault Current Sequence Components",
        xlabel="Current real component",
        ylabel="Current reactive component",
        style=DiagramStyle(arrow_line_width=2.7, arrow_head_size=18.0),
    )

    i0 = 0.9 + 0.1j
    i1 = 4.8 - 1.0j
    i2 = 1.6 + 0.8j

    ia = i0 + i1 + i2
    ib = i0 + A**2 * i1 + A * i2
    ic = i0 + A * i1 + A**2 * i2

    manager.draw_complex(
        "I0",
        i0,
        phasor_type="current",
        color="#7f7f7f",
        label=r"$I_0$",
    )
    manager.draw_complex(
        "I1",
        i1,
        phasor_type="current",
        color="#1f77b4",
        label=r"$I_1$",
    )
    manager.draw_complex(
        "I2",
        i2,
        phasor_type="current",
        color="#9467bd",
        label=r"$I_2$",
    )
    manager.draw_complex(
        "Ia",
        ia,
        phasor_type="current",
        color="#d62728",
        label=r"$I_a$",
    )
    manager.draw_complex(
        "Ib",
        ib,
        phasor_type="current",
        color="#2ca02c",
        label=r"$I_b$",
        alpha=0.82,
    )
    manager.draw_complex(
        "Ic",
        ic,
        phasor_type="current",
        color="#ff7f0e",
        label=r"$I_c$",
        alpha=0.82,
    )

    manager.save(output_path("05_fault_current_sequence_components.png"))


if __name__ == "__main__":
    main()
