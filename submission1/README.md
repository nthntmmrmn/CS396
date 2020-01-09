# Part I. Data Management. (2.5%)
Write one python program using Python3 to answer the following questions:
1. How many reviews are there in tip.json?

2. How many reviews have the maximum length of text among all reviews?

3. We say that a user is "outstanding" if it makes the number of reviews six standard-derivations more than an average user. (That is, #reviews from a user >= average #reviews of all users + 6*std of #reviews of all users). How many outstanding users are there?

4. What is the name of the location with the most reviews? (Hint: you may need to join multiple JSON files using pandas)

5. In the above location, which hour has the least number of reviews? (Hint: the answer should be an integer from [0, 23])

 The program should print out all answers in the following format:

Q1: "integer"

Q2: "integer"

Q3: "integer"

Q4: "string"

Q5: "integer"

Please also write your results in pdf file.

# Part II. Data Cleaning. (2.5%)
Explore the city-name distribution in Arizona. Explore possible dirty data to be cleaned in city names. Document down types of dirty data that you found, how you find them, and how to fixed them.

Please write a python program in Python3 to explore and clean those dirty data. Your project should return a new DataFrame with cleaned city names. Finally, print out the content and the length of the following list

list(df['city'].unique())
where df is the cleaned DataFrame 

(Hint: typical cases include typo, case sensitivity, formatting, missing value, ...) 

Please also write in the pdf file to describe in detail how you explore, identify and clean those dirty data. 
