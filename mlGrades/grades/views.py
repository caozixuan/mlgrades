#encoding:utf-8
from django.shortcuts import render
import xlrd
from grades.models import Student, Classmate
from numpy import *


def import_data_to_database(x,y):
    data = xlrd.open_workbook('1.xls')
    table = data.sheets()[0]
    start = x
    end = y
    i = 0
    while(start<=end):
        Student.objects.create(chinese = table.cell(start-1, 0).value,english = table.cell(start-1, 1).value,
                               math = table.cell(start-1, 2).value,total=table.cell(start-1,3).value)
        start = start +1
    return 'success'

def import_data_to_database2(x,y):
    data = xlrd.open_workbook('2.xls')
    table = data.sheets()[0]
    start = x
    end = y
    i = 0
    while(start<=end):
        Classmate.objects.create(phy = table.cell(start-1, 0).value,che = table.cell(start-1, 1).value,
                               bio = table.cell(start-1, 2).value,total=table.cell(start-1,3).value)
        start = start +1
    return 'success'


def get_student_rank(total):
    if (total >= 675):
        return 'A'
    if (total < 675 and total >= 600):
        return 'B'
    if (total < 600 and total >= 500):
        return 'C'
    if (total < 500):
        return 'D'


def get_student_chinese_rank(chinese):
    if (chinese >= 120):
        return 'A'
    if (chinese < 120 and chinese >= 105):
        return 'B'
    if (chinese < 105 and chinese >= 90):
        return 'C'
    if (chinese < 90):
        return 'D'


def get_student_math_rank(math):
    if (math >= 135):
        return 'A'
    if (math < 135 and math >= 120):
        return 'B'
    if (math < 120 and math >= 90):
        return 'C'
    if (math < 90):
        return 'D'


def get_student_english_rank(english):
    if (english >= 135):
        return 'A'
    if (english < 135 and english >= 120):
        return 'B'
    if (english < 120 and english >= 90):
        return 'C'
    if (english < 90):
        return 'D'


def count_num(subject,rank,total_tank):
    count = 0
    if(subject=="chinese"):
        students = Student.objects.all()
        for student in students:
            if student.get_student_chinese_rank()==rank and student.get_student_rank()==total_tank:
                count = count +1
        return count
    elif(subject=="math"):
        students = Student.objects.all()
        for student in students:
            if student.get_student_math_rank() == rank and student.get_student_rank()==total_tank:
                count = count + 1
        return count
    elif (subject == "english"):
        students = Student.objects.all()
        for student in students:
            if student.get_student_english_rank() == rank and student.get_student_rank()==total_tank:
                count = count + 1
        return count
    elif (subject == "total"):
        students = Student.objects.all()
        for student in students:
            if student.get_student_rank() == rank:
                count = count + 1
        return count

