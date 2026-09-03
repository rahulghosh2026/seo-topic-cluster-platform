import streamlit as st
import pandas as pd

from topic_engine.pipeline import run_analysis


st.set_page_config(
    page_title="SEO Topic Cluster Analyzer",
    layout="wide"
)

st.title(
    "SEO Topic Cluster Analyzer"
)

st.markdown(
    """
Upload a CSV file containing a column named:

`url`
"""
)

uploaded_file = st.file_uploader(
    "Upload URL CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(
        uploaded_file
    )

    if "url" not in df.columns:

        st.error(
            "CSV must contain 'url' column."
        )

    else:

        url_list = (
            df["url"]
            .dropna()
            .tolist()
        )

        if st.button(
            "Run Topic Analysis"
        ):

            with st.spinner(
                "Analyzing Blog URLs..."
            ):

                results = run_analysis(
                    url_list
                )

            st.success(
                "Analysis Complete"
            )

            st.subheader(
                "Summary"
            )

            st.json(
                results["summary"]
            )

            st.subheader(
                "Topic Clusters"
            )

            st.dataframe(
                results["clusters"]
            )

            st.subheader(
                "Hyperlink Audit"
            )

            for page in results["pages"]:

                title = page["title"]

                if title == "":
                    title = page["url"]

                with st.expander(
                    title
                ):

                    link_df = pd.DataFrame(
                        page["links"]
                    )

                    st.dataframe(
                        link_df
                    )
