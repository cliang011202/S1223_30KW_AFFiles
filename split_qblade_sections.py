"""
Split a QBlade-exported multi-section blade point file into one .sldcrv per section.

Input format (QBlade "Export Blade Geometry → Points"):
    Line 1 : blade name (text)
    Line 2 : column header (e.g. "x y z")
    Lines  : numeric x y z, sections separated by one or more blank lines

Output:
    <out_dir>/<basename>_sec01_z0.200.sldcrv
    <out_dir>/<basename>_sec02_z0.374.sldcrv
    ...

Each output file is tab-separated x y z, ready for SolidWorks
"Insert > Curve > Curve Through XYZ Points".

Usage:
    python split_qblade_sections.py <input.txt> [--unit mm|m] [--drop-last-duplicate]
    python split_qblade_sections.py <input.txt> --resample 80 --keep-last-duplicate(目前是)
"""

import argparse
import math
import re
import sys
from pathlib import Path


def parse_sections(path: Path):
    """
    Yield (section_index, list_of_(x,y,z)) tuples.

    Strategy: read all lines, group consecutive numeric lines, ignore everything
    that does not parse as 3 floats. Blank lines naturally break a group.
    """
    num_re = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")

    sections = []
    current = []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                if current:
                    sections.append(current)
                    current = []
                continue
            # try parse 3 floats
            tokens = stripped.split()
            if len(tokens) < 3:
                # header / name line — flush if current, start new
                if current:
                    sections.append(current)
                    current = []
                continue
            try:
                x, y, z = (float(tokens[0]), float(tokens[1]), float(tokens[2]))
            except ValueError:
                if current:
                    sections.append(current)
                    current = []
                continue
            current.append((x, y, z))

    if current:
        sections.append(current)

    return sections


def drop_closing_duplicate(pts):
    if len(pts) >= 2:
        x0, y0, z0 = pts[0]
        xn, yn, zn = pts[-1]
        if abs(x0 - xn) < 1e-9 and abs(y0 - yn) < 1e-9 and abs(z0 - zn) < 1e-9:
            return pts[:-1]
    return pts


