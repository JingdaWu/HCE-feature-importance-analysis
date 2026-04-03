# Code

## Setup

```bash
pip install -r requirements.txt
```

## Usage

'feature_analysis.py': The script which can be used to conduct feature analysis and reproduce Figure 5A, 5B and 6.
'HOMO_LUMO_visualization.py': The script which can be used to visualize the HOMO and LUMO energies of four diluents and reproduce Figure 4.
'ionic_conductivity_diluent_content.py': The script which can be used to visualize the ionic conductivity-diluent content relationships and reproduce Figure 1A-D.
'predict_gpr_fit.py': The script which can be used to fit the ionic conductivity-diluent content figures by GPR method and reproduce Figure 2E.
'predict_poly2_fit.py': The script which can be used to fit the ionic conductivity-diluent content figures by poly2 method and reproduce Figure 2A.
'predict_poly3_fit.py': The script which can be used to fit the ionic conductivity-diluent content figures by poly3 method and reproduce Figure 2B.
'predict_rf_fit.py': The script which can be used to fit the ionic conductivity-diluent content figures by RF method and reproduce Figure 2C.
'predict_svr_fit.py': The script which can be used to fit the ionic conductivity-diluent content figures by SVR method and reproduce Figure 2D.
'R2_visualization.py': The script which can be used to visualize the calculated R^2, corresponding to the four diluents and five fitting methods, and reproduce Figure 3A.
'RMSE_visualization.py': The script which can be used to visualize the calculated RMSE, corresponding to the four diluents and five fitting methods, and reproduce Figure 3B.

## Figure Generation

Each figure in the paper has a corresponding script in `code/`. To regenerate
all figures:

```bash
cd code/figures
scripts=$(find code -name "*.py" | sort)
for script in $scripts; do
    echo "Running $script ..."
    python3 "$script"
done
```

All figure scripts import could be checked from `figures` to ensure
consistent appearance across the paper.
