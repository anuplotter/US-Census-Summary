from altair.vegalite.v4.schema.channels import Tooltip
from altair.vegalite.v4.schema.core import LabelOverlap, TooltipContent
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import math as math
import matplotlib.pyplot as plt
#from vega_datasets import data

# Formatting link: https://d3-wiki.readthedocs.io/zh_CN/master/Formatting/

#df_census = pd.read_csv("C:/Users/anupm/OneDrive/Desktop/Plot AI/Datasets/Al/Census/Census.csv")
url='https://drive.google.com/file/d/1GmjBiRnGWcMVlQEt_iRYpzsOnxZweWGJ/view?usp=sharing'
url2='https://drive.google.com/uc?id=' + url.split('/')[-2]
df_census = pd.read_csv(url2)

#MULTISLECT

#Unique option in select widget
#sel_origin = st.sidebar.multiselect('Origin:', pd.Series(np.append('All', df_census.Origin.unique())), default='All')
#sel_race = st.sidebar.multiselect('Race:', pd.Series(np.append('All', df_census.Race.unique())), default='All')
sel_race_origin = st.sidebar.multiselect('Race and Origin:', pd.Series(np.append('All', df_census.Race_and_Origin.unique())), default='All')
sel_sex = st.sidebar.multiselect('Sex:', pd.Series(np.append('All', df_census.Sex.unique())), default='All')
sel_age_group = st.sidebar.multiselect('Age Group:', pd.Series(np.append('All', df_census.Age_Group.unique())), default='All')
sel_region = st.sidebar.multiselect("Region:", pd.Series(np.append('All', df_census.Region.unique())), default='All')
sel_division = st.sidebar.multiselect("Division:", pd.Series(np.append('All', df_census.Division.unique())), default='All')
sel_state = st.sidebar.multiselect("State:", pd.Series(np.append('All', df_census.State.unique())), default='All')



if "All" in sel_region:
    sel_region = df_census.Region.unique()
if "All" in sel_division:
    sel_division = df_census.Division.unique()
if "All" in sel_state:
    sel_state = df_census.State.unique()
if "All" in sel_sex:
    sel_sex = df_census.Sex.unique()
#if "All" in sel_origin:
#    sel_origin = df_census.Origin.unique()
#if "All" in sel_race:
#    sel_race = df_census.Race.unique()
if "All" in sel_race_origin:
    sel_race_origin = df_census.Race_and_Origin.unique()
if "All" in sel_age_group:
    sel_age_group = df_census.Age_Group.unique()



#DATA MANIPULATION

df_census_copy = df_census

df_census_copy = df_census_copy.loc[df_census_copy['Region'].isin(sel_region)]
df_census_copy = df_census_copy.loc[df_census_copy['Division'].isin(sel_division)]
df_census_copy = df_census_copy.loc[df_census_copy['State'].isin(sel_state)]
df_census_copy = df_census_copy.loc[df_census_copy['Sex'].isin(sel_sex)]
#df_census_copy = df_census_copy.loc[df_census_copy['Origin'].isin(sel_origin)]
#df_census_copy = df_census_copy.loc[df_census_copy['Race'].isin(sel_race)]
df_census_copy = df_census_copy.loc[df_census_copy['Race_and_Origin'].isin(sel_race_origin)]
df_census_copy = df_census_copy.loc[df_census_copy['Age_Group'].isin(sel_age_group)]

line_break = '''---'''

#Text boxes
growth = df_census_copy['Population_2019'].sum()/df_census_copy['Population_2010'].sum()-1
percentage_growth = "{:.1%}".format(growth)

st.header('US Census Data Summary')
st.write('**2010 Population:**', df_census_copy['Population_2010'].sum())
st.write('**2019 Population:**', df_census_copy['Population_2019'].sum(), '(growth ', percentage_growth, ')' )

#st.write('**2010 Population:**', num.numerize(df_census_copy['Population_2010'].sum()*1.00,1))
#st.write('**2019 Population:**', num.numerize(df_census_copy['Population_2019'].sum()*1.00,1), '(growth ', percentage_growth, ')' )
st.markdown(line_break)


#CHARTS

