from recSys import databaseIo
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import pandas as pd
import numpy as nm
import random
import pymssql

# 定义将多条数据存入数据库操作
'''
输入：db_name数据库的名字
      table_name要存储的数据表名
      data_list存储的数据，以列表的形式传入参数格式如[[1,2,3],[2,3,4],.....,[4,5,6]]
'''
def insertData(db_name, table_name, data_list):
    def getcon(db_name):
        # host是选择连接哪的数据库localhost是本地数据库，port是端口号默认3306
        # user是使用的人的身份，root是管理员身份，passwd是密码。db是数据库的名称，charset是编码格式
        conn = pymssql.connect("47.106.213.57", "sa", "ASElab905", "learningrecommend")
        # 创建游标对象
        cursor1 = conn.cursor()
        return conn, cursor1
    # 调用链接到mysql的函数，返回我们的conn和cursor1
    conn, cursor1 = getcon(db_name)
    # 使用pandas 读取csv文件
    df = []
    df = data_list
    # 使用for循环遍历df，每条数据都是一个列表
    # 使用counts计数一下，方便查看一共添加了多少条数据
    counts = 0
    for each in df:
        # 每一条数据都应该单独添加，所以每次添加的时候都要重置一遍sql语句
        sql = 'insert into ' + table_name + ' values('
        # 因为每条数据都是一个列表，所以使用for循环遍历一下依次添加
        for i, n in enumerate(each):
            # 这个时候需要注意的是前面的数据可以直接前后加引号，最后加逗号，但是最后一条的时候不能添加逗号。
            # 所以使用if判断一下
            if i < (len(each) - 1):
                # 若数据为数值型，则不用添加双引号
                #若数据是字符串型，则改为sql = sql + '"' + str(n) + '"' + ','
                sql = sql + str(n) + ','

            else:
                sql = sql + str(n)
        sql = sql + ');'
        # print(sql)
        # 当添加当前一条数据sql语句完成以后，需要执行并且提交一次
        cursor1.execute(sql)
        # 提交sql语句执行操作
        conn.commit()
        # 没提交一次就计数一次
        counts += 1
        # 使用一个输出来提示一下当前存到第几条了
        print('成功添加了' + str(counts) + '条数据 ')



info = {'servername':'47.106.213.57',
        'username':'sa',
        'passwd':'ASElab905',
        'basename':'learningrecommend'}
ddio = databaseIo.DatabaseIo(info)
ddio.open()
sql_dr = """select *          from course_dr"""
sql_course = """select id , system_course_id from course_info"""
sql_user = """select user_id from user_basic_info"""
#读取course_dr的数据
result_dr = ddio.read(sql_dr)
#读取course_info的数据
result_course = ddio.read(sql_course)
#读取user_basic_info的数据
result_user = ddio.read(sql_user)
#print('user')
#print(result_user)
#print('course')
#print(result_course)
course_length = len(result_course)
user_length = len(result_user)
range_length = len(result_dr)
#print('dr')
#print(range_length)
#print('course')
#print(course_length)
#print('user')
#print(user_length)
ddio.close
#把从course_dr中读取出来的数据以列表形式存储
k = []
for i1 in range(len(result_dr)):
    k.append(list(result_dr[i1]))
#print('k')
#print(k)
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
#result_list1 = sorted(b, key=lambda z: z[1])
#print('list')
#print(result_list)
#print('list1')
#print(result_list1)
#print('len result_course')
#print(len(result_course))



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

#print('ttttttttttt')
#print(tg)
#print(rg)
#print(gg)
#print(rated)
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
        po.append(recommend[i5][2])
        recommend_result.append(po)
print(recommend_result)
print(poo)
#将产生的推荐结果以id, course_index, recommend_value存入数据库中的course_model表中
insertData('learningrecommend','course_model',recommend_result)
ddio.close
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





