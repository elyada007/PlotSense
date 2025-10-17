import pandas as pd
import numpy as np


class SmartDataCleaner:
    """
    Smart Analyst: Data Cleaner Module
    Cleans, fixes, and summarizes data issues automatically.
    """

    def __init__(self, strategy='mean', outlier_threshold=3):
        self.strategy = strategy
        self.outlier_threshold = outlier_threshold
        self.report = {}

    def clean(self, df: pd.DataFrame):
        df = df.copy()
        self.report = {}

        #Standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        self.report['column_standardization'] = "Column names standardized to lowercase with underscores."

        #Handle missing values
        missing_summary = df.isnull().sum()
        num_cols = df.select_dtypes(include=np.number).columns
        cat_cols = df.select_dtypes(exclude=np.number).columns

        for col in num_cols:
            if df[col].isnull().sum() > 0:
                if self.strategy == 'mean':
                    df[col] = df[col].fillna(df[col].mean())
                elif self.strategy == 'median':
                    df[col] = df[col].fillna(df[col].median())
                elif self.strategy == 'mode':
                    df[col] = df[col].fillna(df[col].mode()[0])

        for col in cat_cols:
            if df[col].isnull().sum() > 0:
                df[col] = df[col].fillna(df[col].mode()[0])

        self.report['missing_values'] = missing_summary.to_dict()

        #Remove duplicates
        duplicate_count = df.duplicated().sum()
        df = df.drop_duplicates()
        self.report['duplicates_removed'] = int(duplicate_count)

        #Fix data types
        conversions = []
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                    conversions.append(col)
                except:
                    continue
        self.report['type_conversions'] = conversions

        #Outlier detection
        outlier_counts = {}
        for col in df.select_dtypes(include=np.number).columns:
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std(ddof=0))
            outlier_counts[col] = int((z_scores > self.outlier_threshold).sum())
        self.report['outliers_detected'] = outlier_counts

        #Summary
        self.report['final_shape'] = df.shape
        self.report['summary'] = "Data cleaned successfully."

        return df, self.report
        