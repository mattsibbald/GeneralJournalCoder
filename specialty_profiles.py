"""
specialty_profiles.py — Royal College specialty + Family Medicine profiles.

Each specialty has:
  description   : free-text used to generate a specialty embedding vector
  core_terms    : strong ontology matches (title hit = +5, abstract hit = +2)
  adjacent_terms: moderate matches (title = +2, abstract = +1)
  exclusion_terms: penalise spurious matches (-5 each hit)

To add a new specialty, append an entry following the same schema.
"""

from __future__ import annotations
from typing import Dict, Any

# ---------------------------------------------------------------------------
# Type alias for clarity
# ---------------------------------------------------------------------------
SpecialtyProfile = Dict[str, Any]

SPECIALTY_PROFILES: Dict[str, SpecialtyProfile] = {

    # ======================================================================
    # CARDIOLOGY
    # ======================================================================
    "cardiology": {
        "name": "Cardiology",
        "description": (
            "Cardiology covers the diagnosis and management of cardiovascular diseases "
            "including coronary artery disease, acute coronary syndromes, heart failure, "
            "arrhythmias, valvular heart disease, cardiomyopathies, pericardial disease, "
            "adult congenital heart disease, hypertension, dyslipidaemia, cardiac imaging, "
            "cardiac catheterisation, electrophysiology, device therapy, cardiac prevention, "
            "cardio-oncology, cardiogenic shock, ECMO, and heart transplantation."
        ),
        "core_terms": [
            "heart failure", "coronary artery disease", "acute coronary syndrome",
            "myocardial infarction", "STEMI", "NSTEMI", "ACS",
            "atrial fibrillation", "ventricular tachycardia", "ventricular fibrillation",
            "arrhythmia", "cardiac arrest", "sudden cardiac death",
            "percutaneous coronary intervention", "PCI", "coronary stent",
            "coronary artery bypass", "CABG",
            "aortic stenosis", "mitral regurgitation", "mitral stenosis",
            "tricuspid regurgitation", "valvular heart disease",
            "TAVI", "TAVR", "transcatheter aortic valve",
            "echocardiography", "cardiac MRI", "coronary CT angiography", "CTCA",
            "cardiac catheterisation", "coronary angiography",
            "HFpEF", "HFrEF", "HFmrEF", "ejection fraction",
            "cardiomyopathy", "dilated cardiomyopathy", "hypertrophic cardiomyopathy",
            "heart transplant", "LVAD", "ventricular assist device",
            "cardiogenic shock", "ECMO", "extracorporeal membrane oxygenation",
            "pericarditis", "cardiac tamponade", "endocarditis",
            "MACE", "cardiovascular mortality", "cardiovascular outcomes",
            "anticoagulation", "antiplatelet therapy", "thrombolysis",
            "statin", "PCSK9 inhibitor", "beta-blocker", "ACE inhibitor",
            "angiotensin receptor blocker", "ARB", "sacubitril", "ARNI",
            "SGLT2 inhibitor heart failure", "dapagliflozin", "empagliflozin heart",
            "GLP-1 cardiovascular", "semaglutide cardiovascular",
            "pulmonary hypertension", "pulmonary arterial hypertension",
            "electrophysiology", "catheter ablation", "AF ablation",
            "pacemaker", "ICD", "implantable cardioverter defibrillator", "CRT",
            "cardiac resynchronisation", "left atrial appendage closure",
            "troponin", "BNP", "NT-proBNP", "cardiac biomarkers",
            "lipid-lowering", "dyslipidaemia", "hypercholesterolaemia",
            "cardio-oncology", "cardiotoxicity", "anthracycline cardiotoxicity",
            "aortic aneurysm", "aortic dissection",
        ],
        "adjacent_terms": [
            "chronic kidney disease cardiovascular", "CKD heart failure",
            "diabetes cardiovascular outcomes", "obesity cardiovascular",
            "stroke prevention", "AF stroke", "anticoagulation stroke",
            "peripheral arterial disease", "vascular disease",
            "sleep apnoea cardiac", "COVID-19 cardiovascular", "myocarditis COVID",
            "cardiac AI", "machine learning ECG", "deep learning echocardiography",
            "cardiac rehabilitation", "hypertension management",
            "ICU cardiac", "haemodynamic monitoring",
            "GLP-1 weight loss cardiac", "SGLT2 renal cardiac",
            "interventional cardiology", "structural heart",
        ],
        "exclusion_terms": [
            "fetal heart rate", "plant vascular tissue", "veterinary cardiac",
            "emotional heart", "heart of the matter",
        ],
    },

    # ======================================================================
    # CLINICAL IMMUNOLOGY & ALLERGY
    # ======================================================================
    "allergy_immunology": {
        "name": "Clinical Immunology & Allergy",
        "description": (
            "Clinical immunology and allergy covers immune-mediated diseases including "
            "asthma, allergic rhinitis, food allergy, anaphylaxis, urticaria, angioedema, "
            "drug hypersensitivity, atopic dermatitis (shared), primary immunodeficiency, "
            "common variable immunodeficiency, immune dysregulation syndromes, "
            "allergen immunotherapy, and biologics for allergic and immune conditions."
        ),
        "core_terms": [
            "anaphylaxis", "food allergy", "peanut allergy", "allergen",
            "allergic rhinitis", "allergic asthma", "atopic march",
            "urticaria", "chronic spontaneous urticaria", "angioedema",
            "drug hypersensitivity", "penicillin allergy",
            "primary immunodeficiency", "common variable immunodeficiency", "CVID",
            "agammaglobulinaemia", "hypogammaglobulinaemia",
            "immunoglobulin replacement", "subcutaneous immunoglobulin",
            "allergen immunotherapy", "sublingual immunotherapy", "oral immunotherapy",
            "anti-IgE", "omalizumab allergy", "dupilumab allergy",
            "IgE mediated", "mast cell", "eosinophilia",
            "hereditary angioedema", "C1 inhibitor",
            "immune dysregulation", "autoimmune lymphoproliferative",
        ],
        "adjacent_terms": [
            "eosinophilic oesophagitis", "eosinophilic gastrointestinal",
            "atopic dermatitis biologic", "asthma biologic",
            "JAK inhibitor allergy", "monoclonal antibody allergy",
            "COVID-19 vaccine allergy", "vaccine hypersensitivity",
            "mast cell activation", "mastocytosis",
        ],
        "exclusion_terms": [
            "tumour immunology", "transplant immunosuppression", "autoimmune hepatitis only",
        ],
    },

    # ======================================================================
    # CRITICAL CARE MEDICINE
    # ======================================================================
    "critical_care": {
        "name": "Critical Care Medicine",
        "description": (
            "Critical care medicine covers the management of life-threatening conditions "
            "in the ICU, including sepsis, septic shock, ARDS, mechanical ventilation, "
            "haemodynamic monitoring, organ support, renal replacement therapy, "
            "nutritional support, sedation and analgesia, delirium, post-ICU syndrome, "
            "end-of-life care, extracorporeal therapies, and critical care neurology."
        ),
        "core_terms": [
            "sepsis", "septic shock", "ARDS", "acute respiratory distress syndrome",
            "mechanical ventilation", "lung-protective ventilation", "PEEP",
            "ICU", "intensive care unit", "critical illness",
            "vasopressor", "norepinephrine", "vasopressin ICU",
            "renal replacement therapy", "continuous renal replacement", "CRRT",
            "ECMO", "extracorporeal membrane oxygenation",
            "haemodynamic monitoring", "cardiac output monitoring",
            "prone positioning", "neuromuscular blockade ICU",
            "delirium ICU", "sedation analgesia ICU",
            "ICU-acquired weakness", "post-intensive care syndrome",
            "corticosteroid sepsis", "hydrocortisone septic shock",
            "early goal-directed therapy", "bundle sepsis",
            "blood transfusion ICU", "transfusion threshold",
            "nutritional support ICU", "enteral nutrition",
            "multiorgan failure", "organ dysfunction",
            "ventilator-associated pneumonia", "VAP",
            "central line infection", "CLABSI",
        ],
        "adjacent_terms": [
            "COVID-19 ICU", "COVID-19 mechanical ventilation",
            "traumatic brain injury ICU", "status epilepticus",
            "liver failure ICU", "acute liver failure",
            "burns critical care", "pancreatitis severe",
            "cardiogenic shock", "post-cardiac arrest",
            "antibiotic stewardship ICU",
        ],
        "exclusion_terms": [
            "paediatric ICU general", "neonatal intensive care",
        ],
    },

    # ======================================================================
    # DERMATOLOGY
    # ======================================================================
    "dermatology": {
        "name": "Dermatology",
        "description": (
            "Dermatology covers skin, hair, and nail diseases including psoriasis, "
            "atopic dermatitis, acne, rosacea, melanoma and non-melanoma skin cancers, "
            "autoimmune blistering diseases, connective tissue diseases with skin involvement, "
            "hidradenitis suppurativa, alopecia, wound care, dermatologic surgery, "
            "phototherapy, and biologics/small molecules for inflammatory skin disease."
        ),
        "core_terms": [
            "psoriasis", "plaque psoriasis", "psoriatic arthritis skin",
            "atopic dermatitis", "eczema",
            "acne vulgaris", "acne treatment", "isotretinoin",
            "rosacea", "seborrhoeic dermatitis",
            "melanoma", "cutaneous melanoma", "Breslow thickness",
            "basal cell carcinoma", "squamous cell carcinoma skin",
            "Merkel cell carcinoma", "cutaneous lymphoma", "CTCL",
            "pemphigus", "pemphigoid", "bullous pemphigoid",
            "hidradenitis suppurativa",
            "alopecia areata", "androgenetic alopecia",
            "dupilumab", "biologics dermatology", "IL-17 inhibitor skin",
            "IL-23 inhibitor skin", "risankizumab", "secukinumab skin",
            "JAK inhibitor dermatology", "baricitinib atopic",
            "upadacitinib skin",
            "contact dermatitis", "patch testing",
            "phototherapy", "narrow-band UVB",
            "Mohs surgery", "dermatologic surgery",
            "skin microbiome", "wound healing",
            "urticaria", "chronic urticaria",
            "vitiligo", "hyperpigmentation",
        ],
        "adjacent_terms": [
            "skin cancer immunotherapy", "checkpoint inhibitor skin toxicity",
            "cutaneous side effects", "drug reaction skin",
            "COVID dermatology", "chilblains COVID",
            "paediatric skin", "neonatal skin",
            "dermoscopy", "confocal microscopy skin",
        ],
        "exclusion_terms": [
            "subcutaneous injection technique", "dermal filler aesthetic only",
        ],
    },

    # ======================================================================
    # EMERGENCY MEDICINE
    # ======================================================================
    "emergency_medicine": {
        "name": "Emergency Medicine",
        "description": (
            "Emergency medicine covers the acute assessment and management of undifferentiated "
            "and high-acuity patients, including chest pain, dyspnoea, stroke, trauma, "
            "toxicology, resuscitation, procedural sedation, point-of-care ultrasound, "
            "sepsis recognition, triage systems, emergency airway management, "
            "disaster medicine, and emergency department systems and flow."
        ),
        "core_terms": [
            "emergency department", "ED", "emergency medicine",
            "triage", "CTAS", "ESI triage",
            "resuscitation", "cardiac arrest resuscitation", "CPR",
            "return of spontaneous circulation", "ROSC",
            "trauma", "major trauma", "polytrauma", "ATLS",
            "chest pain emergency", "HEART score", "TIMI EM",
            "pulmonary embolism diagnosis", "PE diagnosis ED",
            "Wells score", "PERC rule",
            "stroke thrombolysis", "tPA stroke", "thrombectomy stroke pathway",
            "toxicology", "overdose", "poisoning", "antidote",
            "opioid overdose", "naloxone",
            "point-of-care ultrasound", "POCUS", "FAST exam",
            "emergency airway", "rapid sequence intubation", "RSI",
            "procedural sedation",
            "sepsis recognition ED", "lactate ED",
            "shock undifferentiated",
            "acute abdominal pain ED", "appendicitis diagnosis",
            "headache emergency", "subarachnoid haemorrhage",
            "anaphylaxis management",
            "fracture ED", "dislocation reduction",
        ],
        "adjacent_terms": [
            "crowding ED", "length of stay ED", "boarding",
            "COVID-19 emergency department",
            "paediatric emergency",
            "rural emergency medicine",
            "violence injury prevention",
            "opioid crisis ED", "substance use ED",
        ],
        "exclusion_terms": [
            "emergency preparedness non-clinical",
            # Elective planned procedures that are never emergency medicine
            "left atrial appendage closure", "LAAC", "Watchman",
            "transcatheter aortic valve", "TAVI", "TAVR",
            "elective catheter ablation", "pulmonary vein isolation",
            "coronary artery bypass grafting", "CABG",
            "percutaneous coronary intervention elective",
            "total hip arthroplasty", "total knee arthroplasty",
            "elective colonoscopy", "colorectal cancer screening",
            "bariatric surgery", "sleeve gastrectomy",
            "robotic prostatectomy",
        ],
    },

    # ======================================================================
    # ENDOCRINOLOGY & METABOLISM
    # ======================================================================
    "endocrinology": {
        "name": "Endocrinology & Metabolism",
        "description": (
            "Endocrinology and metabolism covers diabetes mellitus type 1 and 2, obesity, "
            "thyroid disease, adrenal disorders, pituitary disease, reproductive endocrinology, "
            "metabolic bone disease, lipid disorders, polycystic ovary syndrome, "
            "neuroendocrine tumours, and the pharmacology of glucose-lowering and metabolic agents."
        ),
        "core_terms": [
            "type 2 diabetes", "type 1 diabetes", "diabetes mellitus",
            "HbA1c", "glycaemic control", "hyperglycaemia",
            "insulin therapy", "insulin pump", "continuous glucose monitoring", "CGM",
            "SGLT2 inhibitor", "dapagliflozin", "empagliflozin", "canagliflozin",
            "GLP-1 receptor agonist", "semaglutide", "liraglutide", "tirzepatide",
            "DPP-4 inhibitor", "sitagliptin",
            "obesity", "bariatric surgery", "weight loss intervention",
            "metabolic syndrome",
            "hypothyroidism", "hyperthyroidism", "thyroid nodule", "thyroid cancer",
            "Graves disease", "Hashimoto thyroiditis",
            "adrenal insufficiency", "Addison disease",
            "Cushing syndrome", "primary hyperaldosteronism", "Conn syndrome",
            "pheochromocytoma", "paraganglioma",
            "acromegaly", "gigantism", "growth hormone",
            "pituitary adenoma", "prolactinoma", "hypopituitarism",
            "diabetes insipidus", "SIADH",
            "hypogonadism", "testosterone deficiency",
            "polycystic ovary syndrome", "PCOS",
            "osteoporosis", "vitamin D deficiency", "bone density",
            "hyperparathyroidism", "hypoparathyroidism", "calcium disorder",
            "neuroendocrine tumour", "NET", "carcinoid",
            "lipid disorder", "hypertriglyceridaemia",
            "metabolic bone disease",
        ],
        "adjacent_terms": [
            "diabetic nephropathy", "diabetic retinopathy", "diabetic neuropathy",
            "cardiovascular outcomes diabetes", "SGLT2 heart failure",
            "GLP-1 weight obesity", "non-alcoholic fatty liver NAFLD diabetes",
            "MODY", "maturity onset diabetes",
            "thyroid cancer surgery", "adrenal mass",
            "reproductive endocrinology fertility",
            "transgender hormone therapy",
        ],
        "exclusion_terms": [
            "plant hormone", "veterinary endocrinology",
        ],
    },

    # ======================================================================
    # GASTROENTEROLOGY
    # ======================================================================
    "gastroenterology": {
        "name": "Gastroenterology",
        "description": (
            "Gastroenterology covers diseases of the oesophagus, stomach, small intestine, "
            "colon, liver, pancreas, and biliary system. Key areas include inflammatory "
            "bowel disease, colorectal cancer screening, upper GI bleeding, liver disease, "
            "endoscopy, GERD, functional GI disorders, pancreatitis, biliary disease, "
            "gut microbiome, and GI oncology."
        ),
        "core_terms": [
            "inflammatory bowel disease", "IBD", "Crohn disease", "ulcerative colitis",
            "biologic IBD", "vedolizumab", "ustekinumab IBD", "infliximab IBD",
            "JAK inhibitor IBD", "tofacitinib IBD",
            "colorectal cancer", "colon cancer", "colonoscopy", "colorectal screening",
            "polyp", "adenoma", "polypectomy",
            "gastrointestinal bleeding", "upper GI bleed", "variceal bleed",
            "GERD", "gastro-oesophageal reflux", "Barrett oesophagus",
            "oesophageal cancer", "gastric cancer", "helicobacter pylori",
            "celiac disease", "coeliac disease", "gluten",
            "irritable bowel syndrome", "IBS", "functional dyspepsia",
            "pancreatitis", "acute pancreatitis", "chronic pancreatitis",
            "pancreatic cancer", "pancreatic adenocarcinoma",
            "ERCP", "EUS", "endoscopic ultrasound",
            "cholangitis", "PSC", "primary sclerosing cholangitis",
            "PBC", "primary biliary cholangitis",
            "gallstone", "cholelithiasis", "cholecystitis",
            "non-alcoholic fatty liver", "NAFLD", "NASH", "MASLD", "MASH",
            "liver cirrhosis", "portal hypertension", "hepatic encephalopathy",
            "hepatocellular carcinoma", "HCC", "liver cancer",
            "hepatitis C", "hepatitis B", "viral hepatitis",
            "autoimmune hepatitis",
            "gut microbiome", "microbiota", "faecal transplant", "FMT",
            "capsule endoscopy", "small bowel", "small intestine",
            "eosinophilic oesophagitis",
            "endoscopy quality", "adenoma detection rate",
        ],
        "adjacent_terms": [
            "obesity GI", "bariatric GI complications",
            "immunosuppression GI infection", "CMV colitis",
            "GI side effects oncology",
            "COVID-19 GI",
            "nutritional support GI",
            "paediatric IBD", "Crohn disease child", "ulcerative colitis child",
            "celiac disease child", "paediatric celiac",
        ],
        "exclusion_terms": [
            "cardiac output", "pulmonary gastric",
        ],
    },

    # ======================================================================
    # GENERAL INTERNAL MEDICINE
    # ======================================================================
    "general_internal_medicine": {
        "name": "General Internal Medicine",
        "description": (
            "General internal medicine covers undifferentiated complex adult illness, "
            "multimorbidity, hospital medicine, preventive care, chronic disease management, "
            "health system quality improvement, patient safety, medication reconciliation, "
            "transitions of care, diagnostic reasoning, and broadly applicable clinical "
            "pharmacology and evidence-based medicine."
        ),
        "core_terms": [
            "multimorbidity", "polypharmacy", "medication reconciliation",
            "hospital medicine", "inpatient medicine", "acute medicine",
            "preventive care", "clinical preventive services",
            "health screening", "cancer screening general",
            "chronic disease management", "self-management",
            "diagnostic reasoning", "diagnostic error",
            "clinical decision-making", "evidence-based medicine",
            "patient safety", "medical error", "adverse drug event",
            "transitions of care", "discharge planning", "readmission",
            "quality improvement", "QI healthcare", "value-based care",
            "clinical guideline adherence", "de-prescribing",
            "venous thromboembolism prophylaxis", "DVT prevention",
            "healthcare-associated infection", "Clostridioides difficile",
            "antibiotic stewardship", "antimicrobial resistance general",
            "frailty", "functional decline hospitalised",
            "palliative care general", "goals of care",
            "health literacy", "patient communication",
            "sleep disorders general", "insomnia",
        ],
        "adjacent_terms": [
            "primary care interface", "specialist generalist",
            "virtual care", "telemedicine general",
            "social determinants of health",
            "healthcare equity",
            "artificial intelligence clinical decision",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # GERIATRIC MEDICINE
    # ======================================================================
    "geriatrics": {
        "name": "Geriatric Medicine",
        "description": (
            "Geriatric medicine focuses on the care of older adults, addressing frailty, "
            "dementia, delirium, falls prevention, polypharmacy, functional decline, "
            "comprehensive geriatric assessment, age-related syndromes, care of older "
            "adults in hospital and community, end-of-life care, and age-appropriate "
            "clinical trial considerations."
        ),
        "core_terms": [
            "older adults", "elderly", "frailty", "frailty index",
            "comprehensive geriatric assessment", "CGA",
            "dementia", "Alzheimer disease", "vascular dementia", "Lewy body dementia",
            "mild cognitive impairment", "MCI",
            "delirium", "acute confusional state",
            "falls prevention", "fall risk", "osteoporosis hip fracture",
            "hip fracture older adults", "fragility fracture",
            "polypharmacy older", "de-prescribing",
            "sarcopenia", "muscle loss ageing",
            "functional decline", "activities of daily living", "ADL",
            "urinary incontinence older", "pressure ulcer",
            "elder abuse", "social isolation older",
            "age-related macular degeneration", "cataract older",
            "hearing loss ageing", "presbycusis",
            "nutrition elderly", "malnutrition older",
            "care home", "long-term care", "nursing home",
            "palliative care geriatric", "end-of-life older",
            "anticholinergic burden", "Beers criteria",
            "perioperative care older adult",
        ],
        "adjacent_terms": [
            "COVID-19 older adults", "COVID frailty",
            "heart failure older", "atrial fibrillation elderly",
            "diabetes older adults",
            "cancer treatment older adult",
            "driving fitness older",
            "caregiver burden",
        ],
        "exclusion_terms": [
            "paediatric", "neonatal",
        ],
    },

    # ======================================================================
    # HEMATOLOGY
    # ======================================================================
    "hematology": {
        "name": "Hematology",
        "description": (
            "Hematology covers blood and bone marrow diseases including anaemias, "
            "haemoglobinopathies, clotting disorders, haematological malignancies "
            "(leukaemia, lymphoma, myeloma, MDS, MPN), stem cell transplantation, "
            "CAR-T cell therapy, anticoagulation, bleeding disorders, platelet disorders, "
            "and transfusion medicine."
        ),
        "core_terms": [
            "anaemia", "anemia", "iron deficiency anaemia", "haemolytic anaemia",
            "aplastic anaemia", "haemolytic uraemic syndrome",
            "sickle cell disease", "thalassaemia", "haemoglobinopathy",
            "leukaemia", "acute myeloid leukaemia", "AML",
            "acute lymphoblastic leukaemia", "ALL",
            "chronic myeloid leukaemia", "CML", "BCR-ABL", "tyrosine kinase inhibitor",
            "chronic lymphocytic leukaemia", "CLL",
            "lymphoma", "diffuse large B-cell lymphoma", "DLBCL",
            "follicular lymphoma", "Hodgkin lymphoma",
            "multiple myeloma", "plasma cell dyscrasia",
            "myelodysplastic syndrome", "MDS",
            "myeloproliferative neoplasm", "MPN",
            "polycythaemia vera", "essential thrombocythaemia", "myelofibrosis",
            "stem cell transplantation", "haematopoietic stem cell transplant", "HSCT",
            "allogeneic transplant", "autologous transplant",
            "CAR-T cell", "chimeric antigen receptor",
            "bispecific antibody haematology",
            "anticoagulation", "venous thromboembolism", "DVT", "pulmonary embolism",
            "heparin", "warfarin", "DOAC", "direct oral anticoagulant",
            "rivaroxaban", "apixaban", "edoxaban", "dabigatran",
            "thrombocytopenia", "ITP", "immune thrombocytopenia",
            "HIT", "heparin-induced thrombocytopenia",
            "haemophilia", "von Willebrand disease", "bleeding disorder",
            "factor replacement", "emicizumab",
            "bone marrow biopsy", "bone marrow failure",
            "transfusion medicine", "blood transfusion", "transfusion reaction",
            "rituximab", "obinutuzumab", "venetoclax",
            "BTK inhibitor", "ibrutinib", "acalabrutinib",
            "GVHD", "graft-versus-host disease",
        ],
        "adjacent_terms": [
            "coagulation disorder", "thrombophilia",
            "cancer-associated thrombosis",
            "anaemia of chronic disease",
            "haematology COVID",
            "checkpoint inhibitor haematology toxicity",
        ],
        "exclusion_terms": [
            "haemodynamic", "haematoma surgical",
        ],
    },

    # ======================================================================
    # INFECTIOUS DISEASES
    # ======================================================================
    "infectious_diseases": {
        "name": "Infectious Diseases",
        "description": (
            "Infectious diseases covers the diagnosis, treatment, and prevention of bacterial, "
            "viral, fungal, and parasitic infections, including HIV/AIDS, tuberculosis, "
            "antimicrobial resistance, sexually transmitted infections, emerging pathogens, "
            "healthcare-associated infections, travel medicine, vaccines, sepsis microbiology, "
            "opportunistic infections, and infection control."
        ),
        "core_terms": [
            "bacterial infection", "antibiotic treatment", "antimicrobial therapy",
            "antimicrobial resistance", "AMR", "MRSA", "VRE", "CRE",
            "carbapenem-resistant", "ESBL",
            "antibiotic stewardship",
            "HIV", "HIV treatment", "antiretroviral therapy", "ART",
            "pre-exposure prophylaxis", "PrEP",
            "tuberculosis", "TB", "MDR-TB", "XDR-TB",
            "sexually transmitted infection", "STI", "gonorrhoea", "chlamydia", "syphilis",
            "hepatitis B treatment", "hepatitis C treatment", "direct-acting antiviral",
            "COVID-19", "SARS-CoV-2", "nirmatrelvir", "paxlovid", "remdesivir",
            "influenza", "respiratory syncytial virus", "RSV",
            "pneumonia", "community-acquired pneumonia", "hospital-acquired pneumonia",
            "fungal infection", "candida", "aspergillus", "cryptococcus",
            "parasitic infection", "malaria", "dengue",
            "healthcare-associated infection", "Clostridioides difficile",
            "bloodstream infection", "bacteraemia", "candidaemia",
            "endocarditis infective", "septic arthritis infectious",
            "meningitis bacterial", "meningitis viral", "encephalitis",
            "travel medicine", "vaccination travel",
            "vaccine efficacy", "immunisation",
            "opportunistic infection", "immunocompromised infection",
            "infection control", "contact precautions",
            "sepsis microbiology",
            "duration of antibiotic therapy", "oral switch antibiotic",
        ],
        "adjacent_terms": [
            "post-COVID long COVID infection",
            "pandemic preparedness",
            "infection immunocompromised transplant",
            "infection oncology",
            "HIV comorbidity",
            "global health infection",
        ],
        "exclusion_terms": [
            "sterile technique general", "infection wound non-specific",
        ],
    },

    # ======================================================================
    # MEDICAL BIOCHEMISTRY
    # ======================================================================
    "medical_biochemistry": {
        "name": "Medical Biochemistry",
        "description": (
            "Medical biochemistry covers clinical laboratory science including biomarker "
            "development and validation, metabolic disease diagnosis, point-of-care testing, "
            "laboratory reference intervals, mass spectrometry in clinical labs, newborn "
            "screening, inborn errors of metabolism, toxicology screening, and laboratory "
            "quality assurance."
        ),
        "core_terms": [
            "clinical laboratory", "laboratory diagnosis", "biomarker validation",
            "clinical chemistry", "laboratory reference interval",
            "point-of-care testing", "POCT",
            "mass spectrometry clinical", "LC-MS clinical",
            "inborn errors of metabolism", "metabolic disease screening",
            "newborn screening", "tandem mass spectrometry newborn",
            "amino acid disorder", "organic acidaemia", "fatty acid oxidation",
            "lysosomal storage disease",
            "laboratory quality assurance", "analytical validation",
            "diagnostic accuracy", "sensitivity specificity biomarker",
            "troponin assay", "high-sensitivity troponin",
            "HbA1c measurement", "glucose measurement",
            "thyroid function test", "free T4 assay",
            "drug monitoring therapeutic", "TDM",
            "toxicology screening", "drug of abuse testing",
            "lipoprotein analysis", "lipid panel",
            "creatinine eGFR measurement",
        ],
        "adjacent_terms": [
            "genetic testing laboratory", "next-generation sequencing clinical",
            "pharmacogenomics", "metabolomics clinical",
            "liquid biopsy", "circulating tumour DNA",
        ],
        "exclusion_terms": [
            "basic science biochemistry", "protein synthesis basic",
        ],
    },

    # ======================================================================
    # MEDICAL GENETICS & GENOMICS
    # ======================================================================
    "medical_genetics": {
        "name": "Medical Genetics & Genomics",
        "description": (
            "Medical genetics and genomics covers hereditary conditions, chromosomal disorders, "
            "genetic counselling, prenatal diagnosis, newborn screening, rare genetic diseases, "
            "gene therapy, genome sequencing in clinical care, pharmacogenomics, cancer genetics, "
            "polygenic risk scores, and the ethical, legal, and social implications of genomics."
        ),
        "core_terms": [
            "genetic counselling", "hereditary disease", "inherited disorder",
            "chromosomal abnormality", "aneuploidy",
            "whole exome sequencing", "whole genome sequencing", "WES", "WGS",
            "variant of uncertain significance", "VUS", "pathogenic variant",
            "gene therapy", "gene editing", "CRISPR",
            "rare disease genetics", "orphan disease",
            "prenatal diagnosis", "amniocentesis", "chorionic villus sampling",
            "cell-free fetal DNA", "NIPT", "non-invasive prenatal testing",
            "newborn screening genetics",
            "pharmacogenomics", "CYP2D6", "CYP2C19",
            "hereditary cancer", "BRCA1", "BRCA2",
            "Lynch syndrome", "hereditary colorectal cancer",
            "polygenic risk score",
            "mitochondrial disease",
            "connective tissue disorder genetic", "Marfan syndrome", "Ehlers-Danlos",
            "inborn error metabolism genetic",
            "genetic testing direct-to-consumer",
            "return of genetic results",
            "liquid biopsy somatic mutation",
        ],
        "adjacent_terms": [
            "precision medicine genomics",
            "biobank genomics", "population genomics",
            "AI genomics",
            "epigenetics clinical",
        ],
        "exclusion_terms": [
            "plant genetics", "agricultural genomics",
        ],
    },

    # ======================================================================
    # MEDICAL MICROBIOLOGY (Laboratory)
    # ======================================================================
    "medical_microbiology": {
        "name": "Medical Microbiology",
        "description": (
            "Medical microbiology (laboratory) covers clinical microbiology diagnostics, "
            "antimicrobial susceptibility testing, molecular diagnostics for infection, "
            "infection control programs, surveillance of antimicrobial resistance, "
            "laboratory response to outbreaks, rapid diagnostics, and microbiology "
            "quality assurance."
        ),
        "core_terms": [
            "clinical microbiology", "antimicrobial susceptibility testing", "AST",
            "minimum inhibitory concentration", "MIC",
            "blood culture", "culture result", "culture interpretation",
            "rapid diagnostic test infection", "PCR infection",
            "multiplex PCR respiratory", "syndromic testing",
            "infection surveillance", "outbreak investigation",
            "antimicrobial resistance surveillance",
            "carbapenemase", "KPC", "NDM", "OXA-48",
            "MRSA decolonisation", "MRSA surveillance",
            "Clostridioides difficile diagnosis", "C diff testing",
            "infection control laboratory",
            "whole genome sequencing outbreak", "WGS epidemiology",
            "MALDI-TOF identification",
            "mycobacterium tuberculosis laboratory",
            "fungal culture", "antifungal susceptibility",
            "procalcitonin", "CRP infection", "white cell count",
        ],
        "adjacent_terms": [
            "antimicrobial stewardship",
            "hospital epidemiology",
            "COVID-19 diagnostics",
            "wastewater surveillance",
        ],
        "exclusion_terms": [
            "environmental microbiology", "food microbiology",
        ],
    },

    # ======================================================================
    # MEDICAL ONCOLOGY
    # ======================================================================
    "medical_oncology": {
        "name": "Medical Oncology",
        "description": (
            "Medical oncology covers systemic treatment of all solid cancers including chemotherapy, "
            "targeted therapy, immunotherapy (checkpoint inhibitors, CAR-T), endocrine "
            "therapy, antibody-drug conjugates, and supportive care. Includes breast, lung, "
            "colorectal, prostate, bladder, gastric, pancreatic, gynecologic (endometrial, "
            "cervical, ovarian, uterine), renal cell carcinoma, hepatocellular carcinoma, "
            "melanoma, thyroid, head and neck, sarcoma, and haematologic cancers in solid "
            "tumour context, clinical trials, biomarker-driven therapy, and cancer survivorship."
        ),
        "core_terms": [
            "checkpoint inhibitor", "PD-1", "PD-L1", "CTLA-4",
            "pembrolizumab", "nivolumab", "atezolizumab", "durvalumab",
            "immunotherapy cancer", "immune-related adverse event", "irAE",
            "targeted therapy", "EGFR inhibitor", "ALK inhibitor", "BRAF inhibitor",
            "HER2 positive", "trastuzumab", "pertuzumab", "T-DM1", "T-DXd",
            "antibody-drug conjugate",
            "chemotherapy", "cytotoxic chemotherapy", "FOLFOX", "FOLFIRI",
            "breast cancer treatment", "hormonal therapy breast",
            "CDK4/6 inhibitor", "palbociclib", "ribociclib", "abemaciclib",
            "PARP inhibitor", "olaparib", "niraparib",
            "lung cancer treatment", "NSCLC", "SCLC",
            "colorectal cancer treatment", "metastatic colorectal",
            "prostate cancer treatment", "castration-resistant prostate",
            "ARSI", "enzalutamide", "abiraterone", "darolutamide",
            "pancreatic cancer treatment",
            "gastric cancer treatment", "oesophageal cancer treatment",
            "bladder cancer treatment", "urothelial carcinoma",
            "ovarian cancer treatment",
            "cancer biomarker", "tumour mutational burden", "MSI",
            "liquid biopsy cancer", "circulating tumour DNA",
            "clinical trial oncology", "phase III oncology",
            "cancer survivorship", "late effects chemotherapy",
            "nausea vomiting oncology", "CINV",
            "neutropenia febrile", "growth factor GCSF",
            "palliative chemotherapy",
            # Gynaecologic oncology
            "endometrial cancer", "uterine cancer", "endometrial carcinoma",
            "uterine carcinoma", "endometrioid carcinoma",
            "gynaecologic oncology", "gynaecologic cancer", "gynecologic cancer",
            "cervical cancer treatment", "cervical cancer chemotherapy", "cervical cancer systemic",
            "ovarian cancer systemic", "ovarian cancer chemotherapy", "carboplatin ovarian",
            "bevacizumab ovarian", "PARP inhibitor ovarian",
            "vulvar cancer treatment",
            # HCC
            "hepatocellular carcinoma treatment", "sorafenib HCC", "lenvatinib HCC",
            "atezolizumab bevacizumab HCC", "HCC systemic therapy",
            # RCC
            "renal cell carcinoma systemic", "renal cell carcinoma treatment",
            "sunitinib", "pazopanib", "nivolumab RCC", "pembrolizumab RCC",
            "cabozantinib", "axitinib",
            # Melanoma
            "melanoma treatment", "metastatic melanoma",
            "BRAF inhibitor melanoma", "vemurafenib", "dabrafenib", "trametinib",
            "MEK inhibitor",
            # Thyroid cancer
            "thyroid cancer systemic", "lenvatinib thyroid", "sorafenib thyroid",
            "radioiodine refractory thyroid",
            # Head and neck
            "head and neck cancer systemic", "cetuximab head neck",
            "immunotherapy head neck", "pembrolizumab head neck",
            # Sarcoma
            "sarcoma systemic", "soft tissue sarcoma treatment",
            "imatinib GIST", "gastrointestinal stromal tumour", "GIST",
            "doxorubicin sarcoma", "trabectedin",
            # Other
            "mesothelioma systemic", "merkel cell carcinoma treatment",
            "neuroendocrine tumour systemic", "everolimus NET", "somatostatin analogue",
            "anal cancer treatment", "penile cancer",
        ],
        "adjacent_terms": [
            "cardio-oncology cardiotoxicity",
            "renal toxicity immunotherapy",
            "hepatotoxicity checkpoint inhibitor",
            "cancer screening population",
            "precision oncology",
        ],
        "exclusion_terms": [
            "haematologic malignancy stem cell",
            "radiation oncology only",
        ],
    },

    # ======================================================================
    # NEPHROLOGY
    # ======================================================================
    "nephrology": {
        "name": "Nephrology",
        "description": (
            "Nephrology covers chronic kidney disease, acute kidney injury, glomerulonephritis, "
            "nephrotic syndrome, hypertension and the kidney, dialysis (haemodialysis and "
            "peritoneal dialysis), kidney transplantation, electrolyte and acid-base disorders, "
            "renal pharmacology, polycystic kidney disease, lupus nephritis, and ANCA vasculitis."
        ),
        "core_terms": [
            "chronic kidney disease", "CKD", "eGFR", "creatinine",
            "acute kidney injury", "AKI", "acute renal failure",
            "haemodialysis", "peritoneal dialysis", "dialysis",
            "kidney transplantation", "renal transplant", "transplant rejection",
            "glomerulonephritis", "nephrotic syndrome", "nephritic syndrome",
            "proteinuria", "albuminuria", "urine albumin-to-creatinine ratio",
            "IgA nephropathy", "membranous nephropathy",
            "focal segmental glomerulosclerosis", "FSGS",
            "lupus nephritis", "ANCA vasculitis", "anti-GBM disease",
            "polycystic kidney disease", "ADPKD",
            "diabetic nephropathy", "diabetic kidney disease",
            "hypertensive nephropathy", "renal artery stenosis",
            "electrolyte disorder", "hyponatraemia", "hypernatraemia",
            "hyperkalaemia", "hypokalaemia",
            "acid-base disorder", "metabolic acidosis", "metabolic alkalosis",
            "renal anaemia", "erythropoiesis-stimulating agent", "ESA",
            "SGLT2 inhibitor kidney", "finerenone", "sparsentan",
            "ACE inhibitor CKD", "ARB CKD",
            "kidney stone", "nephrolithiasis", "urolithiasis",
            "contrast nephropathy", "AKI contrast",
            "renal replacement therapy",
        ],
        "adjacent_terms": [
            "cardiorenal syndrome", "heart failure kidney",
            "diabetes kidney outcomes",
            "hypertension kidney",
            "COVID-19 AKI",
            "perioperative AKI",
            "intensive care AKI",
        ],
        "exclusion_terms": [
            "urological surgery kidney",
        ],
    },

    # ======================================================================
    # NEUROLOGY
    # ======================================================================
    "neurology": {
        "name": "Neurology",
        "description": (
            "Neurology covers diseases of the brain, spinal cord, peripheral nervous system, "
            "and muscle, including stroke, epilepsy, multiple sclerosis, Parkinson disease, "
            "dementia, headache, neuromuscular disease, ALS, neuroimmunology, neurogenetics, "
            "neuro-oncology, sleep disorders, and neurointensive care."
        ),
        "core_terms": [
            "stroke", "ischaemic stroke", "haemorrhagic stroke", "TIA",
            "thrombolysis tPA stroke", "thrombectomy mechanical",
            "stroke prevention", "anticoagulation stroke AF",
            "epilepsy", "seizure", "status epilepticus",
            "anti-seizure medication", "levetiracetam", "lamotrigine",
            "multiple sclerosis", "MS", "relapsing-remitting MS",
            "disease-modifying therapy MS", "natalizumab", "ocrelizumab",
            "ofatumumab", "cladribine",
            "Parkinson disease", "Parkinson treatment", "levodopa",
            "deep brain stimulation", "Parkinson",
            "dementia", "Alzheimer disease treatment",
            "anti-amyloid therapy", "lecanemab", "donanemab",
            "headache", "migraine", "cluster headache",
            "CGRP antagonist", "erenumab", "fremanezumab",
            "ALS", "amyotrophic lateral sclerosis",
            "Guillain-Barré syndrome", "GBS",
            "myasthenia gravis", "neuromuscular junction",
            "peripheral neuropathy", "Charcot-Marie-Tooth",
            "brain tumour", "glioblastoma", "glioma",
            "neuroimmunology", "autoimmune encephalitis", "NMDA receptor antibody",
            "neuromyelitis optica", "NMOSD",
            "cerebral venous thrombosis",
            "subarachnoid haemorrhage", "cerebral aneurysm",
            "intracranial pressure", "hydrocephalus",
            "EEG", "nerve conduction study", "electromyography",
            "neuroimaging", "brain MRI", "CT head",
        ],
        "adjacent_terms": [
            "cognitive impairment mild",
            "COVID-19 neurological",
            "sleep apnoea neurological",
            "pain neurological",
            "psychiatric neurology interface",
        ],
        "exclusion_terms": [
            "neurosurgery procedural", "veterinary neurology",
        ],
    },

    # ======================================================================
    # PHYSICAL MEDICINE & REHABILITATION
    # ======================================================================
    "physiatry": {
        "name": "Physical Medicine & Rehabilitation",
        "description": (
            "Physical medicine and rehabilitation covers functional restoration after "
            "neurological injury (stroke, spinal cord, TBI), musculoskeletal rehabilitation, "
            "prosthetics and orthotics, pain rehabilitation, electrodiagnostics, spasticity "
            "management, cancer rehabilitation, cardiac rehabilitation, and pulmonary rehabilitation."
        ),
        "core_terms": [
            "rehabilitation", "functional recovery", "functional outcome",
            "stroke rehabilitation", "post-stroke recovery",
            "spinal cord injury rehabilitation", "SCI rehabilitation",
            "traumatic brain injury rehabilitation", "TBI rehabilitation",
            "amputee rehabilitation", "prosthetics", "orthotics",
            "spasticity", "botulinum toxin spasticity",
            "electrodiagnostics", "nerve conduction study", "EMG",
            "musculoskeletal rehabilitation", "physiotherapy",
            "occupational therapy", "speech therapy",
            "cardiac rehabilitation", "exercise training cardiac",
            "pulmonary rehabilitation", "COPD rehabilitation",
            "cancer rehabilitation", "oncology rehabilitation",
            "chronic pain rehabilitation", "interdisciplinary pain",
            "return to work", "disability assessment",
            "activities of daily living", "Barthel index", "FIM",
            "wheelchair", "assistive device",
            "neuroplasticity", "cortical reorganisation",
        ],
        "adjacent_terms": [
            "long COVID rehabilitation",
            "ICU rehabilitation", "post-ICU",
            "paediatric rehabilitation",
            "geriatric rehabilitation",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # PSYCHIATRY
    # ======================================================================
    "psychiatry": {
        "name": "Psychiatry",
        "description": (
            "Psychiatry covers the diagnosis and treatment of mental health disorders "
            "including depression, anxiety, bipolar disorder, schizophrenia, PTSD, OCD, "
            "eating disorders, substance use disorders, personality disorders, ADHD, "
            "autism spectrum disorder, psychopharmacology, psychotherapy, suicide and "
            "self-harm, forensic psychiatry, and consultation-liaison psychiatry."
        ),
        "core_terms": [
            "depression", "major depressive disorder", "MDD",
            "antidepressant", "SSRI", "SNRI", "venlafaxine", "sertraline",
            "treatment-resistant depression", "ketamine depression", "esketamine",
            "anxiety disorder", "generalised anxiety disorder", "GAD",
            "panic disorder", "social anxiety",
            "bipolar disorder", "lithium", "mood stabiliser",
            "schizophrenia", "psychosis", "antipsychotic",
            "clozapine", "risperidone", "olanzapine", "aripiprazole",
            "PTSD", "post-traumatic stress disorder",
            "OCD", "obsessive-compulsive disorder",
            "eating disorder", "anorexia nervosa", "bulimia nervosa", "binge eating",
            "substance use disorder", "alcohol use disorder",
            "opioid use disorder", "methadone", "buprenorphine",
            "ADHD", "attention deficit hyperactivity disorder", "stimulant medication",
            "autism spectrum disorder", "ASD",
            "personality disorder", "borderline personality disorder",
            "suicidality", "suicide", "self-harm", "suicide prevention",
            "psychotherapy", "CBT", "cognitive behavioural therapy",
            "DBT", "dialectical behaviour therapy",
            "electroconvulsive therapy", "ECT",
            "transcranial magnetic stimulation", "TMS",
            "mental health", "psychiatric diagnosis",
            "consultation-liaison psychiatry",
            "perinatal psychiatry", "postpartum depression",
        ],
        "adjacent_terms": [
            "COVID-19 mental health",
            "long COVID psychiatric",
            "digital mental health", "smartphone mental health",
            "youth mental health",
            "social media mental health",
            "cannabis psychiatric",
        ],
        "exclusion_terms": [
            "brain tumour psychiatry", "neurological cause only",
        ],
    },

    # ======================================================================
    # RADIATION ONCOLOGY
    # ======================================================================
    "radiation_oncology": {
        "name": "Radiation Oncology",
        "description": (
            "Radiation oncology covers the use of ionising radiation in cancer treatment, "
            "including external beam radiotherapy, brachytherapy, stereotactic body "
            "radiotherapy (SBRT/SABR), stereotactic radiosurgery, proton therapy, "
            "radiation planning, radiation toxicity, combined modality therapy, "
            "and radiation biology."
        ),
        "core_terms": [
            "radiotherapy", "radiation therapy", "external beam radiation",
            "stereotactic body radiotherapy", "SBRT", "SABR",
            "stereotactic radiosurgery", "SRS", "CyberKnife", "Gamma Knife",
            "brachytherapy", "prostate brachytherapy", "cervical brachytherapy",
            "proton therapy", "carbon ion therapy", "particle therapy",
            "intensity-modulated radiotherapy", "IMRT", "VMAT",
            "radiation planning", "treatment planning", "dosimetry",
            "radiation toxicity", "late effects radiation",
            "radiation pneumonitis", "radiation fibrosis",
            "chemoradiation", "concurrent chemoradiotherapy",
            "adjuvant radiotherapy", "neoadjuvant radiation",
            "palliative radiotherapy", "bone metastasis radiation",
            "brain metastasis radiation", "whole brain radiotherapy",
            "lung cancer radiotherapy", "NSCLC radiation",
            "prostate cancer radiation", "breast cancer radiation",
            "head and neck cancer radiation",
            "radiation biology", "DNA damage radiation",
            "radioimmunotherapy",
        ],
        "adjacent_terms": [
            "radiomics", "AI radiation planning",
            "adaptive radiotherapy",
            "reirradiation",
        ],
        "exclusion_terms": [
            "radiation safety occupational only",
        ],
    },

    # ======================================================================
    # RESPIROLOGY / PULMONOLOGY
    # ======================================================================
    "respirology": {
        "name": "Respirology",
        "description": (
            "Respirology covers diseases of the respiratory system including COPD, asthma, "
            "interstitial lung disease, pulmonary hypertension, lung cancer, pleural disease, "
            "sleep-disordered breathing, respiratory infections, pulmonary vascular disease, "
            "bronchoscopy, mechanical ventilation in non-ICU contexts, and lung transplantation."
        ),
        "core_terms": [
            "COPD", "chronic obstructive pulmonary disease", "emphysema",
            "exacerbation COPD", "bronchodilator", "LAMA", "LABA",
            "inhaled corticosteroid", "triple therapy COPD",
            "asthma", "severe asthma", "biologic asthma",
            "mepolizumab", "benralizumab", "dupilumab asthma", "tezepelumab",
            "interstitial lung disease", "ILD", "pulmonary fibrosis",
            "idiopathic pulmonary fibrosis", "IPF",
            "nintedanib", "pirfenidone",
            "hypersensitivity pneumonitis", "connective tissue ILD",
            "lung cancer", "non-small cell lung cancer", "NSCLC",
            "EGFR lung", "ALK lung", "PD-L1 lung",
            "pleural effusion", "pleural mesothelioma",
            "pneumothorax",
            "obstructive sleep apnoea", "OSA", "CPAP", "sleep-disordered breathing",
            "pulmonary embolism", "pulmonary vascular disease",
            "pulmonary hypertension",
            "pneumonia", "community-acquired pneumonia", "atypical pneumonia",
            "bronchiectasis",
            "cystic fibrosis", "CFTR modulator", "ivacaftor", "elexacaftor-tezacaftor",
            "lung transplantation",
            "bronchoscopy", "endobronchial ultrasound", "EBUS",
            "spirometry", "pulmonary function test",
            "high-flow nasal oxygen", "non-invasive ventilation", "NIV", "CPAP BiPAP",
        ],
        "adjacent_terms": [
            "COVID-19 respiratory", "COVID-19 pulmonary",
            "long COVID respiratory",
            "pulmonary rehabilitation",
            "smoking cessation",
            "air pollution respiratory",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # RHEUMATOLOGY
    # ======================================================================
    "rheumatology": {
        "name": "Rheumatology",
        "description": (
            "Rheumatology covers inflammatory arthritis, connective tissue diseases, "
            "vasculitis (including Kawasaki disease, IgA vasculitis, ANCA vasculitis, "
            "giant cell arteritis), juvenile idiopathic arthritis, crystal arthropathies, "
            "and musculoskeletal disease including rheumatoid arthritis, psoriatic arthritis, "
            "ankylosing spondylitis, SLE, Sjögren syndrome, myositis, scleroderma, gout, "
            "PMR, Behçet disease, IgG4-related disease, adult-onset Still disease, "
            "antiphospholipid syndrome, and the pharmacology of DMARDs and biologics."
        ),
        "core_terms": [
            "rheumatoid arthritis", "RA treatment", "disease activity RA",
            "DAS28", "ACR/EULAR",
            "psoriatic arthritis",
            "ankylosing spondylitis", "axial spondyloarthritis", "nr-axSpA",
            "TNF inhibitor", "adalimumab", "etanercept", "certolizumab",
            "IL-6 inhibitor", "tocilizumab", "sarilumab",
            "IL-17 inhibitor", "secukinumab", "ixekizumab",
            "IL-12/23 inhibitor", "ustekinumab rheumatology",
            "IL-23 inhibitor", "guselkumab", "risankizumab rheum",
            "JAK inhibitor rheumatology", "tofacitinib", "baricitinib", "upadacitinib",
            "methotrexate", "leflunomide", "hydroxychloroquine",
            "DMARD", "biologic DMARD",
            "systemic lupus erythematosus", "SLE", "lupus",
            "belimumab", "anifrolumab",
            "lupus nephritis treatment",
            "antiphospholipid syndrome", "APS",
            "Sjögren syndrome", "primary Sjögren",
            "myositis", "dermatomyositis", "polymyositis",
            "scleroderma", "systemic sclerosis",
            "vasculitis", "ANCA vasculitis", "GPA", "MPA",
            "giant cell arteritis", "temporal arteritis", "tocilizumab GCA",
            "polymyalgia rheumatica", "PMR",
            "gout", "hyperuricaemia", "urate-lowering therapy", "allopurinol", "febuxostat",
            "calcium pyrophosphate", "pseudogout",
            "osteoarthritis",
            "fibromyalgia",
            "antinuclear antibody", "ANA", "ANCA", "anti-dsDNA",
            # Paediatric rheumatology conditions
            "Kawasaki disease", "Kawasaki", "mucocutaneous lymph node syndrome",
            "coronary artery aneurysm Kawasaki", "IVIG Kawasaki", "aspirin Kawasaki",
            "juvenile idiopathic arthritis", "JIA", "oligoarticular JIA",
            "systemic JIA", "Still disease", "juvenile arthritis",
            "adult-onset Still disease", "AOSD",
            "IgA vasculitis", "Henoch-Schönlein purpura", "HSP vasculitis",
            "childhood vasculitis", "paediatric vasculitis",
            "reactive arthritis", "post-infectious arthritis",
            "Behçet disease", "Behcet syndrome",
            "IgG4-related disease", "IgG4-RD",
            "relapsing polychondritis",
            "autoinflammatory disease", "periodic fever syndrome",
            "familial Mediterranean fever", "CAPS", "TRAPS",
        ],
        "adjacent_terms": [
            "rheumatic immune checkpoint toxicity",
            "COVID-19 autoimmune",
            "rheumatic disease pregnancy",
            "osteoporosis RA",
            "paediatric rheumatology",
            "biologics juvenile arthritis",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # CARDIAC SURGERY
    # ======================================================================
    "cardiac_surgery": {
        "name": "Cardiac Surgery",
        "description": (
            "Cardiac surgery covers operative management of coronary artery disease, "
            "valvular heart disease, congenital heart disease in adults, aortic disease, "
            "heart failure surgery, cardiac transplantation, mechanical circulatory support, "
            "arrhythmia surgery, and perioperative cardiac surgical care."
        ),
        "core_terms": [
            "coronary artery bypass grafting", "CABG", "off-pump CABG",
            "valve replacement", "valve repair", "mitral repair", "aortic valve replacement",
            "TAVR vs SAVR", "transcatheter vs surgical valve",
            "aortic root replacement", "Bentall procedure",
            "aortic arch surgery", "circulatory arrest",
            "aortic dissection surgery", "type A aortic dissection",
            "heart transplantation", "cardiac transplantation",
            "LVAD", "ventricular assist device surgery",
            "congenital heart disease adult surgery",
            "Maze procedure", "surgical ablation AF",
            "perioperative cardiac surgery", "cardiac surgery outcomes",
            "cardiopulmonary bypass", "CPB",
            "transcatheter structural heart", "MitraClip",
            "endocarditis surgery",
            "cardiac surgery mortality", "STS score",
        ],
        "adjacent_terms": [
            "hybrid cardiac procedure",
            "minimally invasive cardiac surgery",
            "ECMO cardiac surgery",
            "redo cardiac surgery",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # GENERAL SURGERY
    # ======================================================================
    "general_surgery": {
        "name": "General Surgery",
        "description": (
            "General surgery covers elective and emergency abdominal surgery, colorectal "
            "surgery, hepatobiliary surgery, endocrine surgery (thyroid, adrenal, parathyroid), "
            "hernia repair, breast surgery (oncological and reconstructive), trauma surgery, "
            "laparoscopic and robotic procedures, surgical oncology, and perioperative care."
        ),
        "core_terms": [
            "laparoscopic surgery", "minimally invasive surgery",
            "robotic surgery", "robotic-assisted",
            "appendicectomy", "appendicitis surgery",
            "cholecystectomy", "laparoscopic cholecystectomy",
            "hernia repair", "inguinal hernia", "incisional hernia", "ventral hernia",
            "colorectal surgery", "rectal cancer surgery", "colectomy",
            "low anterior resection", "total mesorectal excision", "TME",
            "hepatectomy", "liver resection", "hepatobiliary surgery",
            "pancreatectomy", "Whipple procedure", "pancreaticoduodenectomy",
            "breast cancer surgery", "mastectomy", "breast conservation",
            "sentinel lymph node biopsy breast",
            "thyroidectomy", "parathyroidectomy", "adrenalectomy",
            "trauma surgery", "damage control surgery",
            "enhanced recovery after surgery", "ERAS",
            "postoperative complication", "anastomotic leak",
            "surgical site infection", "SSI",
            "bariatric surgery", "Roux-en-Y gastric bypass", "sleeve gastrectomy",
            "stoma", "ostomy",
            "oesophageal surgery", "oesophagectomy",
            "splenic surgery", "splenectomy",
        ],
        "adjacent_terms": [
            "perioperative medicine",
            "wound management",
            "surgical simulation", "surgical training",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # NEUROSURGERY
    # ======================================================================
    "neurosurgery": {
        "name": "Neurosurgery",
        "description": (
            "Neurosurgery covers operative management of brain and spine conditions including "
            "brain tumours, cerebrovascular disease, spinal disorders, hydrocephalus, "
            "functional neurosurgery (deep brain stimulation, epilepsy surgery), trauma "
            "neurosurgery, peripheral nerve surgery, and neurosurgical oncology."
        ),
        "core_terms": [
            "craniotomy", "brain tumour surgery", "glioma surgery", "glioblastoma surgery",
            "meningioma surgery", "acoustic neuroma",
            "cerebral aneurysm", "aneurysm clipping", "subarachnoid haemorrhage surgery",
            "arteriovenous malformation", "AVM",
            "cerebrovascular surgery",
            "spine surgery", "discectomy", "laminectomy", "spinal fusion",
            "lumbar disc herniation surgery",
            "cervical disc replacement", "anterior cervical discectomy",
            "spinal cord tumour",
            "hydrocephalus", "ventriculoperitoneal shunt", "VP shunt",
            "deep brain stimulation", "DBS",
            "epilepsy surgery", "temporal lobectomy",
            "intracranial pressure monitoring",
            "traumatic brain injury surgery", "TBI surgery", "decompressive craniectomy",
            "subdural haematoma", "extradural haematoma",
            "peripheral nerve surgery", "carpal tunnel surgery",
            "pituitary surgery", "transsphenoidal surgery",
            "stereotactic biopsy",
        ],
        "adjacent_terms": [
            "intraoperative MRI",
            "awake craniotomy",
            "robotic neurosurgery",
            "radiosurgery",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # OPHTHALMOLOGY
    # ======================================================================
    "ophthalmology": {
        "name": "Ophthalmology",
        "description": (
            "Ophthalmology covers eye diseases and surgery including diabetic retinopathy, "
            "age-related macular degeneration, glaucoma, cataract, refractive surgery, "
            "strabismus, corneal disease, uveitis, retinal detachment, ocular oncology, "
            "neuro-ophthalmology, and anti-VEGF intravitreal therapy."
        ),
        "core_terms": [
            "diabetic retinopathy", "diabetic macular oedema",
            "age-related macular degeneration", "AMD", "wet AMD",
            "anti-VEGF", "ranibizumab", "bevacizumab intravitreal", "aflibercept", "faricimab",
            "intravitreal injection",
            "glaucoma", "open-angle glaucoma", "intraocular pressure",
            "trabeculoplasty", "glaucoma surgery", "trabeculectomy",
            "cataract", "phacoemulsification", "intraocular lens",
            "refractive surgery", "LASIK",
            "corneal disease", "keratoconus", "corneal transplant",
            "uveitis", "ocular inflammation",
            "retinal detachment", "vitrectomy",
            "strabismus", "amblyopia",
            "retinitis pigmentosa", "inherited retinal disease",
            "neuro-ophthalmology", "optic neuritis", "papilloedema",
            "ocular oncology", "uveal melanoma",
            "dry eye disease",
            "visual acuity", "visual field",
        ],
        "adjacent_terms": [
            "telemedicine diabetic screening",
            "AI retinal imaging",
            "gene therapy retina",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # ORTHOPEDIC SURGERY
    # ======================================================================
    "orthopedics": {
        "name": "Orthopedic Surgery",
        "description": (
            "Orthopedic surgery covers musculoskeletal conditions requiring operative or "
            "non-operative treatment, including hip and knee arthroplasty, fracture fixation, "
            "spine surgery, sports medicine surgery, shoulder and elbow surgery, foot and ankle, "
            "paediatric orthopaedics, bone tumour surgery, and arthroplasty revision."
        ),
        "core_terms": [
            "total hip replacement", "total hip arthroplasty", "THA",
            "total knee replacement", "total knee arthroplasty", "TKA",
            "hip fracture", "femoral neck fracture", "intertrochanteric fracture",
            "hip fracture fixation", "hemiarthroplasty",
            "fracture fixation", "intramedullary nail", "ORIF",
            "ACL reconstruction", "anterior cruciate ligament",
            "meniscus repair", "meniscectomy",
            "shoulder arthroplasty", "rotator cuff repair",
            "spinal deformity", "scoliosis correction",
            "lumbar fusion", "vertebral augmentation",
            "bone tumour", "osteosarcoma surgery",
            "arthroplasty infection", "periprosthetic joint infection",
            "revision arthroplasty",
            "perioperative orthopaedic",
            "thromboprophylaxis orthopaedic",
            "osteoarthritis non-operative", "injection knee",
            "paediatric orthopaedics",
            "distal radius fracture", "ankle fracture",
        ],
        "adjacent_terms": [
            "enhanced recovery orthopaedic",
            "tranexamic acid orthopaedic",
            "robotic orthopaedic surgery",
            "virtual reality surgical training",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # OTOLARYNGOLOGY — HEAD & NECK SURGERY
    # ======================================================================
    "otolaryngology": {
        "name": "Otolaryngology — Head & Neck Surgery",
        "description": (
            "Otolaryngology covers diseases of the ear, nose, throat, head, and neck "
            "including hearing loss, cochlear implants, chronic sinusitis, nasal polyps, "
            "head and neck cancer, thyroid surgery, parotid surgery, obstructive sleep "
            "apnoea surgery, voice disorders, vestibular disorders, and paediatric ENT."
        ),
        "core_terms": [
            "hearing loss", "sensorineural hearing loss", "cochlear implant",
            "otitis media", "tympanoplasty",
            "chronic rhinosinusitis", "nasal polyps", "functional endoscopic sinus surgery",
            "dupilumab nasal polyps", "biologic sinusitis",
            "head and neck cancer", "oropharyngeal cancer", "laryngeal cancer",
            "HPV oropharyngeal", "p16 cancer",
            "thyroid surgery ORL", "parathyroid surgery",
            "parotidectomy", "submandibular gland",
            "neck dissection", "lymph node neck",
            "tonsillectomy", "adenoidectomy",
            "obstructive sleep apnoea surgery", "uvulopalatopharyngoplasty",
            "hypoglossal nerve stimulator",
            "voice disorder", "dysphonia", "laryngoscopy",
            "vertigo", "BPPV", "Ménière disease",
            "vestibular rehabilitation",
            "tracheostomy",
        ],
        "adjacent_terms": [
            "free flap reconstruction",
            "radiation head neck",
            "swallowing dysphagia ORL",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # PEDIATRIC SURGERY
    # ======================================================================
    "pediatric_surgery": {
        "name": "Pediatric Surgery",
        "description": (
            "Pediatric surgery covers congenital and acquired surgical conditions in "
            "infants, children, and adolescents, including congenital abnormalities, "
            "paediatric trauma, solid tumours in children (Wilms, neuroblastoma, "
            "hepatoblastoma), neonatal surgery, minimally invasive paediatric procedures, "
            "and paediatric surgical oncology."
        ),
        "core_terms": [
            "paediatric surgery", "pediatric surgery", "neonatal surgery",
            "congenital abnormality", "oesophageal atresia", "tracheoesophageal fistula",
            "anorectal malformation", "Hirschsprung disease",
            "congenital diaphragmatic hernia",
            "pyloric stenosis", "hypertrophic pyloric stenosis",
            "intussusception paediatric",
            "necrotising enterocolitis", "NEC",
            "appendicitis paediatric",
            "inguinal hernia paediatric",
            "Wilms tumour", "nephroblastoma",
            "neuroblastoma",
            "hepatoblastoma", "paediatric liver tumour",
            "paediatric trauma",
            "minimally invasive paediatric",
            "undescended testis", "orchidopexy",
            "paediatric oncology surgery",
        ],
        "adjacent_terms": [
            "congenital heart disease paediatric surgical",
            "paediatric robotic surgery",
        ],
        "exclusion_terms": [
            "paediatric medicine non-surgical",
        ],
    },

    # ======================================================================
    # PLASTIC SURGERY
    # ======================================================================
    "plastic_surgery": {
        "name": "Plastic Surgery",
        "description": (
            "Plastic surgery covers reconstructive and aesthetic procedures including "
            "breast reconstruction, skin cancer reconstruction, free flap reconstruction, "
            "hand surgery, burn management, cleft lip and palate, maxillofacial surgery, "
            "microsurgery, and wound care."
        ),
        "core_terms": [
            "breast reconstruction", "free flap", "DIEP flap",
            "skin graft", "split-thickness skin graft",
            "wound reconstruction", "complex wound",
            "burn management", "burn surgery",
            "hand surgery", "tendon repair", "replantation",
            "microsurgery", "free tissue transfer",
            "cleft lip", "cleft palate",
            "facial reconstruction", "maxillofacial",
            "skin cancer reconstruction", "Mohs defect reconstruction",
            "aesthetic surgery", "breast augmentation", "rhinoplasty",
            "blepharoplasty", "facelift",
            "liposuction", "body contouring",
            "lymphoedema surgery",
            "pressure ulcer reconstruction",
        ],
        "adjacent_terms": [
            "oncoplastic breast surgery",
            "gender affirmation surgery",
            "tissue expander",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # THORACIC SURGERY
    # ======================================================================
    "thoracic_surgery": {
        "name": "Thoracic Surgery",
        "description": (
            "Thoracic surgery covers operative management of lung, oesophageal, pleural, "
            "mediastinal, and chest wall conditions, including lung cancer resection, "
            "VATS lobectomy, oesophagectomy, thymectomy, mesothelioma, lung transplantation, "
            "and management of pleural effusion and pneumothorax."
        ),
        "core_terms": [
            "lung resection", "lobectomy", "segmentectomy", "pneumonectomy",
            "VATS", "video-assisted thoracoscopic surgery",
            "robotic thoracic surgery",
            "lung cancer surgery", "NSCLC surgery", "stage I lung cancer",
            "oesophagectomy", "oesophageal cancer surgery",
            "thymectomy", "thymoma", "mediastinal tumour",
            "mesothelioma surgery", "pleurectomy",
            "pleural effusion management", "talc pleurodesis",
            "pneumothorax surgery", "bullectomy",
            "lung transplantation",
            "chest wall resection",
            "mediastinoscopy", "mediastinal staging",
            "empyema surgery",
        ],
        "adjacent_terms": [
            "neoadjuvant lung cancer",
            "adjuvant osimertinib surgery",
            "stereotactic vs surgery early lung cancer",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # UROLOGY
    # ======================================================================
    "urology": {
        "name": "Urology",
        "description": (
            "Urology covers diseases of the urinary tract and male reproductive system, "
            "including prostate cancer, bladder cancer, kidney cancer, testicular cancer, "
            "benign prostatic hyperplasia, urinary incontinence, kidney stones, erectile "
            "dysfunction, male infertility, robotic prostatectomy, and paediatric urology."
        ),
        "core_terms": [
            "prostate cancer", "localised prostate cancer", "prostate-specific antigen", "PSA",
            "radical prostatectomy", "robotic prostatectomy",
            "prostate biopsy", "MRI prostate", "PSMA PET",
            "active surveillance prostate",
            "bladder cancer", "urothelial carcinoma", "cystectomy",
            "BCG bladder", "intravesical therapy",
            "renal cell carcinoma", "kidney cancer", "partial nephrectomy",
            "testicular cancer", "orchidectomy",
            "benign prostatic hyperplasia", "BPH", "lower urinary tract symptoms", "LUTS",
            "alpha-blocker", "5-alpha reductase inhibitor",
            "urinary incontinence", "stress incontinence", "urgency incontinence",
            "overactive bladder", "pelvic floor",
            "kidney stone", "urolithiasis", "ureteroscopy", "ESWL", "percutaneous nephrolithotomy",
            "erectile dysfunction",
            "male infertility",
            "urinary tract infection", "recurrent UTI",
            "vesicoureteral reflux",
            "neurogenic bladder",
        ],
        "adjacent_terms": [
            "advanced prostate ARSI",
            "immune checkpoint urothelial",
            "retroperitoneal lymph node dissection",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # VASCULAR SURGERY
    # ======================================================================
    "vascular_surgery": {
        "name": "Vascular Surgery",
        "description": (
            "Vascular surgery covers diseases of the arteries, veins, and lymphatics outside "
            "the heart and brain, including aortic aneurysm, peripheral arterial disease, "
            "carotid disease, venous disease, endovascular procedures, dialysis access, "
            "diabetic foot, and limb salvage."
        ),
        "core_terms": [
            "aortic aneurysm", "abdominal aortic aneurysm", "AAA",
            "endovascular aneurysm repair", "EVAR", "TEVAR",
            "aortic dissection",
            "peripheral arterial disease", "PAD",
            "critical limb ischaemia", "critical limb threatening ischaemia", "CLTI",
            "revascularisation lower limb", "bypass surgery peripheral",
            "carotid endarterectomy", "carotid artery stenosis",
            "carotid stenting", "carotid revascularisation",
            "venous disease", "varicose veins", "chronic venous insufficiency",
            "deep vein thrombosis treatment",
            "pulmonary embolism intervention", "catheter-directed thrombolysis",
            "diabetic foot", "foot ulcer vascular", "amputation",
            "dialysis access", "arteriovenous fistula", "AV fistula",
            "mesenteric ischaemia",
            "renovascular hypertension",
            "thoracic outlet syndrome",
        ],
        "adjacent_terms": [
            "antithrombotic peripheral",
            "wound care vascular",
            "endovascular techniques",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # ANATOMICAL PATHOLOGY
    # ======================================================================
    "anatomical_pathology": {
        "name": "Anatomical Pathology",
        "description": (
            "Anatomical pathology covers histopathological diagnosis of disease in tissue "
            "specimens, cytopathology, autopsy pathology, surgical pathology, molecular "
            "pathology of tumours, digital pathology, AI-assisted pathology, biomarker "
            "immunohistochemistry, and tumour grading and staging."
        ),
        "core_terms": [
            "histopathology", "surgical pathology", "biopsy diagnosis",
            "frozen section", "intraoperative pathology",
            "tumour staging", "tumour grading", "TNM staging",
            "immunohistochemistry", "IHC", "PD-L1 IHC", "HER2 IHC",
            "Ki-67", "mitotic index",
            "cytopathology", "fine needle aspiration", "FNA cytology",
            "liquid-based cytology", "cervical cytology", "Pap smear",
            "digital pathology", "whole slide imaging", "WSI",
            "AI pathology", "computational pathology", "machine learning pathology",
            "molecular pathology", "next-generation sequencing tumour",
            "MSI pathology", "mismatch repair", "MLH1", "MSH2",
            "KRAS mutation", "BRAF mutation pathology",
            "autopsy", "post-mortem diagnosis",
            "mesothelioma pathology", "sarcoma pathology",
            "lymphoma pathology", "haematopathology",
            "neuropathology basic",
            "renal pathology", "liver pathology biopsy",
        ],
        "adjacent_terms": [
            "liquid biopsy circulating tumour",
            "proteomics tumour",
            "spatial transcriptomics",
        ],
        "exclusion_terms": [
            "plant pathology", "veterinary pathology",
        ],
    },

    # ======================================================================
    # DIAGNOSTIC RADIOLOGY
    # ======================================================================
    "diagnostic_radiology": {
        "name": "Diagnostic Radiology",
        "description": (
            "Diagnostic radiology covers imaging of disease using X-ray, CT, MRI, ultrasound, "
            "fluoroscopy, and nuclear medicine in a diagnostic context, including interventional "
            "radiology (procedures guided by imaging), breast imaging, neuroradiology, "
            "musculoskeletal radiology, chest radiology, and AI in radiology."
        ),
        "core_terms": [
            "CT scan", "computed tomography", "CT imaging",
            "MRI", "magnetic resonance imaging",
            "ultrasound imaging", "sonography",
            "plain radiograph", "X-ray",
            "PET-CT", "PET scan",
            "interventional radiology", "image-guided intervention",
            "embolisation", "uterine artery embolisation",
            "transjugular intrahepatic portosystemic shunt", "TIPS",
            "percutaneous biopsy", "image-guided biopsy",
            "mammography", "breast MRI", "breast imaging",
            "neuroradiology", "brain CT", "brain MRI",
            "spine imaging MRI",
            "chest CT", "high-resolution CT", "HRCT",
            "coronary CT angiography", "CTCA",
            "musculoskeletal MRI",
            "contrast-enhanced imaging",
            "radiation dose CT",
            "AI radiology", "deep learning radiology", "automated detection",
            "structured reporting",
            "teleradiology",
        ],
        "adjacent_terms": [
            "dual energy CT",
            "photon-counting CT",
            "radiomics imaging",
            "fetal imaging", "obstetric ultrasound",
        ],
        "exclusion_terms": [
            "radiation therapy treatment planning",
        ],
    },

    # ======================================================================
    # GENERAL PATHOLOGY / LABORATORY MEDICINE
    # ======================================================================
    "general_pathology": {
        "name": "General Pathology & Laboratory Medicine",
        "description": (
            "General pathology and laboratory medicine covers clinical laboratory practice "
            "across biochemistry, haematology, microbiology, and anatomical pathology in "
            "an integrated diagnostic context, including laboratory informatics, test "
            "utilisation, quality, and the interface of laboratory medicine with clinical care."
        ),
        "core_terms": [
            "clinical laboratory medicine",
            "laboratory test utilisation", "test ordering",
            "laboratory informatics", "LIS", "laboratory information system",
            "point-of-care testing", "POCT",
            "diagnostic accuracy", "sensitivity specificity",
            "laboratory quality", "proficiency testing",
            "haematology laboratory", "coagulation laboratory",
            "blood bank", "transfusion medicine",
            "reference laboratory", "send-out testing",
            "biomarker clinical",
            "automated haematology analyser",
            "clinical decision support laboratory",
            "laboratory stewardship",
        ],
        "adjacent_terms": [
            "AI laboratory",
            "electronic ordering",
            "laboratory economics",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # NEUROPATHOLOGY
    # ======================================================================
    "neuropathology": {
        "name": "Neuropathology",
        "description": (
            "Neuropathology covers pathological diagnosis of diseases of the nervous system "
            "including brain tumours (gliomas, meningiomas, metastases), neurodegenerative "
            "disease pathology (Alzheimer, Parkinson, CTE), prion disease, neuropathology "
            "of epilepsy, muscle and nerve biopsy, and intraoperative consultation."
        ),
        "core_terms": [
            "brain tumour pathology", "glioma pathology", "glioblastoma IDH",
            "IDH mutation glioma", "MGMT methylation",
            "WHO CNS tumour classification",
            "meningioma pathology", "grade meningioma",
            "medulloblastoma", "ependymoma",
            "brain metastasis pathology",
            "Alzheimer neuropathology", "amyloid plaques", "tau neurofibrillary",
            "Lewy body neuropathology", "alpha-synuclein",
            "CTE", "chronic traumatic encephalopathy",
            "prion disease", "CJD",
            "muscle biopsy", "nerve biopsy",
            "epilepsy neuropathology", "focal cortical dysplasia",
            "demyelinating pathology",
            "intraoperative frozen section brain",
        ],
        "adjacent_terms": [
            "liquid biopsy CNS tumour",
            "digital neuropathology",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # NUCLEAR MEDICINE
    # ======================================================================
    "nuclear_medicine": {
        "name": "Nuclear Medicine",
        "description": (
            "Nuclear medicine covers diagnostic imaging with radiopharmaceuticals (PET, SPECT) "
            "and radionuclide therapy, including FDG-PET oncology, bone scan, thyroid "
            "scintigraphy, PSMA PET prostate, amyloid PET, tau PET, lutetium-177 PSMA "
            "therapy, PRRT for NETs, and radioiodine treatment."
        ),
        "core_terms": [
            "PET scan", "FDG-PET", "positron emission tomography",
            "PET-CT", "PET-MRI",
            "SPECT", "single photon emission CT",
            "bone scan", "bone scintigraphy",
            "myocardial perfusion imaging", "cardiac nuclear",
            "thyroid scan", "radioiodine treatment", "I-131",
            "PSMA PET", "PSMA imaging prostate",
            "lutetium-177 PSMA", "PSMA radioligand therapy",
            "PRRT", "peptide receptor radionuclide therapy",
            "amyloid PET", "florbetapir", "florbetaben",
            "tau PET",
            "FDG staging", "FDG response assessment",
            "theranostics",
            "dosimetry radionuclide",
            "radiopharmaceutical",
        ],
        "adjacent_terms": [
            "SPECT/CT",
            "sentinel node nuclear",
            "RBC scan GI bleed",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # ANESTHESIOLOGY
    # ======================================================================
    "anesthesiology": {
        "name": "Anesthesiology",
        "description": (
            "Anesthesiology covers perioperative patient care including general, regional, "
            "and neuraxial anaesthesia, airway management, haemodynamic monitoring, pain "
            "management, sedation, critical care anaesthesia, obstetric anaesthesia, "
            "paediatric anaesthesia, anaesthesia complications, and perioperative medicine."
        ),
        "core_terms": [
            "general anaesthesia", "inhalational anaesthesia",
            "total intravenous anaesthesia", "TIVA",
            "regional anaesthesia", "nerve block", "peripheral nerve block",
            "neuraxial anaesthesia", "spinal anaesthesia", "epidural",
            "airway management", "intubation", "difficult airway",
            "rapid sequence induction", "RSI",
            "laryngeal mask airway", "LMA",
            "intraoperative monitoring", "processed EEG", "BIS",
            "haemodynamic management intraoperative",
            "intraoperative awareness", "anaesthesia awareness",
            "pain management postoperative", "acute pain service",
            "multimodal analgesia", "opioid-sparing",
            "regional nerve block outcomes",
            "sedation procedural",
            "obstetric anaesthesia", "labour epidural",
            "paediatric anaesthesia",
            "perioperative medicine",
            "enhanced recovery anaesthesia", "ERAS anaesthesia",
            "sugammadex", "neuromuscular reversal",
            "propofol", "ketamine", "dexmedetomidine",
            "opioid pharmacology",
            "transfusion anaesthesia",
        ],
        "adjacent_terms": [
            "ICU anaesthesia",
            "pain medicine anaesthesia",
            "chronic pain anaesthesia",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # COMMUNITY MEDICINE / PUBLIC HEALTH
    # ======================================================================
    "public_health": {
        "name": "Community Medicine & Public Health",
        "description": (
            "Community medicine and public health covers population health, epidemiology, "
            "health promotion and disease prevention, vaccination programs, screening "
            "policy, health equity, social determinants of health, environmental health, "
            "occupational health, global health, pandemic preparedness, and health systems."
        ),
        "core_terms": [
            "population health", "public health", "epidemiology",
            "disease prevention", "health promotion",
            "vaccination program", "immunisation policy",
            "cancer screening population", "breast screening", "cervical screening",
            "colorectal screening population",
            "health equity", "health disparities", "social determinants of health",
            "environmental health", "air pollution health", "climate health",
            "occupational health", "occupational exposure",
            "pandemic preparedness", "outbreak response",
            "global health", "low-income country health",
            "health system", "healthcare policy",
            "cost-effectiveness analysis", "economic evaluation health",
            "incidence prevalence", "disease burden",
            "risk factor population", "attributable risk",
            "primary prevention", "secondary prevention",
            "surveillance system", "reportable disease",
            "alcohol policy", "tobacco policy",
            "obesity prevention population",
        ],
        "adjacent_terms": [
            "COVID-19 population",
            "digital health population",
            "health literacy population",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # OCCUPATIONAL MEDICINE
    # ======================================================================
    "occupational_medicine": {
        "name": "Occupational Medicine",
        "description": (
            "Occupational medicine covers health conditions related to workplace exposures "
            "and activities, including occupational lung disease, occupational skin disease, "
            "work-related musculoskeletal disorders, occupational cancer, fitness for work, "
            "return-to-work programs, workplace mental health, and occupational exposure limits."
        ),
        "core_terms": [
            "occupational health", "work-related disease", "workplace exposure",
            "occupational lung disease", "pneumoconiosis", "silicosis", "asbestosis",
            "mesothelioma occupational", "asbestos",
            "occupational asthma", "isocyanate asthma",
            "occupational skin disease", "contact dermatitis occupational",
            "noise-induced hearing loss",
            "occupational cancer", "occupational carcinogen",
            "work-related musculoskeletal", "repetitive strain", "ergonomics",
            "fitness for work", "functional capacity evaluation",
            "return to work", "disability management",
            "workplace mental health", "burnout occupational",
            "shift work health",
            "occupational exposure limit",
            "toxic exposure", "chemical exposure",
        ],
        "adjacent_terms": [
            "healthcare worker occupational health",
            "physician burnout",
            "COVID-19 healthcare worker",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # PEDIATRICS
    # ======================================================================
    "pediatrics": {
        "name": "Pediatrics",
        "description": (
            "Paediatrics covers the health and diseases of children from birth to adolescence, "
            "including growth and development, paediatric infectious disease, neonatal medicine, "
            "common childhood illnesses (bronchiolitis, croup, otitis media, paediatric wheeze, "
            "preschool wheeze treated with azithromycin or macrolides), paediatric emergency care, "
            "paediatric rheumatology (Kawasaki disease, juvenile idiopathic arthritis, IgA vasculitis), "
            "paediatric gastroenterology (coeliac disease, inflammatory bowel disease in children), "
            "paediatric nephrology (nephrotic syndrome, IgA nephropathy in children), "
            "paediatric neurology (epilepsy, febrile seizures), paediatric oncology, "
            "child mental health, vaccines in children, adolescent medicine, and paediatric subspecialties."
        ),
        "core_terms": [
            "children", "paediatric", "pediatric", "child", "infant",
            "neonatal", "newborn", "NICU", "neonatal intensive care",
            "RSV infant", "bronchiolitis", "croup",
            "paediatric fever", "febrile seizure", "febrile seizure recurrence",
            "otitis media paediatric",
            "paediatric vaccine", "childhood immunisation",
            "growth failure", "failure to thrive",
            "childhood obesity",
            "type 1 diabetes child", "paediatric diabetes",
            "asthma child", "wheezing child", "paediatric asthma",
            "preschool wheeze", "recurrent wheeze infant", "viral wheeze",
            "azithromycin wheeze", "macrolide wheeze", "azithromycin preschool",
            "ADHD child", "autism child",
            "paediatric oncology", "leukaemia child", "Wilms tumour",
            "congenital heart disease paediatric",
            "neonatal jaundice", "hyperbilirubinaemia",
            "neonatal sepsis", "early-onset neonatal sepsis",
            "paediatric mental health", "child psychiatry",
            "adolescent health", "adolescent medicine",
            "child development", "developmental delay", "developmental paediatrics",
            "breastfeeding",
            "safe sleep", "SIDS", "sudden infant death",
            # Paediatric rheumatology
            "Kawasaki disease", "Kawasaki", "mucocutaneous lymph node syndrome",
            "juvenile idiopathic arthritis", "JIA", "paediatric arthritis",
            "IgA vasculitis", "Henoch-Schönlein purpura", "HSP paediatric",
            "paediatric vasculitis", "childhood vasculitis",
            "neonatal lupus", "paediatric lupus", "childhood SLE",
            "autoinflammatory disease child", "periodic fever child",
            # Paediatric gastroenterology
            "coeliac disease child", "celiac disease child", "paediatric celiac",
            "coeliac child", "paediatric coeliac",
            "paediatric inflammatory bowel disease", "Crohn disease child",
            "ulcerative colitis child", "paediatric IBD", "pediatric IBD",
            "eosinophilic oesophagitis child", "paediatric eosinophilic",
            "paediatric liver disease", "biliary atresia",
            # Paediatric nephrology
            "nephrotic syndrome child", "paediatric nephrotic syndrome",
            "paediatric nephrology", "paediatric AKI",
            "vesicoureteral reflux child", "urinary tract infection child",
            # Paediatric neurology
            "paediatric epilepsy", "epilepsy child", "childhood epilepsy",
            "infantile spasms", "West syndrome", "Dravet syndrome",
            "paediatric stroke",
            # Paediatric respiratory
            "cystic fibrosis child", "cystic fibrosis paediatric",
            "paediatric pneumonia",
            # Paediatric infectious disease
            "paediatric meningitis", "bacterial meningitis child",
            "paediatric sepsis",
            "hand foot mouth disease",
            "RSV prophylaxis", "palivizumab",
            # Safeguarding
            "child abuse", "non-accidental injury", "child maltreatment",
        ],
        "adjacent_terms": [
            "transition paediatric adult",
            "long COVID children",
            "COVID-19 children", "MIS-C", "multisystem inflammatory syndrome children",
            "school health", "school-age children",
            "paediatric rheumatology",
            "paediatric critical care", "paediatric ICU", "PICU",
            "paediatric pharmacology", "drug dosing children",
            "growth hormone child", "short stature",
        ],
        "exclusion_terms": [
            "adult patient",
        ],
    },

    # ======================================================================
    # OBSTETRICS & GYNECOLOGY
    # ======================================================================
    "obstetrics_gynecology": {
        "name": "Obstetrics & Gynecology",
        "description": (
            "Obstetrics and gynaecology covers pregnancy and childbirth (prenatal care, "
            "labour and delivery, postpartum care, high-risk obstetrics), gynaecological "
            "disorders (endometriosis, fibroids, prolapse, menstrual disorders), "
            "gynaecologic oncology (cervical, ovarian, uterine cancer), family planning, "
            "menopause, fertility, and minimally invasive gynaecological surgery."
        ),
        "core_terms": [
            "pregnancy", "obstetrics", "prenatal care", "antenatal",
            "labour", "delivery", "caesarean section", "C-section",
            "preeclampsia", "gestational hypertension", "hypertension pregnancy",
            "gestational diabetes",
            "preterm birth", "preterm labour",
            "postpartum haemorrhage",
            "placenta praevia", "placental abruption",
            "fetal growth restriction",
            "maternal mortality",
            "miscarriage", "ectopic pregnancy",
            "endometriosis",
            "uterine fibroid", "myomectomy",
            "pelvic organ prolapse",
            "menorrhagia", "abnormal uterine bleeding",
            "polycystic ovary syndrome PCOS",
            "menopause", "hormone replacement therapy", "HRT",
            "cervical cancer", "HPV vaccination",
            "ovarian cancer", "endometrial cancer",
            "vulvar cancer",
            "fertility", "IVF", "in vitro fertilisation",
            "intrauterine device", "contraception",
            "hysteroscopy", "laparoscopic gynaecology",
            "colposcopy",
        ],
        "adjacent_terms": [
            "COVID-19 pregnancy",
            "autoimmune disease pregnancy",
            "cardiac disease pregnancy",
            "mental health pregnancy",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # PALLIATIVE CARE
    # ======================================================================
    "palliative_care": {
        "name": "Palliative Care",
        "description": (
            "Palliative care covers symptom management and quality of life in serious illness, "
            "goals-of-care conversations, advance care planning, end-of-life care, hospice, "
            "pain management in advanced illness, dyspnoea management, delirium at end of life, "
            "medical assistance in dying (MAID), and paediatric palliative care."
        ),
        "core_terms": [
            "palliative care", "end-of-life care", "hospice",
            "goals of care", "advance care planning", "advance directive",
            "do not resuscitate", "DNR", "DNAR",
            "symptom management", "pain palliative", "cancer pain",
            "opioid palliative", "morphine palliative", "hydromorphone",
            "dyspnoea palliative", "breathlessness",
            "nausea palliative", "delirium palliative",
            "prognosis communication", "serious illness conversation",
            "quality of life terminal", "dignity",
            "medical assistance in dying", "MAID", "euthanasia", "assisted dying",
            "bereavement", "grief",
            "paediatric palliative care",
            "early integration palliative",
            "ICU palliative", "futility",
        ],
        "adjacent_terms": [
            "cancer survivorship palliative",
            "renal palliative",
            "heart failure palliative",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # SPORTS MEDICINE
    # ======================================================================
    "sports_medicine": {
        "name": "Sports Medicine",
        "description": (
            "Sports medicine covers the prevention, diagnosis, and management of exercise "
            "and sports-related injuries and illness, including concussion, overuse injuries, "
            "return-to-sport decisions, exercise as medicine, cardiac screening in athletes, "
            "relative energy deficiency in sport (RED-S), and exercise in chronic disease."
        ),
        "core_terms": [
            "concussion", "sport-related concussion", "SRC",
            "return to sport", "return to play",
            "ACL injury", "ACL rehabilitation",
            "overuse injury", "stress fracture", "tendinopathy",
            "rotator cuff injury",
            "exercise physiology", "physical activity",
            "athlete health", "elite athlete",
            "RED-S", "relative energy deficiency sport", "female athlete triad",
            "cardiac screening athlete", "sudden cardiac death athlete",
            "exercise-induced bronchoconstriction",
            "doping", "performance-enhancing drug", "anti-doping",
            "exercise prescription", "exercise as medicine",
            "exercise and chronic disease",
            "heat illness", "exertional heat stroke",
            "musculoskeletal injection", "corticosteroid injection",
            "platelet-rich plasma",
        ],
        "adjacent_terms": [
            "physical activity cardiovascular",
            "exercise oncology",
            "exercise diabetes",
            "sport psychiatry", "athlete mental health",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # PAIN MEDICINE
    # ======================================================================
    "pain_medicine": {
        "name": "Pain Medicine",
        "description": (
            "Pain medicine covers the multidisciplinary assessment and treatment of chronic "
            "pain conditions, including low back pain, neuropathic pain, fibromyalgia, "
            "headache and migraine, opioid prescribing and stewardship, interventional "
            "pain procedures, non-opioid pharmacology, and psychological approaches to pain."
        ),
        "core_terms": [
            "chronic pain", "persistent pain",
            "low back pain", "chronic low back pain",
            "neuropathic pain", "neuropathy pain",
            "fibromyalgia",
            "opioid prescribing", "opioid chronic pain", "opioid stewardship",
            "opioid use disorder chronic pain",
            "non-opioid analgesia", "multimodal analgesia chronic",
            "gabapentin", "pregabalin", "duloxetine pain",
            "pain neuroscience education",
            "spinal cord stimulation", "neuromodulation pain",
            "epidural steroid injection",
            "radiofrequency ablation pain",
            "ketamine infusion pain",
            "interdisciplinary pain program",
            "cognitive behavioural therapy pain", "CBT chronic pain",
            "pain catastrophising",
            "complex regional pain syndrome", "CRPS",
            "cancer pain",
            "headache management",
        ],
        "adjacent_terms": [
            "post-surgical pain",
            "palliative pain overlap",
            "mental health chronic pain",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # ADDICTION MEDICINE
    # ======================================================================
    "addiction_medicine": {
        "name": "Addiction Medicine",
        "description": (
            "Addiction medicine covers the treatment of substance use disorders and behavioural "
            "addictions, including opioid use disorder, alcohol use disorder, stimulant use "
            "disorder, cannabis use disorder, tobacco cessation, harm reduction, medications "
            "for addiction treatment, and concurrent mental health."
        ),
        "core_terms": [
            "substance use disorder", "addiction",
            "opioid use disorder", "OUD",
            "methadone treatment", "buprenorphine", "suboxone",
            "medications for opioid use disorder", "MOUD",
            "naloxone", "naltrexone addiction",
            "alcohol use disorder", "AUD",
            "alcohol withdrawal", "delirium tremens", "benzodiazepine detox",
            "acamprosate", "disulfiram", "naltrexone alcohol",
            "stimulant use disorder", "cocaine", "methamphetamine",
            "cannabis use disorder", "cannabis dependence",
            "tobacco cessation", "nicotine replacement", "varenicline", "bupropion smoking",
            "harm reduction", "safe supply", "overdose prevention",
            "naloxone distribution",
            "dual diagnosis", "concurrent disorder",
            "withdrawal management",
        ],
        "adjacent_terms": [
            "emergency opioid overdose",
            "homeless health",
            "incarcerated population substance",
            "gambling addiction",
        ],
        "exclusion_terms": [],
    },

    # ======================================================================
    # FAMILY MEDICINE
    # ======================================================================
    "family_medicine": {
        "name": "Family Medicine",
        "description": (
            "Family medicine covers comprehensive, continuous, and person-centred primary "
            "care across all ages and conditions. Includes preventive care, chronic disease "
            "management, undifferentiated illness, mental health in primary care, "
            "reproductive health, paediatric primary care, older adult primary care, "
            "procedural care, and primary care health systems."
        ),
        "core_terms": [
            "primary care", "family medicine", "family physician", "GP",
            "general practitioner",
            "preventive care", "clinical preventive services",
            "cancer screening primary care", "colorectal screening", "breast screening GP",
            "cervical cancer screening", "lung cancer screening",
            "chronic disease management primary care",
            "hypertension primary care", "diabetes primary care",
            "dyslipidaemia primary care", "cardiovascular risk primary care",
            "depression primary care", "anxiety primary care",
            "mental health primary care",
            "medication management primary care",
            "de-prescribing", "polypharmacy primary care",
            "patient-physician communication",
            "shared decision making",
            "continuity of care",
            "undifferentiated illness",
            "fatigue primary care", "headache primary care",
            "lower respiratory infection primary care",
            "urinary tract infection primary care",
            "skin conditions primary care",
            "musculoskeletal primary care",
            "acute care primary care",
            "after-hours care", "urgent care",
            "electronic health record primary care",
            "telemedicine primary care",
            "health coaching",
            "palliative primary care",
            "access to care", "rural primary care",
            "physician shortage",
        ],
        "adjacent_terms": [
            "social prescribing",
            "interprofessional primary care",
            "team-based care",
            "patient-centred medical home",
            "walk-in clinic",
        ],
        "exclusion_terms": [],
    },

}

# ---------------------------------------------------------------------------
# Helper: list all specialty keys
# ---------------------------------------------------------------------------
def list_specialty_keys() -> list:
    return list(SPECIALTY_PROFILES.keys())


def get_specialty_descriptions() -> dict:
    """Return {key: description} for embedding generation."""
    return {k: v["description"] for k, v in SPECIALTY_PROFILES.items()}
