import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import io

sns.set(style='whitegrid')

task_comp_file = 'database\\task.xlsx'

figures = []

class graph:
    def generate(self):
        # Sample data
        df = pd.read_excel(task_comp_file)
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df['Date'] = df['Datetime'].dt.date
        
        self.status_vs_task_all(df)
        self.count_vs_status_today(df)
        self.status_vs_date(df)

        return figures

    def status_vs_task_all(self,df):
        # 1. Double bar graph for count of status of complete and incomplete for each task vs task name
        task_status_count = df.groupby(['Task', 'Status']).size().unstack(fill_value=0)

        fig = plt.figure(figsize=(10, 6))
        task_status_count.plot(kind='bar', stacked=False, ax=plt.gca(), color=['#FF9999', '#66B2FF'])
        plt.title('Count of Complete and Incomplete Tasks by Task Name', fontsize=16)
        plt.xlabel('Task', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        plt.legend(['Incomplete', 'Complete'], fontsize=12)
        plt.xticks(rotation=0, fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        figures.append(buf)
        plt.close(fig)
    
    def count_vs_status_today(self,df):
        # 2. Bar graph for today for count vs status of complete and incomplete
        today = datetime.now().date()
        today_status_count = df[df['Date'] == today]['Status'].value_counts().sort_index()

        fig = plt.figure(figsize=(8, 5))
        sns.barplot(x=today_status_count.index, y=today_status_count.values, palette=['#FF9999', '#66B2FF'])
        plt.title('Count of Complete and Incomplete Tasks for Today', fontsize=16)
        plt.xlabel('Status', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        plt.xticks(ticks=[0, 1], labels=['Incomplete', 'Complete'], fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        figures.append(buf)
        plt.close(fig)
    
    def status_vs_date(self,df):
       # 3. Line graph of each day count vs date
        daily_status_count = df.groupby(['Date', 'Status']).size().unstack(fill_value=0)

        fig = plt.figure(figsize=(10, 6))
        sns.lineplot(data=daily_status_count, markers=True, dashes=False)
        plt.title('Daily Task Completion Count', fontsize=16)
        plt.xlabel('Date', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        plt.legend(['Incomplete', 'Complete'], fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        figures.append(buf)
        plt.close(fig)


