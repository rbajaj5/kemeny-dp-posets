"""Generate a dependency-free SVG of the side-two Y coloring Hasse graph."""

from __future__ import annotations

from html import escape
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from kemeny_dp.hex_y import TriangularYBoard, exact_winner_radii


def main() -> None:
    board = TriangularYBoard.create(2)
    radii = exact_winner_radii(board)
    cell_names = {
        cell: name for cell, name in zip(board.cells, ("a", "b", "c"))
    }
    layers = {
        blue_count: [
            mask
            for mask in range(1 << board.cell_count)
            if mask.bit_count() == blue_count
        ]
        for blue_count in range(board.cell_count + 1)
    }

    width = 760
    height = 600
    margin_x = 120
    top = 135
    layer_gap = 130
    node_width = 132
    node_height = 54
    positions: dict[int, tuple[float, float]] = {}

    for blue_count, layer in layers.items():
        usable = width - 2 * margin_x
        step = usable / len(layer)
        for index, mask in enumerate(layer):
            positions[mask] = (
                margin_x + step * (index + 0.5),
                top + (board.cell_count - blue_count) * layer_gap,
            )

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">',
        "<style>",
        "text{font-family:Inter,Segoe UI,Arial,sans-serif;fill:#172033}",
        ".edge{stroke:#94a3b8;stroke-width:1.5}",
        ".pivotal{stroke:#7c3aed;stroke-width:4}",
        ".node{stroke:#334155;stroke-width:1.2}",
        ".label{font-size:13px;text-anchor:middle}",
        ".layer{font-size:13px;font-weight:700}",
        "</style>",
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
        '<text x="32" y="40" font-size="24" font-weight="700">'
        "Side-2 Y coloring Hasse graph"
        "</text>",
        '<text x="32" y="68" font-size="13">'
        "Each edge recolors one cell yellow to blue; purple edges change the "
        "unique Y winner."
        "</text>",
        '<text x="32" y="91" font-size="12">'
        "Node labels give the blue-cell subset, winner, and distance R to the "
        "opposite outcome."
        "</text>",
    ]

    for mask in range(1 << board.cell_count):
        for cell_index in range(board.cell_count):
            if mask & (1 << cell_index):
                continue
            child = mask | (1 << cell_index)
            x1, y1 = positions[mask]
            x2, y2 = positions[child]
            edge_class = (
                "edge pivotal"
                if board.winner(mask) != board.winner(child)
                else "edge"
            )
            lines.append(
                f'<line class="{edge_class}" '
                f'x1="{x1:.1f}" y1="{y1 - node_height / 2:.1f}" '
                f'x2="{x2:.1f}" y2="{y2 + node_height / 2:.1f}"/>'
            )

    for blue_count, layer in layers.items():
        y = top + (board.cell_count - blue_count) * layer_gap
        lines.append(
            f'<text class="layer" x="24" y="{y + 5:.1f}">'
            f"|B|={blue_count}</text>"
        )
        for mask in layer:
            x, _ = positions[mask]
            blue_cells = [
                cell_names[cell]
                for i, cell in enumerate(board.cells)
                if mask & (1 << i)
            ]
            subset = "{" + ",".join(blue_cells) + "}" if blue_cells else "empty"
            winner = "Blue" if board.winner(mask) else "Yellow"
            fill = "#bfdbfe" if winner == "Blue" else "#fef08a"
            tooltip = escape(
                f"blue subset {subset}; winner {winner}; radius {radii[mask]}"
            )
            lines.extend([
                "<g>",
                f"<title>{tooltip}</title>",
                f'<rect class="node" x="{x - node_width / 2:.1f}" '
                f'y="{y - node_height / 2:.1f}" width="{node_width}" '
                f'height="{node_height}" rx="9" fill="{fill}"/>',
                f'<text class="label" x="{x:.1f}" y="{y - 3:.1f}">'
                f"B={escape(subset)}</text>",
                f'<text class="label" x="{x:.1f}" y="{y + 16:.1f}">'
                f"winner={winner}, R={radii[mask]}</text>",
                "</g>",
            ])

    lines.append("</svg>")
    output_dir = ROOT / "artifacts"
    output_dir.mkdir(exist_ok=True)
    target = output_dir / "hex_y_hasse_n2.svg"
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
