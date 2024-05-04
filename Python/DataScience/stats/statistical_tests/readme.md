# Statistical tests

- Notes from Lewis, N.D.; "100 Statistical tests in R"; Heather Hills Press, 2013
- Null hypothesis $H_0$:
  - assumed correct until shown otherwise
- Alternative hypothesis $H_a$ or $H_1$:
  - there is a difference
  - can't be proven true
- Type 1 error -- incorrectly reject null (false +ve), $\alpha$
- Type 2 error -- fail to reject null when it should've been rejected (false -ve), $\beta$
- Power -- probability of finding a difference between groups if one truly exists = $1 - \beta$
- p-value -- probability of obtaining a result at least as extreme as the current one, assuming the null hypothesis is true
  - low p-value => reject null
  - high p-value => fail to reject null
  - $p < \alpha$ => statistically significant
- Using a significance level ($\alpha$) of 5% means that if the p-value is less than 0.05 then the null hypothesis is rejected
- Types of data:
  - Ordinal -- natural, ordered categories, distances between categories is not known
  - Ranked
  - Continuous
- Different scales:
  - Interval scale -- don't have a true zero, e.g. temperature measured in Celsius
  - Ratio scale -- never fall below zero, e.g height, weight
- Experimental design:

  - **Independent measures** -- AKA between groups
    - different participants are used in each condition of the independent variable
    - each participant should be randomly allocated to a group
    - advantages: avoids order effects (e.g. due to practice, fatigue, boredom)
    - disadvantages: more people are needed; differences between participants (e.g. age, gender, social background) may affect results
  - **Repeated measures** -- AKA within groups
    - participants take part in each condition of the independent variable; alternate the order in which participants perform in different conditions (counterbalancing)
    - advantages: participant variables are reduced; fewer people are needed
    - disadvantages: can be order effects
  - **Matched pairs**
    - each condition uses different but similar participants
    - match participants in each condition based on important characteristics (e.g. age, gender, intelligence)
    - members of each pair should be randomly assigned to conditions
    - advantages: reduces participant variables; avoids order effects
    - disadvantages: if one participant drops out, two persons data are lost; time-consuming to find closely matched pairs; impossible to match people exactly.

- p-value < alpha => reject null hypothesis
- p-value >= alpha => accept null hypothesis

## Install required R libraries

Run the script `install.R`.

## Correlation

### Test 1: Pearson's product moment correlation coefficient t-test

- Null hypothesis of zero correlation between two variables
- Paired random sample
- Approximately normally distributed
- Joint distribution is bivariate normal
- Relationship is linear

### Test 2: Spearman Rank Correlation test

- Is the Spearman rank correlation coefficient between two variables significantly different from zero?
- Assesses the null hypothesis of zero correlation between two variables
- Paired random sample of ordinal or ranked data or continuous data
- Can't assume variables are normally distributed
- Linear relationship assumed

### Test 3: Kendall's Tau Correlation Coefficient test

- Is the Kendall tau correlation coefficient between two variables significantly different from zero?
- Null hypothesis of zero tau correlation between two variables
- Paired random sample of ordinal or ranked data
- Unreasonable to assume variables are normally distributed if they are continuous
- Linear relationship between variables assumed

### Test 4: Z Test of the difference between independent correlations

- Is the difference between two independent correlation coefficients significantly different from zero?
- Null hypothesis of zero correlation between two or more sample correlation coefficients calculated from independent samples
- Data is assumed to be bivariate normal
- Samples can be different sizes

### Test 5: Difference between two overlapping correlation coefficients

- Is the difference between two dependent correlations sharing a common variable significantly different from zero?
- Null hypothesis: zero correlation between one pair of variables to that of a second
- e.g. compare correlation ($z$, $x$) and ($z$, $y$).
- Assumed normally distributed data
- AKA Steiger's t-test, Meng's t-test, Meng, Rosenthall and Rubin's t-test or Williams test

### Test 6: Difference between two non-overlapping dependent correlation coefficients

- Is the difference between two non-overlapping correlation coefficients significantly different from zero?
- Data on the same set of subjects for four variables, e.g. $w$, $x$, $y$ and $z$
- Compare null hypothesis of zero correlation between $w$ and $x$ and with $y$ and $z$
- Frequently used to compare the difference in correlation between two variables at different points in time
- Data assumed to be normally distributed

### Test 7: Bartlett's test of sphericity

- Is the correlation matrix an identity matrix?
- Null hypothesis: correlation matrix is an identity matrix
- Often used in factor analysis studies (rejection of null hypothesis of identity is an indication that the data is suitable for the Factor Analysis model)

