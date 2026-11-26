import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ====== YAHAN SE THEME CHOONO: 'dark' ya 'green' ======
THEME = 'green'
# ======================================================

# dono themes ke rang (dictionary: naam -> rang)
THEMES = {
    'dark':  {'bg': '#1B1F3B', 'side': '#2A2F5A', 'main': '#FFCB05', 'second': '#4FC3F7', 'text': '#F5F5F5', 'template': 'plotly_dark'},
    'green': {'bg': '#EAF6F0', 'side': '#CFE8DC', 'main': '#E4572E', 'second': '#264653', 'text': '#1B2A2F', 'template': 'plotly_white'},
}
t = THEMES[THEME]    # jo theme upar choona, uske rang t main aa gaye

# browser tab ka naam, chhota icon, aur page ko poori chaudai mein phelana (wide layout)
st.set_page_config(page_title='Pokemon Dashboard', page_icon='⚡', layout='wide')

# page ke rang CSS se lagao (MAIN, BG wagera ko asli rang se badal do)
css = """
<style>
.stApp {background-color: BG; color: TEXT;}
[data-testid="stSidebar"] {background-color: SIDE;}
h1, h2, h3 {color: MAIN !important;}
[data-testid="stMetric"] {background-color: SIDE; border: 3px solid MAIN; border-radius: 15px; padding: 10px 15px;}
.stTabs [aria-selected="true"] {color: MAIN;}
</style>
"""
css = css.replace('MAIN', t['main']).replace('BG', t['bg']).replace('SIDE', t['side']).replace('TEXT', t['text'])
st.markdown(css, unsafe_allow_html=True)

# Matplotlib/Seaborn ke graphs ko bhi isi theme ke rang do
plt.rcParams.update({
    'figure.facecolor': t['bg'], 'axes.facecolor': t['bg'],
    'text.color': t['text'], 'axes.labelcolor': t['text'],
    'xtick.color': t['text'], 'ytick.color': t['text'], 'axes.edgecolor': t['text'],
})
sns.set_palette([t['main'], t['second']])

# Plotly ke graphs ko theme dene ka chhota function
def style_plotly(fig):
    fig.update_layout(template=t['template'], paper_bgcolor=t['bg'], plot_bgcolor=t['bg'], font_color=t['text'])
    return fig

@st.cache_data    # data aik bar load huga or yaad rakha jay ga, dashboard fast chale ga
def load_data():
    df = pd.read_csv('pokemon.csv')
    cols = ['name', 'type1', 'type2', 'generation', 'is_legendary', 'hp', 'attack', 'defense', 'sp_attack', 'sp_defense', 'speed', 'base_total', 'height_m', 'weight_kg', 'capture_rate', 'percentage_male']
    df = df[cols].copy()                                             # 41 columns main se sirf wohi notebook wale 16 columns rakhu, aur unki alag copy bana lu
    df['type2'] = df['type2'].fillna('None')                       # type 2 ki khali jaga per None likh do (matlab us pokemon ki sirf aik type h)
    for col in ['height_m', 'weight_kg', 'percentage_male']:       # in teen column ke name aik ek kerke 'col' main aynge
        df[col] = df[col].fillna(df[col].median())                 # har column ki khali jaga us column ke median (beech wali value) se fill ker du
    df['capture_rate'] = df['capture_rate'].astype(str).str.extract(r"(\d+)")[0].astype(int)    # capture_rate ke text main se pehla number nikalo aur usay asli number (integer) bana do
    return df          # saaf kia hua data wapis bhej du

df = load_data()         # upar bana hua function chalao or saaf table df main rakh du

st.title("⚡ Pokemon Data Dashboard")
st.write('Explore the battle stats of 801 Pokemon. Use the sidebar filters to change the data.')

st.sidebar.header("🎮 Filters")

type_list = sorted(df['type1'].unique())   # type1 ke sare alag alag name (18 types) nikalo or A se Z order main lagau
selected_types = st.sidebar.multiselect('Primary Type (type1)', type_list, default=type_list)   # sidebar main box banau jahan se types choose ker saku

gen_list = sorted(df['generation'].unique())     # generation ke sare alag alag number (1-7) nikalu or ascending order main rakhu
selected_gens = st.sidebar.multiselect('Generation', gen_list, default=gen_list)                # sidebar main dusra box banau jisme se generation choose ker saku

# dono filters ke hisaab se data chhanto (type1 AUR generation dono match hon)
filtered_df = df[(df['type1'].isin(selected_types)) & (df['generation'].isin(selected_gens))].copy()
filtered_df['status'] = filtered_df['is_legendary'].map({0: 'Normal', 1: 'Legendary'})   # 0 ko Normal, 1 ko Legendary likho

# agar user ne sab kuch hata diya to data khali hoga, tab warning dikhao aur ruk jao
if filtered_df.empty:
    st.warning('No Pokemon found. Please select at least one type and one generation.')
    st.stop()

# 4 barabar ke dabbe (columns) banao, har dabbe mein aik number dikhega
c1, c2, c3, c4 = st.columns(4)

