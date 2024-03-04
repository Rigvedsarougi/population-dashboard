import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Function to make heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
        y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        color=alt.Color(f'max({input_color}):Q',
                        legend=None,
                        scale=alt.Scale(scheme=input_color_theme)),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25),
    ).properties(width=900).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )
    return heatmap

# Function to make choropleth map
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(input_df[input_column])),
                               scope="usa",
                               labels={'population':'Population'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth


# Function to calculate year-over-year population migrations
def calculate_population_difference(input_df, input_year):
    selected_year_data = input_df[input_df['year'] == input_year].reset_index()
    previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
    selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
    return selected_year_data

# Function to format population number
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

# Main panel
def main():
    st.sidebar.title('Dashboard')
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Load data
        df = pd.read_csv(uploaded_file)

        # Sidebar selections
        selected_year = st.sidebar.selectbox('Select a year', sorted(df.year.unique(), reverse=True))
        selected_color_theme = st.sidebar.selectbox('Select a color theme', ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis'])

        # Gains/Losses panel
        st.title('Dashboard')

        st.markdown('#### Gains/Losses')

        df_population_difference_sorted = calculate_population_difference(df, selected_year)

        first_state_name = df_population_difference_sorted.iloc[0]['states']
        first_state_population = format_number(df_population_difference_sorted.iloc[0]['population'])
        first_state_delta = format_number(df_population_difference_sorted.iloc[0]['population_difference'])
        st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)

        last_state_name = df_population_difference_sorted.iloc[-1]['states']
        last_state_population = format_number(df_population_difference_sorted.iloc[-1]['population'])   
        last_state_delta = format_number(df_population_difference_sorted.iloc[-1]['population_difference'])   
        st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)

        # Total Population panel
        st.markdown('#### Total Population')

        choropleth = make_choropleth(df[df['year'] == selected_year], 'states_code', 'population', selected_color_theme)
        st.plotly_chart(choropleth, use_container_width=True)

        heatmap = make_heatmap(df, 'year', 'states', 'population', selected_color_theme)
        st.altair_chart(heatmap, use_container_width=True)

        # Top States panel
        st.markdown('#### Top States')

        df_selected_year = df[df.year == selected_year]
        df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)
        
        st.dataframe(df_selected_year_sorted[['states', 'population']],
                     width=None)

        st.markdown('''
                    - Utilizing U.S. Census Bureau data, the project examines migration patterns across states for a specific year, focusing on identifying states experiencing significant inbound and outbound migration.
                    - Through analysis, the project calculates the percentage of states with annual inbound and outbound migration, offering insights into overall migration trends within the United States.
                    - The project aims to understand the factors driving population movements and their implications for states' populations, economies, and social dynamics, ultimately contributing to informed policy discussions and decision-making processes.
                    ''')

        # Chatbot functionality
        st.sidebar.markdown('### Chatbot')

        question = st.sidebar.text_input('Ask me anything about the dashboard:')
        if question:
            if 'population' in question.lower():
                st.sidebar.write('The dashboard displays population-related information.')
            elif 'migration' in question.lower():
                st.sidebar.write('The dashboard includes information about population migration.')
            elif 'data source' in question.lower():
                st.sidebar.write('The data is sourced from the U.S. Census Bureau.')
            else:
                st.sidebar.write('I\'m sorry, I couldn\'t understand your question.')

if __name__ == '__main__':
    main()
