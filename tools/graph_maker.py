from tools import ifchelper
from matplotlib import pyplot as plt
import pandas as pd

style = {
    "figure.figsize": (8, 4.5),
    "axes.facecolor": (0.0, 0.0, 0.0, 0),
    "axes.edgecolor": "white",
    "axes.labelcolor": "white",
    "figure.facecolor": (0.0, 0.0, 0.0, 0),  # red with alpha = 30%
    "savefig.facecolor": (0.0, 0.0, 0.0, 0),
    "patch.edgecolor": "#0e1117",
    "text.color": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "white",
    "font.size": 12,
    "axes.labelsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
}

def get_elements_graph(file):
    types = ifchelper.get_types(file, "IfcBuildingElement")
    types_count = ifchelper.get_type_occurence(file, types)
    x_values, y_values = ifchelper.get_x_and_y(types_count)

    plt.rcParams.update(style)
    fig, ax = plt.subplots()
    bars = ax.bar(x_values, y_values, width=0.5, align="center", color="#B0B0B0", alpha=0.5)
    ax.set_title("Building Objects Count")
    ax.tick_params(color="#B0B0B0", rotation=90, labelsize="7", labelcolor="#B0B0B0")
    ax.tick_params(axis="x", rotation=90)
    ax.set_xlabel("Element Class")
    ax.set_ylabel("Count")
    ax.xaxis.label.set_color("#B0B0B0")
    ax.yaxis.label.set_color("#B0B0B0")

    ax.set_box_aspect(aspect=1 / 2)

    # Add numbers on the bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f'{int(height)}',
            ha='center',
            va='bottom',
            color='white',
            fontsize=10
        )

    ax.axis()
    return ax.figure

def get_high_frequency_entities_graph(file):
    types = ifchelper.get_types(file)
    types_count = ifchelper.get_type_occurence(file, types)
    x_values, y_values = ifchelper.get_x_and_y(types_count, 400)

    plt.rcParams.update(style)
    fig, ax = plt.subplots()
    bars = ax.bar(x_values, y_values, width=0.5, align="center", color="#B0B0B0", alpha=0.5)

    ax.set_title("IFC Entity Types Frequency")
    ax.tick_params(color="#B0B0B0", rotation=90, labelsize="7", labelcolor="#B0B0B0")
    ax.tick_params(axis="x", rotation=90)
    ax.set_xlabel("File Entities")
    ax.set_ylabel("No of Occurrences")
    ax.xaxis.label.set_color("#B0B0B0")
    ax.yaxis.label.set_color("#B0B0B0")

    ax.set_box_aspect(aspect=1 / 2)

    # Add numbers on the bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f'{int(height)}',
            ha='center',
            va='bottom',
            color='white',
            fontsize=10
        )

    ax.axis()
    return ax.figure

def load_graph(dataframe, quantity_set, quantity, user_option):
    import plotly.express as px
    if quantity != "Count":
        column_name = f"{quantity_set}.{quantity}"
        figure_pie_chart = px.pie(
            dataframe,
            names=user_option,
            values=column_name,
            color_discrete_sequence=px.colors.sequential.Greys
        )
    return figure_pie_chart




# def create_bar_chart(df, class_name, column_names):
#     # Filter the DataFrame by class_name
#     df_filtered = df[df['Class'] == class_name]

#     # Extract the counts of non-null values for each column
#     values = df_filtered[column_names].notna().sum()

#     # Create a bar chart
#     fig, ax = plt.subplots()
#     values.plot(kind='bar', ax=ax, color='blue')

#     # Set labels and title
#     ax.set_xlabel('Columns')
#     ax.set_ylabel('Count of Fulfilled Values')
#     ax.set_title(f'Distribution of Fulfilled Values for Class: {class_name}')

#     # Add labels to each bar
#     for i, v in enumerate(values):
#         ax.text(i, v + 0.1, str(v), ha='center', va='bottom')

#     return fig