import csv
import math
from contextlib import suppress
from pathlib import Path

import pytest

from PSPhasor import (
    AngleAnnotation,
    DiagramStyle,
    PhasorManager,
    phase_components,
    polar,
    symmetrical_components,
    to_polar,
)


def test_draw_polar_phasor_stores_geometry() -> None:
    manager = PhasorManager()

    phasor = manager.draw_phasor("Vs", magnitude=10, angle=30)

    assert phasor.name == "Vs"
    assert phasor.magnitude == pytest.approx(10)
    assert phasor.angle_deg == pytest.approx(30)
    assert phasor.end_x == pytest.approx(10 * math.cos(math.radians(30)))
    assert phasor.end_y == pytest.approx(10 * math.sin(math.radians(30)))
    assert phasor["magnitude"] == pytest.approx(10)
    assert phasor["angle_deg"] == pytest.approx(30)


def test_reference_phasor_end_point() -> None:
    manager = PhasorManager()
    manager.draw_phasor("Vs", magnitude=10, angle=0)

    drop = manager.draw_phasor(
        "Vl",
        magnitude=2,
        angle=180,
        start_ref="Vs",
        ref_point="end",
    )

    assert drop.start == pytest.approx((10, 0))
    assert drop.end == pytest.approx((8, 0))


def test_explicit_cartesian_coordinates() -> None:
    manager = PhasorManager()

    phasor = manager.draw_phasor("Vr", start_x=1, start_y=2, end_x=4, end_y=6)

    assert phasor.start == pytest.approx((1, 2))
    assert phasor.end == pytest.approx((4, 6))
    assert phasor.dx == pytest.approx(3)
    assert phasor.dy == pytest.approx(4)
    assert phasor.magnitude == pytest.approx(5)
    assert phasor.value == pytest.approx(complex(3, 4))


def test_draw_complex_uses_real_and_imaginary_components() -> None:
    manager = PhasorManager()

    phasor = manager.draw_complex("V", 3 + 4j, scale=2)

    assert phasor.start == pytest.approx((0, 0))
    assert phasor.end == pytest.approx((6, 8))
    assert phasor.magnitude == pytest.approx(10)


def test_polar_helpers_round_trip_complex_value() -> None:
    value = polar(10, -30)
    magnitude, angle = to_polar(value)

    assert value.real == pytest.approx(10 * math.cos(math.radians(-30)))
    assert value.imag == pytest.approx(10 * math.sin(math.radians(-30)))
    assert magnitude == pytest.approx(10)
    assert angle == pytest.approx(-30)


def test_symmetrical_components_round_trip_phase_values() -> None:
    phase_values = (
        7.3 - 0.1j,
        -2.7 - 2.8j,
        -0.7 + 3.0j,
    )

    sequence_values = symmetrical_components(*phase_values)
    reconstructed = phase_components(*sequence_values)

    assert reconstructed[0] == pytest.approx(phase_values[0])
    assert reconstructed[1] == pytest.approx(phase_values[1])
    assert reconstructed[2] == pytest.approx(phase_values[2])


def test_draw_three_phase_positive_sequence() -> None:
    manager = PhasorManager()

    phases = manager.draw_three_phase("V", magnitude=1, angle=0)

    assert [phase.name for phase in phases] == ["Va", "Vb", "Vc"]
    assert phases[0].angle_deg == pytest.approx(0)
    assert phases[1].angle_deg == pytest.approx(-120)
    assert phases[2].angle_deg == pytest.approx(120)


def test_draw_line_to_line_voltage_from_phase_voltages() -> None:
    manager = PhasorManager()
    manager.draw_three_phase("V", magnitude=1, angle=0)

    vab = manager.draw_line_to_line("Vab", "Va", "Vb")

    assert vab.value.real == pytest.approx(1.5)
    assert vab.value.imag == pytest.approx(math.sqrt(3) / 2)
    assert vab.magnitude == pytest.approx(math.sqrt(3))
    assert vab.angle_deg == pytest.approx(30)


