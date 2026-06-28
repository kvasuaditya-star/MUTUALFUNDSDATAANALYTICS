"""
Bluestock MF Capstone — Day 3 EDA
Standalone chart generator — produces all 15 PNGs in charts/
Run: python3 notebooks/run_eda.py
"""

import os, warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')
os.makedirs(OUT, exist_ok=True)

BG   = '#0f1117'
AX   = '#1a1d2e'
FG   = '#e2e8f0'
GRID = '#252840'

plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': AX,
    'axes.labelcolor': FG, 'xtick.color': FG, 'ytick.color': FG,
    'text.color': FG, 'grid.color': GRID, 'axes.edgecolor': GRID,
    'legend.facecolor': AX, 'legend.edgecolor': GRID,
    'figure.dpi': 130,
})
sns.set_theme(style='darkgrid', palette='muted', font_scale=1.05)

np.random.seed(42)

# ── DATE RANGES ────────────────────────────────────────────────────────────
daily_dates   = pd.date_range('2022-01-03', '2025-12-31', freq='B')
monthly_dates = pd.date_range('2022-01', '2025-12', freq='MS')

# ── 40 SCHEMES ─────────────────────────────────────────────────────────────
fund_houses = ['SBI MF','HDFC MF','ICICI Pru MF','Axis MF','Nippon MF',
               'Kotak MF','DSP MF','Franklin MF','Mirae Asset MF','Aditya Birla MF']
categories  = ['Large Cap','Mid Cap','Small Cap','Flexi Cap','ELSS',
               'Debt','Liquid','Hybrid','Index','Thematic']

schemes = [{'scheme_id': f'SCH{i+1:03d}', 'fund_house': fh, 'category': cat}
           for i, (fh, cat) in enumerate((fh, cat)
           for fh in fund_houses for cat in categories)]
schemes_df = pd.DataFrame(schemes)

# ── NAV DATA ───────────────────────────────────────────────────────────────
print("Generating NAV data...")
base_map = {'Large Cap':80,'Mid Cap':55,'Small Cap':30,'Flexi Cap':65,
            'ELSS':45,'Debt':1200,'Liquid':1500,'Hybrid':70,'Index':140,'Thematic':40}
nav_records = []
for _, s in schemes_df.iterrows():
    nav = base_map.get(s['category'], 50) * np.random.uniform(0.8, 1.2)
    for dt in daily_dates:
        yr = dt.year
        drift = (0.0007 if yr == 2023 else
                 -0.0003 if (yr == 2024 and dt.month <= 6) else 0.0004)
        nav = max(nav * (1 + drift + np.random.normal(0, 0.008)), 1)
        nav_records.append({'date': dt, 'scheme_id': s['scheme_id'],
                            'fund_house': s['fund_house'],
                            'category': s['category'], 'nav': round(nav, 4)})
nav_df = pd.DataFrame(nav_records)
print(f"  NAV rows: {len(nav_df):,}")

# ── AUM DATA ───────────────────────────────────────────────────────────────
aum_data = {'SBI MF':[8.2,9.5,10.8,12.5],'HDFC MF':[4.5,5.2,6.1,7.0],
            'ICICI Pru MF':[4.9,5.8,6.5,7.5],'Axis MF':[2.2,2.5,2.9,3.2],
            'Nippon MF':[2.8,3.0,3.5,4.0],'Kotak MF':[2.5,3.1,3.7,4.3],
            'DSP MF':[1.2,1.5,1.8,2.1],'Franklin MF':[1.0,1.2,1.4,1.7],
            'Mirae Asset MF':[1.5,1.9,2.4,2.9],'Aditya Birla MF':[2.9,3.3,3.9,4.5]}
years = [2022,2023,2024,2025]
aum_df = pd.DataFrame([{'fund_house':fh,'year':yr,'aum_lakh_cr':v}
                        for fh,vals in aum_data.items() for yr,v in zip(years,vals)])

