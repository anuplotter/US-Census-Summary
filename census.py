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
import time as time

st.set_page_config(
     page_title="Multicultural Dashboard",
     page_icon="📋",
     #layout="wide",
     #initial_sidebar_state="expanded",
     #menu_items={'Get Help': 'https://www.extremelycoolapp.com/help','Report a bug': "https://www.extremelycoolapp.com/bug",'About': "# This is a header. This is an *extremely* cool app!"}
 )

time.sleep(1)

#HIDING STREAMLIT ELEMENTS
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# Formatting link: https://d3-wiki.readthedocs.io/zh_CN/master/Formatting/

#---------------------------------------------------------------------------------------
#READING RAW DATA
#url_census_updated = 'https://drive.google.com/file/d/1zcNMO5aAFt4CgERA9qzozuhQ1xR7pUpX/view?usp=sharing'
#url2='https://drive.google.com/uc?id=' + url_census_updated.split('/')[-2]
#df_census = pd.read_csv(url2)
df_census = pd.read_csv('census_updated.csv')

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

line_break = '''---'''

#---------------------------------------------------------------------------------------
#SUMMARY
growth = df_census_copy['Population_2020'].sum()/df_census_copy['Population_2010'].sum()-1
percentage_growth = "{:.1%}".format(growth)

#CONTENT FROM AL AND TEAM
st.markdown("<h1 style='text-align: center; color: black;'>Multicultural Dashboard</h1>", unsafe_allow_html=True)
#st.title('Multicultural Dashboard')
st.header('Quick Size Your Multicultural Business Opportunities!')
clients_ask = "***Our clients often ask us to help them size the business opportunity of U.S. Multicultural Markets - for U.S. Hispanic, African-American/Black, Asian, Multiracial and all others.***"
free_dash ="***Here's a free dashboard to help you start thinking about Multicultural markets. Use the dashboard for instant factoids into your target market's profile by ethnicity, race, age, gender, and geography... ***"
st.write(clients_ask, unsafe_allow_html=False)
st.write(free_dash, unsafe_allow_html=False)

from pathlib import Path
def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

dashboard_usage_markdown = read_markdown_file("dashboard_usage.md")
with st.expander("📖 Dashboard Usage Guide:"):
    st.markdown(dashboard_usage_markdown, unsafe_allow_html=True)


how_to_use = "**How to use:** ***To explore different scenarios by any of the variables listed in the Filters on the left of the page, select the dropdown arrows and choose what you would like to learn about. To reset, 'X' out your selection and then click 'All' in any of the Filter boxes. If you would like to save a chart, click the 3 dots in the upper right.***"
st.write(how_to_use, unsafe_allow_html=False)

whats_next = "**What's Next?** ***When you are [ready](https://www.preferenceanalytics.com/contact-us) to reach out to and connect with these growing markets, [Preference Analytics](https://www.preferenceanalytics.com/) can help you figure out the appropriate [brand positioning, marketing strategies, messaging and product development](https://www.preferenceanalytics.com/solutions) path.***"
st.write(whats_next, unsafe_allow_html=False)


st.markdown(line_break)

st.subheader('Total Population per US Census')
#st.write('**2010 Population:**', str(int(df_census_copy['Population_2010'].sum()/1e6)),' M')
#st.write('**2020 Population:**', str(int(df_census_copy['Population_2020'].sum()/1e6)),' M', '(growth rate was:', percentage_growth, ')' )

#col1, col2 = st.columns(2)
#col1.metric("2010", str(int(df_census_copy['Population_2010'].sum()/1e6))+ "M")
#col2.metric("2020", str(int(df_census_copy['Population_2020'].sum()/1e6))+ "M", percentage_growth)
#col3.metric("Growth (2010-2020)", percentage_growth, "")
#st.markdown(line_break)

col1, col2, col3 = st.columns(3)
col1.metric("2010", str(int(df_census_copy['Population_2010'].sum()/1e6))+ "M")
col2.metric("2020", str(int(df_census_copy['Population_2020'].sum()/1e6))+ "M", percentage_growth)
col3.metric("Change (2010 to 2020)", str(int((df_census_copy['Population_2020'].sum()-df_census_copy['Population_2010'].sum())/1e6))+ "M")
st.markdown(line_break)


