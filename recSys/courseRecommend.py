#周洋涛-2019.9
#本代码实现了二部图算法，并将产生的推荐结果存入到course_model表中
#import databaseIo
from decimal import *
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import pandas as pd
import numpy as nm
import random
import pymysql
pymysql.install_as_MySQLdb()
#先引入包名才能引入类
from recSys import databaseIo
import pymysql

# 定义将多条数据存入数据库操作
'''
输入：data_list存储的数据，以元组的形式传入参数格式如((1,2,3),(2,3,4),.....,(4,5,6))
结果：将数据批量存入数据库
'''
def insertData(data_list):
    info = {'address': '192.168.0.187',
            'username': 'root',
            'passwd': 'root123',
            'basename': 'learningrecommend'}

    ddio = databaseIo.DatabaseIo(info)
    ddio.open()
    sql_delete = 'truncate table course_model;'
    ddio.write(sql_delete)
    sql_insert = """INSERT INTO course_model(id, course_index, recommend_value)
                        VALUES (%s, %s, %s)"""
    ddio.writeMany(sql_insert,tuple(data_list))
    ddio.close()



info = {'address':'localhost',
        'username':'root',
        'passwd':'114210',
        'basename':'learningrecommend'}
ddio = databaseIo.DatabaseIo(info)
ddio.open()
sql_dr = """select *          from course_dr"""
sql_course = """select id , system_course_id from course_info"""
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
#按course_id升序排序
result_list = sorted(k, key=lambda z: z[1])
#把从course_info中读取出来的数据以列表形式存储
b = []
for i2 in range(len(result_course)):
    b.append(list(result_course[i2]))
result_list1 = []
result_list1 = b

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
#print('course_mdic')
#print(course_mdic)
sorted(course_mdic,key=lambda x: course_mdic[x])
# 再建立反向字典
course_mdicr = {0: 1}
index = 0
for key in course_mdic:
    course_mdicr[index] = key
    index += 1
#print('course_mdicr')
#print(course_mdicr)


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




# 创建训练图矩阵
graph = nm.zeros([course_length, user_length])
# 创建测试图矩阵
testGraph = nm.zeros([course_length, user_length])
# 创建已评价矩阵
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
        #print('------------------------')
        #print(testGraph[course_mdic[row[1]]][int(row[0]) - 1])
        #print(course_mdic[row[1]])
        #print(int(row[0]) - 1)
        tg = tg +1
    else:
        rated[course_mdic[row[1]], int(row[0]) - 1] = 1
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
temp = nm.dot(graph, temp)
for i in range(course_length):
    weights[i, :] = temp[i, :] / kjs

# 求各个用户的资源分配矩阵
locate = nm.matmul(weights, rated)
#print('locate')
#print(locate)
#将算法产生的推荐结果以列表形式存储
recommend = []
for i in range(len(locate)):
    for j in range(len(locate[i])):
        data = []
        data.append(j+1)
        data.append(i+1)
        data.append(locate[i][j])
        temp_data = list(data)
        recommend.append(temp_data)
#print('recommend')
#print(recommend)
recommend_result = []
poo = 0.0
for i5 in range(len(recommend)):
    if recommend[i5][2] > 0.0:
        poo = poo + 1
        po = []
        po.append(user_mdicr[recommend[i5][0] - 1])
        po.append(course_mdicr[recommend[i5][1] - 1])
        #格式化推荐度的值
        po.append(Decimal(recommend[i5][2]).quantize(Decimal('0.00000')))
        tuple1 = tuple(po)
        recommend_result.append(tuple1)
tuple2 = tuple(recommend_result)
print(recommend_result)
print(poo)
#将产生的推荐结果以id, course_index, recommend_value存入数据库中的course_model表中
insertData(tuple2)
# 开始求预测的准确性
rs = nm.zeros(user_length)

# 求测试集中电影的排名矩阵

# 得到资源配置矩阵对应的排名
indiceLocate = nm.argsort(locate, axis=0)
#print('indicelocate')
#print(indiceLocate)

# 通过矩阵乘法得到测试集的排名数据
# 为方便后续处理，对结果进行转置
testIndice = (indiceLocate * testGraph).T

# 求精确度的值
usum = 0
# 计算测试集中每部已评分电影的距离，并求均值
for i in range(user_length):
    if (testGraph[:, i].sum() > 0):
        usum += ((testIndice[i]).sum() / (ls[i] * testGraph[:, i].sum()))
print("the average value of r is:")
print(usum / user_length)