# ── SIP DATA ───────────────────────────────────────────────────────────────
sip_vals = [11423,11517,11875,12011,12286,12276,12140,12693,13040,13040,13306,13573,
            13686,13686,14276,14749,15245,15426,15245,15814,16042,16928,17073,17610,
            18838,19186,20371,20904,21262,21262,23332,23547,24509,25323,25319,25320,
            26400,26000,27100,28200,29100,29500,30200,30500,30800,31000,31002,31002]
sip_df = pd.DataFrame({'date': monthly_dates[:len(sip_vals)], 'sip_inflow_cr': sip_vals})

# ── CATEGORY INFLOWS ───────────────────────────────────────────────────────
cat_inflow_raw = {}
for cat in categories:
    base = np.random.uniform(500, 5000)
    cat_inflow_raw[cat] = [
        max(base*(1+0.15*np.sin(2*np.pi*dt.month/12))*{2022:1.0,2023:1.25,2024:1.45,2025:1.65}[dt.year]
            + np.random.normal(0,200), 0)
        for dt in monthly_dates]
cat_inflow_df = pd.DataFrame(cat_inflow_raw, index=monthly_dates)

# ── INVESTOR DEMOGRAPHICS ─────────────────────────────────────────────────
age_groups = ['18-25','26-35','36-45','46-55','56-65','65+']
age_pct    = [8,28,32,18,10,4]
n_inv      = 5000
inv_df     = pd.DataFrame({
    'age_group': np.random.choice(age_groups, n_inv, p=[x/100 for x in age_pct]),
    'gender':    np.random.choice(['Male','Female','Other'], n_inv, p=[0.62,0.36,0.02]),
    'sip_amount': np.random.lognormal(8.2, 0.8, n_inv)
})

# ── GEO DATA ───────────────────────────────────────────────────────────────
states    = ['Maharashtra','Delhi NCR','Gujarat','Karnataka','Tamil Nadu',
             'Telangana','Haryana','West Bengal','Andhra Pradesh','Kerala',
             'Rajasthan','Punjab','Uttar Pradesh','Madhya Pradesh','Odisha']
state_sip = [42500,38900,31200,28700,24300,16900,14200,15600,13800,13100,
             12400,11500,11200,9800,7200]
geo_df    = pd.DataFrame({'state': states, 'sip_amount_cr': state_sip}).sort_values('sip_amount_cr')

# ── FOLIO DATA ─────────────────────────────────────────────────────────────
folio_vals = np.linspace(13.26, 26.12, len(monthly_dates)) + np.random.normal(0,0.08,len(monthly_dates))
folio_df   = pd.DataFrame({'date': monthly_dates, 'folio_cr': folio_vals})

milestones = {
    '2022-07-01': (15.0, '15 Cr'),
    '2023-06-01': (17.8, '17.8 Cr'),
    '2024-01-01': (20.5, '20.5 Cr'),
    '2024-09-01': (23.0, '23 Cr'),
    '2025-06-01': (24.5, '24.5 Cr'),
    '2025-12-01': (26.12, '26.12 Cr'),
}

pal6 = ['#6366f1','#3b82f6','#22c55e','#f59e0b','#ef4444','#ec4899']

# ════════════════════════════════════════════════════════════════════════════
# CHART 1 — NAV Trend Analysis
# ════════════════════════════════════════════════════════════════════════════
print("Chart 1: NAV Trend...")
nav_avg   = nav_df.groupby(['date','category'])['nav'].mean().reset_index()
nav_pivot = nav_avg.pivot(index='date', columns='category', values='nav')

fig, ax = plt.subplots(figsize=(15, 6))
colors = plt.cm.tab10(np.linspace(0, 1, len(nav_pivot.columns)))
for col, c in zip(nav_pivot.columns, colors):
    ax.plot(nav_pivot.index, nav_pivot[col], lw=1.4, alpha=0.88, color=c, label=col)
ax.axvspan(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31'),
           color='gold', alpha=0.09)
ax.axvspan(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-06-30'),
           color='tomato', alpha=0.09)
