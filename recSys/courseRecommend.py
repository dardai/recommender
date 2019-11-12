#周洋涛-2019.9
#本代码实现了二部图算法，并用批量存储的方法将产生的推荐结果存入到SQL server数据库中的course_model表中
#import databaseIo
import prettytable as pt
from decimal import *
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import pandas as pd
import numpy as nm
import random
import pymysql
pymysql.install_as_MySQLdb()
#添加项目路径，使项目可以在cmd上运行
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
#先引入包名才能引入类
from recSys import databaseIo
import pymysql
#引入pyspark的相关包
from pyspark import SparkContext
from pyspark.mllib.linalg import Matrix
from pyspark.mllib.linalg.distributed import RowMatrix,DenseMatrix
from tkinter import  _flatten

# 定义将多条数据存入数据库操作
'''
输入：data_list存储的数据，以元组的形式传入参数格式如((1,2,3),(2,3,4),.....,(4,5,6))
结果：将数据批量存入SQL server数据库
'''
def insertData(data_list):
    #更改为SQL server数据库配置
    info = {'address': '47.106.213.57',
            'username': 'sa',
            'passwd': 'ASElab905',
            'basename': 'learningrecommend'}

    ddio = databaseIo.DatabaseIo(info)
    ddio.open()
    sql_delete = 'truncate table course_model;'
    ddio.write(sql_delete)
    sql_insert = """INSERT INTO course_model(id, course_index, recommend_value)
                        VALUES (%s, %s, %s)"""
    ddio.writeMany(sql_insert,tuple(data_list))
    ddio.close()

"""
输入：由pysaprk中的行矩阵rdd转换成的列表，形如[ DenseMatrix[1,1,1], DenseMatrix[1,1,1], DenseMatrix[1,1,1] ]
返回：转换成功的列表，形如[ [1,1,1], [1,1,1], [1,1,1] ]
"""
def transtomatrix(p):
    f = []
    for i in range(len(p)):
        temp = []
        temp = list(p[i])
        f.append(temp)
    #print(f)
    return(f)


"""
输入：要进行矩阵乘法运算的c和d数组，rlength是数组矩阵d的行数，clength是数组矩阵d的列数
返回：实现矩阵乘法的结果矩阵
注意：返回的结果矩阵是numpy.matrix类型，但二部图中定义的矩阵都是numpy.array类型，要对函数返回的结果进行类型转换
"""
def SparkMultiply(c,d,rlength,clength):
    #将d数组里的所有行数组合并成一个大数组
    b2 = _flatten(d.tolist())
    #设置spark相关参数
    sc = SparkContext('local','tests')
    #进行并行化
    t1 = sc.parallelize(c.tolist())
    #t2 = sc.parallelize(d)
    #创建行矩阵
    m1 = RowMatrix(t1)
    #创建密集矩阵，由于pyspark中的矩阵都是按列存储，所以这里参数设置为True使得矩阵创建时与numpy一样按行存储
    m2 = DenseMatrix(rlength,clength,list(b2),True)
    #调用pyspark中的矩阵乘法，注意这里的m2一定要对应输入时的d数据矩阵
    mat = m1.multiply(m2)
    #print(mat.rows.collect())
    #下面两行代码实现将RDD类型转换成列表类型
    k = mat.rows.collect()
    q = transtomatrix(k)
    #结束并行化
    sc.stop()
    #print(q)
    return q






#更改为SQL server
info = {'address':'47.106.213.57',
        'username':'sa',
        'passwd':'ASElab905',
        'basename':'learningrecommend'}
ddio = databaseIo.DatabaseIo(info)
ddio.open()
sql_dr = """select *          from course_dr"""
sql_course = """select id , system_course_id ,course_name from course_info"""
sql_user = """select user_id from user_basic_info"""
#读取course_dr的数据
result_dr = ddio.read(sql_dr)
#读取course_info的数据htew
result_course = ddio.read(sql_course)
#读取user_basic_info的数据
result_user = ddio.read(sql_user)
ddio.close()
course_length = len(result_course)
user_length = len(result_user)
range_length = len(result_dr)
ddio.close
#把从course_dr中读取出来的数据以列表形式存储
k = []
for i1 in range(len(result_dr)):
    k.append(list(result_dr[i1]))
result_list = []
#print(k)
#按course_id升序排序
result_list = sorted(k, key=lambda z: z[1])
#把从course_info中读取出来的数据以列表形式存储
b = []
for i2 in range(len(result_course)):
    b.append(list(result_course[i2]))
