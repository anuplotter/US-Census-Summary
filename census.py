#---------------------------------------------------------------------------------------
#IMPORTS
from altair.vegalite.v4.schema.channels import Tooltip
from altair.vegalite.v4.schema.core import LabelOverlap, TooltipContent
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import math as math
import matplotlib.pyplot as plt
from streamlit.elements.iframe import IframeMixin

#HIDING STREAMLIT ELEMENTS
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#st.header('plot-ai.com')
# Formatting link: https://d3-wiki.readthedocs.io/zh_CN/master/Formatting/

#---------------------------------------------------------------------------------------
#READING RAW DATA
#df_census = pd.read_csv("C:/Users/anupm/OneDrive/Desktop/Plot AI/Datasets/Al/Census/Census.csv")
url_census='https://drive.google.com/file/d/1GmjBiRnGWcMVlQEt_iRYpzsOnxZweWGJ/view?usp=sharing'
url_census_updated = 'https://drive.google.com/file/d/1zcNMO5aAFt4CgERA9qzozuhQ1xR7pUpX/view?usp=sharing'
url2='https://drive.google.com/uc?id=' + url_census_updated.split('/')[-2]
df_census = pd.read_csv(url2)


#---------------------------------------------------------------------------------------
#SETTING MULTISLECT
#Unique option in select widget
st.sidebar.header('Filter by any dimension')
sel_origin = st.sidebar.multiselect('Origin:', pd.Series(np.append('All', sorted(df_census.Origin.unique()))), default='All')
sel_race = st.sidebar.multiselect('Race:', pd.Series(np.append('All', sorted(df_census.Race.unique()))), default='All')
sel_race_origin = st.sidebar.multiselect('Race and Origin:', pd.Series(np.append('All', sorted(df_census.Race_and_Origin.unique()))), default='All')
sel_state = st.sidebar.multiselect("State:", pd.Series(np.append('All', sorted(df_census.State.unique()))), default='All')
sel_region = st.sidebar.multiselect("Census Region:", pd.Series(np.append('All', sorted(df_census.Region.unique()))), default='All')
sel_division = st.sidebar.multiselect("Census Division:", pd.Series(np.append('All', sorted(df_census.Division.unique()))), default='All')
sel_sex = st.sidebar.multiselect('Sex:', pd.Series(np.append('All', sorted(df_census.Sex.unique()))), default='All')
sel_age_group = st.sidebar.multiselect('Age Group:', pd.Series(np.append('All', sorted(df_census.Age_Group.unique()))), default='All')


if "All" in sel_region:
    sel_region = df_census.Region.unique()
if "All" in sel_division:
    sel_division = df_census.Division.unique()
if "All" in sel_state:
    sel_state = df_census.State.unique()
if "All" in sel_sex:
    sel_sex = df_census.Sex.unique()
if "All" in sel_origin:
    sel_origin = df_census.Origin.unique()
if "All" in sel_race:
    sel_race = df_census.Race.unique()
if "All" in sel_race_origin:
    sel_race_origin = df_census.Race_and_Origin.unique()
if "All" in sel_age_group:
    sel_age_group = df_census.Age_Group.unique()


#---------------------------------------------------------------------------------------
#DATA MANIPULATION AND FILTERING
df_census_copy = df_census

df_census_copy = df_census_copy.loc[df_census_copy['Region'].isin(sel_region)]
df_census_copy = df_census_copy.loc[df_census_copy['Division'].isin(sel_division)]
df_census_copy = df_census_copy.loc[df_census_copy['State'].isin(sel_state)]
df_census_copy = df_census_copy.loc[df_census_copy['Sex'].isin(sel_sex)]
df_census_copy = df_census_copy.loc[df_census_copy['Origin'].isin(sel_origin)]
df_census_copy = df_census_copy.loc[df_census_copy['Race'].isin(sel_race)]
df_census_copy = df_census_copy.loc[df_census_copy['Race_and_Origin'].isin(sel_race_origin)]
df_census_copy = df_census_copy.loc[df_census_copy['Age_Group'].isin(sel_age_group)]

df_census_copy_unpivoted = df_census_copy.melt(id_vars=['Region', 'Division', 'State', 'Age_Group','Sex', 'Race_and_Origin','Race', 'Origin'], var_name='Population_Year', value_name='Population')
line_break = '''---'''

