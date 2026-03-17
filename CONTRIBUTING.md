# Contributing to the Diabetes Research Hub

Thank you for your interest in contributing to this open-source diabetes research project. We welcome contributions from researchers, clinicians, data scientists, and anyone passionate about accelerating diabetes research.

## How to Contribute

### Report a Data Error
If you find an incorrect citation, outdated statistic, or factual error in any dashboard:
1. Open a [GitHub Issue](https://github.com/BottumJ/diabetes-research-hub/issues/new) with the label `data-error`
2. Specify which dashboard and which claim is incorrect
3. Provide the correct information with a source (PMID, DOI, or URL)

### Suggest a New Research Gap
If you identify a cross-domain research gap that should be investigated:
1. Open a [GitHub Issue](https://github.com/BottumJ/diabetes-research-hub/issues/new) with the label `new-gap`
2. Describe the two domains and why their intersection is underexplored
3. Provide at least 2 supporting references

### Improve an Existing Dashboard
1. Fork the repository
2. Make your changes in `Analysis/Scripts/` (the Python build scripts)
3. Run `python run_quality_improvements.py` to verify all scripts pass
4. Submit a pull request with a clear description of what changed and why

### Add Citations
We follow a triple-source validation framework. If you can strengthen a claim:
- **GOLD**: 3+ independent sources from major institutions
- **SILVER**: 2 independent sources
- **BRONZE**: Our analysis only (preliminary)

All citations should include a PubMed ID (PMID) where available.

## Project Structure

```
Analysis/Scripts/     # Python scripts that generate all dashboards
Dashboards/           # Generated HTML dashboards (do not edit directly)
docs/                 # GitHub Pages site
Analysis/Results/     # Data files and reports
```

**Important**: Edit the Python scripts in `Analysis/Scripts/`, not the HTML files in `Dashboards/`. The HTML files are regenerated each time the scripts run.

## Validation Standards

- All quantitative claims must cite at least one peer-reviewed source
- PMIDs are preferred; DOIs acceptable when PMID is unavailable
- Clinical trial references should include NCT numbers
- Drug pricing and market data should cite the source and date

## Code of Conduct

This project is dedicated to advancing diabetes research for the benefit of all patients worldwide. We are committed to creating an inclusive environment. Please be respectful, constructive, and focused on the science.

## Contact

- **Maintainer**: Justin Bottum
- **GitHub**: [BottumJ/diabetes-research-hub](https://github.com/BottumJ/diabetes-research-hub)
- **OSF Registration**: [osf.io/hu9ga](https://osf.io/hu9ga)

## Citing This Work

If you use data, analysis, or findings from the Diabetes Research Hub in your research, please cite:

**APA:**
Bottum, J. (2026). Diabetes Research Hub: Open-source computational analysis of the global diabetes research landscape. GitHub. https://github.com/BottumJ/diabetes-research-hub

**BibTeX:**
```bibtex
@misc{bottum2026diabeteshub,
  author = {Bottum, Justin},
  title = {Diabetes Research Hub: Open-source computational analysis of the global diabetes research landscape},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/BottumJ/diabetes-research-hub},
  note = {OSF registration: https://osf.io/hu9ga}
}
```

## License

- Code: MIT License
- Content and analysis: CC-BY 4.0
