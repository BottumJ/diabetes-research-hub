#!/usr/bin/env python3
"""
Build Acronym & Abbreviation Database for Diabetes Research Hub
Generates a searchable HTML reference with Tufte-style design
"""

import os
import json
from datetime import datetime

# Setup paths
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..', '..')
output_dir = os.path.join(base_dir, 'Dashboards')
output_file = os.path.join(output_dir, 'Acronym_Database.html')

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Curated acronym database
acronyms = {
    'Clinical & Medical': [
        ('BMI', 'Body Mass Index', 'Weight (kg) / height (m)^2; obesity measure'),
        ('BP', 'Blood Pressure', 'Systolic/diastolic arterial pressure'),
        ('CHF', 'Congestive Heart Failure', "Heart's inability to pump sufficient blood"),
        ('CKD', 'Chronic Kidney Disease', 'Progressive loss of kidney function'),
        ('CVD', 'Cardiovascular Disease', 'Heart and blood vessel diseases'),
        ('DKA', 'Diabetic Ketoacidosis', 'Life-threatening complication of insulin deficiency'),
        ('DKD', 'Diabetic Kidney Disease', 'Kidney damage from diabetes (also: DN)'),
        ('DME', 'Diabetic Macular Edema', 'Swelling in the retina from diabetic retinopathy'),
        ('DN', 'Diabetic Nephropathy', 'Kidney disease caused by diabetes'),
        ('DPN', 'Diabetic Peripheral Neuropathy', 'Nerve damage in extremities from diabetes'),
        ('DR', 'Diabetic Retinopathy', 'Eye damage from diabetes'),
        ('DFU', 'Diabetic Foot Ulcer', 'Open wound on foot related to neuropathy/vascular disease'),
        ('ESRD', 'End-Stage Renal Disease', 'Complete kidney failure requiring dialysis or transplant'),
        ('IR', 'Insulin Resistance', 'Reduced cellular response to insulin'),
        ('MetS', 'Metabolic Syndrome', 'Cluster of conditions: high BP, high sugar, excess waist fat, abnormal lipids'),
        ('NAFLD', 'Non-Alcoholic Fatty Liver Disease', 'Liver fat accumulation unrelated to alcohol'),
        ('MASH', 'Metabolic-Associated Steatohepatitis', 'Inflammatory form of fatty liver (formerly NASH)'),
        ('PCOS', 'Polycystic Ovary Syndrome', 'Hormonal disorder often co-occurring with IR'),
    ],
    'Diabetes Types & Subtypes': [
        ('T1D', 'Type 1 Diabetes', 'Autoimmune destruction of beta cells'),
        ('T2D', 'Type 2 Diabetes', 'Insulin resistance with progressive beta cell failure'),
        ('T1DM', 'Type 1 Diabetes Mellitus', 'Same as T1D (formal notation)'),
        ('T2DM', 'Type 2 Diabetes Mellitus', 'Same as T2D (formal notation)'),
        ('LADA', 'Latent Autoimmune Diabetes in Adults', 'Slow-onset autoimmune diabetes, often misdiagnosed as T2D'),
        ('GDM', 'Gestational Diabetes Mellitus', 'Diabetes developing during pregnancy'),
        ('MODY', 'Maturity-Onset Diabetes of the Young', 'Genetic form of diabetes (monogenic)'),
        ('GCK-MODY', 'Glucokinase MODY', 'MODY caused by glucokinase gene mutations'),
        ('CFRD', 'Cystic Fibrosis-Related Diabetes', 'Diabetes in cystic fibrosis patients'),
        ('DPP', 'Diabetes Prevention Program', 'Landmark trial showing lifestyle prevents T2D'),
        ('IGT', 'Impaired Glucose Tolerance', 'Pre-diabetic state'),
    ],
    'Drug Classes & Therapies': [
        ('GLP-1 RA', 'Glucagon-Like Peptide-1 Receptor Agonist', 'Incretin-based therapy (semaglutide, dulaglutide, liraglutide)'),
        ('GLP-1', 'Glucagon-Like Peptide-1', 'Incretin hormone that stimulates insulin secretion'),
        ('GIP', 'Glucose-dependent Insulinotropic Polypeptide', 'Incretin hormone; dual GIP/GLP-1 agonists in development'),
        ('SGLT2', 'Sodium-Glucose Cotransporter 2', 'Kidney glucose reabsorption target (empagliflozin, dapagliflozin)'),
        ('SGLT2i', 'SGLT2 Inhibitor', 'Drug class blocking renal glucose reabsorption'),
        ('DPP-4', 'Dipeptidyl Peptidase-4', 'Enzyme that breaks down incretins; DPP-4 inhibitors extend incretin action'),
        ('DPP-4i', 'DPP-4 Inhibitor', 'Drug class (sitagliptin, saxagliptin) that preserves incretin hormones'),
        ('GKA', 'Glucokinase Activator', 'Drug class enhancing glucose sensing (dorzagliatin)'),
        ('TZD', 'Thiazolidinedione', 'Insulin sensitizer class (pioglitazone, rosiglitazone)'),
        ('CAR-T', 'Chimeric Antigen Receptor T Cell', 'Engineered immune cells for targeted therapy'),
        ('CAR-Treg', 'Chimeric Antigen Receptor Regulatory T Cell', 'Engineered immune-suppressive cells for autoimmune tolerance'),
        ('Treg', 'Regulatory T Cell', 'Immune cells that suppress excessive immune responses'),
        ('TCR-Treg', 'T Cell Receptor Regulatory T Cell', 'Alternative engineered Treg approach'),
        ('MSC', 'Mesenchymal Stem Cell', 'Multipotent stromal cells used in cell therapy'),
        ('iPSC', 'Induced Pluripotent Stem Cell', 'Adult cells reprogrammed to embryonic-like state'),
        ('GAD-alum', 'Glutamic Acid Decarboxylase-Alum', 'Immunotherapy vaccine for autoimmune diabetes (Diamyd)'),
        ('ATG', 'Anti-Thymocyte Globulin', 'Immunosuppressive therapy depleting T cells'),
        ('BCG', 'Bacillus Calmette-Guerin', 'Tuberculosis vaccine being repurposed for T1D'),
        ('TUDCA', 'Tauroursodeoxycholic Acid', 'Bile acid derivative with beta cell protective effects'),
        ('DFMO', 'Difluoromethylornithine', 'Polyamine synthesis inhibitor being studied in T1D'),
        ('FMT', 'Fecal Microbiota Transplantation', 'Gut microbiome modulation therapy'),
        ('NPH', 'Neutral Protamine Hagedorn', 'Intermediate-acting insulin'),
        ('MDI', 'Multiple Daily Injections', 'Insulin delivery method'),
        ('CSII', 'Continuous Subcutaneous Insulin Infusion', 'Insulin pump therapy'),
        ('BLA', 'Biologics License Application', 'FDA regulatory submission for biological products'),
        ('ATMP', 'Advanced Therapy Medicinal Product', 'EMA classification for gene/cell therapies'),
        ('IND', 'Investigational New Drug', 'FDA application to begin human testing'),
        ('NDA', 'New Drug Application', 'FDA submission for new pharmaceutical'),
        ('cGMP', 'Current Good Manufacturing Practice', 'FDA manufacturing quality standard'),
        ('NRDL', 'National Reimbursement Drug List', "China's national drug coverage list"),
    ],
    'Biomarkers & Lab Values': [
        ('HbA1c', 'Hemoglobin A1c (Glycated Hemoglobin)', '3-month average blood glucose indicator'),
        ('A1C', 'Hemoglobin A1c', 'Informal abbreviation for HbA1c'),
        ('FBG', 'Fasting Blood Glucose', 'Blood sugar measured after 8+ hour fast'),
        ('OGTT', 'Oral Glucose Tolerance Test', 'Diagnostic test measuring glucose response'),
        ('HOMA-IR', 'Homeostatic Model Assessment of Insulin Resistance', 'Mathematical model estimating IR from fasting glucose/insulin'),
        ('GAD', 'Glutamic Acid Decarboxylase', 'Autoantibody marker for autoimmune diabetes (GAD65)'),
        ('IA-2', 'Insulinoma-Associated Antigen 2', 'Autoantibody marker for T1D'),
        ('CRP', 'C-Reactive Protein', 'Inflammatory biomarker'),
        ('TNF-alpha', 'Tumor Necrosis Factor Alpha', 'Pro-inflammatory cytokine'),
        ('IL-1B', 'Interleukin-1 Beta', 'Pro-inflammatory cytokine'),
        ('IL-6', 'Interleukin-6', 'Pro-inflammatory cytokine'),
        ('IL-10', 'Interleukin-10', 'Anti-inflammatory cytokine'),
        ('TGF-B', 'Transforming Growth Factor Beta', 'Cytokine involved in immune regulation'),
        ('NF-kB', 'Nuclear Factor Kappa B', 'Transcription factor central to inflammation'),
        ('AMPK', 'AMP-Activated Protein Kinase', 'Cellular energy sensor; metformin target'),
        ('NLRP3', 'NLR Family Pyrin Domain Containing 3', 'Inflammasome complex; target of anti-inflammatory therapies'),
        ('PPAR-gamma', 'Peroxisome Proliferator-Activated Receptor Gamma', 'Nuclear receptor; TZD drug target'),
        ('HLA', 'Human Leukocyte Antigen', 'Immune system gene complex; T1D risk factor'),
        ('TIR', 'Time In Range', '% time glucose is 70-180 mg/dL (CGM metric)'),
    ],
    'Research Methods & Standards': [
        ('RCT', 'Randomized Controlled Trial', 'Gold standard experimental study design'),
        ('PRISMA', 'Preferred Reporting Items for Systematic Reviews', 'Reporting guideline for systematic reviews'),
        ('GRADE', 'Grading of Recommendations Assessment', 'Framework for rating evidence quality'),
        ('PROSPERO', 'International Prospective Register of Systematic Reviews', 'Registry for systematic review protocols'),
        ('CEBM', 'Centre for Evidence-Based Medicine', 'Oxford evidence hierarchy (Levels 1-5)'),
        ('RoB', 'Risk of Bias', 'Assessment tool for study quality (Cochrane RoB 2)'),
        ('NNT', 'Number Needed to Treat', 'Patients treated for one to benefit'),
        ('OR', 'Odds Ratio', 'Measure of association in case-control studies'),
        ('CI', 'Confidence Interval', 'Range of plausible values for an estimate'),
        ('HR', 'Hazard Ratio', 'Measure of effect in survival analysis'),
        ('ITT', 'Intention to Treat', 'Analysis including all randomized participants'),
        ('DALY', 'Disability-Adjusted Life Year', 'Measure of disease burden'),
        ('MeSH', 'Medical Subject Headings', 'PubMed controlled vocabulary'),
        ('PMID', 'PubMed Identifier', 'Unique PubMed article number'),
        ('DOI', 'Digital Object Identifier', 'Permanent article link'),
        ('NCT', 'National Clinical Trial', 'ClinicalTrials.gov trial identifier prefix'),
    ],
    'Organizations & Registries': [
        ('ADA', 'American Diabetes Association', 'Major US diabetes organization; publishes Standards of Care'),
        ('IDF', 'International Diabetes Federation', 'Global diabetes organization; publishes Diabetes Atlas'),
        ('JDRF', 'Juvenile Diabetes Research Foundation', 'Now "Breakthrough T1D"; major T1D research funder'),
        ('BT1D', 'Breakthrough T1D', 'Rebranded JDRF'),
        ('NIH', 'National Institutes of Health', 'US biomedical research funding agency'),
        ('NIDDK', 'National Institute of Diabetes and Digestive and Kidney Diseases', 'NIH institute funding diabetes research'),
        ('FDA', 'Food and Drug Administration', 'US drug/device regulatory agency'),
        ('EMA', 'European Medicines Agency', 'EU drug regulatory agency'),
        ('NMPA', 'National Medical Products Administration', 'China drug regulatory agency'),
        ('WHO', 'World Health Organization', 'UN health agency'),
        ('CDC', 'Centers for Disease Control and Prevention', 'US public health agency'),
        ('AHRQ', 'Agency for Healthcare Research and Quality', 'US evidence review agency'),
        ('CITR', 'Collaborative Islet Transplant Registry', 'International islet transplant outcomes database'),
        ('OSF', 'Open Science Framework', 'Pre-registration and open research platform'),
        ('EASD', 'European Association for the Study of Diabetes', 'European diabetes research organization'),
        ('ATTD', 'Advanced Technologies & Treatments for Diabetes', 'Annual diabetes technology conference'),
        ('NASHP', 'National Academy for State Health Policy', 'US health policy organization'),
    ],
    'Technology & Devices': [
        ('CGM', 'Continuous Glucose Monitor', 'Wearable sensor measuring glucose every 5 min'),
        ('rt-CGM', 'Real-Time CGM', 'CGM with live glucose display'),
        ('FGM', 'Flash Glucose Monitoring', 'Scan-to-read glucose sensor (Libre)'),
        ('HCL', 'Hybrid Closed-Loop', 'Automated insulin delivery with user boluses'),
        ('AID', 'Automated Insulin Delivery', 'Umbrella term for closed-loop systems'),
        ('AP', 'Artificial Pancreas', 'Fully automated glucose regulation system'),
        ('PLGS', 'Predictive Low-Glucose Suspend', 'Pump feature stopping insulin before hypoglycemia'),
        ('SMBG', 'Self-Monitoring of Blood Glucose', 'Fingerstick glucose testing'),
        ('BGM', 'Blood Glucose Monitor', 'Device for fingerstick glucose measurement'),
        ('EHR', 'Electronic Health Record', 'Digital patient medical records'),
        ('DSMES', 'Diabetes Self-Management Education and Support', 'Structured diabetes education programs'),
        ('FQHC', 'Federally Qualified Health Center', 'Community health center serving underserved areas'),
        ('CHW', 'Community Health Worker', 'Non-clinical community-based health support'),
        ('SOC', 'Standard of Care', 'Current best-practice treatment'),
    ],
    'Genomics & Omics': [
        ('GWAS', 'Genome-Wide Association Study', 'Scans entire genome for disease-associated variants'),
        ('SNP', 'Single Nucleotide Polymorphism', 'Single DNA base variation'),
        ('QTL', 'Quantitative Trait Locus', 'Genomic region affecting a measurable trait'),
        ('RNA', 'Ribonucleic Acid', 'Gene expression molecule'),
        ('DNA', 'Deoxyribonucleic Acid', 'Genetic blueprint'),
        ('CRISPR', 'Clustered Regularly Interspaced Short Palindromic Repeats', 'Gene editing technology'),
        ('AAV', 'Adeno-Associated Virus', 'Gene therapy delivery vector'),
        ('GMP', 'Good Manufacturing Practice', 'Quality standard for cell/gene therapy production'),
        ('SCFA', 'Short-Chain Fatty Acid', 'Microbiome metabolite affecting metabolism'),
        ('PDX1', 'Pancreatic and Duodenal Homeobox 1', 'Key transcription factor in beta cell development'),
        ('MAFA', 'V-Maf Musculoaponeurotic Fibrosarcoma Oncogene A', 'Beta cell maturation transcription factor'),
    ],
    'Statistics & Data': [
        ('RCT', 'Randomized Controlled Trial', 'Gold standard experimental study design'),
        ('OR', 'Odds Ratio', 'Measure of association in case-control studies'),
        ('CI', 'Confidence Interval', 'Range of plausible values for an estimate'),
        ('NNT', 'Number Needed to Treat', 'Patients treated for one to benefit'),
        ('HR', 'Hazard Ratio', 'Measure of effect in survival analysis'),
    ],
    'Hub-Specific': [
        ('GOLD', 'Gold Validation Tier', '3+ independent expert sources confirm gap relevance'),
        ('SILVER', 'Silver Validation Tier', '2 confirming expert sources'),
        ('BRONZE', 'Bronze Validation Tier', 'Our bibliometric analysis only'),
        ('Gap Score', 'Literature Gap Score', 'Formula: max(0, 1-(joint_pubs/geometric_mean)) x 100'),
        ('LMIC', 'Low- and Middle-Income Country', 'World Bank economic classification'),
        ('HIC', 'High-Income Country', 'World Bank economic classification'),
    ],
}