result_list1 = []
result_list1 = b
#print(b)
#读取user的id
#把从user_basic_info中读取出来的数据以列表形式存储
a = []
for i3 in range(len(result_user)):
    a.append(list(result_user[i3]))
result_list2 = []
result_list2 = a




# 建立字典，实现课程id和索引序号之间的映射，方便后续工作
course_mdic = {1:0}
course_mdic = {}
index = 0
for row in range(len(result_list1)):
    course_mdic[int(result_list1[row][0])] = index
    index += 1
#print(index)
#print(course_mdic)
#print(name_mdic)
#sorted(course_mdic,key=lambda x: course_mdic[x])
# 再建立反向字典
course_mdicr = {0: 1}
index = 0
for key in course_mdic:
    course_mdicr[index] = key
    index += 1
#print(course_mdicr)

#读取推荐课程的名字
def get_keys(value):
    for row in result_list1:
        if row[0] == value:
            return row[2]

# 建立字典，实现用户id和索引序号之间的映射，方便后续工作
user_mdic = {1:0}
user_mdic = {}
index = 0
for row in range(len(result_list2)):
    user_mdic[int(result_list2[row][0])] = index
    index += 1
#print('user_mdic')
#print(user_mdic)
sorted(user_mdic,key=lambda x: user_mdic[x])
# 再建立反向字典
user_mdicr = {0: 1}
index = 0
for key in user_mdic:
    user_mdicr[index] = key
    index += 1
#print('user_mdicr')
#print(user_mdicr)


# 创建所有已评价矩阵
all_rated = nm.zeros([course_length, user_length])
# 创建训练图矩阵
graph = nm.zeros([course_length, user_length])
# 创建测试图矩阵
testGraph = nm.zeros([course_length, user_length])
# 创建训练集里已评价矩阵
rated = nm.zeros([course_length, user_length])

#提取出course_dr的数据
result = []
for j in range(range_length):
    w = []
    w.append(user_mdic[k[j][0]]+1)
    w.append(k[j][1])
    w.append(5 * k[j][2])
    result.append(w)
#print('result')
#print(result)
learned = []
for i6 in range(range_length):
    tl = []
    tl.append(k[i6][0])
    tl.append(k[i6][1])
    t = get_keys(k[i6][1])
    # print(t)
    tl.append(t)
    learned.append(tl)

# 读取course_dr的全部数据
data = pd.DataFrame(result)
#print('data')
#print(data)

# 根据评分初始化训练图矩阵
# 随机抓10000个数据作为训练集
testIDs = random.sample(range(1, range_length), int(range_length/10))
#print('testid')
#print(testIDs)
#print(len(testIDs))
tg = 0.0
rg = 0.0
gg = 0.0
for index, row in data.iterrows():
    if ((index + 1) in testIDs):
        testGraph[course_mdic[row[1]], int(row[0]) - 1] = 1
        all_rated[course_mdic[row[1]], int(row[0]) - 1] = 1
        #print('------------------------')
        #print(testGraph[course_mdic[row[1]]][int(row[0]) - 1])
        #print(course_mdic[row[1]])
        #print(int(row[0]) - 1)
        tg = tg +1
    else:
        rated[course_mdic[row[1]], int(row[0]) - 1] = 1
        all_rated[course_mdic[row[1]], int(row[0]) - 1] = 1
        rg = rg + 1

        if (int(row[2]) >=  3.0):
            gg = gg + 1
            graph[course_mdic[row[1]], int(row[0]) - 1] = 1


# 为资源配置矩阵做准备
kjs = nm.zeros([course_length])
kls = nm.zeros([user_length])

# 求产品的度
for rid in range(course_length):
    kjs[rid] = graph[rid,:].sum()

# 求用户的度
for cid in range(user_length):
    kls[cid] = graph[:,cid].sum()

# 计算每个用户未选择产品的度
s = nm.ones(user_length)
s *= course_length
ls = s - kls

# 为防止之后的除法出现0，手动将其改为极大值
for i in range(course_length):
    if (kjs[i] == 0.0):
        kjs[i] = 99999
#print('kls')
#print(kls)
for i in range(user_length):
    if (kls[i] == 0.0):
        kls[i] = 99999

