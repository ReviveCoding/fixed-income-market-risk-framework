from __future__ import annotations

from pathlib import Path
import pandas as pd
from fimrf.utils import write_markdown


def _read(path: Path) -> pd.DataFrame:
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def generate_enhancement_reports(root: Path) -> None:
    outputs = root / "outputs"
    reports = root / "reports"
    traffic = _read(outputs / "traffic_light_backtest.csv")
    attr = _read(outputs / "exception_attribution.csv")
    stability = _read(outputs / "var_stability_diagnostics.csv")
    grid = _read(outputs / "securitized_stress_grid.csv")
    grid_checks = _read(outputs / "securitized_grid_quality_checks.csv")
    ablation = _read(outputs / "specialty_ablation_table.csv")
    false_safe = _read(outputs / "false_safe_metrics.csv")
    pnl_summary = _read(outputs / "pnl_attribution_summary.csv")
    pnl_proxy = _read(outputs / "pnl_attribution_proxy.csv")
    frtb = _read(outputs / "frtb_inspired_diagnostics.csv")
    challengers = _read(outputs / "challenger_model_selection.csv")
    reverse_stress = _read(outputs / "reverse_stress_diagnostics.csv")
    manifest = _read(outputs / "reproducibility_manifest.csv")

    tl = traffic.iloc[0].to_dict() if not traffic.empty else {}
    top_attr = attr.head(5).to_markdown(index=False) if not attr.empty else "No VaR exceptions were observed in the evaluated window."
    stability_table = stability.to_markdown(index=False) if not stability.empty else "No stability diagnostics generated."
    grid_table = grid.head(10).to_markdown(index=False) if not grid.empty else "No securitized stress grid generated."
    grid_check_table = grid_checks.to_markdown(index=False) if not grid_checks.empty else "No grid quality checks generated."
    ablation_table = ablation.to_markdown(index=False) if not ablation.empty else "No specialty ablation generated."
    false_safe_line = false_safe.iloc[0].to_dict() if not false_safe.empty else {}
    pnl_line = pnl_summary.iloc[0].to_dict() if not pnl_summary.empty else {}
    pnl_slice = pnl_proxy[["date", "actual_pnl_proxy", "hypothetical_pnl_proxy", "unexplained_pnl_proxy", "absolute_unexplained_ratio", "dominant_loss_factor"]].head(8).to_markdown(index=False) if not pnl_proxy.empty else "No P&L attribution proxy generated."
    frtb_table = frtb.to_markdown(index=False) if not frtb.empty else "No FRTB-inspired diagnostics generated."
    challenger_table = challengers.to_markdown(index=False) if not challengers.empty else "No challenger model selection generated."
    reverse_table = reverse_stress.head(10).to_markdown(index=False) if not reverse_stress.empty else "No reverse stress diagnostics generated."
    manifest_summary = f"{len(manifest)} hashed files" if not manifest.empty else "No reproducibility manifest generated."

    write_markdown(reports / "weakness_reinforcement_loop_report.md", "Weakness Reinforcement Loop Report", [
        ("Loop 1: public/small-data readiness", "Identified weakness: v2 already had cached public-compatible samples, but the evidence was still mostly framework-level. Reinforcement: added explicit source catalog, cached sample generation, and small-data validation script so the project can prove local execution without external credentials."),
        ("Loop 2: backtesting interpretability", f"Identified weakness: VaR exceptions were counted but not fully attributed. Reinforcement: added 250-day traffic-light proxy, exception attribution by dominant loss factor and market-health state, and VaR stability diagnostics. Current traffic light: `{tl.get('traffic_light', 'unknown')}` with {tl.get('exceptions', 'NA')} recent exceptions."),
        ("Loop 3: specialty layer effectiveness", f"Identified weakness: the v2 residual correction could leave the exception rate unchanged. Reinforcement: replaced it with a bounded empirical breach-ratio correction and preserved ablation/false-safe metrics. Current specialty ablation:\n\n{ablation_table}"),
        ("Loop 4: securitized proxy depth", "Identified weakness: securitized-products proxy stress was mostly scenario-multiplier based. Reinforcement: added CPR/default/severity/liquidity stress grid plus monotonicity checks while keeping the proxy claim boundary."),
        ("Loop 5: model review depth", f"Identified weakness: v3 still lacked explicit challenger model selection, P&L attribution proxy, FRTB-inspired liquidity-horizon diagnostics, reverse stress tests, and reproducibility hashing. Reinforcement: added challenger selection table, PLA-style proxy summary, FRTB-inspired ES/liquidity-horizon diagnostics, reverse stress multipliers, and a file-hash reproducibility manifest. Challenger summary:\n\n{challenger_table}"),
        ("Stop condition", "Additional possible improvements are now mostly minor for resume-screening purposes unless proprietary market data, real TRACE history, Bloomberg marks, official modellability testing data, or professional desk P&L are available. The remaining gap is professional Fixed Income quant experience, not project structure."),
    ])

    write_markdown(reports / "backtesting_exception_attribution_report.md", "Backtesting Exception Attribution Report", [
        ("Traffic-light diagnostic", f"The most recent {tl.get('evaluation_days', 'NA')} VaR observations had {tl.get('exceptions', 'NA')} exceptions, exception rate {tl.get('exception_rate', 'NA')}, and review status `{tl.get('traffic_light', 'unknown')}`. This is a review proxy, not a formal regulatory capital calculation."),
        ("Dominant-factor attribution", top_attr),
        ("VaR stability diagnostics", stability_table),
        ("Use", "This report helps explain whether VaR breaches are dominated by rates, corporate credit spreads, securitized proxy losses, or stressed market-health regimes."),
    ])

    write_markdown(reports / "securitized_stress_grid_report.md", "Securitized Proxy Stress Grid Report", [
        ("Purpose", "Adds a transparent CPR/default/severity/liquidity sensitivity grid for the securitized-products proxy. It validates structural intuition without claiming production MBS/ABS valuation."),
        ("Top stress cases", grid_table),
        ("Quality checks", grid_check_table),
        ("Boundary", "The grid is synthetic/proxy-based and should be described as public-mortgage-performance-compatible, not as production securitized-products modeling."),
    ])


    write_markdown(reports / "pnl_attribution_proxy_report.md", "P&L Attribution Proxy Report", [
        ("Purpose", "Adds an actual-vs-hypothetical P&L proxy to support model-performance discussion. This is not desk P&L and is used only as an offline review artifact."),
        ("Summary", f"Actual/hypothetical correlation: {pnl_line.get('actual_hypothetical_corr', 'NA')}; p95 unexplained ratio: {pnl_line.get('p95_absolute_unexplained_ratio', 'NA')}; status: `{pnl_line.get('pla_proxy_status', 'unknown')}`."),
        ("Sample rows", pnl_slice),
        ("Use", "This helps explain whether modeled risk-factor losses explain proxy P&L and where unmodeled residuals may require compensating controls."),
    ])

    write_markdown(reports / "frtb_inspired_diagnostics_report.md", "FRTB-Inspired Diagnostics Report", [
        ("Purpose", "Adds Expected Shortfall, liquidity-horizon scaling, and modellability-proxy diagnostics for review discussion. This is not an official FRTB implementation."),
        ("Diagnostics", frtb_table),
        ("Boundary", "The diagnostics are educational/model-risk review artifacts under public-data-compatible and synthetic/proxy constraints."),
    ])

    write_markdown(reports / "challenger_model_selection_report.md", "Challenger Model Selection Report", [
        ("Purpose", "Compares vanilla historical VaR, residual-corrected VaR, and conservative tail-envelope variants using exception rate, false-safe rate, overreach proxy, and complexity penalty."),
        ("Selection table", challenger_table),
        ("Use", "This converts model development from a single chosen model into an explicit champion/challenger decision record."),
    ])

    write_markdown(reports / "reverse_stress_testing_report.md", "Reverse Stress Testing Report", [
        ("Purpose", "Estimates shock multipliers required for scenario stress losses to exceed VaR/ES thresholds, helping identify scenarios that are already near the tail-loss boundary."),
        ("Reverse stress table", reverse_table),
        ("Use", "This supports risk-manager discussion about which scenario families require closer monitoring."),
    ])

    write_markdown(reports / "reproducibility_manifest_report.md", "Reproducibility Manifest Report", [
        ("Manifest", f"Generated `{manifest_summary}` across configs, source code, scripts, tests, reports, and outputs."),
        ("Use", "The SHA-256 manifest supports GitHub/local reproducibility review and makes it easier to verify that outputs match the packaged code."),
        ("Boundary", "The manifest is an engineering control, not a formal audit certification."),
    ])

    write_markdown(reports / "local_github_runnability_audit.md", "Local and GitHub Runnability Audit", [
        ("Local commands", "`python scripts/create_public_compatible_samples.py`, `python scripts/run_pipeline.py`, `python scripts/run_small_data_validation.py`, and `pytest -q` are the canonical local checks."),
        ("GitHub-ready artifacts", "The project includes requirements, pyproject, Makefile, tests, deterministic cached samples, deterministic fallback, governance reports, and GitHub Actions CI workflow."),
        ("Cleanup", "Generated Python bytecode and pytest cache are excluded from the packaged artifact. Runtime outputs are reproducible and can be regenerated."),
        ("Remaining caveat", "Live public downloads require internet access. The default repository path remains offline-runnable through cached public-compatible samples and deterministic fallback."),
    ])
