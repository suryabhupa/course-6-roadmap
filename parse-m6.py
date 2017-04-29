
import re

"""
Parse the html pages to extract all the files and their prereqs!

Author: Surya Bhupatiraju
"""

def build_dict(files):
    name_dict = dict()
    prereq_dict = dict()

    def degen_cases(e):
        if e == "permission" or e == "Permission" or e == "" or e == "\n" or \
            e == "of" or e == "instructor\n" or e == "Instructor" or e == "None\n" or e == "None." or e == "None.\n":
            return False
        return True

    for fname in files:
        content = []
        with open(fname) as f:
            content = f.readlines()

        search = False
        for line in content:
            if line[0:7] == "<p><h3>":
                course_num = line[7:line.index(' ')].strip()
                if "J" in course_num:
                    course_num = course_num[:-3]
                course_name = line[line.index(' '):].strip()
                print 'Number:', course_num
                print 'Name:', course_name
                name_dict[course_num] = course_name
                search = True

            if line[0:12] == "<br>Prereq: " and search == True:
                tmp_prereqs = re.sub("[<].*?[>]", "", line[12:]).split(" or ")

                print 'tmp_prereqs:', tmp_prereqs
                prereqs = []
                for tmp in tmp_prereqs:
                    prereqs.extend([x.strip() for x in filter(degen_cases, re.split("[, ;]+", tmp))])
                print 'Prereqs:', prereqs
                prereq_dict[course_num] = prereqs
                search = False

    return name_dict, prereq_dict

def jsonify(nd, pd):
    with open("data.csv", 'w+') as f:
        f.write("source,target,value,class");
        for i in pd:
            for j in pd[i]:
                f.write(j + "," + i + ",1,test\n");

if __name__ == '__main__':
    # TODO Add automatic curls or wgets to automatically get these pages
    # files = ['m6a.txt', 'm6b.txt', 'm6c.txt']
    files = ['m6.txt']
    nd, pd = build_dict(files)
    jsonify(nd, pd)
