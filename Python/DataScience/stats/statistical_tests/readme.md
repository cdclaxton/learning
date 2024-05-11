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

### Test 48: Chi-Squared test for linear trend

- Each observation results in a success or failure
- Is the difference between the observed probability of success from 2+ samples with a linear trend significantly different from zero?
- Based on test for zero slope in the linear regression of the proportions

### Test 49: Pearson's paired chi-squared test

- Are the paired observations on two variables in a contingency table independent of each other?

### Test 50: Fisher's exact test

- Are the paired observations on two variables in a contingency table independent of each other?
- Often used with small sample sizes

### Test 51: Cochran-Mantel-Haenszel test

- Is there a relationship between two categorical variables after adjusting for control variables?
- Null hypothesis: two nominal variables are conditionally independent

### Test 52: McNemar's test

- Is there a difference between paired proportions?
- Paired version of the chi-square test where the same subject is measured twice
- Applied to a $2 \times 2$ contingency table with a dichotomous trait
- Matched pairs of subjects
- Null hypothesis: no difference

### Test 53: Equal means in a one-way layout with equal variances

- Do 3+ independent sets of samples come from populations with the same mean?
- Population is assumed to be normally distributed
- Variances across samples are assumed equal

### Test 54: Welch-test for more than two samples

- Do 3+ independent sets of samples come from populations with the same mean?
- Population is assumed to be normally distributed
- Variances are not assumed to be equal

### Test 55: Kruskal Wallis rank sum test

- Do 3+ independent sets of samples come from populations with the same mean?
- Sample observations are assumed to come from populations with the same shape of distribution
- AKA one-way ANOVA on ranks
- Non-parametric method

### Test 56: Friedman's rank sum test

- Are the distributions from various groups the same across repeated measures?
- Observations are repeated on the same subjects
- Non-parametric statistical test
- Used to detect differences in treatments across multiple test attempts
- Classic example: $n$ wine judges rate $k$ different wines -- are any of the $k$ wines consistently ranked higher or lower than others?

### Test 57: Quade test

- Are the distributions from various groups the same across repeated measures?
- Quade test -- more powerful for a small number of treatments; Friedman test -- more powerful when the number of treatments is 5+.

## Skewness

### Test 58: D'Agostino test of skewness

- Is the sample skewed?
- Goodness of fit measure of departure from normality
- Null hypothesis: data is normally distributed and so skewness should be zero

## Kurtosis

### Test 59: Anscombe-Glynn test of kurtosis

- Does the sample exhibit more (or less) kurtosis relative to the normal distribution?
- Useful for detecting non-normality caused by tail heaviness

### Test 60: Bonett-Seier test of kurtosis

- Does the sample exhibit more (or less) kurtosis calculated by Geary's measure relative to the normal distribution?
- Used to test for heavy tails in a sample

## Normal distribution

### Test 61: Shapiro-Wilk test

- Is the sample from a normal distribution?

### Test 62: Kolmogorov-Smirnov test of normality

- Is the sample from a normal distribution?

### Test 63: Jarque-Bera test

- Is the sample from a normal distribution?
- Null hypothesis: sample comes from a normal distribution with an unknown mean and variance
- Alternative hypothesis: sample does not come from a normal distribution

### Test 64: D'Agostino test

- Is the sample from a normal distribution?
- Test for non-normality due to a lack of symmetry (i.e. distribution is skewed)

### Test 65: Anderson-Darling test of normality

- Is the sample from a normal distribution?
- Null hypothesis: data is from a normal distribution

### Test 66: Cramer-Von Mises test

- Is the sample from a normal distribution?

### Test 67: Lilliefors test

- Is the sample from a normal distribution?

### Test 68: Shapiro-Francia test

- Is the sample from a normal distribution?

## Multivariate normal distribution

### Test 69: Mardia's test of multivariate normality

- Null hypothesis: multivariate normal distribution for a sample of $k$ factors
- A large multivariate kurtosis indicates one or more observations have a large Mahalanobis distance

## Goodness of fit

### Test 70: Kolomogorov-Smirnov test for goodness of fit

- Is there a significant difference between the observed distribution and the specified population distribution?
- Test statistic is most sensitive to the region near the mode of the sample distribution and less sensitive to tails

### Test 71: Anderson-Darling goodness of fit test

- Is there a significant difference between the observed distribution and the specified population distribution?
- Compares fit of the observed cumulative distribution to a specific cumulative function
- Modification of the Kolomogorov-Smirnov test (giving more weight to tails)
- More sensitive than Kolomogorov-Smirnov test