# 求资源配额矩阵
weights = nm.zeros([course_length, course_length])
# 转换为矩阵乘法和向量除法
# 设定若干中间值
gt = graph.T
#print('gt')
#print(gt)
#print('kls')
#print(kls)
temp = nm.zeros([user_length, course_length])
for i in range(course_length):
    temp[:,i] = gt[:,i] / kls
#temp = nm.dot(graph, temp)
temp = nm.array(SparkMultiply(graph,temp,user_length,course_length))
for i in range(course_length):
    weights[i, :] = temp[i, :] / kjs

# 求各个用户的资源分配矩阵
#locate = nm.matmul(weights, rated)
locate = nm.array(SparkMultiply(weights,rated,course_length,user_length))
#print('locate')
#print(locate)
#将算法产生的推荐结果以列表形式存储
recommend = []
for i in range(len(locate)):
    for j in range(len(locate[i])):
        #过滤掉用户已学习过的课程
        if all_rated[i][j] != 1:
            data = []
            data.append(j+1)
            data.append(i+1)
            data.append(locate[i][j])
            temp_data = list(data)
            recommend.append(temp_data)
#print('recommend')
#252963043984print(recommend)
recommend_result = []
poo = 0.0
for i5 in range(len(recommend)):
    if recommend[i5][2] > 0.0:
        poo = poo + 1
        po = []
        po.append(user_mdicr[recommend[i5][0] - 1])
        po.append(course_mdicr[recommend[i5][1] - 1])
        #po.append(name_mdicr[recommend[i5][1] - 1])
        t = get_keys(course_mdicr[recommend[i5][1] - 1])
        #print(t)
        po.append(t)
        #格式化推荐度的值
        po.append(Decimal(recommend[i5][2]).quantize(Decimal('0.00000')))
        tuple1 = tuple(po)
        recommend_result.append(tuple1)
tuple2 = tuple(recommend_result)
#print(recommend_result)
#myfile = open("data.txt",mode="w",encoding='utf-8')
#myfile = open("C:/share/recommend/recommender8/recSys/data.txt",mode="w",encoding='utf-8')
myfile = open("D:/python程序/PycharmProjects/recommend/recommender8/recSys/data.txt",mode="w",encoding='utf-8')
result_data = sorted(recommend_result)
myfile.write("user_id")
myfile.write("   ")
myfile.write("course_id")
myfile.write("   ")
myfile.write("course_name")
myfile.write("   ")
myfile.write("recommend_value")
myfile.write("\n")
for row in result_data:
    myfile.write(str(row[0]))
    myfile.write(" ")
    myfile.write(str(row[1]))
    myfile.write(" ")
    myfile.write(str(row[2]))
    myfile.write(" ")
    myfile.write(str(row[3]))
    myfile.write("\n")
myfile.close()
result_data = sorted(recommend_result,key = lambda x:x[0] and x[1])
result_data = sorted(result_data,key = lambda x:x[3],reverse=True)
#print(poo)
#将产生的推荐结果以id, course_index, recommend_value存入数据库中的course_model表中
#insertData(tuple2)
# 开始求预测的准确性
rs = nm.zeros(user_length)

# 求测试集中电影的排名矩阵

# 得到资源配置矩阵对应的排名
indiceLocate = nm.argsort(locate, axis=0)
#print('indicelocate')
#print(indiceLocate)

# 通过矩阵对应元素相乘得到测试集的排名数据
# 为方便后续处理，对结果进行转置
testIndice = (indiceLocate * testGraph).T

active = True
while active:
    user_id = input("请输入用户id：")
    if user_id == "quit":
        active = False
    else:
        ta = pt.PrettyTable()
        ta.field_names = ["User_id", "Course_id", "Course_name"]
        for row in learned:
            if row[0] == int(user_id):
                ta.add_row(row)
        print("该用户已学习过的课程有：")
        print(ta)
        tb = pt.PrettyTable()
        tb.field_names = ["User_id", "Course_id", "Course_name", "Recommend_value"]
        for row in result_data:
            if row[0] == int(user_id):
                tb.add_row(row)
        print("为该用户推荐学习的课程有：")
        print(tb)



# 求精确度的值
usum = 0
# 计算测试集中每部已评分电影的距离，并求均值
for i in range(user_length):
    if (testGraph[:, i].sum() > 0):
        usum += ((testIndice[i]).sum() / (ls[i] * testGraph[:, i].sum()))
print("the average value of r is:")
print(usum / user_length)