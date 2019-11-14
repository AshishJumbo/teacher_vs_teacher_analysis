import pandas as pd
import math


# This class is used for managing the console printouts and beautification for easier comprehension of the results
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


pd.set_option("display.width", 180)
pd.set_option("display.max_columns", None)
pd.options.mode.chained_assignment = None

# preprocess data for regression analysis
df_teacher_vs_teacher = pd.read_csv("../data/df_regression_1_avg_score.csv")
problem_ids_with_TA = df_teacher_vs_teacher['plta_problem_id'].unique()
df_teacher_vs_teacher.drop(['Unnamed: 0'], axis=1, inplace=True)

df_teacher_vs_teacher['plta_start_time'] = pd.to_datetime(df_teacher_vs_teacher['plta_start_time'])
unique_user_ids = df_teacher_vs_teacher['user_id'].unique()


# because we are preventing carryover effect we need to only analyse instance where the user is exposed to the
# treatment for the first time for this we do the following pre-processing approaches: 1. remove pre questions that
# had TA in them that were used 2. remove questions with TA in them in the pre 3. assignment_id + user_id combination
# must only occur once as cross over effect across assignment would be less significant:
# Can we assume this?
def console_log_op(old_size, new_size, message):
    print(" Old Size: ", old_size)
    print(Color.RED, message, old_size - new_size, Color.END)
    print(" New Size: ", new_size)
    print(Color.BOLD, "-------------------------------------------------------------------------------------------"
                      "-------------------------------", Color.END)


print(Color.YELLOW, "============================================================================================"
                    "==============================", Color.END)
print(Color.BOLD, "-------------------------------------------------------------------------------------------"
                  "---.drop----------------------------", Color.END)
# STEP 1.
old_size = len(df_teacher_vs_teacher['user_id'])
df_teacher_vs_teacher.drop(df_teacher_vs_teacher[(df_teacher_vs_teacher['pl_p_hint_count'] > 0) |
                                                 (df_teacher_vs_teacher['pl_p_bottom_hint'] > 0)].index,
                           inplace=True)

console_log_op(old_size, len(df_teacher_vs_teacher['user_id']),
               "1. removing the questions in pre that had hints or explanations that got used. "
               "The number of rows deleted was ")

# STEP 2.
old_size = len(df_teacher_vs_teacher['user_id'])
df_teacher_vs_teacher = df_teacher_vs_teacher[~df_teacher_vs_teacher['pl_p_problem_id'].isin(problem_ids_with_TA)]

console_log_op(old_size, len(df_teacher_vs_teacher['user_id']),
               "2. removing the questions in pre that were problems with TA in them. The number of rows dropped was ")

# STEP 3.
old_size = len(df_teacher_vs_teacher['user_id'])
df_teacher_vs_teacher["assignment_id_user_id"] = df_teacher_vs_teacher['user_id'].map(str) + \
                                                 df_teacher_vs_teacher['plta_assignment_id'].map(str)

unique_column_name = "assignment_id_user_id"
# unique_column_name = "user_id"
# df_teacher_vs_teacher = df_teacher_vs_teacher.loc[
#     df_teacher_vs_teacher.groupby(unique_column_name)['plta_start_time'].idxmin()]
df_teacher_vs_teacher = df_teacher_vs_teacher.loc[
    df_teacher_vs_teacher.groupby(unique_column_name)['plta_start_time'].idxmin()]

unique_assignment_id_user_ids = df_teacher_vs_teacher[unique_column_name].unique()

console_log_op(old_size, len(df_teacher_vs_teacher['user_id']),
               "3. Removing duplicate instances from the data as user can only be exposed to 1 TA content to "
               "avoid carry over effect. The number of rows dropped was ")

print(Color.YELLOW, "============================================================================================"
                    "==============================", Color.END)
print(Color.YELLOW, "Some sample data from Previous performance table", Color.END)

df_prev_performance = pd.read_csv("../data/raw_previous_performance_records.csv")
df_prev_performance['start_time'] = pd.to_datetime(df_prev_performance['start_time'])
df_prev_performance.sort_values(by='start_time', ascending=True)

print(" -------------------------------------------------------------------------------------------------")
print(df_prev_performance.head())
print(" -------------------------------------------------------------------------------------------------")
print(" ", df_prev_performance.columns)
print(" -------------------------------------------------------------------------------------------------")
print(Color.YELLOW, "============================================================================================"
                    "==============================", Color.END)


