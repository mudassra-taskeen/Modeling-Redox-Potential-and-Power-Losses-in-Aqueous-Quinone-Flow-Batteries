# From quinone redox potential to flow-battery power

A quinone with a promising reduction potential still has to deliver voltage while current flows. How large is the discrepancy between published theoretical and measured quinone potentials? If a voltage estimate were off by that amount, how much would it matter for peak power? This project follows those questions from five molecular redox couples to an alkaline 2,5-dihydroxy-1,4-benzoquinone (DHBQ) flow cell. A companion powder-diffraction calculation asks what a measurement could distinguish when the active material is a crystalline phosphate cathode.

## Reproduce the study

1. Clone this repository and open its directory.
2. Run `python3 study.py` with Python 3.8 or later. All numerical inputs are in the script. It uses the standard library and writes [results.md](results.md) beside the script.
3. Read the four result tables in order. The code checks each analytical power maximum against current times loaded voltage and checks each simulated diffraction peak count against the equal-Gaussian resolution criterion.
4. For the original polarization and power plots, run [analysis.ipynb](analysis.ipynb) in Jupyter with NumPy and Matplotlib.

## 1. Benchmark the molecular potentials

Table 4 of the ORBAT patent lists measured formal potentials and theoretical potentials in adjacent columns. Pair values within each row, using the formal-potential column consistently. Omit unsubstituted anthraquinone because the table labels it insoluble. The theory values come from the source. The related RedoxFlow implementation shows how a separate computational study could obtain a potential from oxidized and reduced free energies. This benchmark starts where both a prediction and a measurement already exist. [Table 4](https://patents.google.com/patent/US9614245B2/en)

For hydroquinone, the signed difference is (0.70 − 0.68) × 1000 = +20 mV. Repeat for the other four couples. The signed mean is (20 + 70 − 20 − 60 − 70)/5 = −12 mV. Taking absolute values before averaging gives 240/5 = **48 mV**. The signed mean hides the two 70 mV discrepancies, which point in opposite directions.

## 2. Calculate how resistance changes peak power

Yang and colleagues reported a near-full-charge open-circuit voltage of 1.255 V and discharge measurements for three DHBQ/ferrocyanide cells. Use their whole-cell DC area-specific resistance R for each membrane configuration. For current density j in A/cm², the product jR has units of volts. [Yang et al., section 2.4 and Figure 5](https://doi.org/10.1002/aenm.201702056)

1. Write loaded voltage as V = E − jR, with E fixed at the measured open-circuit voltage.
2. Multiply by current density to get P = jE − j²R in W/cm².
3. Set the derivative E − 2jR to zero. Since the second derivative is −2R and R is positive, the maximum occurs at j* = E/(2R). Substitution gives P* = E²/(4R).
4. For N212, j* = 1.255/(2 × 1.28) = 0.490 A/cm². Voltage at the maximum is E/2 = 0.6275 V. Peak power is 307.6 mW/cm², 7.6 mW/cm² above the reported 300. Repeat with 2.41 and 2.85 Ω cm² to obtain 163.4 and 138.2 mW/cm².

## 3. Carry a molecular-scale voltage discrepancy into the cell model

At a fixed state of charge, cell voltage is the positive-electrode potential minus the negative-electrode potential. Holding one electrode fixed transmits a shift of the other electrode one-for-one in magnitude. Use 48 mV as a deliberately chosen perturbation to E and repeat the peak calculation at 1.207 and 1.303 V. For N212, the resulting peaks are 284.5 and 331.6 mW/cm². The fractional response is the same across all three resistances because P* scales with E².

DHBQ itself is outside the five-couple table, and electrolyte conditions differ. The range measures the model's sensitivity to a specified voltage change. Assigning an uncertainty interval to DHBQ would require data for that chemistry under comparable conditions.

## 4. Test sensitivity to mass transport

Choose N212 at j = 0.30 A/cm², below all three trial limiting currents. The baseline loaded voltage is 1.255 − 0.30 × 1.28 = 0.871 V. Model an additional concentration loss at one idealized one-electron electrode, holding the product activity fixed. A steady diffusion film gives a surface-to-bulk reactant concentration ratio of 1 − j/j_lim. Substitution into the Nernst equation gives a positive voltage loss of −(RT/F) ln(1 − j/j_lim), valid for 0 ≤ j < j_lim.

At 298.15 K and j_lim = 0.50 A/cm², the concentration ratio is 0.40 and the loss is 23.5 mV. Loaded voltage falls to 0.847 V and power to 254.2 mW/cm². The three trial limits explore sensitivity. The paper's DC slope may already absorb some transport loss, so adding this term cannot uniquely decompose the experimental losses. Estimating a physical limiting current would require independent transport data or polarization curves at varied flow rates.

## 5. Test whether a solid-cathode diffraction doublet remains visible

The flow cell stores charge in solution. For a solid electrode, lithiation can also change lattice spacings, giving a second way to interrogate battery materials. Use orthorhombic LiFePO₄ and FePO₄ as a separate example. Select the same (200) reflection for both phases. Published a-axis lengths are 10.3298 and 9.8173 Å, respectively. [LiFePO₄ lattice refinement](https://www.sciencedirect.com/science/article/abs/pii/S0378775308021794) · [FePO₄ refinement, supporting information](https://www.rsc.org/suppdata/ta/c4/c4ta01101e/c4ta01101e1.pdf)

1. For (200), d = a/2. At the selected wavelength λ = 1.5406 Å, Bragg's law gives 2θ = 2 asin(λ/a). Convert radians to degrees. The predicted centers are 17.154° and 18.057°.
2. Represent each line by a unit-height Gaussian, exp[−4 ln(2)((x − center)/w)²], where w is the full width at half maximum in degrees. Sum the two profiles with equal heights and a common width. Sample 15–21° every 0.001°.
3. Count interior grid points brighter than both neighbors. At widths of 0.25° and 0.75°, two maxima survive. At 1.25° the trace has one maximum at 17.606°, although both input phases still contribute.
4. As an independent check, the curvature at the midpoint of two equal Gaussians changes sign at a spacing of 2σ. For this pair the transition occurs near w = 0.903 × √(2 ln 2) = 1.06°. Peak heights, background, counting noise, texture and other reflections would all matter for assignment from a measured powder pattern.

## Conclusion

The simple resistance model recovers the three-cell power ranking, with absolute discrepancies of 0.6–7.6 mW/cm² using resistance measured on the same cells. A 48 mV change in one electrode potential moves the N212 peak by about 23–24 mW/cm². Distinguishing molecular error from transport loss in a real cell therefore requires both equilibrium and under-load measurements. The phosphate example illustrates a parallel limit of interpretation in characterization: two crystal phases can produce one local maximum when their lines broaden.

## Project provenance

The five-pair comparison builds on the [aqueous quinone benchmark](https://github.com/mudassra-taskeen/Aqueous-Quinone-Redox-Benchmark). The flow-cell notebook supplies the baseline reproduced here. The voltage propagation, illustrative concentration-loss scenarios and phosphate line-width sweep are calculations in this repository. The external projects below informed the choice of questions. Their teams developed the simulation automation and experimental-pattern workflows.

- [RedoxFlow thermodynamic-cycle implementation](https://github.com/CGruich/RedoxFlow/blob/ccaec183ac9d98b0fb8b465b1d820ebc895fec68/scripts/calculate_nw.py) assembles a potential from electronic, thermal and solvation terms. Its repository includes example NWChem outputs.
- [CrystaLenz reference comparator](https://github.com/MJRaei/CrystaLenz/blob/dc08f09ac09b3e23a0ff0a13f82a926bc16a242d/src/agents/xrd_agent/sub_agents/reference_check/tools/compare_with_mp.py) matches detected peaks against wavelength-specific reference lines. Here the known input phase pair allows a controlled numerical test of peak overlap.
