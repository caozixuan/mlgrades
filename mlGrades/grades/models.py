#coding:utf-8
from __future__ import unicode_literals

from django.db import models

class Student(models.Model):
    chinese = models.FloatField()     #语文成绩
    english = models.FloatField()      #英语成绩
    math = models.FloatField()         #数学成绩
    total = models.FloatField()        #总成绩

    def get_student_grades(self):
        return self.chinese, self.english, self.math, self.total

    def get_student_rank(self):
        if(self.total>=650):
            return 'A'
        if(self.total<650 and self.total>=550):
            return 'B'
        if (self.total < 550 and self.total >= 450):
            return 'C'
        if (self.total < 450):
            return 'D'

    def get_student_chinese_rank(self):
        if(self.chinese>=120):
            return 'A'
        if(self.chinese<120 and self.chinese>=105):
            return 'B'
        if (self.chinese < 105 and self.chinese >= 90):
            return 'C'
        if (self.chinese < 90):
            return 'D'

    def get_student_math_rank(self):
        if(self.math>=135):
            return 'A'
        if(self.math<135 and self.math>=120):
            return 'B'
        if (self.math < 120 and self.math >= 90):
            return 'C'
        if (self.math < 90):
            return 'D'

    def get_student_english_rank(self):
        if(self.english>=135):
            return 'A'
        if(self.english<135 and self.english>=120):
            return 'B'
        if (self.english < 120 and self.english >= 90):
            return 'C'
        if (self.english < 90):
            return 'D'


class Classmate(models.Model):
    phy = models.FloatField()  # 语文成绩
    che = models.FloatField()  # 英语成绩
    bio = models.FloatField()  # 数学成绩
    total = models.FloatField()  # 总成绩

    def get_student_grades(self):
        return self.phy, self.che, self.bio, self.total