import streamlit as st
import pandas as pd
from enrichment import enrich_company
from scoring import compute_lead_score

def main():
    st.title("Lead Enrichment & Scoring")

    uploaded_file = st.file_uploader("Upload SaaSquatch CSV", type="csv")
    if not uploaded_file:
        st.info("Please upload a CSV file containing `company_name` and `website` columns.")
        return

    df = pd.read_csv(uploaded_file)

    if st.button("Enrich & Score Leads"):
        st.info("Enriching data…")
        enriched_records = []
        for _, row in df.iterrows():
            enriched = enrich_company(row["company_name"], row.get("website", ""))
            record = {**row.to_dict(), **enriched}
            enriched_records.append(record)

        df_full = pd.DataFrame(enriched_records)
        st.info("Computing lead scores…")
        df_full["lead_score"] = df_full.apply(compute_lead_score, axis=1)

        min_score = st.sidebar.slider("Minimum Lead Score", 0.0, 1.0, 0.5)
        df_filtered = df_full[df_full["lead_score"] >= min_score]

        st.write(df_filtered)
        csv = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button("Download Scored Leads CSV", data=csv, file_name="scored_leads.csv")

if __name__ == "__main__":
    main()