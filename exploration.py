import numpy as np
import pandas as pd
import json

def save_dict_as_json(filename, dictionary):
    with open(filename, 'w') as fp: 
        json.dump(dictionary, fp, ensure_ascii=False)

def import_json_as_dict(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp)
    return data

def get_data(path):
    data = pd.read_csv(path, sep = ";", parse_dates = True)
    data.columns = columns = ["id", "course", "grade", "date"]
    return data

def select_data_bases_on_dates(data, start_date = '2010-01-01 00:00:00+00', end_date = '2019-12-31 00:00:00+00'):
    date_mask = (data['date'] > start_date) & (data['date'] <= end_date)
    data = data[date_mask]
    return data

def replace_codes_with_course_names(data, dict_courses):
    for cname in dict_courses:
        codes = dict_courses[cname]
        for code in codes:
            data.loc[data.course == code, 'course'] = cname
        return data

def select_rows_with_courses(data, course_names):
    idx = (data.course == course_names[0]).values
    for i in range(1, len(course_names)):
        idx = idx | (data.course == course_names[i]).values
    data = data.loc[idx,:]
    return data

def drop_rows_with_other_than_numeric_grades(data):
    grade_vals = np.unique(data.grade)
    data = data.drop(data.index[data.grade == '0'].values)
    for word in np.unique(data.grade)[5:]:
        #if word != "Hyl." or word != "Hyv.":
        #    data = data.drop(data.index[data.grade == word].values)
        #print(word)
        data = data.drop(data.index[data.grade == word].values)
    return data

def preprocess_data(data):
    print("Select rows between 2010-2019")                                         
    data = select_data_based_on_dates()

    print("Replace course codes with names of the courses")
    data = replace_codes_with_course_names(data)

    print("Pick rows with courses in the list")
    data = select_rows_with_courses(course_names)

    print("Drop rows with values for grade other than [1, 2, 3, 4, 5]")
    data = drop_rows_with_other_than_numeric_grades(data)

    return data

def get_M(data, course_names):
    id_groups = data.groupby("id")
    ids = np.unique(data.id)
    M = np.zeros((len(id_groups), len(course_names)), dtype = 'int')
    for i in range(len(ids)):
        student = id_groups.get_group(ids[i])
        arr = np.zeros(len(course_names), dtype = 'int')
        for j in range(len(course_names)):
            d = dict_courses[course_names[j]]
            grade = student.loc[student.course == course_names[j],].grade.values
            if len(grade) > 0:
                arr[j] = grade[0]
        M[i,:] = arr

    return M

path = "/home/matleino/Desktop/Student-Data-Analysis/credits_all.csv"

cs_ug_courses_dict = import_json_as_dict("/home/matleino/Desktop/Student-Data-Analysis/cs_ug.json")
math_ug_courses_dict = import_json_as_dict("/home/matleino/Desktop/Student-Data-Analysis/math_ug.json")
stat_ug_courses_dict = import_json_as_dict("/home/matleino/Desktop/Student-Data-Analysis/stat_ug.json")

dict_courses = {**cs_ug_courses_dict, **math_ug_courses_dict, **stat_ug_courses_dict}
course_names = list(dict_courses.keys())

print("Get dataset")
#data = get_data(path)

print('Preprocessing data...')
#data = preprocess_data(data)

"""
# Dataset grouped by course-column
course_groups = data.groupby("course")

# Dataset grouped by id-column (each group is for one student)
id_groups = data.groupby("id")
# 659 unique students
ids = np.unique(data.id)
print(len(ids), " unique students")
i = ids[np.random.randint(len(ids))]
id_groups.get_group(i)
"""

print("M is a matrix where each row is a student and each columns is the grades for a course in courses_names")
#M = get_M(data, course_names)
#np.save('coursenames.npy', course_names)
#np.save('M.npy', M)

M = np.load('M.npy')
coursenames = np.load('coursenames.npy')

print("Means of the course grades:")
print(np.sum(M, axis = 0) / np.count_nonzero(M, axis=0))

print("Matrix sparsity:")
print(np.count_nonzero(M) / (M.shape[0] * M.shape[1]))
