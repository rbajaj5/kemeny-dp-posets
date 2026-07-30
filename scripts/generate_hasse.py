"""Generate a dependency-free SVG of the small profile Hasse diagram."""

from __future__ import annotations

from html import escape
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kemeny_dp.core import KemenyAnalyzer, RankingSpace
from kemeny_dp.poset import children, profiles_of_size
from kemeny_dp.sensitivity import SensitivityAnalyzer


def main() -> None:
    space = RankingSpace.create(3)
    kemeny = KemenyAnalyzer(space)
    sensitivity = SensitivityAnalyzer(kemeny)
    maximum_size = 2
    layers = {
        size: list(profiles_of_size(space, size))
        for size in range(maximum_size + 1)
    }
    max_layer = max(len(layer) for layer in layers.values())
    width = max(1100, 116 * max_layer)
    height = 560
    margin_x = 70
    top = 120
    layer_gap = 175
    node_width = 96
    node_height = 42

    positions: dict[tuple[int, ...], tuple[float, float]] = {}
    for size, layer in layers.items():
        usable = width - 2 * margin_x
        step = usable / max(len(layer), 1)
        for index, profile in enumerate(layer):
            x = margin_x + step * (index + 0.5)
            y = top + (maximum_size - size) * layer_gap
            positions[profile] = (x, y)

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        "text{font-family:Inter,Segoe UI,Arial,sans-serif;fill:#172033}",
        ".edge{stroke:#9aa6b8;stroke-width:1.2;opacity:.55}",
        ".node{stroke:#34445d;stroke-width:1.2}",
        ".label{font-size:11px;text-anchor:middle}",
        ".layer{font-size:14px;font-weight:700}",
        "</style>",
        '<rect width="100%" height="100%" fill="#f7f9fc"/>',
        '<text x="36" y="42" font-size="24" font-weight="700">'
        "Kemeny profile Hasse diagram: 3 candidates, at most 2 ballots"
        "</text>",
        '<text x="36" y="70" font-size="13">'
        "Edges add one ballot. Green = unique optimum with radius >= 2; "
        "amber = radius 1; red = tied optimum."
        "</text>",
    ]

    for size, layer in layers.items():
        for profile in layer:
            for child in children(profile):
                if sum(child) > maximum_size:
                    continue
                x1, y1 = positions[profile]
                x2, y2 = positions[child]
                lines.append(
                    f'<line class="edge" x1="{x1:.1f}" y1="{y1 - node_height/2:.1f}" '
                    f'x2="{x2:.1f}" y2="{y2 + node_height/2:.1f}"/>'
                )

    for size in range(maximum_size + 1):
        y = top + (maximum_size - size) * layer_gap
        lines.append(
            f'<text class="layer" x="18" y="{y + 5:.1f}">n={size}</text>'
        )
        for profile in layers[size]:
            x, _ = positions[profile]
            radius = sensitivity.uniqueness_radius(profile)
            optimum_count = len(kemeny.optima(profile))
            color = (
                "#fecaca"
                if optimum_count != 1
                else "#fde68a"
                if radius == 1
                else "#bbf7d0"
            )
            label = escape(space.profile_label(profile))
            selected = space.ranking_label(kemeny.selected_optimum(profile))
            tooltip = escape(
                f"{label}; selected={selected}; optima={optimum_count}; "
                f"uniqueness radius={radius}"
            )
            lines.extend(
                [
                    "<g>",
                    f"<title>{tooltip}</title>",
                    f'<rect class="node" x="{x - node_width/2:.1f}" '
                    f'y="{y - node_height/2:.1f}" width="{node_width}" '
                    f'height="{node_height}" rx="9" fill="{color}"/>',
                    f'<text class="label" x="{x:.1f}" y="{y - 2:.1f}">'
                    f"{label}</text>",
                    f'<text class="label" x="{x:.1f}" y="{y + 13:.1f}">'
                    f"R={radius}, opt={selected}</text>",
                    "</g>",
                ]
            )

    lines.append("</svg>")
    output_dir = ROOT / "artifacts"
    output_dir.mkdir(exist_ok=True)
    target = output_dir / "hasse_m3_n2.svg"
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()

