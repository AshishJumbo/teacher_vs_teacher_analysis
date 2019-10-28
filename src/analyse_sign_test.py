import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import researchpy as rp

pd.options.mode.chained_assignment = None
desired_width = 1000
pd.set_option('display.width', desired_width)

df = pd.read_csv("../data/df_policy_4_teacher_vs_teacher.csv")


# df['plta_start_time'] = pd.to_datetime(df['plta_start_time'], format='%Y-%m-%d %H:%M:%S.%f')
#
# print("-------------teacher assist policy id 4 started from : min time------------------")
# print(min(df['plta_start_time']))
# print("---------------------------------------------------------------------------------")
#
# df_user_ids = df['user_id'].unique()
# print(len(df_user_ids))
# np.savetxt("../data/unique_user_ids.txt", df_user_ids, fmt='%i', delimiter=', ', newline=', ')


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


print(Color.BOLD, Color.DARKCYAN, "ANALYSING TEACHER VS TEACHER : with sign test version 1 ", Color.END, Color.END)

# the dictionary mapping teacher ids to teacher names
id_name = {
    460570: "Starred Teacher 1",
    460571: "Starred Teacher 2",
    460572: "Starred Teacher 3",
    436919: "Andrew Burnett",
    578207: "Nicholas Sackos",
    578208: "Irene Wong",
    578209: "Christina Lussier",
    436143: "Thia Durling",
    485865: "Julie Snyder",
    483200: "Star Teacher",
    294187: "Kim Kelly",
    488160: "Heather Nees"
}


# 633 actually, 720 had nan as pre_correctness
# '1507720.0,1507732.0,1507726.0'#good result
# '1507732.0,1507721.0,1507720.0'#negative result
# '1501984.0,1501999.0,1502006.0'#negative result
# '1501999.0,1502000.0,1501984.0'#negative result
# '1502000.0,1501985.0,1501999.0'#+ve & -ve
# '1217507.0,1217756.0,1350213.0'# good result
# '1501746.0,1501747.0,1501745.0'#negative result
# 594 actually cause above 2 had missing pre
# and post scores -_-

# trying to find a correlation between columns using heatmap
# corr = df_policy_4.corr()
# sns.heatmap(corr,
#         xticklabels=corr.columns,
#         yticklabels=corr.columns)
# plt.show()
# end of heatmaps exploring


