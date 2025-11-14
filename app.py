import matplotlib.pyplot as plt
from shiny import App, render, ui
import pandas as pd

app_ui = ui.page_fluid(
    ui.output_plot("attendance_plot"),  
)

def server(input, output, session):
    @render.plot
    def attendance_plot():  
        df = pd.read_csv("DatascienceSummative1/attendance_anonymised-1.csv") 
        df = df.rename(columns={'Unit Instance Code': 'Module Code', 'Calocc Code': 'Year', 'Long Description': 'Module Name', 'Register Event ID': 'Event ID', 'Register Event Slot ID': 'Event Slot ID', 'Planned Start Date': 'Date', 'is Positive': 'Has Attended', 'Postive Marks': 'Attended', 'Negative Marks': 'Not Atteneded', 'Usage Code': 'Attendance Code'})
        df['Date']= pd.to_datetime(df['Date'])
        history_df = df[df['Module Name'] == 'History']
        fig = history_df.groupby(history_df['Date'].dt.date)['Attended'].mean().plot(kind="line", grid=True, title="Average Attendance for History Module Over Time", ylabel="Average Attendance", xlabel="Date", figsize=(10,6), marker='o')
        return fig
    




app = App(app_ui, server, debug=True)
