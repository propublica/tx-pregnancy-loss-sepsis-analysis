# Identifying sepsis in second-trimester pregnancy-loss complications

This is the code for a first-of-its-kind analysis ProPublica published as part of our February 2025 story “[Texas Banned Abortion. Then Sepsis Rates Soared.](https://www.propublica.org/article/texas-abortion-ban-sepsis-maternal-mortality-analysis)” We found that the sepsis rate in second-trimester pregnancy loss hospitalizations increased by more than 50% after Texas’ near-total abortion ban went into effect in September 2021\. The surge was most pronounced in cases in which the fetus may still have had a heartbeat when the patient arrived at the hospital.

Although the federal government and many states track severe complications in birth events using a federally established methodology, far less is known about complications that arise during a pregnancy loss. There is no federal methodology for tracking this, so we consulted with experts to craft one.

For this analysis, we purchased seven years (2017-2023) of [Texas inpatient hospital discharge data](https://www.dshs.texas.gov/center-health-statistics/texas-health-care-information-collection/health-data-researcher-information/texas-hospital-emergency-department-research-data-file-ed-rdf/texas-inpatient-public-use-data-file-pudf) from the Texas Department of State Health Services. The structure and contents are outlined in the [data dictionary](https://www.dshs.texas.gov/sites/default/files/thcic/hospitals/InpatientDataDictionary2Q2024.pdf). Those wishing to re-create our Texas analysis will need to obtain the data from the department. Hospital discharge data is available for many states and is often structured similarly. 

In addition to this repository, to fully understand our analysis, please refer to our methodology: “[Texas Won’t Study How Its Abortion Ban Impacts Women, So We Did](https://www.propublica.org/article/texas-maternal-mortality-analysis-methodology).”

## Step 0: Data processing and setup

Before we could work with the data, we had to combine and transform the tab-delimited files we received. This repository does not include the code we used for this step, because this data transformation is bespoke to the format of the raw data. 

We loaded the files into a PostgreSQL database, creating a main table called `discharge` with a primary key of `record_id`.

Each row had up to 36 ICD-10-CM diagnosis codes, including an admitting diagnosis, a primary diagnosis, up to 24 other diagnoses and up to 10 external cause codes. We removed those variables from the main table and transformed them from wide to long format, putting those rows into a table called `discharge_diagnosis`, linked to `discharge` by the `record_id` field.

All fields except for “admitting diagnosis” had an accompanying flag for “present on admission”; the value “Y” indicated that it was present at the time of admission. We added a “Y” flag to the `present_on_admission` column for all `admitting diagnosis` codes.

Each row also had up to 25 ICD-10-PCS procedure codes. We removed those variables from the main table and transformed them to a long format in a table called `discharge_procedure`, linked to `discharge` by the `record_id` format.

To connect to our database, we stored the values in a `.env` file in the root of the project. The `env-sample` file is an example of how that file must be structured for the database connection to be created in `scripts/utils.py`.

## Step 1: Generate a coded file

In the file scripts/1\_code\_pregnancy\_ends.ipynb, we generated a coded file with hospitalizations we were interested in and any relevant data for each hospitalization.

We first translated the [methodology published by the Health Resources and Services Administration](https://www.documentcloud.org/documents/25539312-hrsa-federally-available-data-fad-resource-document-for-fy25fy23-application-annual-report/) from SAS to Pandas in order to identify all hospitalizations in which a pregnancy ended and, within those hospitalizations, all rows with a diagnosis or procedure indicating severe maternal morbidity (SMM), based on the [Centers for Disease Control and Prevention definition](https://www.cdc.gov/maternal-infant-health/php/severe-maternal-morbidity/icd.html).

We then identified gestational week codes to allow us to narrow down to pregnancies that ended within a specific window, sepsis codes pertaining to abortive outcomes that weren’t included in the CDC sepsis definition, and codes for missed abortion and intrauterine fetal death — which both indicate no fetal heartbeat.

We then wrote this file out to a CSV.

## Step 2: Analyze second-trimester pregnancy loss

In the file `scripts/2_analyze_outcomes.ipynb`, we used the coded file to identify hospitalizations in which a pregnancy ended between 13 and the end of 21 weeks and explore rates of sepsis within those rows.  