# Bridgewater Forecast

Research and production pipeline for the 2026 Bridgewater and Global Citizen
Forecasting the Future challenge.

## Status

The current PDF is an **author-review draft and is not ready to submit**. The
challenge terms require independently conceived human substantive work and
state that entries may not be substantially AI generated. See
`research/AUTHOR_REVIEW.md`.

## Deliverable

`deliverable/` contains exactly one PDF. The draft uses 10 pages:

- Pages 1-2: 12 binary forecasts and probabilities.
- Pages 3-5: framework and holistic synthesis.
- Pages 6-10: analytical appendix, resolution registry, and sources.

## Reproduce

```powershell
python scripts\calibrate.py
python scripts\build_figures.py
pdflatex -interaction=nonstopmode -halt-on-error `
  -output-directory=deliverable `
  -jobname=Bridgewater_Forecasting_the_Future_2026_DRAFT submission.tex
python scripts\validate_submission.py --allow-draft
```

After substantive author review, change `\drafttrue` to `\draftfalse`, compile
with the final job name, remove the superseded draft PDF, and run the validator
without `--allow-draft`.

## Evidence cutoff

Sources and probabilities are frozen at July 30, 2026. The source ledger,
resolution contracts, forecast data, and scenario conditionals are versioned
separately so that prose changes cannot silently alter the forecast contract.