def Bias_classifier(chi,ma,eng):
    chi_rank = get_student_chinese_rank(chi)
    ma_rank = get_student_math_rank(ma)
    eng_rank = get_student_english_rank(eng)
    rank_A = count_num("total","A",None)
    rank_B = count_num("total", "B",None)
    rank_C = count_num("total", "C",None)
    rank_D = count_num("total", "D",None)
    chi_rank_A = count_num("chinese",chi_rank,'A')
    chi_rank_B = count_num("chinese", chi_rank, 'B')
    chi_rank_C = count_num("chinese", chi_rank, 'C')
    chi_rank_D = count_num("chinese", chi_rank, 'D')

    ma_rank_A = count_num("math", ma_rank,'A')
    ma_rank_B = count_num("math", ma_rank, 'B')
    ma_rank_C = count_num("math", ma_rank, 'C')
    ma_rank_D = count_num("math", ma_rank, 'D')

    eng_rank_A = count_num("english", eng_rank,'A')
    eng_rank_B = count_num("english", eng_rank, 'B')
    eng_rank_C = count_num("english", eng_rank, 'C')
    eng_rank_D = count_num("english", eng_rank, 'D')

    p_A = (rank_A+1)/float(Student.objects.all().count()+4)
    p_B = (rank_B + 1) / float(Student.objects.all().count() + 4)
    p_C = (rank_C + 1) / float(Student.objects.all().count() + 4)
    p_D = (rank_D + 1) / float(Student.objects.all().count() + 4)

    p_chi_A = (chi_rank_A+1)/(float(rank_A)+4)
    p_chi_B = (chi_rank_B+1)/(float(rank_B)+4)
    p_chi_C = (chi_rank_C+1) / (float(rank_C)+4)
    p_chi_D = (chi_rank_D+1) / (float(rank_D)+4)
    p_ma_A = (ma_rank_A+1)/(float(rank_A)+4)
    p_ma_B = (ma_rank_B+1)/(float(rank_B)+4)
    p_ma_C = (ma_rank_C+1) / (float(rank_C)+4)
    p_ma_D = (ma_rank_D+1) / (float(rank_D)+4)
    p_eng_A = (eng_rank_A+1)/(float(rank_A)+4)
    p_eng_B = (eng_rank_B+1) / (float(rank_B)+4)
    p_eng_C = (eng_rank_C+1) / (float(rank_C)+4)
    p_eng_D = (eng_rank_D+1) / (float(rank_D)+4)
    d = {'A':p_A*p_chi_A * p_ma_A * p_eng_A,'B' : p_B*p_chi_B * p_ma_B * p_eng_B,'C' : p_C*p_chi_C * p_ma_C * p_eng_C
         ,'D' : p_D*p_chi_D * p_ma_D * p_eng_D}
    return max(d, key=lambda x: d[x])


def get_correct_pro(x,y):
    correct_num =0
    #data = xlrd.open_workbook('1.xls')
    data = xlrd.open_workbook('2.xls')
    table = data.sheets()[0]
    start = x
    end = y
    i = 0
    while (start <= end):
        chi = table.cell(start - 1, 0).value
        eng = table.cell(start - 1, 1).value
        ma = table.cell(start - 1, 2).value
        total = table.cell(start - 1, 3).value
        start = start + 1
        #rank = Bias_classifier(float(chi), float(ma), float(eng))
        #grade = get_total_grades(chi,eng,ma)
        grade = get_total_grades2(chi, eng, ma)
        rank = get_student_rank(grade)
        if(rank==get_student_rank(float(total))):
            correct_num=correct_num +1
    return correct_num/float(y-x+1)


#def cal_distance():


def gradient_descent():
    step = 0.00001
    pa_array = array([0, 0, 0],dtype=float64)
    students = Student.objects.all()
    #student = Student.objects.all().get(id= 3)

    for student in students:
        grades_array = array([student.chinese,student.english,student.math])
        pa_array = pa_array - step*(pa_array.dot(grades_array.T)-student.total)*(grades_array)
        print pa_array, grades_array,pa_array*grades_array.T


def get_total_grades(x,y,z):
    w = 1.60128012*float(x)+1.44667389*float(y)+1.97840567*float(z)
    return w

def get_total_grades2(x,y,z):
    w = 2.67974757*float(x)+2.08840476*float(y)+2.6064914*float(z)
    return w


def gradient_descent2():
    i = 0
    step = 0.0000004
    pa_array = array([0, 0, 0],dtype=float64)
    classmates = Classmate.objects.all()
    #student = Student.objects.all().get(id= 3)
    for classmate in classmates:
        grades_array = array([classmate.phy, classmate.che, classmate.bio])

        grades_array = array([classmate.phy,classmate.che,classmate.bio])
        pa_array = pa_array - step*(pa_array.dot(grades_array.T)-classmate.total)*(grades_array)
        print pa_array, grades_array,pa_array*grades_array.T

"""
def deter():
    students = Student.objects.all()
    for student in students:
        if(student.get_student_rank()=='A')

"""