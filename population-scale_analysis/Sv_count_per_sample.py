import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = 'SV_per_sample.txt'
df = pd.read_csv(file_path, delim_whitespace=True)

population_order = ['AFR', 'AMR',  'EUR', 'EAS', 'SAS']

df['Population'] = pd.Categorical(df['Population'], categories=population_order, ordered=True)
df = df.sort_values(by='Population')

df['Total_SVs'] = df['Hom'] + df['Het']

plt.figure(figsize=(5.5, 4))
sns.violinplot(x='Population', y='Total_SVs', data=df, order=population_order)

plt.ylabel('Number of SVs', fontsize=12)

plt.xlabel('Population', fontsize=12)

plt.tight_layout()
plt.savefig("1KG_spl_SV_violin.png", dpi=600)
plt.savefig("1KG_spl_SV_violin.pdf", dpi=600, format='pdf')
