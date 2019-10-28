import pandas as pd
import numpy as np

df = pd.read_csv("../data/main_df.csv")

print(df.columns)

df_policy_4 = df.loc[df.teacher_assist_policy_id == 4]
# df_policy_4 =df_policy_4.drop(['Unnamed: 0', 'teacher_assist_policy_id', 'ats_assigned_at', 'plta_assignment_id', 'plta_problem_id', 'plta_first_action', 'plta_attempt_count', 'plta_start_time', 'plta_end_time',
#        'plta_first_response_time', 'plid', 'pl_p_id', 'pl_n_id', 'pl_n_assignment_id', 'pl_n_problem_id', 'pl_n_first_action', 'pl_n_attempt_count', 'pl_n_start_time', 'pl_n_end_time',
#        'pl_n_first_response_time', 'pl_p_assignment_id', 'pl_p_problem_id',  'pl_p_first_action', 'pl_p_attempt_count', 'pl_p_start_time', 'pl_p_end_time', 'pl_p_first_response_time',
#        'pl_p_finished'], axis=1)
df_policy_4 = df_policy_4.drop(
    ['Unnamed: 0', 'teacher_assist_policy_id', 'ats_assigned_at', 'plta_assignment_id', 'plta_first_action',
     'plta_attempt_count', 'plta_start_time', 'plta_end_time',
     'plta_first_response_time', 'plid', 'pl_p_id', 'pl_n_id', 'pl_n_assignment_id', 'pl_n_first_action',
     'pl_n_attempt_count', 'pl_n_start_time', 'pl_n_end_time',
     'pl_n_first_response_time', 'pl_p_assignment_id', 'pl_p_first_action', 'pl_p_attempt_count', 'pl_p_start_time',
     'pl_p_end_time', 'pl_p_first_response_time',
     'pl_p_finished'], axis=1)

df_policy_4.fillna(-1)

print("------------------------data frame policy id 4 ---------------------------")
print(df_policy_4.shape)

unique_teacher_ids = df['ts_owner_id'].unique()

print("--------------------Teacher ids--------------------------")
print(unique_teacher_ids)

print("----------------------------------------------")
print(df_policy_4['ts_owner_id'].value_counts())
print("----------------------------------------------")

unique_pre_questions = df["pl_p_problem_id"].unique()
print("--------------------Pretest questions--------------------------")
print(unique_pre_questions)

print("----------------------------------------------")
print(df_policy_4['pl_p_problem_id'].value_counts())
print("----------------------------------------------")

unique_treatment_questions = df["plta_problem_id"].unique()
print("--------------------Pretest questions--------------------------")
print(unique_treatment_questions)

print("----------------------------------------------")
print(df_policy_4['plta_problem_id'].value_counts())
print("----------------------------------------------")

unique_post_questions = df["pl_n_problem_id"].unique()
print("--------------------Pretest questions--------------------------")
print(unique_post_questions)

print("----------------------------------------------")
print(df_policy_4['pl_n_problem_id'].value_counts())
print("----------------------------------------------")

df_teacher_sign_test_treatment = pd.DataFrame(columns=["teacher_id", "post_test", "pre_test", "+/-"])
df_teacher_sign_test = pd.DataFrame(columns=["teacher_id", "post_test", "pre_test", "+/-"])

for i in range(unique_teacher_ids.size):
    # df.loc[i] = [unique_teacher_ids[i]]+[0]+[0]+[0]
    df_teacher_sign_test = df_teacher_sign_test.append(
        {"teacher_id": unique_teacher_ids[i], "post_test": 0, "pre_test": 0, "+/-": 0}, ignore_index=True)
    df_teacher_sign_test_treatment = df_teacher_sign_test_treatment.append(
        {"teacher_id": unique_teacher_ids[i], "post_test": 0, "pre_test": 0, "+/-": 0}, ignore_index=True)


def extract_information_perTeacher_perTreatmentQuestion(teacher_id):
    df_teacher_specific = df_policy_4.loc[df_policy_4.ts_owner_id == teacher_id]
    pre_count = df_teacher_specific.pl_p_correct.value_counts()[1]
    post_count = df_teacher_specific.pl_n_correct.value_counts()[1]
    df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "pre_test"] = pre_count
    df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "post_test"] = post_count
    df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "+/-"] = (post_count - pre_count)

    df_teacher_specific = df_teacher_specific.loc[
        (df_teacher_specific.plta_hint_count > 0) | (df_teacher_specific.plta_bottom_hint > 0)]
    pre_count = df_teacher_specific.pl_p_correct.value_counts()[1]
    post_count = df_teacher_specific.pl_n_correct.value_counts()[1]
    df_teacher_sign_test_treatment.loc[df_teacher_sign_test_treatment.teacher_id == teacher_id, "pre_test"] = pre_count
    df_teacher_sign_test_treatment.loc[
        df_teacher_sign_test_treatment.teacher_id == teacher_id, "post_test"] = post_count
    df_teacher_sign_test_treatment.loc[df_teacher_sign_test_treatment.teacher_id == teacher_id, "+/-"] = (
                post_count - pre_count)


for val in unique_teacher_ids:
    extract_information_perTeacher_perTreatmentQuestion(val)

print("---------------That were in the treatment condition-------------------")
print(df_teacher_sign_test)
print("----------------That used the treatment condition---------------------")
print(df_teacher_sign_test_treatment)
