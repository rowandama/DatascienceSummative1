import matplotlib.pyplot as plt
from shiny import App, render, ui, reactive 
import pandas as pd
import numpy as np 

app_ui = ui.page_fluid(
    ui.panel_title("University Module Attendance Dashboard"),
    ui.input_select(
        "module_select",
        "Select Module:",
        choices=[],
        selected=None 
    ),
    ui.output_plot("attendance_plot"),
)

def server(input, output, session):


    @reactive.Calc
    def get_data():
        df = pd.read_csv("DatascienceSummative1/attendance_anonymised-1.csv")
        df = df.rename(columns={
            'Unit Instance Code': 'Module Code',
            'Calocc Code': 'Year',
            'Long Description': 'Module Name',
            'Planned Start Date': 'Date',
            'Postive Marks': 'Attended'
        })
        df['Date'] = pd.to_datetime(df['Date'])
        return df

    @reactive.Effect
    @reactive.event(get_data)
    def update_module_choices():
        df = get_data()
        module_names = sorted(df['Module Name'].unique().tolist())

        ui.update_select(
            "module_select",
            choices=module_names,
            selected=module_names[0] if module_names else None
        )

    @render.plot
    def attendance_plot():
        df = get_data()
        selected_module = input.module_select()

        module_df = df[df['Module Name'] == selected_module].copy()
        fig, ax = plt.subplots(figsize=(10, 6))

        module_df.groupby(module_df['Date'].dt.date)['Attended'].mean().plot(
            kind="line",
            grid=True,
            title=f"Average Attendance for {selected_module} Over Time", 
            ylabel="Average Attendance",
            xlabel="Date",
            marker='o',
            ax=ax
        )

        return fig

app = App(app_ui, server, debug=True)