c1.metric('Total Pokemon', len(filtered_df))                                    # kitni rows bachi
c2.metric('Legendary Pokemon', int(filtered_df['is_legendary'].sum()))          # legendary ki ginti (1 = legendary)
c3.metric('Average Base Total', round(filtered_df['base_total'].mean(), 1))     # average taqat
strongest = filtered_df.loc[filtered_df['base_total'].idxmax(), 'name']         # sabse zyada base_total wale ka naam
c4.metric('Strongest Pokemon', strongest)

st.divider()

tab1, tab2, tab3 = st.tabs(['📊 One Column', '🔗 Two Columns', '⚖️ Compare Groups'])

# ---------- TAB 1: univariate ----------
with tab1:
    col_a, col_b = st.columns(2)

    # Graph 1 (Plotly): base_total histogram
    fig1 = px.histogram(filtered_df, x='base_total', nbins=30,
                        title='Distribution of Base Total',
                        labels={'base_total': 'Base Total', 'count': 'Number of Pokemon'})
    fig1.update_traces(marker_color=t['main'])
    col_a.plotly_chart(style_plotly(fig1), use_container_width=True)

    # Graph 2 (Seaborn): har type1 mein kitne Pokemon
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    order = filtered_df['type1'].value_counts().index
    sns.countplot(data=filtered_df, y='type1', order=order, ax=ax2, color=t['second'])
    ax2.set_title('Number of Pokemon per Type')
    ax2.set_xlabel('Count')
    ax2.set_ylabel('Type')
    col_b.pyplot(fig2)

# ---------- TAB 2: bivariate ----------
with tab2:
    col_c, col_d = st.columns(2)

    # Graph 3 (Plotly): attack vs defense
    fig3 = px.scatter(filtered_df, x='attack', y='defense', color='status',
                      hover_name='name', title='Attack vs Defense',
                      color_discrete_map={'Normal': t['second'], 'Legendary': t['main']},
                      labels={'attack': 'Attack', 'defense': 'Defense', 'status': 'Type'})
    col_c.plotly_chart(style_plotly(fig3), use_container_width=True)

    # Graph 4 (Seaborn): height vs weight
    fig4, ax4 = plt.subplots(figsize=(7, 5))
    sns.scatterplot(data=filtered_df, x='height_m', y='weight_kg', ax=ax4, color=t['main'])
    ax4.set_title('Height vs Weight')
    ax4.set_xlabel('Height (m)')
    ax4.set_ylabel('Weight (kg)')
    col_d.pyplot(fig4)

    # Graph 7 (Plotly): base_total vs capture_rate
    fig7 = px.scatter(filtered_df, x='base_total', y='capture_rate', color='status',
                      hover_name='name', title='Base Total vs Capture Rate',
                      color_discrete_map={'Normal': t['second'], 'Legendary': t['main']},
                      labels={'base_total': 'Base Total', 'capture_rate': 'Capture Rate', 'status': 'Type'})
    st.plotly_chart(style_plotly(fig7), use_container_width=True)

# ---------- TAB 3: comparison ----------
with tab3:
    col_e, col_f = st.columns(2)

    # Graph 5 (Seaborn): Legendary vs Normal box plot
    fig5, ax5 = plt.subplots(figsize=(7, 5))
    sns.boxplot(data=filtered_df, x='status', y='base_total', hue='status', ax=ax5,
                palette={'Normal': t['second'], 'Legendary': t['main']}, legend=False)
    ax5.set_title('Base Total: Legendary vs Normal')
    ax5.set_xlabel('Pokemon Group')
    ax5.set_ylabel('Base Total')
    col_e.pyplot(fig5)

    # Graph 6 (Plotly): har type ka average base_total
    avg_type = filtered_df.groupby('type1')['base_total'].mean().sort_values(ascending=False).reset_index()
    fig6 = px.bar(avg_type, x='type1', y='base_total',
                  title='Average Base Total per Type',
                  labels={'type1': 'Type', 'base_total': 'Average Base Total'})
    fig6.update_traces(marker_color=t['second'])
    col_f.plotly_chart(style_plotly(fig6), use_container_width=True)

st.divider()

# ---------- Raw data checkbox ----------
if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.dataframe(filtered_df)
    st.write('Rows:', filtered_df.shape[0], '| Columns:', filtered_df.shape[1])

st.divider()

# ---------- Findings ----------
st.subheader('🔍 Key Findings')
st.caption('These findings are based on the full dataset (all 801 Pokemon).')
st.write('1. Legendary Pokemon are rare (70 out of 801, about 8.7%), but much stronger: median base total is about 600 vs about 420 for normal Pokemon.')
st.write('2. Dragon type has the highest average base total (about 523), followed by steel (492) and psychic (461). Bug type has the lowest.')
st.write('3. Stronger Pokemon are harder to catch: capture rate and base total have a strong negative correlation (-0.71).')
st.info('💡 Suggestion: To build a strong team, focus on dragon and steel types, but be ready for harder catches (use stronger Poke Balls and weaken the Pokemon first).')