class Student:
    name = None
    age = None
    level = None
    course = None

    # encapsulation
    def __init__(self, name='', age='', level='', course=''):  # initializing
        self.name = name
        self.age = age
        self.level = level
        self.course = course



    # methods
    def setname(self, name):
        self.name = name

    def setage(self, age):
        self.age = age

    def setlevel(self, level):
        self.level = level

    def setcourse(self, course):
        self.course = course

    def getname(self):
        return self.name

    def getage(self):
        return self.age

    def getlevel(self):
        return self.level

    def getcourse(self):
        return self.course

    def info(self):
        return '{} is {} years in level {} and offers {}'.format(self.name, self.age, self.level, self.course)

    def get_type(self):
        return 'student'

    # method overloading for course
    def getsubject(self):
        if (self.getcourse.lower()).find('statistics'):
            return 'maths, stats, cscd'


# Inheritance
class CourseRep(Student):
    _class = None

    # creating new Student object as courserep
    def __init__(self, name='', age=0, level=0, course='',  _class='', student=Student()):
        self._class = _class
        if student.getname() != '':
            name = student.getname()
            age = student.getage()
            level = student.getlevel()
            course = student.getcourse()
        super(CourseRep, self).__init__(name=name, age=age, level=level, course=course)

    def setclass(self, _class):
        self._class = _class

    def getclass(self):
        return self._class

    # overwriting method
    def get_type(self):
        return 'course_rep'

    def info(self):
        return '{} is {} years in level {}, offers {} and is a couserep of class {}'.format(self.name, self.age,
                                                                                            self.level, self.course,
                                                                                            self._class)


# polymorphism
class StudentInfo:
    def get_info(self, student):
        return student.info()


ben = Student('Bernard Azumah', 21, 200, 'Computer Science')
print(ben.info())
print(ben.getname())
print(ben.getage())
print(ben.get_type())

chris = Student()
chris.setname('chris amegah')
chris.setage(17)
chris.setlevel(100)
chris.setcourse('Agric Science')
print(chris.info())
print(chris.get_type())

info = StudentInfo()
print(info.get_info(ben))

mili = CourseRep('Millicent', 20, 200, 'Economics', 'ECON 211')
print(mili.info())
print(mili.get_type())

#using a student object to create a courserep object
cben = CourseRep(student=ben, _class='CSCD 201')
print(cben.getclass())
print(cben.info())

crep = CourseRep('Chingy', 21, 200, 'Computer Science', 'CSCD 210')
print(crep.getname())
print(crep.info())
