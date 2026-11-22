# Voltage Losses and Power in an Aqueous Quinone Flow Battery

How much of the difference in peak discharge power across three membranes can a constant-resistance model explain? Section 2.4 and Figure 5 of [the experimental study](https://aziz.seas.harvard.edu/sites/g/files/omnuum6451/files/newaziz/files/mja272.pdf) report near-full-charge open-circuit voltage, whole-cell area-specific resistances and peak powers for a DHBQ/ferrocyanide flow cell. This notebook uses the authors' reported values directly.

## Results and conclusion

The calculated peaks are **307.6, 163.4 and 138.2 mW/cm²** for N212, N115 and N117. The reported peaks are 300, 164 and 137 mW/cm². The simple model reproduces the ranking and is closest in absolute terms for N115. Resistance comes from measurements on these same cells, so agreement is a consistency check. The plotted curves are model outputs. Extending the low-current resistance across the entire discharge curve neglects nonlinear losses at high current.

## Reproduce the calculation

Open [analysis.ipynb](analysis.ipynb) in Jupyter or upload it to Google Colab and choose Run all. The notebook contains the source values, calculation and plot. It uses Python 3 with Matplotlib and NumPy.