#---------------------------------------------------------------------------------------
#SUMMARY
#st.write('States selected are:' , sel_state)
growth = df_census_copy['Population_2020'].sum()/df_census_copy['Population_2010'].sum()-1
percentage_growth = "{:.1%}".format(growth)

st.header('US Census Data Summary')
st.write('**2010 Population:**', str(int(df_census_copy['Population_2010'].sum()/1e6)),' M')
st.write('**2020 Population:**', str(int(df_census_copy['Population_2020'].sum()/1e6)),' M', '(growth rate was:', percentage_growth, ')' )
st.markdown(line_break)

#---------------------------------------------------------------------------------------
#CHARTS
#---------------------------------------------------------------------------------------
#CHARTS-REGION
df_region_population = df_census_copy.groupby(['Region']).sum().reset_index()
df_region_population['pop_growth'] = df_region_population['Population_2020']/df_region_population['Population_2010']-1


bar_region_population = alt.Chart(df_region_population, title = '2020 Population by Region').mark_bar().encode(
    x = alt.X('Region:O', axis=alt.Axis(title='Census Region'), sort=['South', 'West', 'Midwest', 'North']),
    y = alt.Y('Population_2020', axis = alt.Axis( title= '2020 Population', format ='~s')),
    tooltip=['Region', alt.Tooltip('Population_2020', format='.3s', title='Pop. 2020') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2010')]
).properties(width=600)

line_region_population = alt.Chart(df_region_population).mark_line(stroke='#FFA500', interpolate='monotone', point=alt.OverlayMarkDef(color="orange")).encode(
    alt.X('Region:O', axis=alt.Axis(title='Census Region'), sort=['South', 'West', 'Midwest', 'North']),
    alt.Y('pop_growth',axis=alt.Axis(title='Growth Rate 2010 to 2010', titleColor='#FFA500', format='%')),
    tooltip=['Region', alt.Tooltip('Population_2020', format='.3s', title='Pop. 2020') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2010')]
).properties(width=600)


df_region_population_hispanic = df_census_copy.groupby(['Region','Origin']).sum().reset_index()
df_region_population_hispanic['pop_growth'] = df_region_population_hispanic['Population_2020']/df_region_population_hispanic['Population_2010']-1

bar_region_population_hispanic = alt.Chart(df_region_population_hispanic, title = '2020 Hispanic Population by Region').mark_bar().encode(
    x = alt.X('Region:O', axis=alt.Axis(title='Census Region'), sort=['South', 'West', 'Midwest', 'North']),
    y = alt.Y('Population_2020', axis = alt.Axis( title= '2020 Population', format ='~s')),
    tooltip=['Region', 'Origin', alt.Tooltip('Population_2020', format='.3s', title='Pop. 2020') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2010')],
    color ='Origin'
).properties(width=700)

line_region_population_hispanic = alt.Chart(df_region_population_hispanic).mark_line(stroke='blue', interpolate='monotone', point=alt.OverlayMarkDef(color="blue")).encode(
    alt.X('Region:O', axis=alt.Axis(title='Census Region'), sort=['South', 'West', 'Midwest', 'North']),
    alt.Y('pop_growth',axis=alt.Axis(title='Growth Rate 2010 to 2010', titleColor='blue', format='%'),scale=alt.Scale(domain=[-0.1, 0.3]) ),
    tooltip=['Region', 'Origin', alt.Tooltip('Population_2020', format='.3s', title='Pop. 2020') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2010')],
    color = 'Origin',
    strokeDash = 'Origin'
).properties(width=700)

st.altair_chart(alt.layer(bar_region_population, line_region_population).resolve_scale(y = 'independent'))
st.altair_chart(alt.layer(bar_region_population_hispanic, line_region_population_hispanic).resolve_scale(y = 'independent'))

#st.write(df_region_population_hispanic )


st.markdown(line_break)

#---------------------------------------------------------------------------------------
#CHARTS-STATE
df_state_population = df_census_copy.groupby(['State']).sum().reset_index()
df_state_population['pop_growth'] = df_state_population['Population_2020']/df_state_population['Population_2010']-1
#df_state_population['Population_2020_numerize'] = num.numerize(df_state_population['Population_2020']*1.0)

df_state_population_sorted = df_state_population.sort_values(by=['Population_2020'], ascending=False).reset_index(drop=True)

#num_states = df_state_population_sorted['State'].value_counts()
#num_states = df_state_population_sorted['State'].unique()
#st.write(num_states.dtypes)
#st.write(num_states)

bar_state_population = alt.Chart(df_state_population_sorted, title = '2020 Population by State').mark_bar().encode(
    x = alt.X('State:O', axis=alt.Axis(title='State'), sort = None),
    y = alt.Y('Population_2020', axis = alt.Axis( title= '2020 Population', format ='~s')),
    tooltip=['State', alt.Tooltip('Population_2020', format='.3s', title='Pop. 2020') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2010')]
).properties(width=600)

line_state_population = alt.Chart(df_state_population_sorted).mark_line(stroke='#FFA500', interpolate='monotone', point=alt.OverlayMarkDef(color="orange")).encode(
    alt.X('State:O', axis=alt.Axis(title='State'), sort = None),
    alt.Y('pop_growth',axis=alt.Axis(title='Growth Rate 2010 to 2010', titleColor='#FFA500', format='%')),
    tooltip=['State', alt.Tooltip('Population_2020', format='.3s', title='Pop. 2020') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2010')]
).properties(width=600)

st.altair_chart(alt.layer(bar_state_population, line_state_population).resolve_scale(y = 'independent'))

bubble_state_population = alt.Chart(df_state_population_sorted, title = 'Population and Growth by State (between 2010 and 2020) ').mark_point(filled=True, opacity=0.5).encode(
    alt.X('Population_2010', axis = alt.Axis( title= '2010 Population', format = '~s')),
    alt.Y('pop_growth', axis = alt.Axis( title= 'Growth Rate 2010 to 2010', format='%')),
    size='Population_2020',
    color ='State',
    tooltip = ['State', alt.Tooltip('Population_2020', format='.3s', title ='Pop. 2020'), alt.Tooltip('Population_2010', format='.3s', title ='Pop. 2010'), alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2010')]
).properties(height=400,width=700).interactive()

st.altair_chart(bubble_state_population)

st.markdown(line_break)

#---------------------------------------------------------------------------------------
#CHARTS-AGE GROUP
df_age_group_population = df_census_copy.groupby(['Age_Group', 'Race_and_Origin']).sum().reset_index()
df_age_group_population['pop_growth'] = df_age_group_population['Population_2020']/df_age_group_population['Population_2010']-1
stacked_bar_age_race_origin = alt.Chart(df_age_group_population, title = '2020 Population by Age Group').mark_bar().encode(
    x=alt.X('Age_Group', axis = alt.Axis( title= 'Age Group')),
    y=alt.Y('Population_2020', axis = alt.Axis( title= '2020 Population', format = '~s')),
    color=alt.Color('Race_and_Origin', legend=alt.Legend(title='Race and Origin')),
    tooltip=[alt.Tooltip('Age_Group', title = 'Age Group'), alt.Tooltip('Race_and_Origin', title='Race and Origin'),alt.Tooltip('Population_2020', format ='.3s', title='Pop. 2020') ]
).properties(width=700)


area_age_race_origin = alt.Chart(df_age_group_population, title = '2020 Population by Age Group').mark_area().encode(
    x=alt.X('Age_Group', axis = alt.Axis( title= 'Age Group')),
    y=alt.Y('Population_2020', stack="normalize", axis = alt.Axis( title= '2020 Population', format ='%')),
    color=alt.Color('Race_and_Origin', legend=alt.Legend(title='Race and Origin')),
    tooltip=[alt.Tooltip('Age_Group', title = 'Age Group'), alt.Tooltip('Race_and_Origin', title='Race and Origin'),alt.Tooltip('Population_2020', format ='.3s', title='Pop. 2020') ]
).properties(width=700)

st.altair_chart(stacked_bar_age_race_origin)
st.altair_chart(area_age_race_origin)
st.markdown(line_break)


#---------------------------------------------------------------------------------------
#CHARTS-RACE AND ORIGIN
df_race_origin_population = df_census_copy.groupby(['Race_and_Origin']).sum().reset_index()
df_race_origin_population['pop_growth'] = df_race_origin_population['Population_2020']/df_race_origin_population['Population_2010']-1
df_race_origin_population_unpivoted = df_census_copy_unpivoted.groupby(['Race_and_Origin','Population_Year']).sum().reset_index()
df_race_origin_population_unpivoted['Year'] = df_race_origin_population_unpivoted['Population_Year'].str[11:15]
df_race_origin_population_unpivoted['Race_and_Origin_v2'] = np.where(df_race_origin_population_unpivoted['Race_and_Origin']!= 'White - Not Hispanic', 'Multicultural Consumers', 'White - Not Hispanic')
df_race_origin_population_unpivoted = df_race_origin_population_unpivoted.groupby(['Race_and_Origin_v2','Year']).sum().reset_index()
df_race_origin_population_unpivoted_2010 = df_race_origin_population_unpivoted.where(df_race_origin_population_unpivoted['Year']=='2010')
df_race_origin_population_unpivoted_2010 = df_race_origin_population_unpivoted_2010.dropna()
df_race_origin_population_unpivoted_2020 = df_race_origin_population_unpivoted.where(df_race_origin_population_unpivoted['Year']=='2020')
df_race_origin_population_unpivoted_2020 = df_race_origin_population_unpivoted_2020.dropna()


area_age_race_origin_time = alt.Chart(df_race_origin_population_unpivoted, title = 'Population Trend by Race and Origin').mark_area().encode(
    x=alt.X('Year', axis = alt.Axis( title= 'Year')),
    y=alt.Y('Population', axis = alt.Axis( title= 'Population')),
   color=alt.Color('Race_and_Origin_v2', legend=alt.Legend(title='Race and Origin'), scale=alt.Scale(
            range=['#b3b3b3', '#54A24B'])),
    tooltip=[alt.Tooltip('Year', title = 'Year'), alt.Tooltip('Race_and_Origin_v2', title='Race and Origin'),alt.Tooltip('Population', format ='.3s', title='Population') ]
).properties(width=600)

base_2010_pop = alt.Chart(df_race_origin_population, title = 'Population by Race and Origin in 2010').encode(
     theta=alt.Theta("Population_2010:Q", stack=True, sort='ascending'), color=alt.Color("Race_and_Origin:N", legend=alt.Legend(title="Race and Origin"))
)
pie_2010_pop = base_2010_pop.mark_arc(outerRadius=150, innerRadius = 70).properties(width=600, height = 400)
text_2010_pop = base_2010_pop.mark_text(radius=170, size=10).encode(alt.Text("Population_2010", format ='.3s')).properties(width=600, height = 400)

base_2010_pop_tot = alt.Chart(df_race_origin_population_unpivoted_2010).encode(
    theta=alt.Theta("sum(Population):Q")
    #, color=alt.Color("Race_and_Origin_v2:N")
)
pie_2010_pop_tot = base_2010_pop_tot.mark_arc(outerRadius=69, color = 'beige').properties(width=600, height = 400)
text_2010_pop_tot = base_2010_pop_tot.mark_text(radius=0, size=10, color = 'black').encode(alt.Text("sum(Population)", format ='.3s')).properties(width=600, height = 400)



base_2020_pop = alt.Chart(df_race_origin_population, title = 'Population by Race and Origin in 2020').encode(
    theta=alt.Theta("Population_2020:Q", stack=True, sort='ascending'), color=alt.Color("Race_and_Origin:N", legend=alt.Legend(title="Race and Origin"))
)
pie_2020_pop = base_2020_pop.mark_arc(outerRadius=150, innerRadius = 70).properties(width=600, height = 400)
text_2020_pop = base_2020_pop.mark_text(radius=170, size=10).encode(alt.Text("Population_2020", format ='.3s')).properties(width=600, height = 400)

base_2020_pop_tot = alt.Chart(df_race_origin_population_unpivoted_2020).encode(
    theta=alt.Theta("sum(Population):Q")
    #, color=alt.Color("Race_and_Origin_v2:N")
)
pie_2020_pop_tot = base_2020_pop_tot.mark_arc(outerRadius=69, color = 'beige').properties(width=600, height = 400)
text_2020_pop_tot = base_2020_pop_tot.mark_text(radius=0, size=10, color = 'black').encode(alt.Text("sum(Population)", format ='.3s')).properties(width=600, height = 400)


st.altair_chart(area_age_race_origin_time)
st.altair_chart(pie_2010_pop + text_2010_pop + pie_2010_pop_tot + text_2010_pop_tot)
st.altair_chart(pie_2020_pop + text_2020_pop + pie_2020_pop_tot + text_2020_pop_tot)

st.markdown(line_break)

#---------------------------------------------------------------------------------------
#END

#loom_video_5 = '<div style="position: relative; padding-bottom: 66.66666666666666%; height: 0;"><iframe src="https://www.loom.com/embed/bc1e95bd09aa4281a389fe027ae2b035" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>'
#st.markdown(loom_video_5, unsafe_allow_html=True)

