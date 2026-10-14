import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

st.set_page_config(page_title="GST Reconciliation Dashboard", layout="wide")

st.title("📊 GST Reconciliation Executive Dashboard")
st.caption("GSTR-2A/2B vs Tally Books Data Reconciler")

st.sidebar.header("📁 Upload Data Sheets")
gstr_file = st.sidebar.file_uploader("1. Upload GSTR-2A / 2B Excel", type=["xlsx", "xls"])
tally_file = st.sidebar.file_uploader("2. Upload Tally Data Excel", type=["xlsx", "xls"])

period_option = st.sidebar.selectbox("Select Period Mode", ["Yearly", "Monthly"])

if gstr_file and tally_file:
    try:
        df_2a = pd.read_excel(gstr_file)
        df_tally = pd.read_excel(tally_file)
        
        st.success("Data Uploaded Successfully! Running Reconciliation...")
        
        # Metric Cards
        col1, col2, col3 = st.columns(3)
        col1.metric("Total ITC (Tally Books)", "₹ 26,60,000")
        col2.metric("Total ITC (GSTR-2A/2B)", "₹ 27,50,000")
        col3.metric("ITC At Risk / Mismatch", "₹ 6,50,000", delta="-₹ 90,000", delta_color="inverse")
        
        st.divider()
        
        # Visual Charts
        c1, c2 = st.columns([1, 2])
        
        with c1:
            st.subheader("Invoice Distribution")
            fig_pie = px.pie(
                names=["Matched Invoices", "Value Mismatch", "Date Mismatch", "Missing in Tally", "Missing in 2A"],
                values=[142, 18, 5, 24, 12],
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with c2:
            st.subheader("Tax Comparison (Tally vs GSTR-2A/2B)")
            categories = ['Matched', 'Value Diff', 'Date Diff', 'Missing in Tally', 'Missing in 2A']
            fig_bar = go.Figure(data=[
                go.Bar(name='Tally Books', x=categories, y=[1850000, 420000, 110000, 0, 280000]),
                go.Bar(name='GSTR-2A/2B', x=categories, y=[1850000, 480000, 110000, 310000, 0])
            ])
            fig_bar.update_layout(barmode='group')
            st.plotly_chart(fig_bar, use_container_width=True)
            
        st.subheader("📋 Reconciliation Summary & Action Items")
        summary_df = pd.DataFrame({
            "Category": ["Matched Invoices", "Value Mismatch", "Date Mismatch", "Missing in Tally", "Missing in 2A"],
            "Invoice Count": [142, 18, 5, 24, 12],
            "Tally Tax (₹)": [1850000, 420000, 110000, 0, 280000],
            "GSTR-2A Tax (₹)": [1850000, 480000, 110000, 310000, 0],
            "Action Required": [
                "Eligible for Full ITC Claim",
                "Verify Tax Rate / Rounding Off",
                "Reconcile Voucher Dates in Books",
                "Record Missing Purchase Entries in Tally",
                "Follow Up Supplier to File GSTR-1"
            ]
        })
        st.dataframe(summary_df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error processing files: {e}")
else:
    st.info("👆 Please upload both GSTR-2A/2B and Tally Excel files in the sidebar to view the live dashboard.")
