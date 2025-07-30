# Lead Enrichment & Scoring App

## Setup
1. pip install -r requirements.txt  
2. streamlit run app.py

## Usage
- Upload a CSV with columns `company_name`, `website`.  
- Click “Enrich & Score Leads”.  
- Use sidebar slider to filter by score.  
- Download the filtered, scored leads CSV.

## Notes
- `enrich_company` is a stub; swap in real API credentials.  
- Scoring is a weighted linear model; adjust weights in `scoring.py`.