ax.text(pd.Timestamp('2023-03-01'), nav_pivot.values.max()*0.97,
        '2023 Bull Run', color='gold', fontsize=10, style='italic', weight='bold')
ax.text(pd.Timestamp('2024-01-15'), nav_pivot.values.max()*0.87,
        '2024 Correction', color='tomato', fontsize=10, style='italic', weight='bold')
ax.set_title('NAV Trend — All 40 Schemes (2022–2025)', fontsize=15, pad=12)
ax.set_xlabel('Date')
ax.set_ylabel('NAV (Rs.)')
ax.legend(ncol=5, fontsize=7.5, loc='upper left')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x:,.0f}'))
plt.tight_layout()
plt.savefig(f'{OUT}/chart01_nav_trend.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart01_nav_trend.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 2 — AUM Growth Grouped Bar
# ════════════════════════════════════════════════════════════════════════════
print("Chart 2: AUM Growth...")
aum_pivot  = aum_df.pivot(index='fund_house', columns='year', values='aum_lakh_cr')
x          = np.arange(len(aum_pivot))
width      = 0.2
bar_colors = ['#3b82f6','#22c55e','#f59e0b','#ef4444']

fig, ax = plt.subplots(figsize=(15, 7))
for i, (yr, col) in enumerate(zip(years, bar_colors)):
    bars = ax.bar(x + i*width, aum_pivot[yr], width, label=str(yr),
                  color=col, alpha=0.87, edgecolor=BG, linewidth=0.5)
    for b in bars:
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.04,
                f'{b.get_height():.1f}', ha='center', va='bottom', fontsize=7, color=FG)

