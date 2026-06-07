"""
PARCL REAL ESTATE — BUYER SEGMENTATION DASHBOARD
================================================
HOW TO RUN:
  1. Install: pip install streamlit plotly pandas
  2. Place clients_segmented.csv in the same folder as this file
  3. Run: streamlit run 02_Streamlit_Dashboard.py
  4. Browser opens automatically at http://localhost:8501
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Parcl — Buyer Segmentation",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2rem; font-weight: 800; color: #1e3a5f;
        border-bottom: 3px solid #2563eb;
        padding-bottom: 10px; margin-bottom: 6px;
    }
    .sub-header { font-size: 1rem; color: #64748b; margin-bottom: 20px; }
    .kpi-box {
        background: linear-gradient(135deg, #f0f4ff, #e8f0fe);
        border-radius: 10px; padding: 16px 18px;
        border-left: 4px solid #2563eb; margin-bottom: 8px;
    }
    .kpi-val { font-size: 1.7rem; font-weight: 700; color: #1e3a5f; }
    .kpi-lbl { font-size: 0.82rem; color: #64748b; margin-top: 2px; }
    .section-title {
        font-size: 1.2rem; font-weight: 700; color: #1e3a5f;
        margin: 22px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Colour palette ────────────────────────────────────────────────────────────
SEG_COLOR = {
    "C1 — Global Investors":   "#2563eb",
    "C2 — First-Time Buyers":  "#16a34a",
    "C3 — Corporate Buyers":   "#dc2626",
    "C4 — Luxury Investors":   "#d97706",
}

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("clients_segmented.csv")

try:
    df_raw = load_data()
except FileNotFoundError:
    st.error(
        "❌ **clients_segmented.csv not found.**\n\n"
        "Run the Colab notebook first (Cell 18) to generate it, "
        "then place it in the same folder as this file."
    )
    st.stop()

# ── SIDEBAR — Filters ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    all_countries = ["All"] + sorted(df_raw["country"].unique())
    sel_country   = st.selectbox("🌍 Country", all_countries)

    all_regions   = ["All"] + sorted(df_raw["region"].unique())
    sel_region    = st.selectbox("📍 Region", all_regions)

    all_purposes  = ["All"] + sorted(df_raw["acquisition_purpose"].unique())
    sel_purpose   = st.selectbox("🎯 Acquisition Purpose", all_purposes)

    all_types     = ["All"] + sorted(df_raw["client_type"].unique())
    sel_type      = st.selectbox("👤 Client Type", all_types)

    seg_options   = list(SEG_COLOR.keys())
    sel_segs      = st.multiselect("🏷️ Segments", seg_options, default=seg_options)

    st.markdown("---")
    st.caption("Parcl Real Estate Intelligence · 2024")

# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_raw.copy()
if sel_country != "All": df = df[df["country"]             == sel_country]
if sel_region  != "All": df = df[df["region"]              == sel_region]
if sel_purpose != "All": df = df[df["acquisition_purpose"] == sel_purpose]
if sel_type    != "All": df = df[df["client_type"]         == sel_type]
if sel_segs:             df = df[df["segment"].isin(sel_segs)]

if df.empty:
    st.warning("⚠️ No data matches the selected filters. Try adjusting the sidebar.")
    st.stop()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">🏢 Parcl — Buyer Segmentation Intelligence</div>',
            unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">AI-powered buyer clustering · {len(df):,} clients shown after filters</div>',
            unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 — KPI CARDS
# ═════════════════════════════════════════════════════════════════════════════
c1, c2, c3, c4, c5 = st.columns(5)

def kpi(col, icon, val, label):
    col.markdown(
        f'<div class="kpi-box"><div class="kpi-val">{icon} {val}</div>'
        f'<div class="kpi-lbl">{label}</div></div>',
        unsafe_allow_html=True
    )

loan_pct  = (df["loan_applied"] == "Yes").mean() * 100
avg_score = df["satisfaction_score"].mean()
avg_spend = df["total_spend"].mean()

kpi(c1, "👥", f"{len(df):,}",            "Total Clients")
kpi(c2, "🌍", f"{df['country'].nunique()}", "Countries")
kpi(c3, "💰", f"${avg_spend/1000:,.0f}K", "Avg Total Spend")
kpi(c4, "🏦", f"{loan_pct:.0f}%",         "Loan Rate")
kpi(c5, "⭐", f"{avg_score:.1f}/5",        "Avg Satisfaction")

st.markdown("---")

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 — BUYER SEGMENTATION OVERVIEW
# ═════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 Section 1 — Buyer Segmentation Overview</div>',
            unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    seg_cnt = df["segment"].value_counts().reset_index()
    seg_cnt.columns = ["Segment", "Count"]
    fig_pie = px.pie(
        seg_cnt, names="Segment", values="Count",
        color="Segment", color_discrete_map=SEG_COLOR,
        hole=0.42, title="Segment Distribution"
    )
    fig_pie.update_traces(textposition="outside", textinfo="percent+label")
    fig_pie.update_layout(showlegend=False, height=380,
                          margin=dict(t=50, b=10, l=10, r=10))
    st.plotly_chart(fig_pie, use_container_width=True)

with col_b:
    fig_bar = px.bar(
        seg_cnt.sort_values("Count"),
        x="Count", y="Segment", orientation="h",
        color="Segment", color_discrete_map=SEG_COLOR,
        text="Count", title="Client Count per Segment"
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(showlegend=False, height=380,
                          yaxis_title="", xaxis_title="Number of Clients",
                          margin=dict(t=50, b=10, l=10, r=10))
    st.plotly_chart(fig_bar, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3 — INVESTOR BEHAVIOUR DASHBOARD
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">📈 Section 2 — Investor Behaviour Dashboard</div>',
            unsafe_allow_html=True)

col_c, col_d = st.columns(2)

with col_c:
    purpose_df = df.groupby(["segment", "acquisition_purpose"]).size().reset_index(name="count")
    fig_purpose = px.bar(
        purpose_df, x="segment", y="count", color="acquisition_purpose",
        barmode="group", title="Investment vs Home Purchase by Segment",
        color_discrete_map={"Investment": "#2563eb", "Home": "#16a34a"},
        labels={"segment": "", "count": "Clients", "acquisition_purpose": "Purpose"}
    )
    fig_purpose.update_layout(height=360, xaxis_tickangle=-15,
                               margin=dict(t=50, b=10), legend_title="Purpose")
    st.plotly_chart(fig_purpose, use_container_width=True)

with col_d:
    loan_df = (
        df.groupby("segment")
        .apply(lambda x: (x["loan_applied"] == "Yes").mean() * 100)
        .reset_index(name="Loan Rate (%)")
    )
    loan_df.columns = ["Segment", "Loan Rate (%)"]
    fig_loan = px.bar(
        loan_df.sort_values("Loan Rate (%)"),
        x="Loan Rate (%)", y="Segment", orientation="h",
        color="Segment", color_discrete_map=SEG_COLOR,
        text=loan_df["Loan Rate (%)"].map("{:.1f}%".format),
        title="Loan Application Rate by Segment"
    )
    fig_loan.update_traces(textposition="outside")
    fig_loan.update_layout(showlegend=False, height=360,
                            yaxis_title="", margin=dict(t=50, b=10))
    st.plotly_chart(fig_loan, use_container_width=True)

col_e, col_f = st.columns(2)

with col_e:
    spend_df = df.groupby("segment")["total_spend"].mean().reset_index()
    spend_df.columns = ["Segment", "Avg Spend"]
    fig_spend = px.bar(
        spend_df.sort_values("Avg Spend"),
        x="Avg Spend", y="Segment", orientation="h",
        color="Segment", color_discrete_map=SEG_COLOR,
        title="Average Total Spend by Segment"
    )
    fig_spend.update_layout(showlegend=False, height=360,
                             yaxis_title="", margin=dict(t=50, b=10))
    fig_spend.update_xaxes(tickformat="$,.0f")
    st.plotly_chart(fig_spend, use_container_width=True)

with col_f:
    fig_vio = px.violin(
        df, y="satisfaction_score", x="segment",
        color="segment", color_discrete_map=SEG_COLOR,
        box=True, points="outliers",
        title="Satisfaction Score Distribution by Segment",
        labels={"satisfaction_score": "Score (1–5)", "segment": ""}
    )
    fig_vio.update_layout(showlegend=False, height=360,
                           xaxis_tickangle=-15, margin=dict(t=50, b=10))
    st.plotly_chart(fig_vio, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 4 — GEOGRAPHIC BUYER ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">🗺️ Section 3 — Geographic Buyer Analysis</div>',
            unsafe_allow_html=True)

col_g, col_h = st.columns([2, 1])

with col_g:
    country_total = df.groupby("country").size().reset_index(name="total")
    country_seg   = (
        df.groupby(["country", "segment"]).size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        .drop_duplicates("country")[["country", "segment"]]
    )
    country_data = country_total.merge(country_seg, on="country")

    iso_map = {
        "USA": "USA", "Uk": "GBR", "UK": "GBR",
        "Canada": "CAN", "Germany": "DEU", "France": "FRA",
        "Belgium": "BEL", "Mexico": "MEX", "Australia": "AUS",
        "Russia": "RUS", "Denmark": "DNK"
    }
    country_data["iso"] = country_data["country"].map(iso_map)

    fig_map = px.choropleth(
        country_data.dropna(subset=["iso"]),
        locations="iso", color="total",
        hover_name="country",
        hover_data={"segment": True, "total": True, "iso": False},
        color_continuous_scale="Blues",
        title="Buyer Count by Country"
    )
    fig_map.update_layout(height=380, margin=dict(t=50, b=10, l=10, r=10),
                           geo=dict(showframe=False, showcoastlines=True))
    st.plotly_chart(fig_map, use_container_width=True)

with col_h:
    region_df = df["region"].value_counts().head(12).reset_index()
    region_df.columns = ["Region", "Count"]
    fig_reg = px.bar(
        region_df, x="Count", y="Region", orientation="h",
        color="Count", color_continuous_scale="Blues",
        title="Top 12 Regions"
    )
    fig_reg.update_layout(showlegend=False, height=380,
                           coloraxis_showscale=False,
                           margin=dict(t=50, b=10))
    st.plotly_chart(fig_reg, use_container_width=True)

# Stacked bar: segment breakdown by country
country_seg_full = df.groupby(["country", "segment"]).size().reset_index(name="count")
fig_stacked = px.bar(
    country_seg_full, x="country", y="count", color="segment",
    color_discrete_map=SEG_COLOR,
    title="Segment Breakdown by Country",
    labels={"country": "Country", "count": "Clients", "segment": "Segment"}
)
fig_stacked.update_layout(height=370, xaxis_tickangle=-20,
                            margin=dict(t=50, b=10), legend_title="Segment")
st.plotly_chart(fig_stacked, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 5 — SEGMENT INSIGHTS PANEL
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">🔬 Section 4 — Segment Insights Panel</div>',
            unsafe_allow_html=True)

tabs = st.tabs(list(SEG_COLOR.keys()))

for tab, seg in zip(tabs, SEG_COLOR.keys()):
    with tab:
        seg_df = df[df["segment"] == seg]
        if seg_df.empty:
            st.info("No clients in this segment with current filters.")
            continue

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Clients",      f"{len(seg_df):,}")
        m2.metric("Average Age",         f"{seg_df['age'].mean():.0f} yrs")
        m3.metric("Avg Total Spend",     f"${seg_df['total_spend'].mean():,.0f}")
        m4.metric("Avg Satisfaction",    f"{seg_df['satisfaction_score'].mean():.2f} / 5")

        c1, c2 = st.columns(2)
        with c1:
            rc = seg_df["referral_channel"].value_counts().reset_index()
            rc.columns = ["Channel", "Count"]
            fig_rc = px.pie(rc, names="Channel", values="Count",
                            title="Referral Channel Mix", hole=0.35,
                            color_discrete_sequence=["#2563eb", "#16a34a", "#d97706"])
            fig_rc.update_layout(height=280, margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig_rc, use_container_width=True)

        with c2:
            fig_age = px.histogram(
                seg_df, x="age", nbins=20,
                color_discrete_sequence=[SEG_COLOR[seg]],
                title="Age Distribution",
                labels={"age": "Age (years)", "count": "Buyers"}
            )
            fig_age.update_layout(height=280,
                                   margin=dict(t=40, b=10, l=10, r=10),
                                   showlegend=False)
            st.plotly_chart(fig_age, use_container_width=True)

        # Descriptive stats table
        stats = (
            seg_df[["age", "satisfaction_score", "total_spend",
                     "units_bought", "avg_area_sqft"]]
            .describe().T.round(2)
        )
        stats.index.name = "Feature"
        st.markdown("**📋 Descriptive Statistics**")
        st.dataframe(stats, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 6 — FULL DATA TABLE
# ═════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div class="section-title">📋 Filtered Client Data Table</div>',
            unsafe_allow_html=True)

show_cols = ["client_id", "client_type", "gender", "country", "region",
             "age", "acquisition_purpose", "satisfaction_score",
             "loan_applied", "referral_channel", "total_spend",
             "units_bought", "segment"]
st.dataframe(
    df[show_cols].sort_values("segment").reset_index(drop=True),
    use_container_width=True, height=300
)

csv_bytes = df[show_cols].to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️  Download Filtered Data as CSV",
    data=csv_bytes,
    file_name="parcl_filtered_clients.csv",
    mime="text/csv"
)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("🏢 Parcl Real Estate Intelligence Platform · ML Buyer Segmentation · 2024")
