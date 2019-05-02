#!/usr/bin/env python3

#### Extracting data from data frames ####

#### Objectives ####

# review previous week's objectives
# Today:
#   conditional subsetting
#   grouping data
#   visualizing data with matplotlib
#   dealing with missing data

#### Getting set up ####

# make sure folks are working in project directory with data/

# load libraries
import pandas as pd
import matplotlib.pyplot as plt

# Make sure figures appear inline in some interfaces
%matplotlib inline
# can also use plt.show()

# read in data
clinical_df = pd.read_csv("data/clinical.csv") # import data as csv file
# inspect output
clinical_df.head()
len(clinical_df)

#### Conditional subsetting ####

# motivation: extracting data based on criteria

# what samples are from patients born in 1930?
clinical_df.year_of_birth == 1930
# this gives true/false results

# conditional subsetting: all patients born in 1930
clinical_df[clinical_df.year_of_birth == 1930]

# all patients NOT born in 1930
clinical_df[clinical_df.year_of_birth != 1930]

# combining criteria: AND
clinical_df[(clinical_df.year_of_birth >= 1930) & (clinical_df.year_of_birth <= 1940)]

# combining subsetting: OR
clinical_df[(clinical_df.year_of_birth == 1930) | (clinical_df.year_of_birth == 1931)]

## Challenge: print to the screen all data from clinical_df for patients with
# stage ia tumors who live more than 365 days

# what if you wanted to extract observations matching a collection of categories?
# create list of desired values
cancer_list = ["LGG", "UCEC", "GBM", "LUSC", "BRCA"]
# extract values
reduced_clinical = clinical_df[clinical_df["disease"].isin(cancer_list)]

#### Grouping ####

# motivation: evaluting data available for a category (column)

# what categories exist for race?
# identify number of unique elements in a column
pd.unique(clinical_df.race) # same as above, specifying column differently

# how can we summarize data by category?
# group data by race (object isn't interpretable by us)
grouped_data = clinical_df.groupby("race")
# note: we can't specify race as an attribute here because of the syntax of the method groupby

# summary stats for all columns by race
grouped_data.describe()
# for only one column
grouped_data.race.describe()

# count the number of each race (only one summary stat from above)
grouped_data.count()
# for only one column
grouped_data.race.count()

# count the number of each race for which days to death data is available
grouped_data.days_to_death.count()
# how does this differ from the last command?

# only display one race
grouped_data.days_to_death.count().asian
# remember this is synonymous with:
clinical_df.groupby("race")["days_to_death"].count()["asian"]
# this second command differs because of the data object (clinical_df) and the syntax for identifying columns

# save output to object for later use
race_counts = grouped_data.days_to_death.count()
print(race_counts) # see script-friendly output

## Challenge: Write code that will display:
# the number of patients in this dataset who are listed as alive

#### Visualizing grouped data as bar charts ####

# Create a quick bar chart of number of patients with race known
race_counts.plot(kind="bar");
# the semicolon suppresses the output, allowing the plot to show

## Challenge:
# create a new object called total_count that counts the number of samples for each cancer type (disease)
total_count = clinical_df.groupby("disease")["disease"].count()
total_count = clinical_df.groupby("disease").disease.count() # same as above
# plot the number of samples for each cancer type
total_count.plot(kind="bar");

#### Missing data: replacing data in copied df ####

## replace missing data in copied data frame

# create new copy of data frame
birth_replace = clinical_df.copy()

# look for missing data
birth_replace[pd.isnull(birth_replace.year_of_birth)]
# fill missing values with 0
birth_replace.year_of_birth = birth_replace.year_of_birth.fillna(0)

# filling with 0 gives different answer!
birth_replace.year_of_birth.mean()
clinical_df.year_of_birth.mean()

# fill NaN with mean for all weight values
birth_replace.year_of_birth = birth_replace.year_of_birth.fillna(birth_replace.year_of_birth.mean())
# this won't do anything since we've already replaced all missing data!

# can convert between data types, but is difficult without dealing with missing data
# convert the age_at_diagnosis from an float to integer
birth_replace.year_of_birth = birth_replace.year_of_birth.astype("int64")
birth_replace.year_of_birth.dtype
#clinical_df["year_of_birth"].dtype # gives error

#### Missing data: masking ####

# mask: excluding missing values

# check for missing data anywhere in dataset
pd.isnull(clinical_df)
# gives true/false matrix
# other options include pd.isna (alias of pd.isnull) and pd.notna (removes missing data)

# extract all rows values WITHOUT missing data
clinical_df[-pd.isnull(clinical_df).any(axis=1)]
len(clinical_df[-pd.isnull(clinical_df).any(axis=1)])
# another way to extract rows WITHOUT missing data
clinical_df.dropna() # yet another way
len(clinical_df.dropna())
# filtering for any missing data cuts out a lot of the dataset!

# exclude missing data in only days to death
clinical_df[-pd.isnull(clinical_df.cigarettes_per_day)]
clinical_df.dropna(subset = ["cigarettes_per_day"])

# save masked results to new object
smoke_complete = clinical_df.dropna(subset = ["cigarettes_per_day"])
# apply additional filter for age at diagnosis
smoke_complete = smoke_complete[smoke_complete.age_at_diagnosis > 0]
# save filtered data to file
smoke_complete.to_csv("data/smoke_complete.csv", index=False)

#### Visualizing scatterplots ####

# define plot variables
x = smoke_complete["cigarettes_per_day"]
y = smoke_complete["age_at_diagnosis"]

# plot two quantitative variables
plt.scatter(x, y)

# add transparency
plt.scatter(x, y, alpha=0.2)

# change colors to match cancer type
# show different categories
pd.unique(smoke_complete["disease"])
# create coded list of disease types
group = smoke_complete["disease"].astype("category").cat.codes
# create plot
plt.scatter(x, y, alpha=0.2, c=group, label=group)

# add axis labels (need to execute all lines at once)
plt.scatter(x, y, alpha=0.2, c=group, label=group)
plt.xlabel("cigarettes per day")
plt.ylabel("age at diagnosis (days)")

#### Wrapping up ####

# review objectives
# preview next week's objectives
