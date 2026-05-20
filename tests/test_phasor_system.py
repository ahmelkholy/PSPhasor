import math
from contextlib import suppress
from pathlib import Path

import pytest

from PSPhasor import DiagramStyle, PhasorManager


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


def test_draw_three_phase_positive_sequence() -> None:
    manager = PhasorManager()

    phases = manager.draw_three_phase("V", magnitude=1, angle=0)

    assert [phase.name for phase in phases] == ["Va", "Vb", "Vc"]
    assert phases[0].angle_deg == pytest.approx(0)
    assert phases[1].angle_deg == pytest.approx(-120)
    assert phases[2].angle_deg == pytest.approx(120)


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
