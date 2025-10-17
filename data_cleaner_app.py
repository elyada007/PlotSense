import streamlit as st
import pandas as pd
from plotsense import SmartDataCleaner

#Page config
st.set_page_config(page_title="Smart Data Cleaner", layout="wide")

st.title("SmartDataCleaner Demo (PlotSenseAI)")
st.markdown("Upload a dataset, clean it automatically, and view insights in real-time.")

#Upload dataset
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Original Data Preview")
    st.dataframe(df.head(10))

    st.write("Shape before cleaning:", df.shape)

    #Clean the data
    cleaner = SmartDataCleaner(strategy='mean', outlier_threshold=3)
    cleaned_df, report = cleaner.clean(df)

    st.subheader("Cleaned Data Preview")
    st.dataframe(cleaned_df.head(10))
    st.write("Shape after cleaning:", cleaned_df.shape)

    #Cleaning Report
    st.subheader("Cleaning Summary")
    st.json(report)

    #Option to download cleaned dataset
    csv = cleaned_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Cleaned Dataset",
        data=csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )

else:
    st.info("Upload a CSV file to begin cleaning.")