# Build flat list with counts
all_acronyms = []
category_list = []
for category, terms in acronyms.items():
    category_list.append(category)
    for acronym, full_name, description in terms:
        all_acronyms.append({
            'acronym': acronym,
            'full_name': full_name,
            'category': category,
            'description': description
        })

# Sort by acronym for alphabetization
all_acronyms.sort(key=lambda x: x['acronym'].upper())

# Count statistics
total_acronyms = len(all_acronyms)
total_categories = len(acronyms)

# Generate HTML
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Acronym & Abbreviation Database - Diabetes Research Hub</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background-color: #fafaf7;
            color: #1a1a1a;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif;
            line-height: 1.6;
            padding: 2rem;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            margin-bottom: 3rem;
        }

        h1 {
            font-family: Georgia, serif;
            font-size: 2.5rem;
            font-weight: normal;
            margin-bottom: 0.5rem;
            letter-spacing: -0.02em;
        }

        .subtitle {
            color: #636363;
            font-size: 1.1rem;
            margin-bottom: 1rem;
            font-style: normal;
        }

        .stats {
            color: #636363;
            font-size: 0.95rem;
            border-top: 1px solid #e0ddd5;
            border-bottom: 1px solid #e0ddd5;
            padding: 0.75rem 0;
        }

        .search-section {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            padding: 1.5rem;
            margin: 2rem 0;
        }

        .search-label {
            display: block;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
            color: #1a1a1a;
        }

        input[type="text"] {
            width: 100%;
            padding: 0.75rem;
            font-size: 1rem;
            border: 1px solid #e0ddd5;
            background-color: #fafaf7;
            color: #1a1a1a;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #1a1a1a;
            background-color: #ffffff;
        }

        .filter-buttons {
            margin: 2rem 0;
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .filter-btn {
            padding: 0.5rem 1rem;
            border: 1px solid #e0ddd5;
            background-color: #ffffff;
            color: #1a1a1a;
            cursor: pointer;
            font-size: 0.9rem;
            transition: none;
        }

        .filter-btn:hover {
            border-color: #1a1a1a;
            background-color: #f5f5f2;
        }

        .filter-btn.active {
            border-color: #1a1a1a;
            background-color: #1a1a1a;
            color: #ffffff;
        }

        .alphabet-nav {
            margin: 2rem 0;
            display: flex;
            flex-wrap: wrap;
            gap: 0.3rem;
            font-size: 0.85rem;
        }

        .alpha-link {
            padding: 0.3rem 0.5rem;
            border: 1px solid #e0ddd5;
            background-color: #ffffff;
            color: #1a1a1a;
            cursor: pointer;
            text-decoration: none;
        }

        .alpha-link:hover {
            border-color: #1a1a1a;
        }

        .table-wrapper {
            background-color: #ffffff;
            border: 1px solid #e0ddd5;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.95rem;
        }

        thead {
            background-color: #fafaf7;
            border-bottom: 2px solid #e0ddd5;
        }

        th {
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif;
            color: #1a1a1a;
            border-right: 1px solid #e0ddd5;
        }

        th:last-child {
            border-right: none;
        }

        td {
            padding: 1rem;
            border-bottom: 1px solid #e0ddd5;
            border-right: 1px solid #e0ddd5;
        }

        td:last-child {
            border-right: none;
        }

        tbody tr:hover {
            background-color: #fafaf7;
        }

        .acronym {
            font-family: "SF Mono", Monaco, Consolas, monospace;
            font-weight: 600;
            color: #1a1a1a;
        }

        .full-name {
            font-weight: 500;
        }

        .category-tag {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            background-color: #fafaf7;
            border: 1px solid #e0ddd5;
            font-size: 0.85rem;
            color: #636363;
        }

        .description {
            color: #636363;
            font-size: 0.9rem;
        }

        .no-results {
            text-align: center;
            padding: 2rem;
            color: #636363;
        }

        footer {
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #e0ddd5;
            font-size: 0.85rem;
            color: #636363;
        }

        .footer-title {
            font-family: Georgia, serif;
            color: #1a1a1a;
            margin-bottom: 0.5rem;
        }

        .footer-sources {
            margin: 1rem 0;
            line-height: 1.8;
        }

        .footer-note {
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid #e0ddd5;
            font-style: normal;
        }

        .alpha-anchor {
            display: block;
            height: 0;
            visibility: hidden;
        }
    </style>
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-JGMD5VRYPH"></script>
    <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-JGMD5VRYPH');</script>
</head>
<body>
    <div class="container">
        <header>
            <h1>Acronym & Abbreviation Database</h1>
            <p class="subtitle">Diabetes Research Hub - Quick reference for all terms used across dashboards and analyses</p>
            <div class="stats">
                <strong>''' + str(total_acronyms) + ''' acronyms</strong> |
                <strong>''' + str(total_categories) + ''' categories</strong> |
                Use the search below to find what you need instantly
            </div>
        </header>

        <div class="search-section">
            <label class="search-label">Search by acronym, full name, or description:</label>
            <input type="text" id="searchInput" placeholder="Type to filter (e.g., HbA1c, insulin, kidney)">
        </div>

        <div>
            <strong style="font-size: 0.9rem; color: #636363;">Filter by category:</strong>
            <div class="filter-buttons" id="filterButtons">
                <button class="filter-btn active" data-filter="">All Categories</button>
'''

# Add category filter buttons
for category in category_list:
    html_content += f'                <button class="filter-btn" data-filter="{category}">{category}</button>\n'

html_content += '''            </div>
        </div>

        <div class="alphabet-nav" id="alphabetNav">
'''

# Add alphabet navigation
for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    html_content += f'            <a class="alpha-link" onclick="jumpToLetter(\'{letter}\')">{letter}</a>\n'

html_content += '''        </div>

        <div class="table-wrapper">
            <table>
                <thead>
                    <tr>
                        <th style="width: 12%;">Acronym</th>
                        <th style="width: 22%;">Full Name</th>
                        <th style="width: 16%;">Category</th>
                        <th style="width: 50%;">Context & Description</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
'''

# Add table rows
current_letter = None
for item in all_acronyms:
    first_letter = item['acronym'][0].upper()
    if first_letter != current_letter:
        html_content += f'                    <span class="alpha-anchor" id="letter-{first_letter}"></span>\n'
        current_letter = first_letter

    html_content += f'''                    <tr class="data-row" data-category="{item['category']}" data-search="{item['acronym'].lower()} {item['full_name'].lower()} {item['description'].lower()}">
                        <td class="acronym">{item['acronym']}</td>
                        <td class="full-name">{item['full_name']}</td>
                        <td><span class="category-tag">{item['category']}</span></td>
                        <td class="description">{item['description']}</td>
                    </tr>
'''

html_content += '''                </tbody>
            </table>
        </div>

        <div id="noResults" class="no-results" style="display: none;">
            No acronyms match your search. Try different keywords.
        </div>

        <footer>
            <div class="footer-title">Diabetes Research Hub - Acronym Database</div>
            <div class="footer-sources">
                <strong>Sources:</strong> ADA Standards of Care, IDF Diabetes Atlas, ClinicalTrials.gov, PubMed MeSH, FDA/EMA regulatory frameworks
            </div>
            <div class="footer-note">
                This reference is maintained alongside the research dashboards. If you encounter an undefined term, please flag it for addition.
            </div>
        </footer>
    </div>

    <script>
        // Real-time search and filtering
        function filterTable() {
            const searchInput = document.getElementById('searchInput').value.toLowerCase();
            const activeFilter = document.querySelector('.filter-btn.active').getAttribute('data-filter');
            const rows = document.querySelectorAll('.data-row');
            let visibleCount = 0;

            rows.forEach(row => {
                const searchText = row.getAttribute('data-search');
                const category = row.getAttribute('data-category');

                const matchesSearch = searchInput === '' || searchText.includes(searchInput);
                const matchesCategory = activeFilter === '' || category === activeFilter;

                if (matchesSearch && matchesCategory) {
                    row.style.display = '';
                    visibleCount++;
                } else {
                    row.style.display = 'none';
                }
            });

            document.getElementById('noResults').style.display = visibleCount === 0 ? 'block' : 'none';
        }

        // Event listeners
        document.getElementById('searchInput').addEventListener('input', filterTable);

        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                this.classList.add('active');
                filterTable();
            });
        });

        // Alphabet jump
        function jumpToLetter(letter) {
            const anchor = document.getElementById('letter-' + letter);
            if (anchor) {
                anchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }

        // Focus search on load
        document.getElementById('searchInput').focus();
    </script>
</body>
</html>
'''

# Write to file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Successfully generated Acronym Database')
print(f'Output: {output_file}')
print(f'Statistics: {total_acronyms} acronyms across {total_categories} categories')