### Test 72: Two-sample Kolomogorov-Smirnov test

- Do two independent random samples come from the same probability distribution?

### Test 73: Anderson-Darling multiple sample goodness of fit test

- Is there a significant difference between the observed distributions in $k$ distinct samples?
- Test does not assume equal variances

##

### Test 74: Brunner-Munzel Test for stochastic equality

- Are the scores on an ordinally scaled variable larger in one population than another?
- Variances are not assumed to be equal
- Distributions are non-symmetric (skewed)
- AKA generalized Wilcoxon test

## Outliers

### Test 75: Dixon's Q test

- Do sample data contain one (and only one) outlier?
- Assumes a normal distribution
- Small sample (typically less than 30 observations)

### Test 76: Chi-squared test for outliers

- Do sample data contain an outlier?
- Test requires specification of the population variance

### Test 77: Bonferroni outlier test

- Do sample data contain an outlier?
- Null hypothesis: largest absolute residual is not an outlier
- Alternative hypothesis: largest absolute residual is an outlier

### Test 78: Grubbs test

- Do sample data contain an outlier?
- Detect outliers from a normal distribution
- Test is based on the largest absolute deviation from the mean of the sample
- Minimum of 7 samples

## Heteroscedasticity

### Test 79: Goldfeld-Quandt test for heteroscedasticity

- Are the residuals in a linear regression model hetereoscedastic?
- Null hypothesis: homoscedastic (constant variance)

### Test 80: Breusch-Pagan test for heteroscedasticity

- Are the residuals in a linear regression model hetereoscedastic?
- Null hypothesis: homoscedastic (constant variance)

### Test 81: Harrison-McCabe test for heteroscedasticity

- Are the residuals in a linear regression model hetereoscedastic?
- Null hypothesis: homoscedastic (constant variance)

## Linearity

### Test 82: Harvey-Collier test for linearity

- Is the regression model correctly specified as linear?
- Null hypothesis: regression model is linear
- Alternative hypothesis: regression model is non-linear

### Test 83: Ramsey reset test

- Is the regression model correctly specified as linear?
- Null hypothesis: regression model is linear
- Alternative hypothesis: regression model is non-linear

### Test 84: White neural network test

- Is the sample of timeseries observations linear in the mean?
- Uses a single hidden layer feed-forward neural network

## Stationarity

### Test 85: Augmented Dickey-Fuller test

- Null hypothesis: data contains a unit root and is thus non-stationary

### Test 86: Phillips-Perron test

- Does the data contain a unit root?
- Unit root => non-stationary

### Test 87: Phillips-Ouliaris test

- Is the sample of multivariate observations cointegrated?
- Null hypothesis: not cointegrated

### Test 88: Kwiatkowski-Phillips-Schmidt-Shin test

- Is the sample of timeseries observations stationary around a deterministic trend?
- Null hypothesis: stationary, alternative hypothesis: unit root
- Higher power than the Augmented Dickey-Fuller and Philips-Perron unit root tests

### Test 89: Elliott, Rothenberg and Stock test

- Does the data contain a unit root?
- Null hypothesis: Unit root => non-stationary
- Higher power than the Augmented Dickey-Fuller and Philips-Perron unit root tests

### Test 90: Schmidt-Phillips test

- Does the data contain a unit root?
- Null hypothesis: Unit root => non-stationary.

### Test 91: Zivot and Andrews test

- Does the data with an expected structural break contain a unit root?
- Structural break may appear on intercept, trend or both
- Null hypothesis of a unit root process

## Survival analysis

### Test 92: Grambsch-Therneau test of proportionality

- Is the assumption of proportional hazards for a Cox regression model fit valid?

### Test 93: Mantel-Haenszel log-rank test

- Are there statistically significant differences between two or more survival curves?
- Emphasises the tail of the survival curve

### Test 94: Peto and Peto test

- Are there statistically significant differences between two or more survival curves?
- Emphasises the beginning of the survival curve (earlier failures receive higher weight)

## Angles

### Test 95: Kuiper's test of uniformity

- Is the sample equally distributed with respect to angle?
- Null hypothesis: sample is uniformly distributed on circle
- As sensitive in the tails as at the median
- Invariant under cyclical data transformations

### Test 96: Rao's spacing test of uniformity

- Is the sample equally distributed with respect to angle?
- Null hypothesis: uniformity

### Test 97: Rayleigh test of uniformity

- Is the sample equally distributed with respect to angle?
