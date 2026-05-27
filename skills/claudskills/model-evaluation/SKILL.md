---
name: model-evaluation
description: Model evaluation criteria and QA compliance thresholds
license: MIT
compatibility: opencode
metadata:
  audience: engineers
  workflow: model-validation
---

## What I Do

I document the model evaluation methodology and Quality Assurance (QA) gates
for this project. When an agent works on model training, evaluation, or QA
reporting, I provide the acceptance criteria so it knows what "good enough"
means.

## QA Acceptance Thresholds

These are defined in `app/src/qa_report.py` — `SUCCESS_CRITERIA`:

| Task | Metric | Threshold |
|------|--------|-----------|
| Regression (avg_cpu) | R² | >= 0.70 |
| Regression (avg_cpu) | MAPE / WMAPE | informational — zero-inflated target (see tech spec §1.5) |
| Regression (cost, waste) | MAPE | <= 15.0% |
| Regression (cost, waste) | R² | >= 0.70 |
| Classification | F1 | >= 0.85 |
| Clustering | Silhouette score | >= 0.30 |
| Time series | MAE | <= 5.0 |

## Evaluation Methodology

### Train/Test Split

Always use chronological split (no leakage):

```python
from app.src.models import train_test_split_by_time
train_df, test_df = train_test_split_by_time(df, timestamp_col='timestamp_created', test_size=0.2)
```

### Supported Tasks

- `regression_avg_cpu` — predict average CPU utilisation
- `regression_waste` — predict waste fraction
- `regression_cost` — predict VM cost
- `classification_idle` — binary: is VM idle?
- `classification_tier` — multi-class: waste tier (Low/Medium/High)

### Feature Sets

- `all` — core numeric + temporal features
- `minimal` — core numeric features only
- `no_temporal` — core numeric without temporal encoding

## Model Wrappers

All models follow the `BaseModel` ABC with `fit`, `predict`, `evaluate`, `save`:

| Class | Underlying Estimator |
|-------|---------------------|
| `RidgeModel` | `sklearn.linear_model.Ridge` |
| `RandomForestModel` | `sklearn.ensemble.RandomForestRegressor` / `RandomForestClassifier` |
| `XGBoostModel` | `xgboost.XGBRegressor` / `XGBClassifier` |
| `ClusterModel` | `sklearn.cluster.KMeans` (with `StandardScaler`) |
| `AnomalyModel` | `sklearn.ensemble.IsolationForest` |
| `GenericModel` | Fallback for loading unknown saved models |

## Model Comparison

Use `comparison_table()` from `app.src.visualize`:

```python
from app.src.visualize import comparison_table
df = comparison_table(results)  # rows=models, cols=metrics
```

Best values per metric are auto-highlighted (lower is better for
MAE/RMSE/MSE, higher is better for everything else).

## QA Report

Generate the compliance report:

```bash
python -m app.src.qa_report
```

This reads `models/run_log.csv` and checks each run against the success
criteria table above. The report prints:
- Total runs, passing, failing, pass rate
- Breakdown by task type
- Specific failure reasons per model run
