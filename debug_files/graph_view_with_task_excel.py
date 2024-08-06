import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import base64
from io import BytesIO

df = pd.read_excel("task.xlsx")


# Convert Datetime column to datetime type
df['Datetime'] = pd.to_datetime(df['Datetime'])

# Extract date part
df['Date'] = df['Datetime'].dt.date

# Set Seaborn style
sns.set(style='whitegrid')

def fig_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()
    return img_str

# 1. Double bar graph for count of status of complete and incomplete for each task vs task name
task_status_count = df.groupby(['Task', 'Status']).size().unstack(fill_value=0)

fig1 = plt.figure(figsize=(10, 6))
task_status_count.plot(kind='bar', stacked=False, ax=plt.gca(), color=['#FF9999', '#66B2FF'])
plt.title('Count of Complete and Incomplete Tasks by Task Name', fontsize=16)
plt.xlabel('Task', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.legend(['Incomplete', 'Complete'], fontsize=12)
plt.xticks(rotation=0, fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

# Convert to base64
graph1_base64 = fig_to_base64(fig1)

# 2. Bar graph for today for count vs status of complete and incomplete
today = datetime.now().date()
today_status_count = df[df['Date'] == today]['Status'].value_counts().sort_index()

fig2 = plt.figure(figsize=(8, 5))
sns.barplot(x=today_status_count.index, y=today_status_count.values, palette=['#FF9999', '#66B2FF'])
plt.title('Count of Complete and Incomplete Tasks for Today', fontsize=16)
plt.xlabel('Status', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.xticks(ticks=[0, 1], labels=['Incomplete', 'Complete'], fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()

# Convert to base64
graph2_base64 = fig_to_base64(fig2)

# 3. Line graph of each day count vs date
daily_status_count = df.groupby(['Date', 'Status']).size().unstack(fill_value=0)

fig3 = plt.figure(figsize=(10, 6))
sns.lineplot(data=daily_status_count, markers=True, dashes=False)
plt.title('Daily Task Completion Count', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.legend(['Incomplete', 'Complete'], fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()


# Convert to base64
graph3_base64 = fig_to_base64(fig3)

# Show the base64 strings
print(graph1_base64)
print(graph2_base64)
print(graph3_base64)
