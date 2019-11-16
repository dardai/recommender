# 18级叶航-2019.8
# 本代码主要实现对数据进行预处理，将结果写回数据库中

#添加项目路径，使项目可以在cmd上运行
#coding:utf-8
import sys
import os
import time as counttime
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
#先引入包名才能引入类
import databaseIo
import sparkdatabaseIO as sd
import time as counttime
import numpy as nm
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import StructField, StringType, FloatType, StructType,LongType,DoubleType,DecimalType
start = counttime.clock()
sql = """(SELECT id FROM course_dr) T"""
sql_dr = '(select * from course_dr) T'
sql_select = """(select user_id,course_id,
        (CASE 
        WHEN learning_time>10 THEN 1
        ELSE 0 END)as time,
        CASE collect_status
        WHEN 'YES' THEN 1 ELSE 0 END AS collect,
        CASE commit_status
        WHEN 'YES' THEN 1.5 ELSE 0 END AS commit_status,
        CASE 
        WHEN score>50 THEN 1 ELSE 0 END AS score
        FROM user_course) T"""
#print(result)
pp = sd.SparkDBIO()
k = pp.sparkread(sql_select)
userCourseList = []
for row in k:
    user_id = row[0]
    course_id = row[1]
    time = row[2]
    collect = row[3]
    commit = row[4]
    score = row[5]
    # 计算各用户对课程的综合评分，将可用于数据分析的数据放入新的列表里
    count = (3 * time + 2 * commit + collect + score) / 8
    list = [user_id, course_id, count]
    #print(type(count))
    userCourseList.append(list)
#print(userCourseList)
#sc = SparkContext('local','tests')
"""
sc = SparkContext(appName="pyspark mysql demo")
sqlContext = SQLContext(sc)
n = sc.parallelize(userCourseList)
field = [StructField("id",LongType(),True),StructField("course_index",LongType(),True),StructField("recommend_value",DecimalType(38,5),True)]
schema = StructType(field)
spark_df = sqlContext.createDataFrame(n,schema)
spark_df.write.mode("overwrite").format("jdbc").options(
    url='jdbc:mysql://localhost:3306/learningrecommend',
    user='root',
    password='114210',
    dbtable="course_dr",
    #batchsize="1000",
).save()
def sparksave(data,dtable,field):
    sc = SparkContext(appName="pyspark mysql demo")
    sqlContext = SQLContext(sc)
    n = sc.parallelize(data)
    schema = StructType(field)
    spark_df = sqlContext.createDataFrame(n, schema)
    spark_df.write.mode("overwrite").format("jdbc").options(
        url='jdbc:mysql://localhost:3306/learningrecommend',
        user='root',
        password='114210',
        dbtable=dtable,
        # batchsize="1000",
    ).save()
"""
field = [StructField("user_id",LongType(),True),StructField("course_index",LongType(),True),StructField("recommend_value",DecimalType(38,5),True)]
dtable = 'course_dr'
pp.sparksave(userCourseList,dtable,field)
pp.close()
end = counttime.clock()
print("耗费时间： %f s" % (end - start))