# ⚡ Pokemon Data Analysis

Exploratory Data Analysis (EDA) and an interactive dashboard of 801 Pokemon.

## 🔗 Links
- **Live Dashboard:** https://YAHAN-APNA-APP-LINK.streamlit.app

## 📊 About the Project
This project explores the battle stats of Pokemon to find out which Pokemon are strongest, which types are best, and how stats are related to each other.

## 📁 Dataset
- **Source:** Kaggle, "Pokemon Complete Stats"
- **Size:** 801 rows (one row = one Pokemon), 16 columns used out of 41
- **Columns:** name, type1, type2, generation, is_legendary, hp, attack, defense, sp_attack, sp_defense, speed, base_total, height_m, weight_kg, capture_rate, percentage_male

## 🧹 Data Cleaning
- Filled missing `type2` with "None" (the Pokemon has only one type)
- Filled missing height, weight and percentage_male with the median
- Converted `capture_rate` from text to number
- Checked duplicates and outliers (box plot + IQR rule)

## 🔍 Key Findings
1. Legendary Pokemon are rare (70 out of 801, about 8.7%) but much stronger (median base total about 600 vs about 420).
2. Dragon type has the highest average base total (about 523), followed by steel and psychic.
3. Stronger Pokemon are harder to catch (correlation between capture rate and base total is -0.71).

**Suggestion:** To build a strong team, focus on dragon and steel types, but be ready for harder catches.

## 🖥️ Dashboard Features
- 2 sidebar filters (Primary Type, Generation)
- 4 key numbers
- 7 graphs (univariate, bivariate, comparison, with Plotly)
- Raw data checkbox
- Findings section

## 📂 Files
- `app.py`: Streamlit dashboard
- `Pokemon_analysis.ipynb`: EDA notebook
- `pokemon.csv`: dataset
- `requirements.txt`: packages needed
- `.streamlit/config.toml`: theme settings

## 🛠️ Tools
Python, Pandas, NumPy, Matplotlib, Seaborn, Plotly, Streamlit

## 👩‍💻 Author
Syeda Bisma ([GitHub](https://github.com/syeda-bisma05))