# this function compares the teachers vs teacher
# For the combinations in which all the teachers made the same treatment
# with the sequence of: pre, treatment, post [combo is treatment-post-pre in column "prev_treat_next"]
# NOTE: analysis is happening at a question level
def find_info_for_all_tVst(key, count):
    df_tvst = df.loc[df.prev_treat_next == key]
    print(Color.BOLD, count, ". The following pre_treat_post combination is being searched :", Color.END, Color.PURPLE, key, "[treat-post-pre] :: ", df_tvst.shape, Color.END)

    df_tvst.drop(['prev_treat_next', 'Unnamed: 0', 'user_id'], axis=1, inplace=True)

    # listing the set of columns, just to be sure, after dropping the irrelevant ones
    # print(df_tvst.columns)

    # This function gets the unique instances in the following columns
    # 1. ts_owner_id        : id of the teacher who made the tutoring
    # 2. pl_p_problem_id    : id of the pre test
    # 3. plta_problem_id    : id of the treatment problem
    # 4. pl_n_problem_id    : id of the post test
    def get_Unique_info(column_name):
        unique_instances = df_tvst[column_name].unique()
        # print("--------more info on " + column_name + "------------")
        # print(df_tvst[column_name].value_counts())
        return unique_instances

    unique_teacher_ids = get_Unique_info('ts_owner_id')
    pre_problem_ids = get_Unique_info('pl_p_problem_id')
    treatment_problem_ids = get_Unique_info('plta_problem_id')
    post_problem_ids = get_Unique_info('pl_n_problem_id')

    # print("--------teacher-ids------------------", unique_teacher_ids)
    # print("--------previous-ids------------------", pre_problem_ids)
    # print("--------treatment-ids------------------", treatment_problem_ids)
    # print("--------post-ids------------------", post_problem_ids)
    # print("------------teacher counts---------------------")
    # print(df_tvst['ts_owner_id'].value_counts())

    df_tvst["avg_p_score_question"] = 0
    df_tvst["avg_a_score_question"] = 0
    df_tvst["avg_n_score_question"] = 0

    # This function finds the average question score for all pre, treatment and post
    # we did this because the average score is indicative of the difficulty of the problem
    def find_avg_question_score(unique_id, column_name, avg_col, correctness_column):
        mean = df_tvst.loc[(df_tvst[column_name] == unique_id)][correctness_column].mean()
        df_tvst.loc[df_tvst[column_name] == unique_id, avg_col] = mean

    # this was done because initially there could have been multiple ids in a single treatment/pre/post condition
    # which is no longer the case
    # TODO: Hence, we might actually remove this whole code block during code refactoring
    def calculate_the_average(ids, column_name, avg_for_column, correctness_column):
        for val in ids:
            find_avg_question_score(val, column_name, avg_for_column, correctness_column)

    calculate_the_average(pre_problem_ids, "pl_p_problem_id", "avg_p_score_question", "pl_p_correct")
    calculate_the_average(treatment_problem_ids, "plta_problem_id", "avg_a_score_question", "plta_correct")
    calculate_the_average(post_problem_ids, "pl_n_problem_id", "avg_n_score_question", "pl_n_correct")

    # average score is indicative of the difficulty of the problem
    avg_p_score = df_tvst["avg_p_score_question"].unique()
    avg_a_score = df_tvst["avg_a_score_question"].unique()
    avg_n_score = df_tvst["avg_n_score_question"].unique()

    # print("average pre score", avg_p_score)
    # print("average treatment score", avg_a_score)
    # print("average post score", avg_n_score)

    df_teacher_sign_test = pd.DataFrame(columns=["teacher_id", "total_treated_exposed", "pre_test", "post_test", "+/-"])
    df_teacher_sign_test_treatment = pd.DataFrame(
        columns=["teacher_id", "total_treated_used", "pre_test", "post_test", "+/-"])

    for i in range(unique_teacher_ids.size):
        df_teacher_sign_test = df_teacher_sign_test.append(
            {"teacher_id": unique_teacher_ids[i], "post_test": 0, "post_score(avg)": 0, "pre_test": 0,
             "pre_score(avg)": 0, "+/-": 0, "total_treated_exposed": 0},
            ignore_index=True)
        df_teacher_sign_test_treatment = df_teacher_sign_test_treatment.append(
            {"teacher_id": unique_teacher_ids[i], "post_test": 0, "post_score(avg)": 0, "pre_test": 0,
             "pre_score(avg)": 0, "+/-": 0, "total_treated_used": 0},
            ignore_index=True)

    def extract_information_perTeacher_perTreatmentQuestion(teacher_id):
        df_teacher_specific = df_tvst.loc[df_tvst.ts_owner_id == teacher_id]

        pre_count = (df_teacher_specific.pl_p_correct == 1).sum()
        post_count = (df_teacher_specific.pl_n_correct == 1).sum()

        mean_p = df_teacher_specific.loc[df_teacher_specific.ts_owner_id == teacher_id]["avg_p_score_question"].mean()
        mean_n = df_teacher_specific.loc[df_teacher_specific.ts_owner_id == teacher_id]["avg_n_score_question"].mean()

        df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "pre_test"] = pre_count
        df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "pre_score(avg)"] = mean_p

        df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "post_test"] = post_count
        df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "post_score(avg)"] = mean_n
        df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "total_treated_exposed"] = len(
            df_teacher_specific.pl_n_correct)

        df_teacher_sign_test.loc[df_teacher_sign_test.teacher_id == teacher_id, "+/-"] = (post_count - pre_count)

        df_teacher_specific = df_teacher_specific.loc[
            (df_teacher_specific.plta_hint_count > 0) | (df_teacher_specific.plta_bottom_hint > 0)]

        pre_count = (df_teacher_specific.pl_p_correct == 1).sum()
        post_count = (df_teacher_specific.pl_n_correct == 1).sum()

        mean_p_t = df_teacher_specific.loc[df_teacher_specific.ts_owner_id == teacher_id]["avg_p_score_question"].mean()
        mean_n_t = df_teacher_specific.loc[df_teacher_specific.ts_owner_id == teacher_id]["avg_n_score_question"].mean()
        df_teacher_sign_test_treatment.loc[
            df_teacher_sign_test_treatment.teacher_id == teacher_id, "pre_test"] = pre_count
        df_teacher_sign_test_treatment.loc[
            df_teacher_sign_test_treatment.teacher_id == teacher_id, "pre_score(avg)"] = mean_p_t
        df_teacher_sign_test_treatment.loc[
            df_teacher_sign_test_treatment.teacher_id == teacher_id, "post_test"] = post_count
        df_teacher_sign_test_treatment.loc[
            df_teacher_sign_test_treatment.teacher_id == teacher_id, "post_score(avg)"] = mean_n_t
        df_teacher_sign_test_treatment.loc[df_teacher_sign_test_treatment.teacher_id == teacher_id, "+/-"] = (
                post_count - pre_count)
        df_teacher_sign_test_treatment.loc[
            df_teacher_sign_test_treatment.teacher_id == teacher_id, "total_treated_used"] = len(
            df_teacher_specific.pl_n_correct)

        df_teacher_sign_test.fillna(0, inplace=True)
        df_teacher_sign_test_treatment.fillna(0, inplace=True)

    for val in unique_teacher_ids:
        extract_information_perTeacher_perTreatmentQuestion(val)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    n_largest = df_teacher_sign_test_treatment['total_treated_used'].nlargest(2)
    # if (df_teacher_sign_test_treatment['total_treated_used'].max()) > 20:
    if (n_largest.min()) > 40:
        print(Color.RED, "\n", 'This is a good Data more than 15 used instances', Color.END)
        print(n_largest.max(), " min : ", n_largest.min())
        # print("--------------------------------That were in the treatment condition-----------------------------------")
        # print(df_teacher_sign_test)
        print("---------------------------------That used the treatment condition-------------------------------------")
        print(df_teacher_sign_test_treatment)

        X = np.arange(len(df_teacher_sign_test_treatment.teacher_id))
        plt.bar(X + 0.0, df_teacher_sign_test_treatment.pre_test, color='b', width=0.3,
                label='pretest score')
        plt.bar(X + 0.3, df_teacher_sign_test_treatment.post_test, color='g', width=0.3,
                label='posttest score')
        plt.bar(X + 0.6, df_teacher_sign_test_treatment.total_treated_used, color='r', width=0.3,
                label='total_treatment_used')

        for id in df_teacher_sign_test_treatment.teacher_id:
            if id in id_name.keys():
                df_teacher_sign_test_treatment.loc[df_teacher_sign_test_treatment.teacher_id == id, "teacher_id"] = id_name[id]

        plt.xticks(X + 0.15, df_teacher_sign_test_treatment.teacher_id)
        plt.title(str(count) + ". figure")
        plt.legend()

        plt.show()

        for teacher_id in unique_teacher_ids:
            df_teacher_specific = df_tvst.loc[df_tvst.ts_owner_id == teacher_id]
            df_teacher_specific = df_teacher_specific.loc[
                (df_teacher_specific.plta_hint_count > 0) | (df_teacher_specific.plta_bottom_hint > 0)]

            print("-------------------------------------------------------------------------------------------------------")
            print(Color.BOLD, Color.GREEN, id_name[teacher_id], Color.END, Color.END)

            descriptives, results = rp.ttest( df_teacher_specific.pl_n_correct, df_teacher_specific.pl_p_correct)

            print("-------------------------------------------------------------------------------------------------------")
            print(descriptives)
            print("-------------------------------------------------------------------------------------------------------")
            print(results)
            print("-------------------------------------------------------------------------------------------------------")
        print("\n")


keys = df['prev_treat_next'].unique()
count = 0
for key in keys:
    count += 1
    find_info_for_all_tVst(key, count)
    # if count >= 30:
    #     break
