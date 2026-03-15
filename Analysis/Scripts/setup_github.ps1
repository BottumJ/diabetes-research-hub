# Diabetes Research Hub - GitHub Setup Script
# Run this from the Diabetes_Research folder in PowerShell
#
# PREREQUISITES:
# 1. Install git: https://git-scm.com/download/win
# 2. Create a repo on GitHub: https://github.com/new
#    - Name: diabetes-research-hub
#    - Description: Open-source computational analysis of the global diabetes research landscape
#    - Public
#    - Do NOT initialize with README (we already have one)
# 3. Run this script from inside the Diabetes_Research folder

# Initialize repo
git init
git branch -m main

# Stage all project files (excluding large snapshots and temp files)
git add README.md
git add RESEARCH_DOCTRINE.md
git add CONTRIBUTION_STRATEGY.md
git add Research_Findings_Summary.md
git add OSF_PREREGISTRATION.md
git add LICENSE
git add .gitignore
git add Diabetes_Research_Tracker.xlsx

# Scripts
git add Analysis/Scripts/run_all.py
git add Analysis/Scripts/project1_literature_gap_analysis.py
git add Analysis/Scripts/baseline_clinical_trials.py
git add Analysis/Scripts/baseline_pubmed_alerts.py
git add Analysis/Scripts/hub_monitor.py

# Analysis results (reports + data)
git add Analysis/Results/literature_gap_report.md
git add Analysis/Results/clinical_trials_summary.md
git add Analysis/Results/pubmed_recent_summary.md
git add Analysis/Results/clinical_trials_latest.json
git add Analysis/Results/pubmed_recent_latest.json
git add Analysis/Results/literature_gap_data.json
git add Analysis/Results/literature_gap_matrix.xlsx

# Dashboards
git add Dashboards/Research_Dashboard.html
git add Dashboards/Clinical_Trial_Dashboard.html

# GitHub Pages website
git add docs/index.html

# Commit
git commit -m "Initial commit: Diabetes Research Hub

- Research Doctrine with triple-source validation framework (PRISMA/GRADE/CEBM)
- Contribution Strategy with 4-stage pipeline and 90-day plan
- Literature Gap Analysis: 30 domains, 435 pairwise combinations (Project 1)
- Clinical Trial Intelligence: 746 trials from ClinicalTrials.gov API v2
- PubMed surveillance: 15 alert domains with cross-domain detection
- Interactive Research Dashboard (6 tabs, 55 pipeline entries)
- Clinical Trial Intelligence Dashboard (6 tabs, searchable trial database)
- GitHub Pages website with project overview
- OSF pre-registration: https://osf.io/hu9ga
- 5 automated Python analysis scripts
- Research Tracker spreadsheet (5 sheets, 35 domains)"

# Connect to GitHub and push
# REPLACE the URL below with your actual repo URL after creating it on github.com
git remote add origin https://github.com/BottumJ/diabetes-research-hub.git
git push -u origin main

Write-Host ""
Write-Host "Done! Your repo should now be live at:"
Write-Host "https://github.com/BottumJ/diabetes-research-hub"
Write-Host ""
Write-Host "NEXT STEPS:"
Write-Host "1. Go to repo Settings > Pages"
Write-Host "2. Under 'Source', select 'Deploy from a branch'"
Write-Host "3. Select 'main' branch and '/docs' folder"
Write-Host "4. Click Save"
Write-Host "5. Your site will be live at: https://justinbottum.github.io/diabetes-research-hub/"
