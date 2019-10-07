import numpy as np
import pandas as pd

"""
1. Ohjelmoinnin perusteet		    581325	TKT10002
2. Ohjelmoinnin jatkokurssi		    582103	TKT10003
3. Tietokoneen toiminta			    581305	TKT10005
4. Käyttöjärjestelmät			    582219	TKT20003
5. Tietorakenteet ja algoritmit		58131	TKT20001
6. Tietoliikenteen perusteet		582202	TKT20004
7. Laskennan mallit			        582206	TKT20005
8. Ohjelmistotuotanto			    581259	TKT20006
9. Johdatus yliopistomatematiikkaan	57033	MAT11001
10. Todennäköisyyslaskenta I		57045	MAT12003
"""

dict_courses = {
    "Ohjelmoinnin perusteet": ["581325", "TKT10002"],
    "Ohjelmoinnin jatkokurssi": ["582103", "TKT10003"],
    "Tietokoneen toiminta": ["581305", "TKT10005"],
    "Käyttöjärjestelmät": ["582219", "TKT20003"],
    "Tietorakenteet ja algoritmit": ["58131", "TKT20001"],
    "Tietoliikenteen perusteet": ["582202", "TKT20004"],
    "Laskennan mallit": ["582206", "TKT20005"],
    "Ohjelmistotuotanto": ["581259", "TKT20006"],
    "Johdatus yliopistomatematiikkaan": ["57033", "MAT11001"],
    "Todennäköisyyslaskenta I": ["57045", "MAT12003"]
}

courses_names = np.array(["Ohjelmoinnin perusteet", "Ohjelmoinnin jatkokurssi", "Tietokoneen toiminta", 
    "Käyttöjärjestelmät", "Tietorakenteet ja algoritmit", "Tietoliikenteen perusteet", "Laskennan mallit", 
    "Ohjelmistotuotanto", "Johdatus yliopistomatematiikkaan", "Todennäköisyyslaskenta I"])

path = "/home/matleino/Desktop/Student-Data-Analysis/credits.csv"
data = pd.read_csv(path, sep = ";", parse_dates = True)
data.columns = columns = ["id", "course", "grade", "date"]

# Select rows between 2010-2019
start_date = '2010-01-01 00:00:00+00'                                       
end_date = '2019-12-31 00:00:00+00'                                         
date_mask = (data['date'] > start_date) & (data['date'] <= end_date)
data = data[date_mask]

# Drop rows with values for grade other than [0, 1, 2, 3, 4, 5, Hyv., Hyl.]
grade_vals = np.unique(data.grade)
data = data.drop(data.index[data.grade == '0'].values)
for word in np.unique(data.grade)[6:]:
    if word != "Hyl." or word != "Hyv.":
        data = data.drop(data.index[data.grade == word].values)

# replace course codes with names of the courses
for cname in courses_names:
    codes = dict_courses[cname]
    for code in codes:
        data.loc[data.course == code, 'course'] = cname

# number of unique course names
len(np.unique(data["course"]))

#data[["course", "grade"]]
#data[data.grade == 'Hyl.'].loc["grade"] = '0' 

# All Tietorakenteet ja algoritmit-rows
tira1_idx = (data.course == "58131").values
tira2_idx = (data.course == "TKT20001").values
tira = data.iloc[tira1_idx | tira2_idx]

# Dataset grouped by course-column
course_groups = data.groupby("course")

#tira1 = course_groups.get_group("58131")
#tira2 = course_groups.get_group("TKT20001")

#tira.loc[tira.grade == 'Hyl.','grade'] = -1
#tira = tira.drop(tira.index[tira.grade == "Eisa"].values)
#tira = tira.drop(tira.index[tira.grade == "Luop"].values)
#tira.grade = tira.grade.astype('int')

# Dataset grouped by id-column (each group is for one student)
id_groups = data.groupby("id")
# 659 unique students
ids = np.unique(data.id)
i = ids[np.random.randint(len(ids))]
id_groups.get_group(i)

# M is a matrix where each row is a student and each columns is the grades for a course in courses_names
M = np.zeros((len(id_groups), 10), dtype = 'int')
for i in range(len(ids)):
    student = id_groups.get_group(ids[i])
    arr = np.zeros(10, dtype = 'int')
    for j in range(len(courses_names)):
        d = dict_courses[courses_names[j]]
        grade = student.loc[student.course == courses_names[j],].grade.values
        if len(grade) > 0:
            arr[j] = grade[0]
    M[i,:] = arr