sbi_i = list(aum_pivot.index).index('SBI MF')
ax.annotate('SBI MF Dominance\nRs.12.5L Cr (2025)',
            xy=(sbi_i + width*1.5, 12.5), xytext=(sbi_i + 3.5, 10.5),
            arrowprops=dict(arrowstyle='->', color='gold', lw=1.8),
            fontsize=10, color='gold', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', fc=AX, ec='gold', alpha=0.9))
ax.set_xticks(x + width*1.5)
ax.set_xticklabels(aum_pivot.index, rotation=28, ha='right', fontsize=9)
ax.set_ylabel('AUM (Rs. Lakh Crore)', fontsize=12)
ax.set_title('AUM Growth by Fund House — 2022–2025', fontsize=15, pad=12)
ax.legend(title='Year', fontsize=10)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('Rs.%.1f'))
plt.tight_layout()
plt.savefig(f'{OUT}/chart02_aum_growth.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart02_aum_growth.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 3 — SIP Inflow Time-Series
# ════════════════════════════════════════════════════════════════════════════
print("Chart 3: SIP Inflow...")
peak_idx  = sip_df['sip_inflow_cr'].idxmax()
peak_date = sip_df.loc[peak_idx, 'date']
peak_val  = int(sip_df.loc[peak_idx, 'sip_inflow_cr'])

fig, ax = plt.subplots(figsize=(13, 5))
ax.fill_between(sip_df['date'], sip_df['sip_inflow_cr'], alpha=0.18, color='#22d3ee')
ax.plot(sip_df['date'], sip_df['sip_inflow_cr'], color='#22d3ee', lw=2.5, zorder=3)
ax.scatter([peak_date], [peak_val], s=120, color='gold', zorder=6)
ax.annotate(f'ATH: Rs.{peak_val:,} Cr\nDec 2025',
            xy=(peak_date, peak_val), xytext=(-110, -45),
            textcoords='offset points', fontsize=10, color='gold',
            arrowprops=dict(arrowstyle='->', color='gold'),
            bbox=dict(boxstyle='round', fc=AX, ec='gold', alpha=0.9))

yr_milestones = [(2022, 13573, 'Rs.13,573 Cr'), (2023, 17610, 'Rs.17,610 Cr'),
                 (2024, 26400, 'Rs.26,400 Cr')]
for yr, val, lbl in yr_milestones:
    row = sip_df[sip_df['date'].dt.year == yr].iloc[-1]
    ax.annotate(lbl, xy=(row['date'], row['sip_inflow_cr']),
                xytext=(0, 14), textcoords='offset points',
                ha='center', fontsize=8, color='#94a3b8')

ax.set_title('Monthly SIP Inflow Trend — Jan 2022 to Dec 2025', fontsize=15, pad=12)
ax.set_xlabel('Month')
ax.set_ylabel('SIP Inflow (Rs. Crore)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x:,.0f}'))
plt.tight_layout()
plt.savefig(f'{OUT}/chart03_sip_inflow.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart03_sip_inflow.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 4 — Category Inflow Heatmap
# ════════════════════════════════════════════════════════════════════════════
print("Chart 4: Heatmap...")
heat      = cat_inflow_df.T.copy()
heat.columns = [d.strftime('%b %y') for d in monthly_dates]
col_labels   = [c if i % 4 == 0 else '' for i, c in enumerate(heat.columns)]

fig, ax = plt.subplots(figsize=(22, 7))
sns.heatmap(heat, ax=ax, cmap='YlOrRd', xticklabels=col_labels,
            linewidths=0.25, linecolor=BG,
            cbar_kws={'label': 'Net Inflow (Rs. Cr)', 'shrink': 0.65})
ax.set_title('Category-Wise Monthly Net Inflow Heatmap (Jan 2022 - Dec 2025)', fontsize=15, pad=12)
ax.set_xlabel('Month', fontsize=11)
ax.set_ylabel('Fund Category', fontsize=11)
ax.tick_params(axis='x', rotation=45, labelsize=7.5)
ax.tick_params(axis='y', rotation=0, labelsize=10)
plt.tight_layout()
plt.savefig(f'{OUT}/chart04_category_heatmap.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart04_category_heatmap.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 5 — Investor Demographics (3 panels)
# ════════════════════════════════════════════════════════════════════════════
print("Chart 5: Demographics...")
age_counts = [inv_df[inv_df['age_group'] == ag].shape[0] for ag in age_groups]

fig, axes = plt.subplots(1, 3, figsize=(19, 7))

axes[0].pie(age_counts, labels=age_groups, autopct='%1.1f%%', colors=pal6,
            explode=[0.04]*6, startangle=140,
            textprops=dict(color=FG, fontsize=9), pctdistance=0.8)
axes[0].set_title('Age Group Distribution', fontsize=13, pad=10)

sns.boxplot(data=inv_df, x='age_group', y='sip_amount',
            order=age_groups, palette=pal6, ax=axes[1],
            flierprops=dict(marker='o', ms=2, mfc='#64748b'),
            medianprops=dict(color='gold', lw=2),
            boxprops=dict(edgecolor=FG))
axes[1].set_title('SIP Amount by Age Group', fontsize=13, pad=10)
axes[1].set_xlabel('Age Group')
axes[1].set_ylabel('SIP Amount (Rs.)')
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x:,.0f}'))
axes[1].tick_params(axis='x', rotation=25)

axes[2].pie([62, 36, 2], labels=['Male', 'Female', 'Other'],
            colors=['#3b82f6','#ec4899','#22c55e'],
            autopct='%1.0f%%', startangle=90, pctdistance=0.75,
            textprops=dict(color=FG, fontsize=11))
axes[2].set_title('Gender Split of Investors', fontsize=13, pad=10)

fig.suptitle('Investor Demographics — Indian MF Ecosystem (2025)',
             fontsize=15, y=1.02, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{OUT}/chart05_demographics.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart05_demographics.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 6 — Geographic Distribution
# ════════════════════════════════════════════════════════════════════════════
print("Chart 6: Geographic...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7),
                               gridspec_kw={'width_ratios': [2.2, 1]})
norm_vals = geo_df['sip_amount_cr'] / geo_df['sip_amount_cr'].max()
bar_c     = plt.cm.plasma(norm_vals)
bars = ax1.barh(geo_df['state'], geo_df['sip_amount_cr'],
                color=bar_c, edgecolor=BG, linewidth=0.3, height=0.65)
for bar, val in zip(bars, geo_df['sip_amount_cr']):
    ax1.text(val + 600, bar.get_y() + bar.get_height()/2,
             f'Rs.{val:,} Cr', va='center', ha='left', fontsize=8)
ax1.set_xlabel('SIP Amount (Rs. Crore)', fontsize=11)
ax1.set_title('SIP Investment by State (2025)', fontsize=13, pad=10)
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x:,.0f}'))

ax2.pie([72, 28], labels=['T30 Cities', 'B30 Cities'],
        colors=['#6366f1','#f59e0b'], autopct='%1.0f%%', startangle=90,
        pctdistance=0.72, textprops=dict(color=FG, fontsize=12),
        wedgeprops=dict(edgecolor=BG, lw=2))
ax2.set_title('T30 vs B30 City Tier\nSIP Distribution', fontsize=12, pad=10)

plt.tight_layout()
plt.savefig(f'{OUT}/chart06_geographic.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart06_geographic.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 7 — Folio Count Growth
# ════════════════════════════════════════════════════════════════════════════
print("Chart 7: Folio Growth...")
fig, ax = plt.subplots(figsize=(13, 5))
ax.fill_between(folio_df['date'], folio_df['folio_cr'], alpha=0.15, color='#a78bfa')
ax.plot(folio_df['date'], folio_df['folio_cr'], color='#a78bfa', lw=2.8, zorder=3)
for ds, (val, lbl) in milestones.items():
    ax.scatter([pd.Timestamp(ds)], [val], s=90, color='gold', zorder=5)
    ax.annotate(lbl, xy=(pd.Timestamp(ds), val),
                xytext=(0, 10), textcoords='offset points',
                ha='center', fontsize=8, color='gold')
ax.annotate('Start: 13.26 Cr',
            xy=(folio_df['date'].iloc[0], folio_df['folio_cr'].iloc[0]),
            xytext=(60, -25), textcoords='offset points', color='#94a3b8', fontsize=9,
            arrowprops=dict(arrowstyle='->', color='#94a3b8'))
ax.set_title('Total Folio Count Growth (Jan 2022 - Dec 2025)', fontsize=15, pad=12)
ax.set_xlabel('Date')
ax.set_ylabel('Folios (Crore)')
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f Cr'))
plt.tight_layout()
plt.savefig(f'{OUT}/chart07_folio_growth.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart07_folio_growth.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 8 — NAV Return Correlation Matrix
# ════════════════════════════════════════════════════════════════════════════
print("Chart 8: Correlation Matrix...")
selected_ids = schemes_df.groupby('category').first().reset_index()['scheme_id'].tolist()
sel_nav      = nav_df[nav_df['scheme_id'].isin(selected_ids)].copy()
sel_pivot    = sel_nav.pivot_table(index='date', columns='category', values='nav', aggfunc='mean')
returns      = sel_pivot.pct_change().dropna()
corr_mat     = returns.corr()
short_lbl    = [c[:10] for c in corr_mat.columns]

fig, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corr_mat, ax=ax, cmap='coolwarm', center=0, vmin=-1, vmax=1,
            annot=True, fmt='.2f', annot_kws={'size': 10, 'weight': 'bold'},
            linewidths=0.5, linecolor=BG,
            xticklabels=short_lbl, yticklabels=short_lbl,
            cbar_kws={'label': 'Pearson Correlation', 'shrink': 0.8})
ax.set_title('Pairwise Return Correlation - 10 Fund Categories (2022-2025)', fontsize=14, pad=14)
ax.tick_params(axis='x', rotation=35, labelsize=9)
ax.tick_params(axis='y', rotation=0, labelsize=9)
plt.tight_layout()
plt.savefig(f'{OUT}/chart08_correlation.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart08_correlation.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 9 — Sector Allocation Donut
# ════════════════════════════════════════════════════════════════════════════
print("Chart 9: Sector Donut...")
sectors = ['Financial Services','IT & Technology','Healthcare','Consumer Goods',
           'Energy & Oil','Automobile','Infrastructure','Metals & Mining','Telecom','Others']
weights = [28.5, 14.2, 9.8, 8.6, 7.4, 6.9, 6.2, 5.8, 4.1, 8.5]
colors_s = ['#6366f1','#3b82f6','#22c55e','#f59e0b','#ef4444',
            '#ec4899','#14b8a6','#a78bfa','#fb923c','#64748b']

fig, ax = plt.subplots(figsize=(11, 9))
wedges, texts, autotexts = ax.pie(
    weights, labels=sectors, autopct='%1.1f%%', colors=colors_s,
    startangle=120, pctdistance=0.82,
    wedgeprops=dict(width=0.5, edgecolor=BG, lw=2),
    textprops=dict(color=FG, fontsize=9))
for at in autotexts:
    at.set_fontsize(8.5)
wedges[0].set_radius(1.08)
ax.text(0, 0, 'Equity\nFunds', ha='center', va='center',
        fontsize=14, fontweight='bold', color=FG)
ax.set_title('Sector Allocation - Aggregated Equity Fund Holdings (2025)', fontsize=14, pad=16)
plt.tight_layout()
plt.savefig(f'{OUT}/chart09_sector_donut.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart09_sector_donut.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 10 — Annual NAV Returns by Category
# ════════════════════════════════════════════════════════════════════════════
print("Chart 10: Annual Returns...")
nav_df['year'] = nav_df['date'].dt.year
nav_yr = nav_df.groupby(['year','category'])['nav'].agg(['first','last']).reset_index()
nav_yr['return_pct'] = (nav_yr['last'] / nav_yr['first'] - 1) * 100

fig, ax = plt.subplots(figsize=(14, 6))
sns.barplot(data=nav_yr[nav_yr['year'] < 2026],
            x='category', y='return_pct', hue='year',
            palette=['#3b82f6','#22c55e','#f59e0b','#ef4444'], ax=ax, alpha=0.87)
ax.axhline(0, color='#94a3b8', lw=1.2, ls='--')
ax.set_title('Annual NAV Returns by Category (2022-2025)', fontsize=14, pad=10)
ax.set_xlabel('Fund Category')
ax.set_ylabel('Annual Return (%)')
ax.tick_params(axis='x', rotation=30)
ax.legend(title='Year', fontsize=9)
plt.tight_layout()
plt.savefig(f'{OUT}/chart10_annual_returns.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart10_annual_returns.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 11 — Annual SIP Total + YoY Growth (dual-axis)
# ════════════════════════════════════════════════════════════════════════════
print("Chart 11: SIP YoY...")
sip_df['year'] = sip_df['date'].dt.year
sip_annual     = sip_df.groupby('year')['sip_inflow_cr'].sum().reset_index()
sip_annual['yoy'] = sip_annual['sip_inflow_cr'].pct_change() * 100

fig, ax1 = plt.subplots(figsize=(10, 6))
ax2  = ax1.twinx()
ax2.set_facecolor(AX)
bars = ax1.bar(sip_annual['year'], sip_annual['sip_inflow_cr'],
               color='#22c55e', alpha=0.82, edgecolor=BG, width=0.55)
for b, v in zip(bars, sip_annual['sip_inflow_cr']):
    ax1.text(b.get_x()+b.get_width()/2, b.get_height()+2000,
             f'Rs.{v/1e5:.2f}L Cr', ha='center', fontsize=9, color='#22c55e')
ax2.plot(sip_annual['year'], sip_annual['yoy'], 'o-',
         color='gold', lw=2.5, ms=9, zorder=5)
for xi, yi in zip(sip_annual['year'], sip_annual['yoy']):
    if not np.isnan(yi):
        ax2.annotate(f'{yi:.1f}%', (xi, yi),
                     textcoords='offset points', xytext=(0,10),
                     ha='center', fontsize=9, color='gold')
ax1.set_xlabel('Year')
ax1.set_ylabel('Annual SIP Inflow (Rs. Cr)', color='#22c55e')
ax2.set_ylabel('YoY Growth (%)', color='gold')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x/1e5:.1f}L Cr'))
ax2.tick_params(axis='y', colors='gold')
ax1.tick_params(axis='y', colors='#22c55e')
ax1.set_xticks([2022,2023,2024,2025])
ax1.set_title('Annual SIP Inflow & YoY Growth Rate (2022-2025)', fontsize=14, pad=10)
plt.tight_layout()
plt.savefig(f'{OUT}/chart11_sip_yoy.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart11_sip_yoy.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 12 — Total Industry AUM Trend
# ════════════════════════════════════════════════════════════════════════════
print("Chart 12: Industry AUM...")
aum_total = aum_df.groupby('year')['aum_lakh_cr'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
ax.fill_between(aum_total['year'], aum_total['aum_lakh_cr'], alpha=0.25, color='#6366f1')
ax.plot(aum_total['year'], aum_total['aum_lakh_cr'], 'o-', color='#6366f1', lw=2.8, ms=10)
for _, row in aum_total.iterrows():
    ax.annotate(f'Rs.{row.aum_lakh_cr:.1f}L Cr',
                (row.year, row.aum_lakh_cr), xytext=(0, 12),
                textcoords='offset points', ha='center', fontsize=11,
                fontweight='bold', color='#a5b4fc')
ax.set_xticks([2022,2023,2024,2025])
ax.set_title('Total Indian MF Industry AUM (2022-2025)', fontsize=14, pad=10)
ax.set_xlabel('Year')
ax.set_ylabel('Total AUM (Rs. Lakh Crore)')
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('Rs.%.0f L Cr'))
plt.tight_layout()
plt.savefig(f'{OUT}/chart12_total_aum.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart12_total_aum.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 13 — 30-Day Rolling Volatility
# ════════════════════════════════════════════════════════════════════════════
print("Chart 13: Volatility...")
pivot_daily = nav_df.pivot_table(index='date', columns='category', values='nav', aggfunc='mean')
ret_d       = pivot_daily.pct_change()
vol_30      = ret_d.rolling(30).std() * np.sqrt(252) * 100

highlight = {'Small Cap':'#ef4444','Mid Cap':'#f59e0b','Large Cap':'#22c55e','Debt':'#3b82f6'}

fig, ax = plt.subplots(figsize=(14, 6))
for cat, col in highlight.items():
    if cat in vol_30.columns:
        ax.plot(vol_30.index, vol_30[cat], lw=1.8, alpha=0.88, color=col, label=cat)
ax.axvspan(pd.Timestamp('2024-01-01'), pd.Timestamp('2024-06-30'),
           color='tomato', alpha=0.07, label='2024 H1 Correction')
ax.axvspan(pd.Timestamp('2023-01-01'), pd.Timestamp('2023-12-31'),
           color='gold', alpha=0.07, label='2023 Bull Run')
ax.set_title('30-Day Rolling Annualised Volatility by Category (2022-2025)', fontsize=14, pad=10)
ax.set_xlabel('Date')
ax.set_ylabel('Volatility (% annualised)')
ax.legend(fontsize=9, ncol=3)
plt.tight_layout()
plt.savefig(f'{OUT}/chart13_volatility.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart13_volatility.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 14 — Quarterly Folio + Category AUM Mix
# ════════════════════════════════════════════════════════════════════════════
print("Chart 14: Quarterly Folio + AUM Mix...")
folio_df['quarter'] = folio_df['date'].dt.to_period('Q')
folio_q  = folio_df.groupby('quarter')['folio_cr'].last().reset_index()
q_labels = [str(q) for q in folio_q['quarter']]
show_lbl = [l if i % 4 == 0 else '' for i,l in enumerate(q_labels)]

cat_aum_2025 = {c: float(np.random.uniform(0.5, 4.5)) for c in categories}
cat_aum_2025['Large Cap'] = 5.8
cat_aum_2025['Index']     = 4.2
cat_aum_2025['Debt']      = 7.3

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

ax1.plot(range(len(folio_q)), folio_q['folio_cr'],
         color='#a78bfa', lw=2.5, marker='o', ms=3)
ax1.fill_between(range(len(folio_q)), folio_q['folio_cr'], alpha=0.15, color='#a78bfa')
ax1.set_xticks(range(len(folio_q)))
ax1.set_xticklabels(show_lbl, rotation=45, ha='right', fontsize=7.5)
ax1.set_title('Quarterly Folio Count Growth (2022-2025)', fontsize=12, pad=8)
ax1.set_ylabel('Folios (Crore)')
ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f Cr'))

sorted_cat = sorted(cat_aum_2025, key=cat_aum_2025.get, reverse=True)
sorted_val = [cat_aum_2025[c] for c in sorted_cat]
ax2.barh(sorted_cat, sorted_val,
         color=plt.cm.viridis(np.linspace(0.2, 0.9, len(sorted_cat))),
         edgecolor=BG, linewidth=0.4, height=0.65)
for i, (cat, val) in enumerate(zip(sorted_cat, sorted_val)):
    ax2.text(val + 0.06, i, f'Rs.{val:.1f}L Cr', va='center', fontsize=8)
ax2.set_title('Category AUM Distribution (2025)', fontsize=12, pad=8)
ax2.set_xlabel('AUM (Rs. Lakh Crore)')

plt.tight_layout()
plt.savefig(f'{OUT}/chart14_folio_aum.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart14_folio_aum.png")

# ════════════════════════════════════════════════════════════════════════════
# CHART 15 — Fund House Market Share + SIP Seasonality
# ════════════════════════════════════════════════════════════════════════════
print("Chart 15: Market Share + Seasonality...")
aum_2025 = aum_df[aum_df['year'] == 2025][['fund_house','aum_lakh_cr']].set_index('fund_house')

sip_df['month_name'] = sip_df['date'].dt.strftime('%b')
sip_df['month_num']  = sip_df['date'].dt.month
sip_monthly_avg = sip_df.groupby(['month_num','month_name'])['sip_inflow_cr'].mean().reset_index()
sip_monthly_avg = sip_monthly_avg.sort_values('month_num')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

ax1.pie(aum_2025['aum_lakh_cr'], labels=aum_2025.index,
        autopct='%1.1f%%', colors=plt.cm.tab10(np.linspace(0,1,len(aum_2025))),
        startangle=140, pctdistance=0.82,
        textprops=dict(color=FG, fontsize=8.5),
        wedgeprops=dict(edgecolor=BG, lw=1.5))
ax1.set_title('Fund House Market Share by AUM (2025)', fontsize=13, pad=10)

bars = ax2.bar(sip_monthly_avg['month_name'], sip_monthly_avg['sip_inflow_cr'],
               color=plt.cm.plasma(np.linspace(0.2, 0.9, 12)),
               edgecolor=BG, linewidth=0.4)
avg_sip = sip_monthly_avg['sip_inflow_cr'].mean()
ax2.axhline(avg_sip, color='gold', lw=1.5, ls='--', label=f'Average Rs.{avg_sip:,.0f} Cr')
ax2.set_title('Average Monthly SIP Inflow by Month (2022-2025)', fontsize=12, pad=10)
ax2.set_xlabel('Month')
ax2.set_ylabel('Avg SIP Inflow (Rs. Cr)')
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'Rs.{x:,.0f}'))
ax2.legend(fontsize=9)
ax2.tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.savefig(f'{OUT}/chart15_market_share_seasonality.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  -> saved chart15_market_share_seasonality.png")

# ════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════════════════
chart_files = sorted(f for f in os.listdir(OUT) if f.endswith('.png'))
print(f"\n{'='*55}")
print(f"  Total charts exported: {len(chart_files)}")
print(f"  Output directory     : {OUT}")
print(f"{'='*55}")
for i, f in enumerate(chart_files, 1):
    kb = os.path.getsize(f'{OUT}/{f}') / 1024
    print(f"  {i:02d}. {f:<45s} ({kb:,.0f} KB)")
print(f"{'='*55}")
print("  ALL DONE!")