### Test 8: Jennrich test of equality of two matrices

- Are a pair of correlation matrices equal?
- Test for equality between two correlation matrices computed over independent sub-samples
- Underlying observations are assumed to be independent and normally distributed

### Test 9: Granger causality test

- Is one time series useful in forecasting another?
- A time series $X$ is said to Granger-cause $Y$ if it can be shown that those $X$ values provide statistically significant information about the future values of $Y$
- t-tests and F-tests on lagged values of $X$ and lagged values of $Y$ are used
- Null hypothesis: lagged $x$ values don't explain the variation $y$, i.e. $x(t)$ doesn't Granger-cause $y(t)$

### Test 10: Durbin-Watson autocorrelation test

- Is there serial correlation in the sample?
- $H_0$: No correlation among residuals
- $H_a$: Residuals are autocorrelated
- Used to investigate if residuals from a linear or multiple regression model are independent
- Assumed that residuals are stationary and normally distributed with a zero mean
- Test is not valid if there are lagged values of the dependent variable (use Breusch-Godfrey test instead)

### Test 11: Breusch-Godfrey autocorrelation test

- Is there serial correlation in the sample?
- Null hypothesis: errors are uncorrelated
- Are residuals from linear or multiple regression independent?
- Residuals are assumed to be stationary, normally distributed, zero mean

## Means and medians

### Test 12: One sample t-test for a hypothesised mean

- Is the mean of the sample significantly different from a hypothesised mean?
- Assumes sample observations are normally distributed and population standard deviation is unknown

### Test 13: One sample Wilcoxon signed rank test

- Is the median of a sample significantly different from a hypothesised value?
- Null hypothesis: mean is a specified value.
- Non-parametric test, therefore no assumption for the sample distribution.

### Test 14: Sign test for a hypothesised median

- Is the median of a sample significantly different from a hypothesised median?
- Null hypothesis: median is a given value
- Non-parametric test

### Test 15: Two sample t-test for the difference in sample means

- Is the difference between the mean of two independent samples significantly different from zero?
- Assumes observations are normally distributed with the same variance
- Null hypothesis: No difference in sample means

### Test 16: Pairwise t-test for the difference in sample means

- Is the difference between the mean of three or more samples significantly different from zero?
- Assumes sample observations are normally distributed

### Test 17: Pairwise t-test for the difference in sample means with common variance

- Is the difference between the mean of three or more samples significantly different from zero?
- Assumes sample observations are normally distributed and the variances are equal across samples

### Test 18: Welch t-test for the difference in sample means

- Is the difference between the mean of two samples significantly different from zero?
- Assumes sample observations are normally distributed and sample variances are not equal

### Test 19: Paired t-test for the difference in sample means

- Is the difference between the mean of two samples significantly different from zero?
- Used when each subject is measured twice (before and after a treatment) or in a matched pairs experimental design where subjects are matched in pairs and different treatments are given to each subject pair
- Normal distribution assumed

### Test 20: Matched pairs Wilcoxon test

- Is the difference between the mean of two samples significantly different from zero?
- Used when each subject is measured twice (before and after a treatment) or in a matched pairs experimental design where subjects are matched in pairs and different treatments are given to each subject within a pair
- Assumes subjects are measured on a scale that allows rank ordering
- Doesn't assume a normal distribution

### Test 21: Pairwise t-test for the difference in sample means

- Is the difference between the mean of two samples significantly different from zero?
- Multiple samples
- Use when:
  - each subject is measured twice, before and after treatment; or
  - matched pairs experimental design
- Assumes subjects are drawn from a population with a normal distribution

### Test 22: Pairwise Wilcox test for the difference in sample means

- Is the difference between the mean of two samples significantly different from zero?
- Multiple samples
- Use when:
  - each subject is measured twice, before and after treatment; or
  - matched pairs experimental design
- Used when subjects cannot be assumed to be drawn from a population with a normal distribution

### Test 23: Two sample dependent sign rank test for difference in medians

- Is the difference between the median of two samples significantly different from zero?
- Each subject is measured twice (before and after) or in matched pairs design
- Continuous underlying distribution assumed

### Test 24: Wilcoxon rank sum test for the difference in medians

- Is the difference between the median of two samples significantly different from zero?
- Less sensitive to outliers than the two sample t-test
- AKA Mann-Whitney U test, Mann-Whitney-Wilcoxon test

## Randomness of the sequence of events

