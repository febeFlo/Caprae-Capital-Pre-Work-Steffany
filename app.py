import streamlit as st
import pandas as pd
import traceback

from enrichment import enrich_company
from scoring import compute_lead_score

def main():
    st.title("Lead Enrichment & Scoring")

    uploaded_file = st.file_uploader("Upload SaaSquatch CSV", type=["csv"])
    if not uploaded_file:
        st.info("Please upload a CSV file containing `company_name` and `website` columns.")
        return

    try:
        st.write("Uploaded:", uploaded_file.name)
    except Exception:
        pass

    try:
        raw = uploaded_file.getvalue()
        st.write("Size:", len(raw), "bytes")
    except Exception:
        pass

    try:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error("Error reading CSV:")
        st.error(traceback.format_exc())
        return

    st.write("Columns detected:", df.columns.tolist())
    st.write(df.head())

    required = {"company_name", "website"}
    if not required.issubset(df.columns):
        st.error(f"CSV must contain columns: {required}")
        return

    if st.button("Enrich & Score Leads"):
        with st.spinner("Enriching and scoring leads…"):
            try:
                enriched_records = []

                for idx, row in df.iterrows():
                    try:
                        enriched = enrich_company(
                            row["company_name"],
                            row.get("website", "")
                        )
                    except Exception as e_row:
                        st.warning(f"Failed to enrich row {idx} ({row['company_name']}): {e_row}")
                        enriched = {}

                    record = {**row.to_dict(), **enriched}
                    enriched_records.append(record)

                df_full = pd.DataFrame(enriched_records)

                try:
                    df_full["lead_score"] = df_full.apply(compute_lead_score, axis=1)
                except Exception as e_score:
                    st.error("Error computing lead scores:")
                    st.error(traceback.format_exc())
                    return

            except Exception as main_e:
                st.error("Unexpected error during enrichment/scoring:")
                st.error(traceback.format_exc())
                return

        min_score = st.sidebar.slider("Minimum Lead Score", 0.0, 1.0, 0.5)
        df_filtered = df_full[df_full["lead_score"] >= min_score]

        st.success("Done! Here are your filtered leads:")
        st.write(df_filtered)

        csv_bytes = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Scored Leads CSV",
            data=csv_bytes,
            file_name="scored_leads.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
