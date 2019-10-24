# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
#
# df = pd.read_csv("../data/df_policy_4.csv")
#
# print(df.columns)
#
# df_policy_4 = df.loc[df.teacher_assist_policy_id == 4]
# df_policy_4 = df_policy_4.drop(
#     ['Unnamed: 0', 'teacher_assist_policy_id', 'ats_assigned_at', 'plta_assignment_id', 'plta_first_action',
#      'plta_attempt_count', 'plta_start_time', 'plta_end_time',
#      'plta_first_response_time', 'plid', 'pl_p_id', 'pl_n_id', 'pl_n_assignment_id', 'pl_n_first_action',
#      'pl_n_attempt_count', 'pl_n_start_time', 'pl_n_end_time',
#      'pl_n_first_response_time', 'pl_p_assignment_id', 'pl_p_first_action', 'pl_p_attempt_count', 'pl_p_start_time',
#      'pl_p_end_time', 'pl_p_first_response_time',
#      'pl_p_finished'], axis=1)
#
# print("------------------------data frame policy id 4 ---------------------------")
# print(df_policy_4.shape)
#
#
# def get_Unique_info(column_name):
#     unique_instances = df_policy_4[column_name].unique()
#     # print("------------" + column_name + "--------------------")
#     # print(unique_instances)
#     print("--------more info on" + column_name + "------------")
#     print(df_policy_4[column_name].value_counts())
#     return unique_instances
#
# # trying to find a correlation between columns using heatmap
# # corr = df_policy_4.corr()
# # sns.heatmap(corr,
# #         xticklabels=corr.columns,
# #         yticklabels=corr.columns)
# # plt.show()
# # end of heatmaps exploring
#
#
# print(df_policy_4.shape)
# # df_policy_4 = df_policy_4.groupby('pl_p_problem_id').filter(
# #     lambda x: len(x) > 5)  # 5 is just an arbitrary number that I picked
# df_policy_4 = df_policy_4.groupby('plta_problem_id').filter(
#     lambda x: len(x) > 5)  # should I have done this for the treatment condition only
# # df_policy_4 = df_policy_4.groupby('pl_n_problem_id').filter(lambda x: len(x) > 5)
# print(df_policy_4.shape)
#
# unique_teacher_ids = get_Unique_info('ts_owner_id')
# pre_problem_ids = get_Unique_info('pl_p_problem_id')
# treatment_problem_ids = get_Unique_info('plta_problem_id')
# post_problem_ids = get_Unique_info('pl_n_problem_id')
#
# def find_avg_question_score(unique_id, column_name, avg_col):
#     # print("-----------------", unique_id, "-------------------------")
#     # print(df_policy_4.loc[df_policy_4[column_name] == unique_id]["plta_correct"].value_counts())
#     mean = df_policy_4.loc[(df_policy_4[column_name] == unique_id)]["plta_correct"].mean()
#     df_policy_4.loc[df_policy_4[column_name] == unique_id, avg_col] = mean
#     # print(mean, "mean for ", unique_id)
#     # df_policy_4_temp = df_policy_4.loc[df_policy_4[column_name] == unique_id]
#
#
# df_policy_4["avg_p_score_question"] = 0
# df_policy_4["avg_a_score_question"] = 0
# df_policy_4["avg_n_score_question"] = 0
# def calculate_the_average(ids, column_name, avg_for_column):
#     for val in ids:
#         find_avg_question_score(val, column_name, avg_for_column)
#
#
# calculate_the_average(pre_problem_ids, "pl_p_problem_id", "avg_p_score_question")
# calculate_the_average(treatment_problem_ids, "plta_problem_id", "avg_a_score_question")
# calculate_the_average(post_problem_ids, "pl_n_problem_id", "avg_n_score_question")
#
# avg_p_score = df_policy_4["avg_p_score_question"].unique()
# avg_a_score = df_policy_4["avg_a_score_question"].unique()
# avg_n_score = df_policy_4["avg_n_score_question"].unique()
# print("average pre score", len(avg_p_score))
# print("average treatment score", len(avg_a_score))
# print("average post score", len(avg_n_score))
#
#
#
# df_teacher_sign_test_treatment = pd.DataFrame(columns=["teacher_id", "post_test", "pre_test", "+/-"])
# df_teacher_sign_test = pd.DataFrame(columns=["teacher_id", "post_test", "pre_test", "+/-"])
#
# for i in range(unique_teacher_ids.size):
#     # df.loc[i] = [unique_teacher_ids[i]]+[0]+[0]+[0]
#     # for j in range(pre_problem_ids.size):
#     #     print(pre_problem_ids)
#     # for k in range(treatmentimageimage_problem_ids.size):
#     #     print(treatment_problem_ids)
#     # for l in range(post_problem_ids.size):
#     #     print(post_problem_ids)
#
#     df_teacher_sign_test = df_teacher_sign_test.append(
#         {"teacher_id": unique_teacher_ids[i], "post_test": 0, "post_score(avg)": 0, "pre_test": 0, "pre_score(avg)": 0, "+/-": 0}, ignore_index=True)
#     df_teacher_sign_test_treatment = df_teacher_sign_test_treatment.append(
#         {"teacher_id": unique_teacher_ids[i], "post_test": 0, "post_score(avg)": 0, "pre_test": 0, "pre_score(avg)": 0, "+/-": 0}, ignore_index=True)
#
#
# def extract_information_perTeacher_perTreatmentQuestion(teacher_id):
#     df_teacher_specific = df_policy_4.loc[df_policy_4.ts_owner_id == teacher_id]
#
#     pre_count = df_teacher_specific.pl_p_correct.value_counts()[1]
#     post_count = df_teacher_specific.pl_n_correct.value_counts()[1]
#
#     mean_p = df_teacher_specific.loc[df_teacher_specific.ts_owner_id == teacher_id]["avg_p_score_question"].mean()
#     mean_a = df_teacher_specific.loc[df_teacher_specific.ts_owner_id == teacher_id]["avg_a_score_question"].mean()
#     mean_n = df_teacher_specific.loc[df_teacher_specific.ts_owner_id == teacher_id]["avg_n_score_question"].mean()
#     df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "pre_test"] = pre_count
#     df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "pre_score(avg)"] = mean_p
#     df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "post_test"] = post_count
#     df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "post_score(avg)"] = mean_n
#     # df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "trt_score(avg)"] = mean_a
#     df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "+/-"] = (post_count - pre_count)
#
#     df_teacher_specific = df_teacher_specific.loc[
#         (df_teacher_specific.plta_hint_count > 0) | (df_teacher_specific.plta_bottom_hint > 0)]
#
#     pre_count = df_teacher_specific.pl_p_correct.value_counts()[1]
#     post_count = df_teacher_specific.pl_n_correct.value_counts()[1]
#
#     mean_p_t = df_teacher_specific.loc[df_teacher_specific.ts_owner_id == teacher_id]["avg_p_score_question"].mean()
#     mean_a_t = df_teacher_specific.loc[df_teacher_specific.ts_owner_id == teacher_id]["avg_a_score_question"].mean()
#     mean_n_t = df_teacher_specific.loc[df_teacher_specific.ts_owner_id == teacher_id]["avg_n_score_question"].mean()
#     df_teacher_sign_test_treatment.loc[df_teacher_sign_test_treatment.teacher_id == teacher_id, "pre_test"] = pre_count
#     df_teacher_sign_test_treatment.loc[df_teacher_sign_test_treatment.teacher_id == teacher_id, "pre_score(avg)"] = mean_p_t
#     df_teacher_sign_test_treatment.loc[df_teacher_sign_test_treatment.teacher_id == teacher_id, "post_test"] = post_count
#     df_teacher_sign_test_treatment.loc[df_teacher_sign_test_treatment.teacher_id == teacher_id, "post_score(avg)"] = mean_n_t
#     # df_teacher_sign_test_treatment.loc[df_teacher_sign_test_treatment.teacher_id == teacher_id, "trt_score(avg)"] = mean_a_t
#     df_teacher_sign_test_treatment.loc[df_teacher_sign_test_treatment.teacher_id == teacher_id, "+/-"] = (
#                 post_count - pre_count)
#
#
# for val in unique_teacher_ids:
#     extract_information_perTeacher_perTreatmentQuestion(val)
#
#
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# print("---------------That were in the treatment condition-------------------")
# print(df_teacher_sign_test)
# print("----------------That used the treatment condition---------------------")
# print(df_teacher_sign_test_treatment)
#
#
# X = np.arange(len(df_teacher_sign_test_treatment.teacher_id))
# plt.bar( X + 0.00, df_teacher_sign_test_treatment.pre_test, color = 'b', width = 0.35, label = 'pretest score(mean of means)')
# plt.bar( X + 0.35, df_teacher_sign_test_treatment.post_test, color = 'g', width = 0.35, label= 'posttest score(mean of means)')
# plt.xticks( X+0.15, df_teacher_sign_test_treatment.teacher_id)
# plt.legend()
#
#
# plt.show()
#
# import researchpy as rp
#
# descriptives, results = rp.ttest( df_teacher_sign_test_treatment.post_test, df_teacher_sign_test_treatment.pre_test)
#
# print(descriptives)
#
# print(results)
#
# common_treatment_problem_id = np.array([0])
# def common_treatment_problem_between_teachers(teacher1, teacher2):
#     df_teacher1 = df_policy_4.loc[df_policy_4["ts_owner_id"] == teacher1]["plta_problem_id"].unique()
#     df_teacher2 = df_policy_4.loc[df_policy_4["ts_owner_id"] == teacher2]["plta_problem_id"].unique()
#     print( teacher1,"----------------", teacher2)
#     common_treatment_problem_id = np.array([0])
#     for val in df_teacher1:
#         if( val in df_teacher2):
#             if(common_treatment_problem_id[0] == 0):
#                 common_treatment_problem_id[0] = val
#             else:
#                 common_treatment_problem_id = np.append(common_treatment_problem_id, val)
#     print(common_treatment_problem_id.size)
#     return common_treatment_problem_id
#     # print(b)
#
# i = 0
# while i < (unique_teacher_ids.size):
#     j = i+1;
#     while j < (unique_teacher_ids.size):
#         common_treatment_problem_between_teachers(unique_teacher_ids[i], unique_teacher_ids[j])
#         j += 1
#     i += 1
#
#
# # common_treatment_problem_between_teachers(488160, 485865)
#
# # Using these two teachers( 488160, 485865) as they have the most common problems(148) in treatment condition
# def compare_teachers():
#     teacher1 = 488160
#     teacher2 = 578208
#     common_treatment_problem_id = common_treatment_problem_between_teachers(teacher1, teacher2)
#     print(common_treatment_problem_id.size)
#     df_comparing_teacher_per_problem = pd.DataFrame(columns=["problem_id", "post_488160", "post_485865"])
#     for val in common_treatment_problem_id:
#         post_488160 = df_policy_4.loc[(df_policy_4["ts_owner_id"] == teacher1) & (df_policy_4["plta_problem_id"] == val) & (df_policy_4["pl_n_correct"] == 1)]["plta_problem_id"].size
#         post_485865 = df_policy_4.loc[(df_policy_4["ts_owner_id"] == teacher2) & (df_policy_4["plta_problem_id"] == val) & (df_policy_4["pl_n_correct"] == 1)]["plta_problem_id"].size
#         df_comparing_teacher_per_problem = df_comparing_teacher_per_problem.append({"problem_id": val,
#                                                  "post_488160": post_488160,
#                                                  "post_578208": post_485865
#                                                  }, ignore_index=True)
#     return df_comparing_teacher_per_problem
#
#
#
# df_comparing_teacher_per_problem = compare_teachers()
#
# descriptives, results = rp.ttest( df_comparing_teacher_per_problem.post_488160, df_comparing_teacher_per_problem.post_578208)
#
# print("comparing teachers 488160 vs 485865")
# print(descriptives)
# print(results)
#
# from scipy import stats
#
# t, p = stats.ttest_ind(df_comparing_teacher_per_problem.post_488160, df_comparing_teacher_per_problem.post_485865, equal_var = True)
# print("-------------------------------------")
# print("ttest_ind:            t = %g  p = %g" % (t, p))
