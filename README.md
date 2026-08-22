# parcl-buyer-segmentation-ml
Machine learning based buyer segmentation and investment profiling for Parcl real estate market intelligence, Completed as part of a Data Analyst internship at Unified Mentor Pvt. Ltd. Uses K-Means and Hierarchical clustering to identify 4 buyer segments: Global Investors, First-Time Buyers, Corporate Buyers, and Luxury Investors. Includes Streamlit dashboard.
## 🌐 Live Dashboard
👉 **[Click here to open the live Streamlit Dashboard](https://parcl-buyer-segmentation-ml-6xrw5zwx9tsscld4lsgu6c.streamlit.app/)**

## 📊 Project Overview
This project applies unsupervised machine learning to segment real estate buyers into 4 meaningful groups, enabling Parcl to build smarter marketing strategies and data-driven investment decisions.

### 4 Buyer Segments Identified
| Segment | Clients | Key Characteristics |
|---------|---------|-------------------|
| C1 — Global Investors | 819 (40.95%) | International buyers, mixed investment & home purchase |
| C2 — First-Time Buyers | 636 (31.8%) | Younger buyers, highest loan dependency |
| C3 — Corporate Buyers | 102 (5.1%) | Companies, multiple units, office spaces |
| C4 — Luxury Investors | 443 (22.15%) | High spend, premium properties, investment focused |

## 📁 Repository Files
| File | Description |
|------|-------------|
| `Parcl_Buyer_Segmentation.ipynb` | Google Colab notebook — full ML pipeline |
| `02_Streamlit_Dashboard.py` | Streamlit dashboard source code |
| `clients_segmented.csv` | Final labelled dataset with segment assignments |
| `requirements.txt` | Python dependencies |

## 🔬 Methodology
- **Data Cleaning** — Parsed dates, cleaned prices, removed duplicates
- **Feature Engineering** — Merged client + property transaction data
- **Encoding** — Binary and Label encoding of categorical features
- **Scaling** — StandardScaler applied to all numeric features
- **Clustering** — K-Means (K=4) validated by Elbow Method, Silhouette Score, and Hierarchical Dendrogram
- **Visualisation** — PCA 2D projection, cluster profiles, geographic maps

## 📈 Dashboard Features
- Buyer Segmentation Overview — pie and bar charts
- Investor Behaviour Dashboard — spend, loan rate, satisfaction
- Geographic Buyer Analysis — world map + country breakdown
- Segment Insights Panel — per-segment stats and demographics
- Interactive sidebar filters — Country, Region, Purpose, Client Type

## 🛠️ Tech Stack
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)
![Scikit-learn](https://img.shields.io/badge/ScikitLearn-1.5-orange)
![Plotly](https://img.shields.io/badge/Plotly-5.22-purple)

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| Pandas & NumPy | Data cleaning and feature engineering |
| Scikit-learn | K-Means clustering, StandardScaler, PCA, Silhouette Score |
| SciPy | Hierarchical clustering and dendrogram |
| Matplotlib & Seaborn | Static chart generation |
| Plotly | Interactive dashboard charts |
| Streamlit | Web dashboard deployment |

## 📋 How to Run

### Colab Notebook
1. Open [Google Colab](https://colab.research.google.com)
2. Upload `Parcl_Buyer_Segmentation.ipynb`
3. Upload `clients.csv` and `properties.csv` to the Files panel
4. Click Runtime → Run All

### Streamlit Dashboard
```bash
pip install -r requirements.txt
streamlit run 02_Streamlit_Dashboard.py
```

## 👩‍💻 Author
**Arpita Sarkar**
