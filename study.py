"""Regenerate results.md with Python 3.8+ and its standard library."""
from math import asin, degrees, exp, log, log1p, sqrt
from pathlib import Path
from statistics import mean

# Table 4, US9614245B2. Measured formal and published theoretical values in V.
quinones = [
    ("Hydroquinone", .68, .70),
    ("Hydroquinone sulfonic acid", .70, .77),
    ("1,2-benzoquinone-3,5-disulfonic acid", .87, .85),
    ("Anthraquinone-2-sulfonic acid", .15, .09),
    ("Anthraquinone-2,6-disulfonic acid", .19, .12),
]
# Yang et al., section 2.4. Whole-cell DC resistance and reported peak power.
cells = [("N212", 1.28, 300), ("N115", 2.41, 164), ("N117", 2.85, 137)]
ocv = 1.255
report = ["# Calculated results", "", "## Quinone potentials", "",
          "| Couple | Formal (V) | Theory (V) | Theory − formal (mV) |",
          "|---|---:|---:|---:|"]
errors = []
for name, formal, theory in quinones:
    errors.append(theory - formal)
    report.append(f"| {name} | {formal:.2f} | {theory:.2f} | {1000*errors[-1]:+.0f} |")
delta = mean(map(abs, errors))
report += ["", f"Mean signed error {1000*mean(errors):+.0f} mV. Mean absolute error {1000*delta:.0f} mV.",
           "", "## Power at the analytical maximum", "",
           "| Cell | ASR (Ω cm²) | j* (A/cm²) | Model | Observed | Residual | At −48 mV | At +48 mV |",
           "|---|---:|---:|---:|---:|---:|---:|---:|"]
for name, resistance, observed in cells:
    current = ocv / (2 * resistance)
    peak = 1000 * current * (ocv - current * resistance)
    assert abs(peak - 1000 * ocv**2 / (4 * resistance)) < 1e-9
    low, high = [1000 * voltage**2 / (4 * resistance) for voltage in (ocv-delta, ocv+delta)]
    report.append(f"| {name} | {resistance:.2f} | {current:.3f} | {peak:.1f} | {observed} | {peak-observed:+.1f} | {low:.1f} | {high:.1f} |")
report += ["", "All power densities in mW/cm².", "", "## Transport sensitivity at 0.30 A/cm² (N212)", "",
           "| Assumed limiting current (A/cm²) | Additional loss (mV) | Loaded voltage (V) | Power (mW/cm²) |",
           "|---:|---:|---:|---:|"]
for limit in (.35, .50, 1.0):
    loss = -8.314462618 * 298.15 / 96485.33212 * log1p(-.30/limit)
    voltage = ocv - .30 * cells[0][1] - loss
    report.append(f"| {limit:.2f} | {1000*loss:.1f} | {voltage:.3f} | {300*voltage:.1f} |")

# Published orthorhombic a-axis lengths. Only the allowed (200) line is modeled.
centers = [2 * degrees(asin(1.5406 / a)) for a in (10.3298, 9.8173)]
gap = centers[1] - centers[0]
report += ["", "## Simulated (200) cathode reflections", "",
           f"LiFePO₄ {centers[0]:.3f}°, FePO₄ {centers[1]:.3f}°, separation {gap:.3f}° (2θ).",
           "", "| FWHM (°) | Calculated local maxima (° 2θ) |", "|---:|---|"]
angles = [15 + i*.001 for i in range(6001)]
for width in (.25, .75, 1.25):
    intensity = [sum(exp(-4*log(2)*((x-center)/width)**2) for center in centers) for x in angles]
    maxima = [angles[i] for i in range(1,len(angles)-1) if intensity[i-1] < intensity[i] > intensity[i+1]]
    # Equal-height Gaussian doublet has two maxima for separation > 2 sigma.
    assert len(maxima) == (2 if gap > width / sqrt(2*log(2)) else 1)
    report.append(f"| {width:.2f} | {', '.join(f'{x:.3f}' for x in maxima)} |")
Path(__file__).with_name("results.md").write_text("\n".join(report)+"\n", encoding="utf-8")
