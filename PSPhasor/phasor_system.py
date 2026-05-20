"""Core phasor drawing tools for PSPhasor."""

from __future__ import annotations

import math
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

ReferencePoint = Literal["start", "end"]
SequenceType = Literal["abc", "acb", "positive", "negative"]
LabelOffset = float | tuple[float, float] | None

DEFAULT_COLORS: dict[str, str] = {
    "voltage": "#1f77b4",
    "current": "#d62728",
    "power": "#2ca02c",
}
THREE_PHASE_COLORS: tuple[str, str, str] = ("#1f77b4", "#d62728", "#2ca02c")


@dataclass(frozen=True)
class DiagramStyle:
    """Engineering-oriented rendering defaults for phasor diagrams."""

    background_color: str = "white"
    axis_color: str = "#111111"
    major_grid_color: str = "#b8bcc2"
    minor_grid_color: str = "#e1e4e8"
    major_grid_width: float = 0.7
    minor_grid_width: float = 0.35
    axis_width: float = 1.1
    arrow_line_width: float = 2.8
    arrow_head_size: float = 18.0
    label_font_size: int = 10
    label_font_weight: str = "bold"
    label_box: bool = True
    label_box_alpha: float = 0.85
    auto_label_offset_fraction: float = 0.045


@dataclass(frozen=True)
class Phasor(Mapping[str, Any]):
    """A drawn phasor stored in Cartesian coordinates.

    The class exposes typed attributes for new code and implements the mapping
    protocol so older dictionary-style reads such as ``phasor["magnitude"]``
    continue to work.
    """

    name: str
    start_x: float
    start_y: float
    end_x: float
    end_y: float
    phasor_type: str = "voltage"
    color: str = DEFAULT_COLORS["voltage"]
    label: str | None = None
    label_offset: LabelOffset = None
    line_width: float | None = None
    alpha: float = 1.0
    linestyle: str = "-"
    metadata: Mapping[str, Any] = field(default_factory=dict, repr=False)

    @property
    def start(self) -> tuple[float, float]:
        """Return the start point as ``(x, y)``."""

        return self.start_x, self.start_y

    @property
    def end(self) -> tuple[float, float]:
        """Return the end point as ``(x, y)``."""

        return self.end_x, self.end_y

    @property
    def dx(self) -> float:
        """Return the phasor's real-axis component."""

        return self.end_x - self.start_x

    @property
    def dy(self) -> float:
        """Return the phasor's imaginary-axis component."""

        return self.end_y - self.start_y

    @property
    def value(self) -> complex:
        """Return the phasor value as a complex number."""

        return complex(self.dx, self.dy)

    @property
    def magnitude(self) -> float:
        """Return the phasor magnitude."""

        return abs(self.value)

    @property
    def angle_deg(self) -> float:
        """Return the phasor angle in degrees."""

        return math.degrees(math.atan2(self.dy, self.dx))

    def as_dict(self) -> dict[str, Any]:
        """Return a dictionary representation of the phasor."""

        return {
            "name": self.name,
            "type": self.phasor_type,
            "phasor_type": self.phasor_type,
            "start_x": self.start_x,
            "start_y": self.start_y,
            "end_x": self.end_x,
            "end_y": self.end_y,
            "dx": self.dx,
            "dy": self.dy,
            "value": self.value,
            "magnitude": self.magnitude,
            "angle": self.angle_deg,
            "angle_deg": self.angle_deg,
            "color": self.color,
            "label": self.label or self.name,
            "metadata": dict(self.metadata),
        }

    def __getitem__(self, key: str) -> Any:
        """Return a value from the dictionary representation."""

        return self.as_dict()[key]

    def __iter__(self) -> Iterator[str]:
        """Iterate over dictionary representation keys."""

        return iter(self.as_dict())

    def __len__(self) -> int:
        """Return the number of dictionary representation keys."""

        return len(self.as_dict())