### Test 25: Wald-Wolfowitz runs test for dichotomous data

- Is the sequence of binary events in a sample randomly distributed?
- Run = series of a given value
- Null hypothesis: data is random

### Test 26: Wald-Wolfowitz runs test for continuous data

- Is the sequence of observations in a sample randomly distributed?
- Null hypothesis: randomly distributed
- Run = series of increasing values or decreasing values
- Number of increasing or decreasing values is the length of the run

### Test 27: Bartels test of randomness in a sample

- Is the sequence of observations in a sample randomly distributed?
- Null hypothesis: randomly distributed

### Test 28: Ljung-Box test

- Is the sequence of observations in a sample randomly distributed?
- Based on the autocorrelation plot
- Series is deemed random if the autocorrelations are small
- Tests the overall randomness on a given lag
- Rule of thumb: set lag to ln(n) where n = number of samples

### Test 29: Box-Pierce test

- Is the sequence of observations in a sample randomly distributed?
- Based on the autocorrelation plot
- Series is deemed random if the autocorrelations are small

## Distributions

### Test 30: BDS test

- Is the sample independent and identically distributed?
- Frequently used as a diagnostic for residuals in statistical models
- Rejection of the null hypothesis implies non-stationarity of the sample (e.g. existence of trends)
- $m$ = embedding dimension.
- Common to test for a range of embedding dimensions (e.g. $m \in [2,8]$)
- Could be unreliable for fewer than 500 observations.

### Test 31: Wald-Wolfowitz two sample run test

- Do two random samples come from populations with the same distribution?
- Non-parametric test
- Evaluates if two continuous cumulative distributions are significantly different or not
- Looks at an ascending ordered list of the data from the two distributions keeping an identifier with the data on which line the data point originated

### Test 32: Mood's test

- Do two independent samples come from the same distribution?
- Null hypothesis: two population distributions are identical
- Alternative hypothesis: same median and shape but different dispersions

## Variances

### Test 33: F-test of equality of variances

- Null hypothesis: two independent samples have the same variance
- Sensitive to non-normal data

### Test 34: Pitman-Morgan test

- Are the variances of two correlated samples equal?
- Test for equality of the variances of marginal distributions of two correlated variables
- Sensitive to non-normal data

### Test 35: Ansari-Bradley test

- Do two independent samples come from the same distribution?
- Null hypothesis: population distributions for both samples are identical
- Alternative hypothesis: Distributions have the same median and shape but different dispersions (scale)

### Test 36: Bartlett test for homogeneity of variance

- Null hypothesis: multiple independent samples have the same variance
- Sensitive to non-normal data

### Test 37: Fligner-Killeen test

- Null hypothesis: multiple independent samples have the same variance
- Robust to departures from normally distributed data

### Test 38: Levene's test of equality of variance

- Null hypothesis: multiple independent samples have the same variance
- More robust to non-normally distributed data than Bartlett's test for homogeneity of variance

## Variances with multiple samples

### Test 39: Cochran C test for inlying or outlying variance

- Do $k$ samples come from populations with equal variance?
- Null hypothesis: equality of variances
- Alternative hypothesis: one variance is larger (or smaller) than the rest
- Sample data for each factor should have the same length
- Each data series is assumed to be drawn from a normal distribution

### Test 40: Brown-Forsythe Levene-type test

- Do $k$ samples come from populations with equal variance?
- Null hypothesis: multiple independent samples have the same variance.
- More robust to non-normally distributed data than Bartlett's test for homogeneity of variance.

### Test 41: Mauchly's sphericity test

- Sphericity = variances of the differences between all pairs of groups are equal.
- Null hypothesis $H_0$ = no difference in variances for all pairwise group comparisons.

## Proportions

### Test 42: Binomial test

- Assumes a binomial distribution.
- Do the observed frequencies of two categories of a dichotomous variable differ from the expected frequencies?

### Test 43: One sample proportions test

- Is the observed proportion of successes equal to a pre-specified probability?

### Test 44: One sample Poisson test

- Is the rate parameter of a Poisson distributed sample significantly different from a hypothesised value?

### Test 45: Pairwise comparison of proportions test

- Do the pairwise observed frequencies of 2+ dichotomous samples differ from each other?

### Test 46: Two sample Poisson test

- Null hypothesis: ratio of means of two Poisson distributions is equal to 1.

### Test 47: Multiple sample proportions test

- Each observation results in a success or failure
- Is the difference between the observed number of successes from two or more samples significantly different from zero?

## Trend

### Test 48: Chi-Squared test for linear trend
