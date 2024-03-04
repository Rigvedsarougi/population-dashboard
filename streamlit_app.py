import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>
/* Add your CSS styling here */
</style>
""", unsafe_allow_html=True)

#######################
# Load data function
def load_data(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"An error occurred: {e}")

#######################
# Sidebar
st.sidebar.title('🏂 US Population Dashboard')

# File upload
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df_reshaped = load_data(uploaded_file)

    if df_reshaped is not None:
        year_list = list(df_reshaped.year.unique())[::-1]
        selected_year = st.sidebar.selectbox('Select a year', year_list)
        df_selected_year = df_reshaped[df_reshaped.year == selected_year]
        df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

        color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.sidebar.selectbox('Select a color theme', color_theme_list)

        #######################
        # Chatbot
        st.sidebar.subheader("Chatbot")

        # Define chatbot responses
        chat_responses = {
            "What is this data about?": "This data contains information about US population for different years.",
            "How many years of data are there?": f"There are {len(df_reshaped['year'].unique())} years of data.",
            # Add more responses as needed
        }

        # Chatbot input
        user_input = st.sidebar.text_input("Ask me anything")

        # Display chatbot response
        if user_input in chat_responses:
            st.sidebar.write("Chatbot:", chat_responses[user_input])
        elif user_input:
            st.sidebar.write("Chatbot: Sorry, I don't understand that question.")

        #######################
        # Dashboard Main Panel
        col = st.columns((1.5, 4.5, 2), gap='medium')

        with col[0]:
            st.markdown('#### Gains/Losses')

            df_population_difference_sorted = calculate_population_difference(df_reshaped, selected_year)

            if selected_year > 2010:
                first_state_name = df_population_difference_sorted.states.iloc[0]
                first_state_population = format_number(df_population_difference_sorted.population.iloc[0])
                first_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[0])
            else:
                first_state_name = '-'
                first_state_population = '-'
                first_state_delta = ''
            st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)

            if selected_year > 2010:
                last_state_name = df_population_difference_sorted.states.iloc[-1]
                last_state_population = format_number(df_population_difference_sorted.population.iloc[-1])   
                last_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[-1])   
            else:
                last_state_name = '-'
                last_state_population = '-'
                last_state_delta = ''
            st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)

            
            st.markdown('#### States Migration')

            if selected_year > 2010:
                # Filter states with population difference > 50000
                # df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference_absolute > 50000]
                df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference > 50000]
                df_less_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference < -50000]
                
                # % of States with population difference > 50000
                states_migration_greater = round((len(df_greater_50000)/df_population_difference_sorted.states.nunique())*100)
                states_migration_less = round((len(df_less_50000)/df_population_difference_sorted.states.nunique())*100)
                donut_chart_greater = make_donut(states_migration_greater, 'Inbound Migration', 'green')
                donut_chart_less = make_donut(states_migration_less, 'Outbound Migration', 'red')
            else:
                states_migration_greater = 0
                states_migration_less = 0
                donut_chart_greater = make_donut(states_migration_greater, 'Inbound Migration', 'green')
                donut_chart_less = make_donut(states_migration_less, 'Outbound Migration', 'red')

            migrations_col = st.columns((0.2, 1, 0.2))
            with migrations_col[1]:
                st.write('Inbound')
                st.altair_chart(donut_chart_greater)
                st.write('Outbound')
                st.altair_chart(donut_chart_less)

        with col[1]:
            st.markdown('#### Total Population')
            
            choropleth = make_choropleth(df_selected_year, 'states_code', 'population', selected_color_theme)
            st.plotly_chart(choropleth, use_container_width=True)
            
            heatmap = make_heatmap(df_reshaped, 'year', 'states', 'population', selected_color_theme)
            st.altair_chart(heatmap, use_container_width=True)
            

        with col[2]:
            st.markdown('#### Top States')

            st.dataframe(df_selected_year_sorted,
                         column_order=("states", "population"),
                         hide_index=True,
                         width=None,
                         column_config={
                            "states": st.column_config.TextColumn(
                                "States",
                            ),
                            "population": st.column_config.ProgressColumn(
                                "Population",
                                format="%f",
                                min_value=0,
                                max_value=max(df_selected_year_sorted.population),
                             )}
                         )
            
            with st.expander('About', expanded=True):
                st.write('''
                    - Data: [U.S. Census Bureau](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html).
                    - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
                    - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
                    ''')

    else:
        st.warning("Please upload a CSV file.")

else:
    st.info("Please upload a CSV file to get started.")
