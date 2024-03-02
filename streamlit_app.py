import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

# Function to detect column types
def detect_column_types(df):
    column_types = {}
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            column_types[column] = 'numeric'
        elif pd.api.types.is_string_dtype(df[column]):
            column_types[column] = 'categorical'
        else:
            column_types[column] = 'other'
    return column_types

# Function to make heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
        y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
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
def make_bar_chart(input_df, x_column, y_column):
    bar_chart = alt.Chart(input_df).mark_bar().encode(
        x=x_column,
        y=y_column
    ).properties(width=700)
    return bar_chart

# Function to make pie chart
def make_pie_chart(input_df, category_column):
    pie_chart = alt.Chart(input_df).mark_arc().encode(
        color=category_column,
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

        # Detect column types
        column_types = detect_column_types(df)

        # Display column types
        st.sidebar.subheader("Detected Column Types")
        for column, ctype in column_types.items():
            st.sidebar.write(f"{column}: {ctype}")

        # Sidebar selections
        selected_columns = st.sidebar.multiselect('Select Columns', list(df.columns), default=list(df.columns)[:2])
        selected_chart_type = st.sidebar.selectbox('Select Chart Type', ['Heatmap', 'Bar Chart', 'Pie Chart'])
        selected_color_theme = st.sidebar.selectbox('Select a color theme', ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis'])

        # Display data
        st.subheader("Preview Data")
        st.write(df[selected_columns].head())

        # Display visualization
        st.subheader("Visualization")

        if selected_chart_type == 'Heatmap':
            st.write(make_heatmap(df, selected_columns[0], selected_columns[1], selected_columns[0], selected_color_theme))
        elif selected_chart_type == 'Bar Chart':
            st.write(make_bar_chart(df, x_column=selected_columns[0], y_column=selected_columns[1]))
        elif selected_chart_type == 'Pie Chart' and column_types[selected_columns[0]] == 'categorical':
            st.write(make_pie_chart(df, category_column=selected_columns[0]))
        else:
            st.error("Invalid chart type or column selection.")

if __name__ == '__main__':
    main()