#---------------------------------------------------------------------------------------
#CHARTS
#---------------------------------------------------------------------------------------
#CHARTS-REGION
st.subheader('Breakdown by Census Regions')

df_region_population = df_census_copy.groupby(['Region']).sum().reset_index()
df_region_population['pop_growth'] = df_region_population['Population_2020']/df_region_population['Population_2010']-1


bar_region_population = alt.Chart(df_region_population, title = '2020 Population by Census Region').mark_bar().encode(
    x = alt.X('Region:O', axis=alt.Axis(title='Census Region'), sort=['South', 'West', 'Midwest', 'North']),
    y = alt.Y('Population_2020', axis = alt.Axis( title= '2020 Population', format ='~s')),
    tooltip=['Region', alt.Tooltip('Population_2020', format='.3s', title='Pop. 2020') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2020')]
).properties(width=600)

line_region_population = alt.Chart(df_region_population).mark_line(stroke='#FFA500', interpolate='monotone', point=alt.OverlayMarkDef(color="orange")).encode(
    alt.X('Region:O', axis=alt.Axis(title='Census Region'), sort=['South', 'West', 'Midwest', 'North']),
    alt.Y('pop_growth',axis=alt.Axis(title='Growth Rate 2010 to 2020', titleColor='#FFA500', format='%')),
    tooltip=['Region', alt.Tooltip('Population_2020', format='.3s', title='Pop. 2020') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2020')]
).properties(width=600)


df_region_population_hispanic = df_census_copy.groupby(['Region','Origin']).sum().reset_index()
df_region_population_hispanic['pop_growth'] = df_region_population_hispanic['Population_2020']/df_region_population_hispanic['Population_2010']-1

bar_region_population_hispanic = alt.Chart(df_region_population_hispanic, title = '2020 Hispanic Population by Census Region').mark_bar().encode(
    x = alt.X('Region:O', axis=alt.Axis(title='Census Region'), sort=['South', 'West', 'Midwest', 'North']),
    y = alt.Y('Population_2020', axis = alt.Axis( title= '2020 Population', format ='~s')),
    tooltip=['Region', 'Origin', alt.Tooltip('Population_2020', format='.3s', title='Pop. 2020') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2020')],
    color ='Origin'
).properties(width=700)

line_region_population_hispanic = alt.Chart(df_region_population_hispanic).mark_line(stroke='blue', interpolate='monotone', point=alt.OverlayMarkDef(color="blue")).encode(
    alt.X('Region:O', axis=alt.Axis(title='Census Region'), sort=['South', 'West', 'Midwest', 'North']),
    alt.Y('pop_growth',axis=alt.Axis(title='Growth Rate 2010 to 2020', titleColor='blue', format='%'),scale=alt.Scale(domain=[-0.1, 0.3]) ),
    tooltip=['Region', 'Origin', alt.Tooltip('Population_2020', format='.3s', title='Pop. 2020') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2020')],
    color = 'Origin',
    strokeDash = 'Origin'
).properties(width=700)

st.altair_chart(alt.layer(bar_region_population, line_region_population).resolve_scale(y = 'independent'))
st.altair_chart(alt.layer(bar_region_population_hispanic, line_region_population_hispanic).resolve_scale(y = 'independent'))
st.markdown(line_break)

#---------------------------------------------------------------------------------------
#CHARTS-STATE
st.subheader('Trends by State')
df_state_population = df_census_copy.groupby(['State']).sum().reset_index()
df_state_population_sorted = df_state_population.sort_values(by=['Population_2020'], ascending=False).reset_index(drop=True)
df_state_population_sorted['State_v2'] = np.where(df_state_population_sorted.index <=25,df_state_population_sorted['State'],'Others - Avg.')
df_state_population_sorted['State_v2_rank'] = np.where(df_state_population_sorted.index <=25,df_state_population_sorted.index,26)
df_state_population_sorted = df_state_population_sorted.groupby(['State_v2','State_v2_rank']).mean().reset_index()
df_state_population_sorted = df_state_population_sorted.sort_values(by=['State_v2_rank'], ascending=True).reset_index(drop=True)
df_state_population_sorted['pop_growth'] = df_state_population['Population_2020']/df_state_population['Population_2010']-1

bar_state_population = alt.Chart(df_state_population_sorted, title = '2020 Population by State').mark_bar().encode(
    x = alt.X('State_v2:O', axis=alt.Axis(title='State'), sort = None),
    y = alt.Y('Population_2020', axis = alt.Axis( title= '2020 Population', format ='~s')),
    tooltip=[alt.Tooltip('State_v2', title='State'), alt.Tooltip('Population_2020', format='.3s', title='Pop. 2020') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2020')]
).properties(width=600)

line_state_population = alt.Chart(df_state_population_sorted).mark_line(stroke='#FFA500', interpolate='monotone', point=alt.OverlayMarkDef(color="orange")).encode(
    alt.X('State_v2:O', axis=alt.Axis(title='State'), sort = None),
    alt.Y('pop_growth',axis=alt.Axis(title='Growth Rate 2010 to 2020', titleColor='#FFA500', format='%')),
    tooltip=[alt.Tooltip('State_v2', title='State'), alt.Tooltip('Population_2020', format='.3s', title='Pop. 2020') ,alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2020')]
).properties(width=600)

st.altair_chart(alt.layer(bar_state_population, line_state_population).resolve_scale(y = 'independent'))

bubble_state_population = alt.Chart(df_state_population_sorted, title = 'Population and Growth by State (between 2010 and 2020) ').mark_point(filled=True, opacity=0.5).encode(
    alt.X('Population_2010', axis = alt.Axis( title= '2010 Population', format = '~s')),
    alt.Y('pop_growth', axis = alt.Axis( title= 'Growth Rate 2010 to 2020', format='%')),
    size=alt.Size('Population_2020', legend=alt.Legend(title='2020 Population')),
    color=alt.Color('State_v2', legend=alt.Legend(title='State')),
    tooltip = [alt.Tooltip('State_v2', title='State'), alt.Tooltip('Population_2020', format='.3s', title ='Pop. 2020'), alt.Tooltip('Population_2010', format='.3s', title ='Pop. 2010'), alt.Tooltip('pop_growth:Q', format='.1%', title='Growth Rate 2010 to 2020')]
).properties(height=500,width=700).interactive()

st.altair_chart(bubble_state_population)
st.markdown(line_break)

#---------------------------------------------------------------------------------------
#CHARTS-AGE GROUP
st.subheader('Changes by Age Group')
df_age_group_population = df_census_copy.groupby(['Age_Group', 'Race_and_Origin']).sum().reset_index()
#df_age_group_population = df_census_copy.groupby(['Age_Group', 'Race_and_Origin','Race_and_Origin_rank']).sum().reset_index()
#df_age_group_population = df_age_group_population.sort_values(by=['Race_and_Origin_rank'], ascending=True).reset_index(drop=True)
df_age_group_population['pop_growth'] = df_age_group_population['Population_2020']/df_age_group_population['Population_2010']-1
stacked_bar_age_race_origin = alt.Chart(df_age_group_population, title = '2020 Population (# of people) by Age Group').mark_bar().encode(
    x=alt.X('Age_Group', axis = alt.Axis( title= 'Age Group')),
    y=alt.Y('Population_2020', axis = alt.Axis( title= '2020 Population', format = '~s')),
    color=alt.Color('Race_and_Origin', legend=alt.Legend(title='Race and Origin')),
    tooltip=[alt.Tooltip('Age_Group', title = 'Age Group'), alt.Tooltip('Race_and_Origin', title='Race and Origin'),alt.Tooltip('Population_2020', format ='.3s', title='Pop. 2020') ]
).properties(width=700)


area_age_race_origin = alt.Chart(df_age_group_population, title = '2020 Percentage of the Population by Age Group').mark_area().encode(
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
st.subheader('Distribution by Race and Origin')
df_race_origin_population = df_census_copy.groupby(['Race_and_Origin']).sum().reset_index()
df_race_origin_population['pop_growth'] = df_race_origin_population['Population_2020']/df_race_origin_population['Population_2010']-1

df_census_copy_unpivoted = df_census_copy.melt(id_vars=['Region', 'Division', 'State', 'Age_Group','Sex', 'Race_and_Origin','Race_and_Origin_rank','Race', 'Origin'], var_name='Population_Year', value_name='Population')
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
    y=alt.Y('Population', axis = alt.Axis( title= 'Population', format = '~s')),
   color=alt.Color('Race_and_Origin_v2', legend=alt.Legend(title='Race and Origin'), scale=alt.Scale(
            range=['#b3b3b3', '#54A24B'])),
    tooltip=[alt.Tooltip('Year', title = 'Year'), alt.Tooltip('Race_and_Origin_v2', title='Race and Origin'),alt.Tooltip('Population', format ='.3s', title='Population') ]
).properties(width=700)

base_2010_pop = alt.Chart(df_race_origin_population, title = 'Population by Race and Origin in 2010').encode(
     theta=alt.Theta("Population_2010:Q", stack=True, sort='ascending'), color=alt.Color("Race_and_Origin:N", legend=alt.Legend(title="Race and Origin"))
)
pie_2010_pop = base_2010_pop.mark_arc(outerRadius=150, innerRadius = 70).properties(width=700, height = 400)
text_2010_pop = base_2010_pop.mark_text(radius=170, size=10).encode(alt.Text("Population_2010", format ='.3s')).properties(width=700, height = 400)

base_2010_pop_tot = alt.Chart(df_race_origin_population_unpivoted_2010).encode(
    theta=alt.Theta("sum(Population):Q")
    #, color=alt.Color("Race_and_Origin_v2:N")
)
pie_2010_pop_tot = base_2010_pop_tot.mark_arc(outerRadius=69, color = 'beige').properties(width=700, height = 400)
text_2010_pop_tot = base_2010_pop_tot.mark_text(radius=0, size=10, color = 'black').encode(alt.Text("sum(Population)", format ='.3s')).properties(width=700, height = 400)



base_2020_pop = alt.Chart(df_race_origin_population, title = 'Population by Race and Origin in 2020').encode(
    theta=alt.Theta("Population_2020:Q", stack=True, sort='ascending'), color=alt.Color("Race_and_Origin:N", legend=alt.Legend(title="Race and Origin"))
)
pie_2020_pop = base_2020_pop.mark_arc(outerRadius=150, innerRadius = 70).properties(width=700, height = 400)
text_2020_pop = base_2020_pop.mark_text(radius=170, size=10).encode(alt.Text("Population_2020", format ='.3s')).properties(width=700, height = 400)

base_2020_pop_tot = alt.Chart(df_race_origin_population_unpivoted_2020).encode(
    theta=alt.Theta("sum(Population):Q")
    #, color=alt.Color("Race_and_Origin_v2:N")
)
pie_2020_pop_tot = base_2020_pop_tot.mark_arc(outerRadius=69, color = 'beige').properties(width=700, height = 400)
text_2020_pop_tot = base_2020_pop_tot.mark_text(radius=0, size=10, color = 'black').encode(alt.Text("sum(Population)", format ='.3s')).properties(width=700, height = 400)


st.altair_chart(area_age_race_origin_time)
st.altair_chart(pie_2010_pop + text_2010_pop + pie_2010_pop_tot + text_2010_pop_tot)
st.altair_chart(pie_2020_pop + text_2020_pop + pie_2020_pop_tot + text_2020_pop_tot)

#---------------------------------------------------------------------------------------
#EXCEL DASHBOARD BY PLOT-AI
st.write('Want this in Excel? Download 👇, signup and install add-in by [**Plot-AI**] (https://plot-ai.com/)')
with open('Multicultural Dashboard US Census.xlsm', 'rb') as f:
   st.download_button('💾 Excel US Census Dashboard', f, file_name='Multicultural Dashboard US Census.xlsm')  # Defaults to 'application/octet-stream'
#---------------------------------------------------------------------------------------
#END

