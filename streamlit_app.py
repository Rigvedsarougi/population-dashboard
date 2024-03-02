import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Function to make heatmap
def make_heatmap(input_df, input_x, input_y, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
        x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        color=alt.Color(f'{input_color}:Q',
                        legend=None,
                        scale=alt.Scale(scheme=input_color_theme)),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25),
    ).properties(width=900).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    )
    return heatmap

# Function to make bar chart
def make_bar_chart(input_df, input_x, input_y):
    bar_chart = alt.Chart(input_df).mark_bar().encode(
        x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        y=alt.Y(f'{input_y}:Q', axis=alt.Axis(title="Count", titleFontSize=18, titlePadding=15, titleFontWeight=900))
    ).properties(width=700)
    return bar_chart

# Function to make pie chart
def make_pie_chart(input_df, input_column):
    pie_chart = alt.Chart(input_df).mark_arc().encode(
        color=alt.Color(f'{input_column}:O', legend=None),
        theta='count()'
    ).properties(width=350, height=350)
    return pie_chart

# Main panel
def main():
    st.sidebar.title('🏂 Dynamic Dashboard')
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Load data
        df = pd.read_csv(uploaded_file)

        # Sidebar selections
        selected_columns = st.sidebar.multiselect('Select Columns', list(df.columns), default=[df.columns[0]])
        selected_chart_type = st.sidebar.selectbox('Select Chart Type', ['Heatmap', 'Bar Chart', 'Pie Chart'])
        selected_color_theme = st.sidebar.selectbox('Select a color theme', ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis'])

        # Display data
        st.subheader("Preview Data")
        st.write(df[selected_columns].head())

        # Display visualization
        st.subheader("Visualization")

        if selected_chart_type == 'Heatmap':
            if len(selected_columns) >= 3:
                st.write(make_heatmap(df, input_x=selected_columns[0], input_y=selected_columns[1], input_color=selected_columns[2], input_color_theme=selected_color_theme))
            else:
                st.error("Heatmap requires at least three columns.")
        elif selected_chart_type == 'Bar Chart':
            if len(selected_columns) >= 2:
                st.write(make_bar_chart(df, input_x=selected_columns[0], input_y=selected_columns[1]))
            else:
                st.error("Bar Chart requires at least two columns.")
        elif selected_chart_type == 'Pie Chart':
            if len(selected_columns) >= 1:
                st.write(make_pie_chart(df, input_column=selected_columns[0]))
            else:
                st.error("Pie Chart requires at least one column.")

if __name__ == '__main__':
    main()
