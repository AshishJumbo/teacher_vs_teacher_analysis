import pandas as pd
import numpy as np

df = pd.read_csv("../data/problem_logs_with_teacher_assists_sept30.csv")

# the first 3 ids are for star teacher 1,2,3 which are test users ans the last is for Irene Wong
# which is the account for the summer scrub team
teacher_ids_todrop = [460570, 460571, 460572, 578208]
df = df[~df['ts_owner_id'].isin(teacher_ids_todrop)]

teacher_id_less_than_15 = [543489, 539153, 166406, 490219, 488943, 519775, 478214, 558127]
df = df[~df['ts_owner_id'].isin(teacher_id_less_than_15)]

print(df.head())

print(df.columns)

# df['plta_start_time'] = pd.to_datetime(df['plta_start_time'], format='%Y-%m-%d %H:%M:%S.%f')
#
# print("-------------teacher assist policy id 4 started from : min time------------------")
# print(min(df['plta_start_time']))
# print(max(df['plta_start_time']))
# print("---------------------------------------------------------------------------------")

# November 28 2018 was the first date teacher assist was ever run

df_policy_4 = df.loc[df.teacher_assist_policy_id == 4]

df_policy_4.to_csv("../data/main_df.csv")

print("------------------------data frame policy id 4 ---------------------------")
print(df_policy_4.shape)
# print(len(df_policy_4['user_id'].unique()))

print("------------------------data frame policy id 1,2,3,4 ---------------------------")
print(df.shape)


def drop_rename_columns(df_input):
    df_input = df_input.drop(['ts_owner_id', 'content_type', 'teacher_assist_policy_id', 'assigned_tutor_strategy_id',
                              'alternative_tutor_strategy_ids', 'ats_assigned_at', 'plta_assignment_id',
                              'plta_first_action',
                              'plta_attempt_count', 'plta_first_response_time', 'plta_finished', 'plid', 'pl_p_id',
                              'pl_n_id',
                              'pl_n_assignment_id', 'pl_n_problem_id', 'pl_n_correct', 'pl_n_first_action',
                              'pl_n_hint_count',
                              'pl_n_bottom_hint', 'pl_n_attempt_count', 'pl_n_start_time', 'pl_n_end_time',
                              'pl_n_first_response_time', 'pl_n_finished', 'pl_p_assignment_id', 'pl_p_problem_id',
                              'pl_p_correct',
                              'pl_p_first_action', 'pl_p_hint_count', 'pl_p_bottom_hint', 'pl_p_attempt_count',
                              'pl_p_start_time',
                              'pl_p_end_time', 'pl_p_first_response_time', 'pl_p_finished'], axis=1)
    df_input.rename(
        columns={"plta_problem_id": "problem_id", "plta_correct": "correct", "plta_hint_count": "hint_count",
                 "plta_bottom_hint": "bottom_hint", "plta_start_time": "start_time",
                 "plta_end_time": "end_time"}, inplace=True)
    return df_input


df_control = df.loc[df['assigned_tutor_strategy_id'] == 0]
# historical calculates the previous performance however as we add control as well we can have mode data for problem
# difficulty overall.
df_historical = pd.read_csv("../data/historical_problem_records.csv")
df_historical.append(drop_rename_columns(df_control), ignore_index=True, sort=True)
df_historical.to_csv("../data/historical_control_problem_records.csv")


# everything below was for other exploration, this is not important for regression analysis being done currently

# df_treatment = drop_rename_columns(df.loc[df['assigned_tutor_strategy_id'] != 0])
# df_treatment.to_csv("../data/historical_treatment_problem_records.csv")

# df_treatment['problem_avg'] = 0
#
#
# def calculate_avg(df_treat, pr_id, count):
#     count += 1
#     df_temp = df_treat.loc[df_treat['problem_id'] == pr_id]
#     average = 0
#     if len(df_temp.index) > 0:
#         average = df_temp.correct.mean()
#
#     df_treat.loc[df_treat['problem_id'] == pr_id, 'problem_avg'] = average
#     if count <= 5:
#         print(count, " the average for the problem id : ", pr_id, " is the average : ", average)
#
#
# unique_pr_id = df_treatment['problem_id'].unique()
# count = 0
# for unique_id in unique_pr_id:
#     count += 1
#     calculate_avg(df_treatment, unique_id, count)
#
# print("treatment average \n", df_treatment['problem_avg'].value_counts())

