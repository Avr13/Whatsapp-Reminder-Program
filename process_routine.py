import pandas as pd
from datetime import datetime, timedelta

file_path = 'routine.xlsx'
task_comp_file = 'database\\task.xlsx'

class reg_routine:
    def load(self):
        df = pd.read_excel(file_path)
        
        rows_list = []

        for index, row in df.iterrows():
            time_value = self.__convert_to_today_time(row['Time'])
            if time_value>datetime.now(): 
                row_dict = {
                    'message_id': None,
                    'task': row['Task'],  
                    'start_time': time_value - timedelta(minutes=7),
                    'end_time': time_value + timedelta(minutes=7)
                }
                rows_list.append(row_dict)
                rows_list = sorted(rows_list, key=lambda x: x['start_time'])

        return rows_list
    
    def add_to_excel(self, data: dict):
        df = pd.read_excel(task_comp_file)
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_excel(task_comp_file, index=False)
    
    def __convert_to_today_time(self, time_str):
        today = datetime.now().date()
        time_obj = time_str.strftime('%H:%M:%S')
        time_obj = datetime.strptime(time_obj, '%H:%M:%S').time()
        return datetime.combine(today, time_obj)