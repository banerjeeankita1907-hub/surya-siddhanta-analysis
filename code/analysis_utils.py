"""Reusable, unit-safe helpers for comparing angular longitudes."""
from __future__ import annotations
import numpy as np

def angular_residual_deg(model_deg, reference_deg) -> np.ndarray:
    """Return signed model-minus-reference residuals in [-180, 180) degrees."""
    model = np.asarray(model_deg, dtype=float)
    reference = np.asarray(reference_deg, dtype=float)
    if model.shape != reference.shape:
        raise ValueError("model and reference arrays must have the same shape")
    if not np.all(np.isfinite(model)) or not np.all(np.isfinite(reference)):
        raise ValueError("longitude arrays must contain only finite values")
    return (model - reference + 180.0) % 360.0 - 180.0

def summarize_residuals(residuals_deg) -> dict[str, float | int]:
    """Summarize signed angular residuals without losing circular wrap handling."""
    residuals = np.asarray(residuals_deg, dtype=float)
    if residuals.size == 0:
        raise ValueError("at least one residual is required")
    if not np.all(np.isfinite(residuals)):
        raise ValueError("residuals must contain only finite values")
    absolute = np.abs(residuals)
    return {
        "count": int(residuals.size),
        "mean_absolute_error_deg": float(np.mean(absolute)),
        "standard_deviation_deg": float(np.std(residuals)),
        "maximum_absolute_error_deg": float(np.max(absolute)),
        "root_mean_square_error_deg": float(np.sqrt(np.mean(residuals ** 2))),
        "mean_signed_error_deg": float(np.mean(residuals)),
    }