def test_draw_resultant_sums_existing_phasors() -> None:
    manager = PhasorManager()
    manager.draw_complex("I1", 3 + 1j, phasor_type="current")
    manager.draw_complex("I2", -1 + 2j, phasor_type="current")

    resultant = manager.draw_resultant(
        "Itotal",
        ["I1", "I2"],
        phasor_type="current",
    )

    assert resultant.value == pytest.approx(2 + 3j)
    assert resultant["metadata"]["components"] == ["I1", "I2"]


def test_angle_marker_is_stored_and_removed_with_phasor() -> None:
    manager = PhasorManager()
    manager.draw_phasor("V", magnitude=1, angle=0)
    manager.draw_phasor("I", magnitude=1, angle=-30)

    marker = manager.add_angle_marker("V", "I", label=r"$\phi$")

    assert isinstance(marker, AngleAnnotation)
    assert len(manager.angle_annotations) == 1

    manager.remove_phasor("I")

    assert manager.get_phasor("I") is None
    assert len(manager.angle_annotations) == 0


def test_remove_unknown_phasor_raises_value_error() -> None:
    manager = PhasorManager()

    with pytest.raises(ValueError, match="does not exist"):
        manager.remove_phasor("missing")


def test_custom_diagram_style_controls_label_defaults() -> None:
    style = DiagramStyle(label_box=False, arrow_line_width=4.0)
    manager = PhasorManager(style=style)

    phasor = manager.draw_phasor("Vs", magnitude=1, angle=0)

    assert phasor.line_width == pytest.approx(4.0)


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"magnitude": 1}, "Provide either"),
        ({"angle": 0}, "Provide either"),
        ({"end_x": 1}, "Both end_x and end_y"),
        ({"magnitude": 1, "angle": 0, "end_x": 1, "end_y": 0}, "either"),
        ({"magnitude": -1, "angle": 0}, "magnitude"),
    ],
)
def test_invalid_geometry_raises_value_error(
    kwargs: dict[str, float],
    message: str,
) -> None:
    manager = PhasorManager()

    with pytest.raises(ValueError, match=message):
        manager.draw_phasor("bad", **kwargs)


def test_unknown_reference_raises_value_error() -> None:
    manager = PhasorManager()

    with pytest.raises(ValueError, match="does not exist"):
        manager.draw_phasor("Vl", magnitude=2, angle=150, start_ref="missing")


def test_duplicate_name_raises_value_error() -> None:
    manager = PhasorManager()
    manager.draw_phasor("Vs", magnitude=10, angle=0)

    with pytest.raises(ValueError, match="already exists"):
        manager.draw_phasor("Vs", magnitude=5, angle=90)


def test_save_returns_output_path() -> None:
    manager = PhasorManager()
    manager.draw_phasor("Vs", magnitude=10, angle=0)
    output = Path("tests/test-output/diagram.png")

    try:
        saved_path = manager.save(output)

        assert saved_path == output
        assert output.exists()
        assert output.stat().st_size > 0
    finally:
        with suppress(FileNotFoundError):
            output.unlink()
        with suppress(OSError):
            output.parent.rmdir()


def test_save_csv_exports_engineering_records() -> None:
    manager = PhasorManager()
    manager.draw_phasor("Vs", magnitude=10, angle=0, label=r"$V_s$")
    output = Path("tests/test-output/phasors.csv")

    try:
        saved_path = manager.save_csv(output)

        assert saved_path == output
        with output.open("r", newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        assert rows[0]["name"] == "Vs"
        assert rows[0]["type"] == "voltage"
        assert float(rows[0]["magnitude"]) == pytest.approx(10)
        assert rows[0]["label"] == r"$V_s$"
    finally:
        with suppress(FileNotFoundError):
            output.unlink()
        with suppress(OSError):
            output.parent.rmdir()
