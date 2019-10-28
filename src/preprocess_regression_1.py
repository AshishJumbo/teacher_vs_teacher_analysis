import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../data/main_df.csv")

print(df.columns)

print(len(df['user_id'].unique()))

df_policy_4 = df.loc[df.teacher_assist_policy_id == 4]
# df_policy_4 = df_policy_4.drop(
#     ['Unnamed: 0', 'teacher_assist_policy_id', 'ats_assigned_at', 'plta_assignment_id', 'plta_first_action',
#      'plta_attempt_count', 'plta_start_time', 'plta_end_time',
#      'plta_first_response_time', 'plid', 'pl_p_id', 'pl_n_id', 'pl_n_assignment_id', 'pl_n_first_action',
#      'pl_n_attempt_count', 'pl_n_start_time', 'pl_n_end_time',
#      'pl_n_first_response_time', 'pl_p_assignment_id', 'pl_p_first_action', 'pl_p_attempt_count', 'pl_p_start_time',
#      'pl_p_end_time', 'pl_p_first_response_time',
#      'pl_p_finished'], axis=1)
df_policy_4 = df_policy_4.drop(
    ['Unnamed: 0', 'teacher_assist_policy_id', 'ats_assigned_at', 'plta_first_action',
     'plta_attempt_count', 'plta_end_time', 'plta_first_response_time', 'plid', 'pl_p_id', 'pl_n_id',
     'pl_n_assignment_id', 'pl_n_first_action', 'pl_n_attempt_count', 'pl_n_start_time', 'pl_n_end_time',
     'pl_n_first_response_time', 'pl_p_assignment_id', 'pl_p_first_action', 'pl_p_attempt_count',
     'pl_p_end_time', 'pl_p_first_response_time', 'pl_p_finished'], axis=1)

# combine: plta_problem_id, pl_n_problem_id, pl_p_problem_id


# we only analyze next correct for nan becuase others should not be a nan period

df_policy_4.dropna(subset=['plta_problem_id', 'pl_n_problem_id', 'pl_p_problem_id', "pl_n_correct"], inplace=True)

# df_policy_4['plta_start_time'] = pd.to_datetime(df_policy_4['plta_start_time'], format='%Y-%m-%d %H:%M:%S.%f')
#
# print("-------------teacher assist policy id 4 started from : min time------------------")
# print(min(df_policy_4['plta_start_time']))
# print(max(df_policy_4['plta_start_time']))
# print("---------------------------------------------------------------------------------")

df_policy_4['prev_treat_next'] = df_policy_4[['plta_problem_id', 'pl_n_problem_id', 'pl_p_problem_id']].apply(
    lambda x: ','.join(x.dropna().astype(str)), axis=1)

print("------------------------data frame policy id 4 ---------------------------")
print(df_policy_4.shape)

print("-----------------------unique pre treatment and post count-------------------------------")
print(df_policy_4['prev_treat_next'].value_counts().nlargest(10))

count = df_policy_4['prev_treat_next'].value_counts()
# print("--------------------------counts above 25------------------------------")
# count = count[count > 25]
print("--------------------------counts above 1------------------------------")
count = count[count > 0]
print(count)
print("-----------------------------------------------------------------------")
print("count length ", count.size)
print("-----------------------------------------------------------------------")

print("unique combinations", df_policy_4['prev_treat_next'].unique().size)
print("-----------------------------------------------------------------------")

# df_policy_4 = df_policy_4[df_policy_4['prev_treat_next'].isin(count[count > 25].index)]
df_policy_4 = df_policy_4[df_policy_4['prev_treat_next'].isin(count[count > 0].index)]

print("-----------------------------------------------------------------------")
print("unique combinations", df_policy_4['prev_treat_next'].unique().size)
print("-----------------------------------------------------------------------")


df_policy_4_teacher_vs_teacher = df_policy_4.to_csv("../data/df_regression_1.csv")