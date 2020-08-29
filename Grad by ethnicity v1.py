import json

import pandas as pd
import numpy as np

data = pd.read_csv('Grad by ethnicity.csv')  

# Define a list of models that we want to review
rows_4 = ["3","4","41", "42"]
rows_2 = ["30", "33", "47", "48"]

# Create a copy of the data with only the top 8 manufacturers
df4 = data[data.GRTYPE.isin(rows_4)].copy()
df2 = data[data.GRTYPE.isin(rows_2)].copy()

summary4 = pd.crosstab(df4.UNITID, df4.GRTYPE, values=df4.GRTOTLT, aggfunc='sum')
summary4 = summary4.fillna(0)
summary4['Total'] = summary4.sum(axis=1)
summary4['Overall grad rate'] = summary4[3]/summary4['Total']
summary4['Overall transfer rate'] = summary4[4]/summary4['Total']
summary4['2 or 4'] = '4-year'
#print(summary4)

summary2 = pd.crosstab(df2.UNITID, df2.GRTYPE, values=df2.GRTOTLT, aggfunc='sum')
summary2 = summary2.fillna(0)
summary2['Total'] = summary2.sum(axis=1)
summary2['Overall grad rate'] = summary2[30]/summary2['Total']
summary2['Overall transfer rate'] = summary2[33]/summary2['Total']
summary2['2 or 4'] = '2-year or less'
#print(summary2)

frames = [summary4, summary2]

overall_rates = pd.concat(frames)
overall_rates = overall_rates[['2 or 4','Total', 'Overall grad rate', 'Overall transfer rate']]
#print(overall_rates)

black4 = pd.crosstab(df4.UNITID, df4.GRTYPE, values=df4.GRBKAAT, aggfunc='sum')
black4 = black4.fillna(0)
black4['Black total'] = black4.sum(axis=1)
black4['Black grad rate'] = black4[3]/black4['Black total']
black4['Black transfer rate'] = black4[4]/black4['Black total']

black2 = pd.crosstab(df2.UNITID, df2.GRTYPE, values=df2.GRBKAAT, aggfunc='sum')
black2 = black2.fillna(0)
black2['Black total'] = black2.sum(axis=1)
black2['Black grad rate'] = black2[30]/black2['Black total']
black2['Black transfer rate'] = black2[33]/black2['Black total']
#print(summary2)

frames = [black4, black2]

black_rates = pd.concat(frames)
black_rates = black_rates[['Black total', 'Black grad rate', 'Black transfer rate']]
#print(black_rates)

hispanic4 = pd.crosstab(df4.UNITID, df4.GRTYPE, values=df4.GRHISPT, aggfunc='sum')
hispanic4 = hispanic4.fillna(0)
hispanic4['Hispanic total'] = hispanic4.sum(axis=1)
hispanic4['Hispanic grad rate'] = hispanic4[3]/hispanic4['Hispanic total']
hispanic4['Hispanic transfer rate'] = hispanic4[4]/hispanic4['Hispanic total']

hispanic2 = pd.crosstab(df2.UNITID, df2.GRTYPE, values=df2.GRHISPT, aggfunc='sum')
hispanic2 = hispanic2.fillna(0)
hispanic2['Hispanic total'] = hispanic2.sum(axis=1)
hispanic2['Hispanic grad rate'] = hispanic2[30]/hispanic2['Hispanic total']
hispanic2['Hispanic transfer rate'] = hispanic2[33]/hispanic2['Hispanic total']
#print(summary2)

frames = [hispanic4, hispanic2]

hispanic_rates = pd.concat(frames)
hispanic_rates = hispanic_rates[['Hispanic total', 'Hispanic grad rate', 'Hispanic transfer rate']]
#print(hispanic_rates)


final_rates = overall_rates.join(black_rates)
final_rates = final_rates.join(hispanic_rates)


mapping = pd.read_excel('UNITID mapping.xlsx', index_col = 0)  
mapping = mapping[['NAME', 'STATE']]
final_rates = final_rates.join(mapping)

data = pd.read_csv('Pell grad rates.csv', index_col = 0)  

# Define a list of models that we want to review
rows = ["1", "4"]

# Pell grad rates data
dfpell = data[data.PSGRTYPE.isin(rows)].copy()

dfpell['Pell grad rate'] = dfpell['PGCMTOT']/dfpell['PGADJCT']
dfpell['Non-pell grad rate'] = dfpell['NRCMTOT']/dfpell['NRADJCT']
dfpell['% Pell population'] = dfpell['PGADJCT']/dfpell['TTADJCT']
dfpell = dfpell[['Pell grad rate', 'Non-pell grad rate', '% Pell population']]

final_rates = final_rates.join(dfpell)
final_rates = final_rates.fillna(0)
final_rates = final_rates.sort_values(by='Total', ascending=False)


#correct college type
collegetype = pd.read_csv('UNITID info.csv', encoding = "latin-1", index_col = 0)
collegetype = collegetype[['ICLEVEL']]
final_rates = final_rates.join(collegetype)
final_rates = final_rates.drop(['2 or 4'], axis=1)
final_rates.loc[(final_rates.ICLEVEL == 1),'ICLEVEL']='4-year'
final_rates.loc[(final_rates.ICLEVEL == 2),'ICLEVEL']='2-year'
final_rates.loc[(final_rates.ICLEVEL == 3),'ICLEVEL']='Less than 2-year'
final_rates = final_rates.rename(columns={"ICLEVEL": "2 or 4"})

#Pell gap
final_rates['Pell gap'] = final_rates['Non-pell grad rate'] - final_rates['Pell grad rate']


#convert all to %s
final_rates['Overall grad rate'] = pd.Series(["{0:.1f}".format(val * 100) for val in final_rates['Overall grad rate']], index = final_rates.index)
final_rates['Overall transfer rate'] = pd.Series(["{0:.1f}".format(val * 100) for val in final_rates['Overall transfer rate']], index = final_rates.index)
final_rates['Black grad rate'] = pd.Series(["{0:.1f}".format(val * 100) for val in final_rates['Black grad rate']], index = final_rates.index)
final_rates['Black transfer rate'] = pd.Series(["{0:.1f}".format(val * 100) for val in final_rates['Black transfer rate']], index = final_rates.index)
final_rates['Hispanic grad rate'] = pd.Series(["{0:.1f}".format(val * 100) for val in final_rates['Hispanic grad rate']], index = final_rates.index)
final_rates['Hispanic transfer rate'] = pd.Series(["{0:.1f}".format(val * 100) for val in final_rates['Hispanic transfer rate']], index = final_rates.index)
final_rates['Pell grad rate'] = pd.Series(["{0:.1f}".format(val * 100) for val in final_rates['Pell grad rate']], index = final_rates.index)
final_rates['Non-pell grad rate'] = pd.Series(["{0:.1f}".format(val * 100) for val in final_rates['Non-pell grad rate']], index = final_rates.index)
final_rates['% Pell population'] = pd.Series(["{0:.1f}".format(val * 100) for val in final_rates['% Pell population']], index = final_rates.index)
final_rates['Pell gap'] = pd.Series(["{0:.1f}".format(val * 100) for val in final_rates['Pell gap']], index = final_rates.index)

print(final_rates)
d = final_rates.to_dict(orient='records')
j = json.dumps(d)
print(j)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=4)