# df.dropna(inplace=True)
# unique_plp_id = df['pl_p_problem_id'].unique()
# unique_pln_id = df['pl_n_problem_id'].unique()
# unique_pla_id = df['plta_problem_id'].unique()
#
# unique_list = set(list(unique_plp_id) + list(unique_pla_id) + list(unique_pln_id))
#
# print(len(unique_list), ' length of unique list. ')
# np.savetxt("../data/problem_ids_in_TA_research.txt", list(unique_list), fmt='%i', delimiter=', ', newline=', ')
# np.savetxt("../data/problem_ids_in_TA_pre.txt", list(unique_list), fmt='%i', delimiter=', ', newline=', ')
# np.savetxt("../data/problem_ids_in_TA_next.txt", list(unique_list), fmt='%i', delimiter=', ', newline=', ')
# np.savetxt("../data/problem_ids_in_TA_treatment.txt", list(unique_list), fmt='%i', delimiter=', ', newline=', ')


# df_pre_treatment = df.loc[df['assigned_tutor_strategy_id'] != 0]
# df_pre_treatment = df_pre_treatment.drop(['ts_owner_id', 'content_type', 'teacher_assist_policy_id',
#                                           'assigned_tutor_strategy_id', 'alternative_tutor_strategy_ids',
#                                           'ats_assigned_at', 'plta_assignment_id', 'plta_first_action',
#                                           'plta_attempt_count', 'plta_first_response_time', 'plta_finished', 'plid',
#                                           'pl_p_id', 'pl_n_id', 'pl_n_assignment_id', 'pl_n_problem_id', 'pl_n_correct',
#                                           'pl_n_first_action', 'pl_n_hint_count', 'pl_n_bottom_hint',
#                                           'pl_n_attempt_count', 'pl_n_start_time', 'pl_n_end_time',
#                                           'pl_n_first_response_time', 'pl_n_finished', 'pl_p_assignment_id',
#                                           'plta_problem_id', 'plta_correct', 'pl_p_first_action', 'plta_hint_count',
#                                           'plta_bottom_hint', 'pl_p_attempt_count', 'plta_start_time',
#                                           'plta_end_time', 'pl_p_first_response_time', 'pl_p_finished'], axis=1)
# df_pre_treatment.rename(columns={"pl_p_problem_id": "problem_id", "pl_p_correct": "correct",
#                                  "pl_p_hint_count": "hint_count", "pl_p_bottom_hint": "bottom_hint",
#                                  "pl_p_start_time": "start_time", "pl_p_end_time": "end_time"
#                                  }, inplace=True)
#
# df_pre_treatment['problem_avg'] = 0
# unique_pr_id = df_pre_treatment['problem_id'].unique()
#
# count = 0
# for unique_id in unique_pr_id:
#     count += 1
#     calculate_avg(df_pre_treatment, unique_id, count)
#
# print("pre-treatment average \n", df_pre_treatment['problem_avg'].value_counts())
#
# df_post_treatment = df.loc[df['assigned_tutor_strategy_id'] != 0]
# df_post_treatment = df_post_treatment.drop(['ts_owner_id', 'content_type', 'teacher_assist_policy_id',
#                                             'assigned_tutor_strategy_id', 'alternative_tutor_strategy_ids',
#                                             'ats_assigned_at', 'plta_assignment_id', 'plta_first_action',
#                                             'plta_attempt_count', 'plta_first_response_time', 'plta_finished', 'plid',
#                                             'pl_p_id', 'pl_n_id', 'pl_n_assignment_id', 'pl_p_problem_id',
#                                             'pl_p_correct',
#                                             'pl_n_first_action', 'pl_p_hint_count', 'pl_p_bottom_hint',
#                                             'pl_n_attempt_count', 'pl_p_start_time', 'pl_p_end_time',
#                                             'pl_n_first_response_time', 'pl_n_finished', 'pl_p_assignment_id',
#                                             'plta_problem_id', 'plta_correct', 'pl_p_first_action', 'plta_hint_count',
#                                             'plta_bottom_hint', 'pl_p_attempt_count', 'plta_start_time',
#                                             'plta_end_time', 'pl_p_first_response_time', 'pl_p_finished'], axis=1)
# df_post_treatment.rename(columns={"pl_n_problem_id": "problem_id", "pl_n_correct": "correct",
#                                   "pl_n_hint_count": "hint_count", "pl_n_bottom_hint": "bottom_hint",
#                                   "pl_n_start_time": "start_time", "pl_n_end_time": "end_time"
#                                   }, inplace=True)
#
# df_post_treatment['problem_avg'] = 0
# unique_pr_id = df_post_treatment['problem_id'].unique()
# count = 0
# for unique_id in unique_pr_id:
#     count += 1
#     calculate_avg(df_post_treatment, unique_id, count)
#
# print("post-treatment average \n", df_post_treatment['problem_avg'].value_counts())
