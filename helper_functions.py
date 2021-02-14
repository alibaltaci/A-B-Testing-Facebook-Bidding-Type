#  HELPER FUNCTIONS FOR A/B TESTING


# Hypothesis Test
def hypothesis_test(choose_test):
    """
    :param choose_test:
        Enter the test

    :return:

    """
    pvalue = choose_test[1]

    if pvalue < 0.05:
        print("P-value = %.4f, so that H0 can be REJECTED!" % (pvalue))
    else:
        print("P-value = %.4f, so that H0 can NOT be REJECTED!" % (pvalue))



# Conversion Rate
def conversion_rate(col1, col2):
    """
    Conversion Rate = Number of Actions / Number of Website Clicks x 100

    :param col1:
        Number of Actions

    :param col2:
        Number of Website Clicks

    :return:

    """
    Conversion_rate_result = (((col1 / col2).sum()) / len(col1))
    return Conversion_rate_result