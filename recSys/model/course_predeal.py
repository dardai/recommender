# 18级叶航-2019.8
# 本代码主要实现对数据进行预处理，将结果写回数据库中

#添加项目路径，使项目可以在cmd上运行
import sys
import os
import time as counttime
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
#先引入包名才能引入类
import databaseIo
start = counttime.clock()
#import sparkdatabaseIO as sd
info = {'address':'39.100.100.198',
        'username':'root',
        'passwd':'ASElab905',
        'basename':'learningrecommend'}

ddio = databaseIo.DatabaseIo(info)

ddio.open()

sql_select = """select user_id,course_id,
        (CASE 
        WHEN learning_time>10 THEN 1
        ELSE 0 END)as time,
        CASE collect_status
        WHEN 'YES' THEN 1 ELSE 0 END AS collect,
        CASE commit_status
        WHEN 'YES' THEN 1.5 ELSE 0 END AS commit_status,
        CASE 
        WHEN score>50 THEN 1 ELSE 0 END AS score
        FROM user_course"""

result = ddio.read(sql_select)

userCourseList = []

for row in result:
    user_id = row[0]
    course_id = row[1]
    time = row[2]
    collect = row[3]
    commit = row[4]
    score = row[5]
    #计算各用户对课程的综合评分，将可用于数据分析的数据放入新的列表里
    count = (3*time+2*commit+collect+score)/8
    list = [user_id, course_id, count]
    userCourseList.append(list)

#用于批量插入的插入语句
sql_insert = """INSERT INTO course_dr(user_id, course_index, recommend_value)
                    VALUES (%s, %s, %s)"""
sql_delete = 'truncate table course_dr;'

#新建一个列表，用于盛放元组的容器
list_tuple = []

#python中需要用range()函数进行遍历
for i in range(len(userCourseList)):
    #tuple()函数：用于将列表转换为元组
    #用tuple()函数将二维数组的每一行都转换为元组
    tuple2 = tuple(userCourseList[i])
    list_tuple.append(tuple2)
    # userid = userCourseList[i][0]
    # courseindex = userCourseList[i][1]
    # recommendvalue = userCourseList[i][2]
    #print("id=%d, course_id=%d, recommend_value=%f" % (userid, courseindex, recommendvalue))

#将盛放了元组的列表再转换为元组，用于将大量数据批量插入到数据库
tuple_collect = tuple(list_tuple)

# test_list = ((1019389160706723840, 1017291046411976704, 0.6), (1021585286373498880, 1052825830662688768, 0.5))

ddio.write(sql_delete)
ddio.writeMany(sql_insert, tuple_collect)

ddio.close()

end = counttime.clock()
print("耗费时间： %f s" % (end - start))