def find_prev_avg_score(user_id, pl_p_problem_id, plta_problem_id, unique_assignment_id_user_id_, unique_column_name_):
    # print(" calculate the avg for the user: ", user_id, " with pre problem", pl_p_problem_id, " treatment id ",
    #       plta_problem_id)
    df_pre_proformance_temp = df_prev_performance.loc[df_prev_performance['user_id'] == user_id]
    df_pre_proformance_temp = df_pre_proformance_temp[df_pre_proformance_temp['problem_id'] != pl_p_problem_id]
    df_current_problem_start_time = df_pre_proformance_temp[df_pre_proformance_temp['problem_id'] ==
                                                            plta_problem_id]['start_time'].values[0]

    # len1 = len(df_pre_proformance_temp['user_id']) - 1
    df_pre_proformance_temp = df_pre_proformance_temp[df_pre_proformance_temp['start_time'] <
                                                      df_current_problem_start_time]
    # print("---------------")
    # print(len1, '===========================', len(df_pre_proformance_temp['user_id']))
    # print("---------------")
    average = df_pre_proformance_temp['correct'].mean()
    # normalizing a left-tailed normal distribution : 1 - sqrt(1-avg)
    df_teacher_vs_teacher.loc[df_teacher_vs_teacher[unique_column_name_] == unique_assignment_id_user_id_,
                              'pre_scores'] = (1 - math.sqrt(1 - average))


df_teacher_vs_teacher["pre_scores"] = 0
for unique_assignment_id_user_id in unique_assignment_id_user_ids:
    df_temp = df_teacher_vs_teacher.loc[df_teacher_vs_teacher[unique_column_name] ==
                                        unique_assignment_id_user_id]
    find_prev_avg_score(df_temp.user_id.iloc[0], df_temp.pl_p_problem_id.iloc[0], df_temp.plta_problem_id.iloc[0],
                        unique_assignment_id_user_id, unique_column_name)

# replacing with 0 will make the distribution bimodal
# df_teacher_vs_teacher['pre_scores'].fillna(df_teacher_vs_teacher.pre_scores.mean(), inplace=True)

# df_teacher_vs_teacher.to_csv("../data/df_regression_1_avg_pre_score.csv")
df_teacher_vs_teacher.to_csv("../data/df_regression_1_avg_pre_score_problem_level.csv")


# for user_id in unique_user_ids:


# count = 0
# df_teacher_vs_teacher["pre_scores"] = 0
# def calculate_previous_scores(user_id, problem_id):
#     global count
#     count += 1
#     df_teacher_vs_teacher_temp = df_teacher_vs_teacher.loc[(df_teacher_vs_teacher['user_id'] == user_id) &
#                                                            (df_teacher_vs_teacher['plta_problem_id'] == problem_id)]
#     df_prev_performance_temp = df_prev_performance.loc[(df_prev_performance['user_id'] == user_id)]
#     if len(df_teacher_vs_teacher_temp['plta_start_time'].unique()) > 0:
#         plta_start_time = df_teacher_vs_teacher_temp['plta_start_time'].unique()[0]
#         mask = (df_prev_performance_temp['start_time'] < plta_start_time)
#         df_prev_performance_temp = df_prev_performance_temp.loc[mask]
#
#         df_prev_performance_temp.sort_values(by='start_time', ascending=True)
#         df_prev_performance_temp.loc[df_prev_performance_temp['problem_id'] == df_teacher_vs_teacher_temp['pl_p_problem_id'].unique()[0]]
#         if len(df_prev_performance_temp.user_id) > 0:
#             print(count, ". calculating previous score for user: ", user_id, " for the problem: ", problem_id,
#                   "with size", len(df_prev_performance_temp.user_id))
#     else:
#         print("---------------------ERROR---------------------------------")
#         print(count, ". calculating previous score for user: ", user_id, " for the problem: ", problem_id,
#               "with size", df_prev_performance_temp.size())
#
#
# for user_id in unique_user_ids:
#     # will probably need to do one for pre, treat and post each
#     unique_problem_ids_per_user = df_teacher_vs_teacher.loc[df_teacher_vs_teacher['user_id'] == user_id][
#         'plta_problem_id'].unique()
#     for problem_id in unique_problem_ids_per_user:
#         calculate_previous_scores(user_id, problem_id)
#
# print("---- test call complete ----")