# Region
df_region_population = df_census_copy.groupby(['Region']).sum().reset_index()
df_region_population['pop_growth'] = df_region_population['Population_2019']/df_region_population['Population_2010']-1

df_region_population_hispanic = df_census_copy[df_census_copy['Race_and_Origin']=='Hispanic'].groupby(['Region']).sum().reset_index()
df_region_population_hispanic['pop_growth'] = df_region_population_hispanic['Population_2019']/df_region_population_hispanic['Population_2010']-1

bar_region_population = alt.Chart(df_region_population, title = '2019 Population by Region').mark_bar().encode(
    x = alt.X('Region:O', axis=alt.Axis(title='Region'), sort=['South', 'West', 'Midwest', 'North']),
    y = alt.Y('Population_2019', axis = alt.Axis( title= '2019 Population', format ='~s')),
    tooltip=['Region', alt.Tooltip('Population_2019', format='.3s', title='Pop. 2019') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth')]
).properties(width=600)

line_region_population = alt.Chart(df_region_population).mark_line(stroke='#FFA500', interpolate='monotone', point=alt.OverlayMarkDef(color="orange")).encode(
    alt.X('Region:O', axis=alt.Axis(title='Region'), sort=['South', 'West', 'Midwest', 'North']),
    alt.Y('pop_growth',axis=alt.Axis(title='Growth', titleColor='#FFA500', format='%')),
    tooltip=['Region', alt.Tooltip('Population_2019', format='.3s', title='Pop. 2019') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth')]
).properties(width=600)



bar_region_population_hispanic = alt.Chart(df_region_population_hispanic, title = '2019 Hispanic Population by Region').mark_bar().encode(
    x = alt.X('Region:O', axis=alt.Axis(title='Region'), sort=['South', 'West', 'Midwest', 'North']),
    y = alt.Y('Population_2019', axis = alt.Axis( title= '2019 Population', format ='~s')),
    tooltip=['Region', alt.Tooltip('Population_2019', format='.3s', title='Pop. 2019') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth')]
).properties(width=600)


line_region_population_hispanic = alt.Chart(df_region_population_hispanic).mark_line(stroke='#FFA500', interpolate='monotone', point=alt.OverlayMarkDef(color="#FFA500")).encode(
    alt.X('Region:O', axis=alt.Axis(title='Region'), sort=['South', 'West', 'Midwest', 'North']),
    alt.Y('pop_growth',axis=alt.Axis(title='Growth', titleColor='#FFA500', format='%')),
    tooltip=['Region', alt.Tooltip('Population_2019', format='.3s', title='Pop. 2019') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth')]
).properties(width=600)

st.write('1) South and West regions which account for close to two thirds of the US population also had the highest growth rates.')

st.altair_chart(alt.layer(bar_region_population, line_region_population).resolve_scale(y = 'independent'))
st.altair_chart(alt.layer(bar_region_population_hispanic, line_region_population_hispanic).resolve_scale(y = 'independent'))

#st.write(df_region_population_hispanic )


st.markdown(line_break)


# State
df_state_population = df_census_copy.groupby(['State']).sum().reset_index()
df_state_population['pop_growth'] = df_state_population['Population_2019']/df_state_population['Population_2010']-1
#df_state_population['Population_2019_numerize'] = num.numerize(df_state_population['Population_2019']*1.0)

df_state_population_sorted = df_state_population.sort_values(by=['Population_2019'], ascending=False).reset_index(drop=True)

bar_state_population = alt.Chart(df_state_population_sorted, title = '2019 Population by State').mark_bar().encode(
    x = alt.X('State:O', axis=alt.Axis(title='State'), sort = None),
    y = alt.Y('Population_2019', axis = alt.Axis( title= '2019 Population', format ='~s')),
    tooltip=['State', alt.Tooltip('Population_2019', format='.3s', title='Pop. 2019') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth')]
).properties(width=600)

line_state_population = alt.Chart(df_state_population_sorted).mark_line(stroke='#FFA500', interpolate='monotone', point=alt.OverlayMarkDef(color="orange")).encode(
    alt.X('State:O', axis=alt.Axis(title='State'), sort = None),
    alt.Y('pop_growth',axis=alt.Axis(title='Growth', titleColor='#FFA500', format='%')),
    tooltip=['State', alt.Tooltip('Population_2019', format='.3s', title='Pop. 2019') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth')]
).properties(width=600)

st.altair_chart(alt.layer(bar_state_population, line_state_population).resolve_scale(y = 'independent'))

bubble_state_population = alt.Chart(df_state_population_sorted, title = 'Population and Growth by State').mark_point(filled=True, opacity=0.5).encode(
    alt.X('Population_2010', axis = alt.Axis( title= '2010 Population', format = '~s')),
    alt.Y('pop_growth', axis = alt.Axis( title= 'Population Growth', format='%')),
    size='Population_2019',
    color ='State',
    tooltip = ['State', alt.Tooltip('Population_2019', format='.3s', title ='Pop. 2019'), alt.Tooltip('Population_2010', format='.3s', title ='Pop. 2010'), alt.Tooltip('pop_growth:Q', format='.1%', title='Growth')]
).properties(height=400,width=700).interactive()

st.altair_chart(bubble_state_population)

st.markdown(line_break)

# Age Group
df_age_group_population = df_census_copy.groupby(['Age_Group', 'Race_and_Origin']).sum().reset_index()
df_age_group_population['pop_growth'] = df_age_group_population['Population_2019']/df_age_group_population['Population_2010']-1
stacked_bar_age_race_origin = alt.Chart(df_age_group_population, title = '2019 Population by Age Group').mark_bar().encode(
    x=alt.X('Age_Group', axis = alt.Axis( title= 'Age Group')),
    y=alt.Y('Population_2019', axis = alt.Axis( title= '2019 Population', format = '~s')),
    color='Race_and_Origin',
    tooltip=[alt.Tooltip('Age_Group', title = 'Age Group'), alt.Tooltip('Race_and_Origin', title='Race and Origin'),alt.Tooltip('Population_2019', format ='.3s', title='Pop. 2019') ]
).properties(width=700)


area_age_race_origin = alt.Chart(df_age_group_population, title = '2019 Population by Age Group').mark_area().encode(
    x=alt.X('Age_Group', axis = alt.Axis( title= 'Age Group')),
    y=alt.Y('Population_2019', stack="normalize", axis = alt.Axis( title= '2019 Population', format ='%')),
    color='Race_and_Origin',
    tooltip=[alt.Tooltip('Age_Group', title = 'Age Group'), alt.Tooltip('Race_and_Origin', title='Race and Origin'),alt.Tooltip('Population_2019', format ='.3s', title='Pop. 2019') ]
).properties(width=700)

st.altair_chart(stacked_bar_age_race_origin)
st.altair_chart(area_age_race_origin)
st.markdown(line_break)



#Race and Origin
df_race_origin_population = df_census_copy.groupby(['Race_and_Origin']).sum().reset_index()
df_race_origin_population['pop_growth'] = df_race_origin_population['Population_2019']/df_race_origin_population['Population_2010']-1


base_2010_pop = alt.Chart(df_race_origin_population, title = '2010 Population by Race and Origin').encode(
    theta=alt.Theta("Population_2010:Q", stack=True), color=alt.Color("Race_and_Origin:N")
)
pie_2010_pop = base_2010_pop.mark_arc(outerRadius=120).properties(width=600, height = 400)
text_2010_pop = base_2010_pop.mark_text(radius=150, size=10).encode(alt.Text("Population_2010", format ='.3s')).properties(width=600, height = 400)


base_2019_pop = alt.Chart(df_race_origin_population, title = '2019 Population by Race and Origin').encode(
    theta=alt.Theta("Population_2019:Q", stack=True), color=alt.Color("Race_and_Origin:N")
)
pie_2019_pop = base_2019_pop.mark_arc(outerRadius=120).properties(width=600, height = 400)
text_2019_pop = base_2019_pop.mark_text(radius=140, size=10).encode(alt.Text("Population_2019", format ='.3s')).properties(width=600, height = 400)


st.altair_chart(pie_2010_pop + text_2010_pop)
st.altair_chart(pie_2019_pop + text_2019_pop)
#st.altair_chart(pie_2019_pop + text_2019_pop | pie_2010_pop + text_2010_pop)

st.markdown(line_break)


