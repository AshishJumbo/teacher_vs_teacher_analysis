import pandas as pd
import numpy as np

df = pd.read_csv("../data/problem_logs_with_teacher_assists_sept30.csv")

print(df.head())

print(df.columns)

# df['plta_start_time'] = pd.to_datetime(df['plta_start_time'], format='%Y-%m-%d %H:%M:%S.%f')
#
# print("-------------teacher assist policy id 4 started from : min time------------------")
# print(min(df['plta_start_time']))
# print(max(df['plta_start_time']))
# print("---------------------------------------------------------------------------------")

df_policy_4 = df.loc[df.teacher_assist_policy_id == 4]

df_policy_4.to_csv("../data/df_policy_4.csv")

print("------------------------data frame policy id 4 ---------------------------")
print(df_policy_4.shape)
# print(len(df_policy_4['user_id'].unique()))

print("------------------------data frame policy id 1,2,3,4 ---------------------------")
print(df.shape)