def dedup_consecutive(pts, tol_m: float = 1e-7):
    """
    Remove points that are within `tol_m` (meters) of the previous point.
    SolidWorks "Curve Through XYZ Points" rejects splines with coincident
    consecutive vertices.  Default 1e-7 m = 1e-4 mm = below SW tolerance.
    """
    if len(pts) < 2:
        return list(pts), 0
    out = [pts[0]]
    removed = 0
    for p in pts[1:]:
        q = out[-1]
        d2 = (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2
        if d2 < tol_m * tol_m:
            removed += 1
            continue
        out.append(p)
    return out, removed


def remove_double_trace(pts, tol_m: float = 1e-6):
    """
    If the open polyline loops back to start and then traces the same
    profile a second time (QBlade double-export), keep only the first
    traversal.  Returns (trimmed_pts, was_double).
    """
    if len(pts) < 4:
        return list(pts), False
    x0, y0, z0 = pts[0]
    cum = 0.0
    for i in range(1, len(pts)):
        dx = pts[i][0] - pts[i - 1][0]
        dy = pts[i][1] - pts[i - 1][1]
        dz = pts[i][2] - pts[i - 1][2]
        cum += (dx * dx + dy * dy + dz * dz) ** 0.5
    total = cum
    if total <= 0:
        return list(pts), False

    cum = 0.0
    for i in range(1, len(pts)):
        dx = pts[i][0] - pts[i - 1][0]
        dy = pts[i][1] - pts[i - 1][1]
        dz = pts[i][2] - pts[i - 1][2]
        cum += (dx * dx + dy * dy + dz * dz) ** 0.5
        if cum < 0.25 * total:
            continue
        d2_start = (pts[i][0] - x0) ** 2 + (pts[i][1] - y0) ** 2 + (pts[i][2] - z0) ** 2
        if d2_start < tol_m * tol_m:
            return pts[:i + 1], True
    return list(pts), False


def resample_arclength(pts, n: int):
    """
    Resample an open polyline to `n` points uniformly distributed along its
    cumulative chord length.  Endpoints preserved.
    """
    if n <= 0 or len(pts) <= 2 or len(pts) <= n:
        return list(pts)
    cum = [0.0]
    for i in range(1, len(pts)):
        dx = pts[i][0] - pts[i - 1][0]
        dy = pts[i][1] - pts[i - 1][1]
        dz = pts[i][2] - pts[i - 1][2]
        cum.append(cum[-1] + math.sqrt(dx * dx + dy * dy + dz * dz))
    total = cum[-1]
    if total <= 0:
        return list(pts)

    out = [pts[0]]
    j = 1
    for k in range(1, n - 1):
        s = total * k / (n - 1)
        while j < len(cum) - 1 and cum[j] < s:
            j += 1
        seg = cum[j] - cum[j - 1] or 1.0
        t = (s - cum[j - 1]) / seg
        x = pts[j - 1][0] + t * (pts[j][0] - pts[j - 1][0])
        y = pts[j - 1][1] + t * (pts[j][1] - pts[j - 1][1])
        z = pts[j - 1][2] + t * (pts[j][2] - pts[j - 1][2])
        out.append((x, y, z))
    out.append(pts[-1])
    return out


def section_centroid(pts):
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    return cx, cy


def principal_axis(pts, degenerate_tol: float = 0.05):
    """
    Return ((ux, uy), is_degenerate). The unit vector lies along the section's
    longest axis (chord direction for airfoils). is_degenerate=True for circles
    where the axis is ill-defined.
    """
    cx, cy = section_centroid(pts)
    sxx = syy = sxy = 0.0
    for x, y, _ in pts:
        dx, dy = x - cx, y - cy
        sxx += dx * dx
        syy += dy * dy
        sxy += dx * dy
    n = len(pts)
    sxx /= n; syy /= n; sxy /= n

    tr = sxx + syy
    det = sxx * syy - sxy * sxy
    disc = max(0.0, tr * tr / 4.0 - det)
    lam1 = tr / 2.0 + math.sqrt(disc)
    lam2 = tr / 2.0 - math.sqrt(disc)

    is_degen = (lam1 < 1e-18) or ((lam1 - lam2) / lam1 < degenerate_tol)

    if abs(sxy) > 1e-18:
        ux, uy = lam1 - syy, sxy
    else:
        ux, uy = (1.0, 0.0) if sxx >= syy else (0.0, 1.0)
    norm = math.hypot(ux, uy) or 1.0
    return (ux / norm, uy / norm), is_degen


def resolve_axes(sections):
    """
    Compute the principal axis for each section. Replace degenerate (cylinder)
    axes with the axis of the nearest non-degenerate neighbor (by section index).
    Returns a list of (ux, uy) per section.
    """
    raw = [principal_axis(s) for s in sections]
    axes = [a for a, _ in raw]
    degen = [d for _, d in raw]

    # find nearest non-degenerate neighbor for each degenerate slot
    n = len(sections)
    fixed = list(axes)
    for i in range(n):
        if not degen[i]:
            continue
        # search outward
        best = None
        for d in range(1, n):
            for j in (i - d, i + d):
                if 0 <= j < n and not degen[j]:
                    best = axes[j]
                    break
            if best is not None:
                break
        if best is not None:
            fixed[i] = best
        # ensure axis sign matches neighbor (avoid 180° flip ambiguity)
    # global sign alignment: keep all axes pointing into the same half-plane as axes[k0]
    k0 = next((i for i in range(n) if not degen[i]), 0)
    refx, refy = fixed[k0]
    for i in range(n):
        ux, uy = fixed[i]
        if ux * refx + uy * refy < 0:
            fixed[i] = (-ux, -uy)
    return fixed, degen


def cyclic_shift_to_start(pts, mode: str, axis=None):
    """
    Cyclically rotate the open-loop point list so it starts at a chosen reference.

    mode:
      "principal-pos" : start at the point with max projection onto `axis`
                        (= chord-aft / TE for airfoils when axis is the chord direction).
      "principal-neg" : opposite end (= LE for airfoils).
      "max-x" / "min-x" / "max-y" / "min-y" : pick by absolute coord.
      "max-r"         : furthest from section centroid.

    `axis` is required for principal-pos / principal-neg modes.
    """
    if not pts:
        return pts

    if mode in ("principal-pos", "principal-neg"):
        cx, cy = section_centroid(pts)
        ux, uy = axis if axis is not None else (1.0, 0.0)
        sign = 1.0 if mode == "principal-pos" else -1.0
        idx = max(
            range(len(pts)),
            key=lambda i: sign * ((pts[i][0] - cx) * ux + (pts[i][1] - cy) * uy),
        )
    elif mode == "max-r":
        cx, cy = section_centroid(pts)
        idx = max(range(len(pts)), key=lambda i: (pts[i][0] - cx) ** 2 + (pts[i][1] - cy) ** 2)
    elif mode == "max-x":
        idx = max(range(len(pts)), key=lambda i: pts[i][0])
    elif mode == "min-x":
        idx = min(range(len(pts)), key=lambda i: pts[i][0])
    elif mode == "max-y":
        idx = max(range(len(pts)), key=lambda i: pts[i][1])
    elif mode == "min-y":
        idx = min(range(len(pts)), key=lambda i: pts[i][1])
    else:
        return pts

    return pts[idx:] + pts[:idx]


def enforce_direction(pts, sense: str):
    """
    Ensure the loop traversal direction is consistent.
    Computes the signed polygon area in X-Y; reverses if needed.

    sense: "ccw" or "cw" (counter/clockwise viewed from +Z)
    """
    if len(pts) < 3 or sense not in ("ccw", "cw"):
        return pts
    s = 0.0
    for i in range(len(pts)):
        x1, y1, _ = pts[i]
        x2, y2, _ = pts[(i + 1) % len(pts)]
        s += (x2 - x1) * (y2 + y1)
    # shoelace: s>0 => CW (in screen coords); s<0 => CCW
    is_cw = s > 0
    want_cw = sense == "cw"
    if is_cw != want_cw:
        # keep the first point fixed, reverse the rest
        return [pts[0]] + list(reversed(pts[1:]))
    return pts


def write_sldcrv(points, out_path: Path, scale: float):
    with out_path.open("w", encoding="utf-8", newline="\r\n") as f:
        for x, y, z in points:
            f.write(f"{x*scale:.6f}\t{y*scale:.6f}\t{z*scale:.6f}\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path, help="QBlade point export .txt")
    ap.add_argument(
        "--unit",
        choices=["m", "mm"],
        default="mm",
        help="Output unit. Input is assumed meters. Default: mm (SolidWorks default).",
    )
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default: <input_basename>_sections next to input).",
    )
    ap.add_argument(
        "--drop-last-duplicate",
        action="store_true",
        default=True,
        help="If first and last point coincide, drop the last one (recommended for SolidWorks closed profiles).",
    )
    ap.add_argument(
        "--keep-last-duplicate",
        dest="drop_last_duplicate",
        action="store_false",
        help="Keep the duplicate closing point.",
    )
    ap.add_argument(
        "--align-start",
        choices=["none", "principal-pos", "principal-neg", "max-x", "min-x", "max-y", "min-y", "max-r"],
        default="principal-pos",
        help=(
            "Cyclically shift each section so its starting point is at a consistent reference. "
            "Default 'principal-pos' uses each section's PCA principal axis to find the "
            "trailing-edge end (chord-aft); robust to per-section twist, prebend and Y-offset. "
            "For pure cylinders it falls back to global +X automatically."
        ),
    )
    ap.add_argument(
        "--direction",
        choices=["none", "ccw", "cw"],
        default="cw",
        help=(
            "Enforce a consistent loop direction (viewed from +Z). "
            "Default 'cw' matches QBlade's typical export. Use 'none' to preserve QBlade order."
        ),
    )
    ap.add_argument(
        "--dedup-tol-mm",
        type=float,
        default=1e-3,
        help="Remove consecutive points closer than this (mm). Default 1e-3 mm.",
    )
    ap.add_argument(
        "--resample",
        type=int,
        default=0,
        help=(
            "Resample each section to N points uniformly along arc length. "
            "0 (default) keeps original points. Recommended ~80 for SolidWorks loft stability."
        ),
    )
    args = ap.parse_args()

    if not args.input.is_file():
        print(f"ERROR: input not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    scale = 1000.0 if args.unit == "mm" else 1.0
    out_dir = args.out_dir or args.input.with_name(args.input.stem + "_sections")
    out_dir.mkdir(parents=True, exist_ok=True)

    sections = parse_sections(args.input)
    if not sections:
        print("ERROR: no sections parsed.", file=sys.stderr)
        sys.exit(2)

    width = max(2, len(str(len(sections))))
    print(f"Parsed {len(sections)} sections from {args.input.name}")
    print(f"Writing to: {out_dir}  (unit: {args.unit})")
    print()

    # ALWAYS work on an OPEN-loop representation internally.
    # Closing duplicate (if any) is added back at the very end if requested.
    dedup_tol_m = args.dedup_tol_mm / 1000.0
    prepared = []
    dedup_counts = []
    was_closed = []
    double_trace_removed = []
    for raw_pts in sections:
        is_closed = (
            len(raw_pts) >= 2
            and abs(raw_pts[0][0] - raw_pts[-1][0]) < 1e-9
            and abs(raw_pts[0][1] - raw_pts[-1][1]) < 1e-9
            and abs(raw_pts[0][2] - raw_pts[-1][2]) < 1e-9
        )
        was_closed.append(is_closed)
        pts = drop_closing_duplicate(raw_pts)  # always strip for clean processing
        pts, removed = dedup_consecutive(pts, tol_m=dedup_tol_m)
        dedup_counts.append(removed)
        pts, was_double = remove_double_trace(pts)
        double_trace_removed.append(was_double)
        if args.direction != "none":
            pts = enforce_direction(pts, args.direction)
        prepared.append(pts)

    # Compute principal axes with cylinder-fallback-to-neighbor logic
    if args.align_start in ("principal-pos", "principal-neg"):
        axes, degen = resolve_axes(prepared)
    else:
        axes = [None] * len(prepared)
        degen = [False] * len(prepared)

    base = args.input.stem
    for i, pts in enumerate(prepared, start=1):
        z_vals = [p[2] for p in pts]
        z_mean = sum(z_vals) / len(z_vals)
        n_in = len(sections[i - 1])

        if args.align_start != "none":
            pts = cyclic_shift_to_start(pts, args.align_start, axis=axes[i - 1])

        if args.resample and args.resample >= 4:
            pts = resample_arclength(pts, args.resample)

        # Re-close the curve as the very last step, so SolidWorks sees a
        # closed XYZ-curve. Required for Filled Surface to recognize a
        # closed boundary at the root/tip.
        if (not args.drop_last_duplicate) and was_closed[i - 1] and len(pts) >= 2:
            if pts[0] != pts[-1]:
                pts = list(pts) + [pts[0]]

        fname = f"{base}_sec{i:0{width}d}_z{z_mean:.3f}.sldcrv"
        out_path = out_dir / fname
        write_sldcrv(pts, out_path, scale)

        sx, sy, _ = pts[0]
        cx, cy = section_centroid(pts)
        ang_c = math.degrees(math.atan2(sy - cy, sx - cx))
        flags = []
        if degen[i - 1]:
            flags.append("cyl-borrow")
        if dedup_counts[i - 1]:
            flags.append(f"dedup={dedup_counts[i-1]}")
        if double_trace_removed[i - 1]:
            flags.append("half-trace-kept")
        flag_str = " (" + ", ".join(flags) + ")" if flags else ""
        print(
            f"  sec{i:0{width}d}  z={z_mean*scale:9.2f} {args.unit}  "
            f"pts={n_in}->{len(pts)}  start=({sx*scale:.2f},{sy*scale:.2f}) "
            f"θ_centroid={ang_c:+6.1f}°{flag_str}"
        )

    print()
    print("Done.")
    print()
    print("Next in SolidWorks:")
    print("  1. Insert > Curve > Curve Through XYZ Points -> select each .sldcrv")
    print("     (or use a macro to batch-import all files)")
    print("  2. Insert > Surface > Loft -> select all section curves in order")
    print("     Add a Leading-Edge guide curve (3D sketch through LE points)")
    print("     Add a Trailing-Edge guide curve (3D sketch through TE points)")
    print("  3. Cap root and tip with Filled Surface, then Knit.")


if __name__ == "__main__":
    main()
