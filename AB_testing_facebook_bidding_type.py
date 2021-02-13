"""
Analyze and Present A/B Test Results

Facebook recently introduced a new bidding type, “average bidding”, as an alternative to its
exisiting bidding type, called “maximum bidding”. One of our clients, bombabomba.com, has
decided to test this new feature and wants to conduct an A/B test to understand if average
bidding brings more conversions than maximum bidding.

In this A/B test, bombabomba.com randomly splits its audience into two equally sized
groups, e.g. the test and the control group. A Facebook ad campaign with “maximum
bidding” is served to “control group” and another campaign with “average bidding” is served
to the “test group”.

The A/B test has run for 1 month and bombabomba.com now expects you to analyze and
present the results of this A/B test.

You should answer the following questions in your presentation:

    1. How would you define the hypothesis of this A/B test?
    2. Can we conclude statistically significant results?
    3. Which statistical test did you use, and why?
    4. Based on your answer to Question 2, what would be your recommendation to client?

Hints:

    1. Your presentation should last about 15 minutes, and should be presented in English.
    2. The ultimate success metric for bombabomba.com is Number of Purchases.
    Therefore, you should focus on Purchase metrics for statistical testing.
    3. Explain the concept of statistical testing for a non-technical audience.
    4. The customer journey for this campaign is:
        1. User sees an ad (Impression)
        2. User clicks on the website link on the ad (Website Click)
        3. User makes a search on the website (Search)
        4. User views details of a product (View Content)
        5. User adds the product to the cart (Add to Cart)
        6. User purchases the product (Purchase)
    5. Use visualizations to compare test and control group metrics, such as Website Click
    Through Rate, Cost per Action, and Conversion Rates in addition to Purchase
    numbers.
    6. If you see trends, anomalies or other patterns, discuss these in your presentation.
    7. You can make assumptions if needed.

Data Source:

Attached you can find the “ab_testing_data.xlsx” document. The control and test group
campaign results are in Control Group and Test Group tabs, respectively.
"""

# Import libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import shapiro
import scipy.stats as stats
from statsmodels.stats.proportion import proportions_ztest
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

# Load the datasets

# Control Group - Maximum Bidding
df_A = pd.read_excel(r"C:\Users\TOSHIBA\Desktop\A-B TESTING\ab_testing_data.xlsx", sheet_name="Control Group")
df_A.head()

# Test Group - Average Bidding
df_B = pd.read_excel(r"C:\Users\TOSHIBA\Desktop\A-B TESTING\ab_testing_data.xlsx", sheet_name="Test Group")
df_B.head()
#df_B=df_B[["Impression","Click","Purchase","Earning"]]

# describe
df_A.describe()
df_B.describe()

# Missing values analysis
df_A.isnull().sum() # 0
df_B.isnull().sum() # 0

# Histogram

# for df_A
df_A.hist()
plt.show()

# for df_B
df_B.hist()
plt.show()

# We will only use the "Purchase" variable in our transactions now.
A = df_A["Purchase"]
B = df_B["Purchase"]

# Let's save as pkl as we'll be using A and B again in the future.
A.to_pickle(r"C:\Users\TOSHIBA\Desktop\A-B TESTING\A.pkl")
B.to_pickle(r"C:\Users\TOSHIBA\Desktop\A-B TESTING\B.pkl")

# A and Group A
GROUP_A = np.arange(len(A))
GROUP_A = pd.DataFrame(GROUP_A)
GROUP_A[:] = "A"
A = pd.concat([A, GROUP_A], axis=1)

# B and Group B
GROUP_B = np.arange(len(B))
GROUP_B = pd.DataFrame(GROUP_B)
GROUP_B[:] = "B"
B = pd.concat([B, GROUP_B], axis=1)

# All data
AB = pd.concat([A, B])
AB.columns = ["Purchase", "GROUP"]
print(AB.head())
print(AB.tail())

# groupby
AB["GROUP"].value_counts()
AB.groupby("GROUP").agg({"Purchase": ["count", np.mean, np.median, np.std]})

# Visualization with boxplot
sns.boxplot(x="GROUP", y="Purchase", data=AB)
plt.show()
# The average purchase of group A is higher than that of group B.
# Now we want to find out if this situation is random.
# So we will test to find out whether it is statistically significant or not.

# Steps to follow:
"""
 1. Hypothesis Definitions
 2. Assumption Control
    2.1. Normality Assumption
    2.2. Variance Homogenity
 3. Check p-value and interpret the results
"""

# Firstly, define a function for our hypotheses
def hypothesis_test(choose_test):
    pvalue = choose_test[1]
    if pvalue < 0.05:
        print("P-value = %.4f, so that H0 can be REJECTED!" % (pvalue))
    else:
        print("P-value = %.4f, so that H0 can NOT be REJECTED!" % (pvalue))

# Now recall A and B we saved as pkl
A = pd.read_pickle(r"C:\Users\TOSHIBA\Desktop\A-B TESTING\A.pkl")
B = pd.read_pickle(r"C:\Users\TOSHIBA\Desktop\A-B TESTING\B.pkl")

# 1. Hypothesis Definitions
"""
# H0 : M1=M2 ("There is no statistically significant difference between the Purchase averages of the two groups.")
# H1: M1 != M2 ("There is a statistically significant difference between the Purchase averages of the two groups.")
"""

# 2. Assumption Control

# 2.1. Normality Assumption (shapiro)
# Shapiro Wilk Test is used for the assumption of normality.

"""
# Defining hypothesis theses for the assumption of normality.
# H0 : Normality assumption is provided for this sample.
# H1 : Normality assumption is not provided for this sample.
"""

hypothesis_test(shapiro(A)) # P-value = 0.5891, so that H0 can NOT be REJECTED!
hypothesis_test(shapiro(B)) # P-value = 0.1541, so that H0 can NOT be REJECTED!

#Normality assumption is provided for both samples.

# 2.2 Variance Homogenity Assumption (levene)

"""
# Defining hypothesis theses for the Variance Homogenity Assumption.
# H0 : Variance homogeneity assumption is provided.
# H1 : Variance homogeneity assumption is NOT provided.
"""

hypothesis_test(stats.levene(A, B))  # P-value = 0.1083, so that H0 can NOT be REJECTED!

# Variance homogeneity assumption is provided.

# 3. Check p-value and interpret the results (ttest)

"""
# Remember the hypotheses
# H0 : M1=M2 ("There is no statistically significant difference between the Purchase averages of the two groups.")
# H1: M1 != M2 ("There is a statistically significant difference between the Purchase averages of the two groups.")
"""

hypothesis_test(stats.ttest_ind(A, B, equal_var=True)) # P-value = 0.3493, so that H0 can NOT be REJECTED!


# Since there is no statistically significant difference between the two groups, the current system can be continued.
