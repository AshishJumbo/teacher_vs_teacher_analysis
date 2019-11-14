import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import seaborn as sns
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
import math as math


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


star_teacher_names = {
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

df = pd.read_csv('../data/df_regression_1_avg_pre_score.csv')
# df = pd.read_csv('../data/df_regression_1_avg_pre_score_problem_level.csv')

df.drop(['Unnamed: 0', 'user_id', 'assigned_tutor_strategy_id', 'alternative_tutor_strategy_ids',
         'plta_assignment_id', 'plta_problem_id',
         # 'plta_hint_count', 'plta_bottom_hint',
         'plta_start_time', 'plta_finished', 'pl_n_problem_id',
         'pl_n_hint_count', 'pl_n_bottom_hint',
         'pl_n_finished', 'pl_p_problem_id', 'pl_p_hint_count', 'pl_p_bottom_hint', 'pl_p_start_time',
         'prev_treat_next', 'assignment_id_user_id'], inplace=True, axis=1)

df['pre_scores'].fillna(df.pre_scores.mean(), inplace=True)
df['treatment_hint_use'] = df['plta_bottom_hint'] + df['plta_hint_count']
df.dropna(inplace=True)
df.pre_scores.plot.kde()
# plt.show()

star_teacher_string = "TA_by"

df.rename(columns={'plta_correct': 'treatment_score', 'pl_p_correct': 'pre_test_score',
                   'pl_n_correct': 'post_test_score', 'ts_owner_id': star_teacher_string,
                   'pre_scores': 'previous_performance', 'pl_n_avg': 'post item avg',
                   'pl_p_avg': 'pre item avg', 'plta_avg': 'exp item avg'}, inplace=True)

df['real_post_measure'] = df['post_test_score'] - df['previous_performance']

# df.rename(columns={'plta_correct': 'treatment_score', 'pl_p_correct': 'pre-test score',
#                    'pl_n_correct': 'post-test score', 'ts_owner_id': 'ST',
#                    'pre_scores': 'prior-correctness', 'pl_n_avg': 'post item avg',
#                    'pl_p_avg': 'pre item avg', 'plta_avg': 'exp item avg'}, inplace=True)

df.replace({star_teacher_string: star_teacher_names}, inplace=True)
df_backup = df
# df[star_teacher_string] = df[star_teacher_string].astype(str)

df.real_post_measure.plot.kde()
plt.legend()
plt.show()

df.to_csv("../data final to share/data_user_first_problem_across_assignment.csv")

df.drop([
         'treatment_score',
         'plta_hint_count', 'plta_bottom_hint',
         # 'post_test_score',
         # 'previous_performance',
         'treatment_hint_use'  # , 'content_type'
         ], axis=1, inplace=True)

df[star_teacher_string] = df[star_teacher_string].astype('category')

df_test = df.copy()

df = pd.get_dummies(df)
# X = df[['pre_test_score', 'content_type', star_teacher_string]]
X = df.drop(['post_test_score', 'real_post_measure'
                , 'content_type_Explanation'
                , 'pre_test_score'
                , 'post item avg'
                , 'TA_by_Andrew Burnett', 'TA_by_Christina Lussier', 'TA_by_Heather Nees', 'TA_by_Julie Snyder'
                , 'TA_by_Nicholas Sackos', 'TA_by_Thia Durling'
                # , 'previous_performance'
                , 'pre item avg', 'exp item avg'
                # , 'TA_by_Heather Nees'
             ], axis=1)
# y = df['real_post_measure']
y = df['post_test_score']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)


def print_scores(model_print, X_print, y_print, alpha):
    print(Color.PURPLE, 'The alpha : ', alpha, Color.END)
    print(f'score = {model_print.score(X_print, y_print)}')

    print(f'alpha = {model_print.intercept_}')
    print(f'betas = {model_print.coef_}')


# initialize and fit the linear model
lm = linear_model.LinearRegression()
model_linear = lm.fit(X_train, y_train)
print_scores(model_linear, X_train, y_train, 1)

print(Color.RED, "====================================================================================="
                 "==================================", Color.END)
print("the statsmodel output:")
X_sm = X_train.copy()
X_sm2 = sm.add_constant(X_sm)
estimate = sm.OLS(y_train, X_sm2).fit()
print(estimate.summary())

print(Color.RED, "====================================================================================="
                 "==================================", Color.END)

lasso = Lasso(alpha=1)
model = lasso.fit(X_train, y_train)
print_scores(model, X_train, y_train, 1)

for i in range(3):
    j = i + 4
    lasso = Lasso(alpha=(1 / math.pow(10, j)), max_iter=10e5)
    model3 = lasso.fit(X_train, y_train)
    print_scores(model, X_train, y_train, (1 / math.pow(10, j)))

plt.plot(model.coef_, alpha=0.7, linestyle='none', marker='*', markersize=5, color='red',
         label=r'Lasso; $\alpha = 1$', zorder=7)  # zorder for ordering the markers
plt.plot(model3.coef_, alpha=0.5, linestyle='none', marker='d', markersize=5, color='blue',
         label=r'Lasso; $\alpha = 0.0000001$', zorder=5)  # zorder for ordering the markers
plt.plot(model_linear.coef_, alpha=0.3, linestyle='none', marker='o', markersize=7, color='green',
         label='Linear Regression')
plt.xlabel('Coefficient Index', fontsize=16)
plt.ylabel('Coefficient Magnitude', fontsize=16)
plt.legend(fontsize=13, loc=0)
plt.show()

print(Color.RED, "====================================================================================="
                 "==================================", Color.END)


ridge = Ridge(alpha=0)
model = ridge.fit(X_train, y_train)
print_scores(model, X_train, y_train, 0)

for i in range(3):
    j = i
    ridge = Ridge(alpha=(math.pow(10, j)))
    model3 = ridge.fit(X_train, y_train)
    print_scores(model3, X_train, y_train, math.pow(10, j))

print(Color.RED, "====================================================================================="
                 "==================================", Color.END)

plt.plot(model.coef_, alpha=0.7, linestyle='none', marker='*', markersize=5, color='red',
         label=r'Ridge; $\alpha = 1$', zorder=7)  # zorder for ordering the markers
plt.plot(model3.coef_, alpha=0.5, linestyle='none', marker='d', markersize=5, color='blue',
         label=r'Ridge; $\alpha = 10000$', zorder=5)  # zorder for ordering the markers
plt.plot(model_linear.coef_, alpha=0.3, linestyle='none', marker='o', markersize=7, color='green',
         label='Linear Regression')
plt.xlabel('Coefficient Index', fontsize=16)
plt.ylabel('Coefficient Magnitude', fontsize=16)
plt.legend(fontsize=13, loc=0)
plt.show()

# NOTES: the Ridge regression approach was the best approach with alpha value 1


y_predict = lm.predict(X_test)
print("Mean squared error: %.2f" % mean_squared_error(y_test, y_predict))
print('Variance score: %.2f' % r2_score(y_test, y_predict))

corr = X.corr()

# Generate a mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(250, 150, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
sns_heatmap = sns.heatmap(corr,
                          mask=mask,
                          cmap=cmap, vmax=.3, center=0, square=True, linewidths=.5,
                          cbar_kws={"shrink": .5}, annot=True, fmt='.2f')
bottom, top = sns_heatmap.get_ylim()
sns_heatmap.set_ylim(bottom + 0.5, top - 0.5)
plt.show()