class PhasorManager:
    """Create, store, and render phasor diagrams with Matplotlib.

    The manager is suitable for simple teaching diagrams and larger power-system
    studies because it supports polar input, complex-number input, referenced
    phasors, and balanced three-phase sets.
    """

    def __init__(
        self,
        figsize: tuple[float, float] = (9.0, 5.0),
        title: str = "Phasor Diagram",
        xlabel: str = "Real axis",
        ylabel: str = "Imaginary axis",
        style: DiagramStyle | None = None,
    ) -> None:
        """Initialize a phasor diagram manager.

        Args:
            figsize: Matplotlib figure size in inches.
            title: Plot title.
            xlabel: Label for the horizontal axis.
            ylabel: Label for the vertical axis.
            style: Optional engineering plot style.
        """

        self.fig: Figure
        self.ax: Axes
        self.fig, self.ax = plt.subplots(figsize=figsize, constrained_layout=True)
        self.phasors: dict[str, Phasor] = {}
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.style = style or DiagramStyle()
        self.setup_plot()
        self.fit()

    def setup_plot(self) -> None:
        """Reset plot styling while preserving stored phasor data."""

        self.ax.set_facecolor(self.style.background_color)
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.minorticks_on()
        self._apply_grid(True)
        self.ax.axhline(
            y=0.0,
            color=self.style.axis_color,
            linewidth=self.style.axis_width,
            zorder=1,
        )
        self.ax.axvline(
            x=0.0,
            color=self.style.axis_color,
            linewidth=self.style.axis_width,
            zorder=1,
        )

    def _apply_grid(self, visible: bool) -> None:
        """Apply engineering grid styling."""

        self.ax.grid(
            visible,
            which="major",
            linestyle="--",
            linewidth=self.style.major_grid_width,
            color=self.style.major_grid_color,
            alpha=0.9,
        )
        self.ax.grid(
            visible,
            which="minor",
            linestyle=":",
            linewidth=self.style.minor_grid_width,
            color=self.style.minor_grid_color,
            alpha=0.8,
        )

    def draw_phasor(
        self,
        name: str,
        magnitude: float | None = None,
        angle: float | None = None,
        *,
        start_ref: str = "abs",
        start_x: float = 0.0,
        start_y: float = 0.0,
        end_x: float | None = None,
        end_y: float | None = None,
        ref_point: ReferencePoint = "end",
        phasor_type: str = "voltage",
        color: str | None = None,
        label_offset: LabelOffset = None,
        arrow_width: float | None = None,
        line_width: float | None = None,
        label: str | None = None,
        alpha: float = 1.0,
        linestyle: str = "-",
        metadata: Mapping[str, Any] | None = None,
    ) -> Phasor:
        """Draw a phasor and store its geometry.

        Define a phasor either by ``magnitude`` and ``angle`` or by explicit
        ``end_x`` and ``end_y`` coordinates. The start point can be absolute or
        referenced from the start or end of a previously drawn phasor.

        Args:
            name: Unique phasor identifier.
            magnitude: Phasor length when using polar input.
            angle: Phasor angle in degrees when using polar input.
            start_ref: ``"abs"`` for coordinates, or another phasor name.
            start_x: Absolute start x-coordinate.
            start_y: Absolute start y-coordinate.
            end_x: Explicit end x-coordinate.
            end_y: Explicit end y-coordinate.
            ref_point: Referenced phasor point, either ``"start"`` or ``"end"``.
            phasor_type: Type label used for default color selection.
            color: Matplotlib-compatible color. Defaults by phasor type.
            label_offset: Scalar or ``(x, y)`` label offset from the midpoint.
                Use ``None`` for automatic engineering label placement.
            arrow_width: Backward-compatible alias for line width.
            line_width: Arrow shaft width in points.
            label: Optional display label. Defaults to ``name``.
            alpha: Arrow and label opacity.
            linestyle: Matplotlib line style for the arrow shaft.
            metadata: Optional user data stored on the returned phasor.

        Returns:
            The stored :class:`Phasor`.

        Raises:
            ValueError: If the phasor definition is incomplete or invalid.
        """

        phasor_name = _validate_name(name)
        if phasor_name in self.phasors:
            raise ValueError(f"Phasor '{phasor_name}' already exists.")

        start = self._resolve_start(start_ref, start_x, start_y, ref_point)
        end = _resolve_end(start, magnitude, angle, end_x, end_y)
        normalized_type = _normalize_phasor_type(phasor_type)
        draw_color = color or DEFAULT_COLORS.get(normalized_type, "#6f7782")
        resolved_line_width = _resolve_line_width(
            arrow_width,
            line_width,
            self.style.arrow_line_width,
        )

        phasor = Phasor(
            name=phasor_name,
            start_x=start[0],
            start_y=start[1],
            end_x=end[0],
            end_y=end[1],
            phasor_type=normalized_type,
            color=draw_color,
            label=label,
            label_offset=label_offset,
            line_width=resolved_line_width,
            alpha=_coerce_unit_interval(alpha, "alpha"),
            linestyle=linestyle,
            metadata=metadata or {},
        )

        self.phasors[phasor.name] = phasor
        self.render()
        return phasor

    def draw_complex(
        self,
        name: str,
        value: complex,
        *,
        scale: float = 1.0,
        start_ref: str = "abs",
        start_x: float = 0.0,
        start_y: float = 0.0,
        ref_point: ReferencePoint = "end",
        phasor_type: str = "voltage",
        color: str | None = None,
        label_offset: LabelOffset = None,
        label: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> Phasor:
        """Draw a phasor from a complex value.

        Args:
            name: Unique phasor identifier.
            value: Complex phasor value where real is the horizontal component
                and imaginary is the vertical component.
            scale: Multiplier applied before drawing.
            start_ref: ``"abs"`` for coordinates, or another phasor name.
            start_x: Absolute start x-coordinate.
            start_y: Absolute start y-coordinate.
            ref_point: Referenced phasor point, either ``"start"`` or ``"end"``.
            phasor_type: Type label used for default color selection.
            color: Matplotlib-compatible color. Defaults by phasor type.
            label_offset: Optional label offset. ``None`` enables auto placement.
            label: Optional display label. Defaults to ``name``.
            metadata: Optional user data stored on the returned phasor.

        Returns:
            The stored :class:`Phasor`.
        """

        start = self._resolve_start(start_ref, start_x, start_y, ref_point)
        value = _coerce_complex(value, "value")
        scale = _coerce_float(scale, "scale")
        return self.draw_phasor(
            name,
            start_x=start[0],
            start_y=start[1],
            end_x=start[0] + value.real * scale,
            end_y=start[1] + value.imag * scale,
            phasor_type=phasor_type,
            color=color,
            label_offset=label_offset,
            label=label,
            metadata=metadata,
        )

    def draw_three_phase(
        self,
        prefix: str,
        magnitude: float,
        *,
        angle: float = 0.0,
        sequence: SequenceType = "abc",
        names: Sequence[str] | None = None,
        labels: Sequence[str] | None = None,
        phasor_type: str = "voltage",
        colors: Sequence[str] = THREE_PHASE_COLORS,
        label_offset: LabelOffset = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> list[Phasor]:
        """Draw a balanced three-phase phasor set.

        Args:
            prefix: Name prefix, such as ``"V"`` or ``"I"``.
            magnitude: Phase magnitude.
            angle: Phase-a angle in degrees.
            sequence: ``"abc"``/``"positive"`` or ``"acb"``/``"negative"``.
            names: Optional exact phasor names.
            labels: Optional exact display labels.
            phasor_type: Type label used for default styling.
            colors: Three Matplotlib-compatible colors.
            label_offset: Optional shared label offset. ``None`` enables auto.
            metadata: Optional user data stored on each returned phasor.

        Returns:
            Stored phasors for phases a, b, and c.
        """

        prefix = _validate_name(prefix)
        magnitude = _coerce_float(magnitude, "magnitude")
        base_angle = _coerce_float(angle, "angle")
        phase_angles = _phase_angles(base_angle, sequence)
        phase_names = list(names or [f"{prefix}a", f"{prefix}b", f"{prefix}c"])
        phase_labels = list(labels or _default_phase_labels(prefix))

        if len(phase_names) != 3:
            raise ValueError("names must contain exactly three values.")
        if len(phase_labels) != 3:
            raise ValueError("labels must contain exactly three values.")
        if len(colors) != 3:
            raise ValueError("colors must contain exactly three values.")

        phasors: list[Phasor] = []
        for phase_name, phase_label, phase_angle, phase_color in zip(
            phase_names,
            phase_labels,
            phase_angles,
            colors,
            strict=True,
        ):
            phasors.append(
                self.draw_phasor(
                    phase_name,
                    magnitude=magnitude,
                    angle=phase_angle,
                    phasor_type=phasor_type,
                    color=phase_color,
                    label=phase_label,
                    label_offset=label_offset,
                    metadata=metadata,
                )
            )
        return phasors

    def get_phasor(self, name: str) -> Phasor | None:
        """Return a phasor by name, or ``None`` if it does not exist."""

        return self.phasors.get(name)

    def clear(self) -> None:
        """Clear all phasors and reset the plot."""

        self.phasors.clear()
        self.render()

    def render(self) -> None:
        """Redraw the full diagram from stored phasor data."""

        self.ax.cla()
        self.setup_plot()
        self.fit()
        for phasor in self.phasors.values():
            self._draw_arrow(phasor)
            self._draw_label(phasor)

    def fit(self, margin: float = 0.15, equal_aspect: bool = True) -> None:
        """Fit the axes to all phasors without shrinking the plot area.

        Args:
            margin: Fractional padding added around the phasor extents.
            equal_aspect: Preserve geometric angles and magnitudes when true.
        """

        margin = _coerce_float(margin, "margin")
        if margin < 0:
            raise ValueError("margin must be greater than or equal to 0.")

        x_min, x_max, y_min, y_max = self._data_limits(margin)
        if equal_aspect:
            x_min, x_max, y_min, y_max = _match_figure_aspect(
                x_min,
                x_max,
                y_min,
                y_max,
                self.fig,
            )
            self.ax.set_aspect("equal", adjustable="box")
        else:
            self.ax.set_aspect("auto")

        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)

    def show(
        self,
        grid: bool = True,
        equal_aspect: bool = True,
        margin: float = 0.15,
    ) -> None:
        """Display the diagram."""

        self.fit(margin=margin, equal_aspect=equal_aspect)
        self._apply_grid(grid)
        plt.show()

    def save(
        self,
        filename: str | Path,
        *,
        dpi: int = 300,
        grid: bool = True,
        equal_aspect: bool = True,
        margin: float = 0.15,
    ) -> Path:
        """Save the current diagram and return the output path."""

        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.fit(margin=margin, equal_aspect=equal_aspect)
        self._apply_grid(grid)
        self.fig.savefig(output_path, bbox_inches="tight", dpi=dpi)
        return output_path

    def _resolve_start(
        self,
        start_ref: str,
        start_x: float,
        start_y: float,
        ref_point: ReferencePoint,
    ) -> tuple[float, float]:
        if start_ref == "abs":
            return (
                _coerce_float(start_x, "start_x"),
                _coerce_float(start_y, "start_y"),
            )

        if ref_point not in {"start", "end"}:
            raise ValueError("ref_point must be either 'start' or 'end'.")

        try:
            ref_phasor = self.phasors[start_ref]
        except KeyError as exc:
            raise ValueError(f"Phasor '{start_ref}' does not exist.") from exc

        return ref_phasor.start if ref_point == "start" else ref_phasor.end

    def _data_limits(self, margin: float = 0.15) -> tuple[float, float, float, float]:
        points = [(0.0, 0.0)]
        for phasor in self.phasors.values():
            points.extend([phasor.start, phasor.end])

        x_values = [point[0] for point in points]
        y_values = [point[1] for point in points]
        x_min, x_max = _expand_limits(min(x_values), max(x_values), margin)
        y_min, y_max = _expand_limits(min(y_values), max(y_values), margin)
        return x_min, x_max, y_min, y_max

    def _data_span(self) -> float:
        x_min, x_max, y_min, y_max = self._data_limits(margin=0.0)
        return max(x_max - x_min, y_max - y_min, 1.0)

    def _draw_arrow(self, phasor: Phasor) -> None:
        line_width = phasor.line_width or self.style.arrow_line_width
        self.ax.annotate(
            "",
            xy=phasor.end,
            xytext=phasor.start,
            arrowprops={
                "arrowstyle": "-|>",
                "color": phasor.color,
                "linewidth": line_width,
                "linestyle": phasor.linestyle,
                "mutation_scale": self.style.arrow_head_size,
                "shrinkA": 0,
                "shrinkB": 0,
                "alpha": phasor.alpha,
                "capstyle": "round",
                "joinstyle": "miter",
            },
            zorder=3,
        )

    def _draw_label(self, phasor: Phasor) -> None:
        label_x, label_y = self._label_position(phasor)
        label_box = None
        if self.style.label_box:
            label_box = {
                "boxstyle": "round,pad=0.16",
                "facecolor": self.style.background_color,
                "edgecolor": "none",
                "alpha": self.style.label_box_alpha,
            }

        self.ax.text(
            label_x,
            label_y,
            phasor.label or phasor.name,
            color=phasor.color,
            fontsize=self.style.label_font_size,
            fontweight=self.style.label_font_weight,
            ha="center",
            va="center",
            alpha=phasor.alpha,
            bbox=label_box,
            zorder=4,
        )

    def _label_position(self, phasor: Phasor) -> tuple[float, float]:
        mid_x = phasor.start_x + phasor.dx / 2.0
        mid_y = phasor.start_y + phasor.dy / 2.0

        offset = phasor.label_offset
        if offset is not None:
            offset_x, offset_y = _coerce_label_offset(offset)
            return mid_x + offset_x, mid_y + offset_y

        if phasor.magnitude == 0:
            return mid_x, mid_y

        normal_x = -phasor.dy / phasor.magnitude
        normal_y = phasor.dx / phasor.magnitude
        if normal_y < 0:
            normal_x *= -1.0
            normal_y *= -1.0

        offset_size = self._data_span() * self.style.auto_label_offset_fraction
        return mid_x + normal_x * offset_size, mid_y + normal_y * offset_size


def _validate_name(name: str) -> str:
    phasor_name = str(name).strip()
    if not phasor_name:
        raise ValueError("name must be a non-empty string.")
    return phasor_name


def _normalize_phasor_type(phasor_type: str) -> str:
    normalized = str(phasor_type).strip().lower()
    if not normalized:
        raise ValueError("phasor_type must be a non-empty string.")
    return normalized


def _resolve_end(
    start: tuple[float, float],
    magnitude: float | None,
    angle: float | None,
    end_x: float | None,
    end_y: float | None,
) -> tuple[float, float]:
    has_end = end_x is not None or end_y is not None
    has_polar = magnitude is not None or angle is not None

    if has_end and has_polar:
        raise ValueError("Provide either end coordinates or magnitude/angle.")

    if has_end:
        if end_x is None or end_y is None:
            raise ValueError("Both end_x and end_y are required together.")
        return _coerce_float(end_x, "end_x"), _coerce_float(end_y, "end_y")

    if magnitude is None or angle is None:
        raise ValueError("Provide either end_x/end_y or magnitude/angle.")

    phasor_magnitude = _coerce_float(magnitude, "magnitude")
    if phasor_magnitude < 0:
        raise ValueError("magnitude must be greater than or equal to 0.")

    angle_rad = math.radians(_coerce_float(angle, "angle"))
    return (
        start[0] + phasor_magnitude * math.cos(angle_rad),
        start[1] + phasor_magnitude * math.sin(angle_rad),
    )


def _phase_angles(
    base_angle: float,
    sequence: SequenceType,
) -> tuple[float, float, float]:
    normalized = str(sequence).strip().lower()
    if normalized in {"abc", "positive"}:
        return base_angle, base_angle - 120.0, base_angle + 120.0
    if normalized in {"acb", "negative"}:
        return base_angle, base_angle + 120.0, base_angle - 120.0
    raise ValueError("sequence must be 'abc', 'acb', 'positive', or 'negative'.")


def _default_phase_labels(prefix: str) -> tuple[str, str, str]:
    return (
        rf"${prefix}_a$",
        rf"${prefix}_b$",
        rf"${prefix}_c$",
    )


def _resolve_line_width(
    arrow_width: float | None,
    line_width: float | None,
    default: float,
) -> float:
    if line_width is not None:
        return _coerce_float(line_width, "line_width")

    if arrow_width is None:
        return default

    legacy_width = _coerce_float(arrow_width, "arrow_width")
    if legacy_width <= 0:
        raise ValueError("arrow_width must be greater than 0.")
    if legacy_width < 0.1:
        return default
    return legacy_width


def _coerce_float(value: float, field_name: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a finite number.") from exc

    if not math.isfinite(result):
        raise ValueError(f"{field_name} must be a finite number.")
    return result


def _coerce_complex(value: complex, field_name: str) -> complex:
    try:
        result = complex(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a finite complex number.") from exc

    if not math.isfinite(result.real) or not math.isfinite(result.imag):
        raise ValueError(f"{field_name} must be a finite complex number.")
    return result


def _coerce_unit_interval(value: float, field_name: str) -> float:
    result = _coerce_float(value, field_name)
    if result < 0.0 or result > 1.0:
        raise ValueError(f"{field_name} must be between 0 and 1.")
    return result


def _coerce_label_offset(
    label_offset: float | tuple[float, float],
) -> tuple[float, float]:
    if isinstance(label_offset, tuple):
        if len(label_offset) != 2:
            raise ValueError("label_offset tuple must contain exactly two values.")
        return (
            _coerce_float(label_offset[0], "label_offset[0]"),
            _coerce_float(label_offset[1], "label_offset[1]"),
        )

    offset = _coerce_float(label_offset, "label_offset")
    return offset, offset


def _expand_limits(
    lower: float,
    upper: float,
    margin: float,
    minimum_span: float = 1.0,
) -> tuple[float, float]:
    center = (lower + upper) / 2.0
    span = max(upper - lower, minimum_span)
    padded_span = span * (1.0 + 2.0 * margin)
    return center - padded_span / 2.0, center + padded_span / 2.0


def _match_figure_aspect(
    x_min: float,
    x_max: float,
    y_min: float,
    y_max: float,
    fig: Figure,
) -> tuple[float, float, float, float]:
    width, height = fig.get_size_inches()
    if width <= 0 or height <= 0:
        return x_min, x_max, y_min, y_max

    target_ratio = height / width
    x_span = x_max - x_min
    y_span = y_max - y_min
    data_ratio = y_span / x_span

    if data_ratio < target_ratio:
        y_center = (y_min + y_max) / 2.0
        y_span = x_span * target_ratio
        y_min = y_center - y_span / 2.0
        y_max = y_center + y_span / 2.0
    elif data_ratio > target_ratio:
        x_center = (x_min + x_max) / 2.0
        x_span = y_span / target_ratio
        x_min = x_center - x_span / 2.0
        x_max = x_center + x_span / 2.0

    return x_min, x_max, y_min, y_max


def main() -> None:
    """Run a small demonstration when the module is executed directly."""

    manager = PhasorManager(title="PSPhasor engineering demo")
    manager.draw_phasor("Vs", magnitude=10, angle=0, label=r"$V_s$")
    manager.draw_phasor(
        "Vline",
        magnitude=2,
        angle=150,
        start_ref="Vs",
        color="#9467bd",
        label=r"$V_{line}$",
    )
    manager.draw_phasor(
        "Vr",
        start_x=0,
        start_y=0,
        end_x=8.27,
        end_y=1.0,
        color=DEFAULT_COLORS["power"],
        label=r"$V_R$",
    )
    manager.draw_phasor(
        "Iload",
        magnitude=4,
        angle=-30,
        phasor_type="current",
        label=r"$I_L$",
    )
    manager.save("phasor_diagram.png")
    manager.show()


if __name__ == "__main__":
    main()
