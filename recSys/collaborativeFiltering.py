#周洋涛-2019.9
#本代码实现了协同过滤算法
import numpy
from numpy import *
import csv
import time
from texttable import Texttable
import random
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import databaseIo


class CF:
    def __init__(self, movies, ratings, course_length, user_length, k=10, n=20):
        self.movies = movies
        self.ratings = ratings
        self.course_length = course_length
        self.user_length = user_length
        # 邻居个数
        self.k = k
        # 推荐个数
        self.n = n
        # 训练数据中用户对电影的评分
        # 数据格式{'UserID：用户ID':[(MovieID：电影ID,Rating：用户对电影的评星)]}
        self.userDict = {}
        # 训练数据中对某电影评分的用户
        # {'1',[1,2,3..],...}
        self.ItemUser = {}
        # 数据格式：{'MovieID：电影ID',[UserID：用户ID]}
        # 邻居的信息
        self.neighbors = []
        # 推荐列表
        self.recommandList = []
        self.cost = 0.0

        # 训练数据与测试数据
        self.trans_data = []
        self.test_data = []
        # 测试数据中用户对电影的评分
        self.test_userDict = {}
        # 测试数据中对某电影评分的用户
        self.test_ItemUser = {}

        self.test_neighbors = []
        # 推荐列表
        self.test_recommandList = []
        self.trans_sort = []

        self.trans_data_id = []
        self.test_userid = []

    #  增加划分函数
    #  对数据进行划分，取10000个数据作为训练集，剩下数据作为测试集
    def get_sample(self):

        testIDs = random.sample(list(arange(1, len(self.ratings))), int(9 * len(self.ratings) / 10))
        for i in range(len(self.ratings)):
            # print(i)
            if i in testIDs:
                # self.transGraph[int(self.ratings[i][1]),int(self.ratings[i][0])] = 1
                self.trans_data.append(self.ratings[i])
                self.trans_data_id.append((self.ratings[i][0]))
            else:
                # self.testGraph[int(self.ratings[i][1]),int(self.ratings[i][0])] = 1
                self.test_userid.append(i)
                self.test_data.append(self.ratings[i])

    # 基于用户的推荐
    # 根据对电影的评分计算用户之间的相似度
    def recommendByUser(self):
        self.get_sample()
        #userId = self.trans_data[0][0]
        tt = random.sample(self.trans_data_id,1)
        userId = tt[0]
        print('userid')
        print(userId)
        self.formatRate()
        # 推荐个数 等于 本身评分电影个数，用户计算准确率
        # self.n = len(self.userDict[userId])
        self.neighbors = self.getNearestNeighbor(userId)
        print("neighbor: ")
        print(self.neighbors)
        self.trans_sort = self.getrecommandList(userId)
        print("recommandList: ")
        print(self.recommandList)
        print("邻居的长度：")
        print(len(self.neighbors))
        print("推荐列表的长度：")
        print(len(self.recommandList))
        self.test_compare()

        # 测试数据用户与观看过的电影的矩阵
        #for z in self.test_userid:
         #   for e in self.ratings[z][0]:
         #       for g in arange(len(self.test_userDict[userId])):
         #           self.test_graph[int(e)][int(self.test_userDict[userId][g][0])] = 1

    # 获取推荐列表
    def getrecommandList(self, userId):
        temp_recommandList = []
        self.recommandList = []
        # 建立推荐字典
        recommandDict = {}
        for neighbor in self.neighbors:
            courses = self.userDict[neighbor[1]]
            for course in courses:
                if (course[0] in recommandDict):
                    recommandDict[course[0]] += neighbor[0]
                else:
                    recommandDict[course[0]] = neighbor[0]

        # 建立推荐列表
        for key in recommandDict:
            self.recommandList.append([recommandDict[key], key])
        self.recommandList.sort(reverse=True)
        temp_recommandList = self.recommandList
        self.recommandList = self.recommandList[:self.n]
        #for g in arange(len(temp_recommandList)):
        #    self.graph[int(userId)][int(temp_recommandList[g][1])] = 1
        return temp_recommandList

    '''
    训练集为每个用户产生了n个推荐结果，测试集为了对比也需要为每个用户拿出n部电影：
    1、若测试集里用户看过电影数多于n，随机取出n个
    2、若测试集里用户看过电影数少于n，用unknown作为电影，填充到n个为止
    对比测试集电影在训练集结果的排名时：
    1、若测试集电影在训练集结果里没有，就排名8000，之后继续出现没有的电影排8001，以此类推
    2、unknown电影进行排名，直接排9000，第二部unknown排9001，以此类推
  
    输出：与测试集对比计算相对排名，输出相对排名
    '''

    def test_compare(self):
        tt = []
        L = 0.0
        R = 0.0
        R8 = 0.0
        R9 = 0.0
        Z = 0.0
        self.test_formatRate()
        userId = self.test_data[0][0]
        temp_test = list(self.test_userDict[userId])
        for y in arange(self.n):
            if len(self.test_userDict[userId]) < self.n:
                unknow = ['unknow', 1.0]
                temp_test.append(unknow)
        #print(temp_test)
        for q in arange(len(temp_test)):
            for r in arange(len(self.recommandList)):
                if temp_test[q][0] == self.recommandList[r][1]:
                    L = L + 1
                    R = R + r
                elif temp_test[q][0] == 'unknown':  # 若测试电影在训练集推荐列表中
                    L = L + 1
                    R = R + 8000 + R8
                    R8 = R8 + 1
                else:
                    L = L + 1
                    R = R + 9000 + R9
                    R9 = R9 + 1
        Z = R / L
        #Z1 = R /()
        print('sort:')
        print(Z)

    '''
    将测试集进行数据格式化，将测试集数据转换为test_userDict和test_ItemUser
    '''

    def test_formatRate(self):
        self.test_userDict = {}
        self.test_ItemUser = {}
        for i in self.test_data:  # 将ratings替换为测试集
            # 评分最高为5 除以5 进行数据归一化
            temp = (i[1], float(float(i[2])) / 5)
            # 计算userDict {'1':[(1,5),(2,5)...],'2':[...]...}
            if (i[0] in self.test_userDict):
                self.test_userDict[i[0]].append(temp)
            else:
                self.test_userDict[i[0]] = [temp]
            # 计算ItemUser {'1',[1,2,3..],...}
            if (i[1] in self.test_ItemUser):
                self.test_ItemUser[i[1]].append(i[0])
            else:
                self.test_ItemUser[i[1]] = [i[0]]
        #print('self.test_userDict')
        #print(self.test_userDict)

    '''
    将训练集数据转换为userDict和ItemUser
    '''

    def formatRate(self):
        self.userDict = {}
        self.ItemUser = {}
        for i in self.trans_data:  # 将ratings替换为训练集
            # 评分最高为5 除以5 进行数据归一化
            temp = (i[1], float(float(i[2])) / 5)
            # 计算userDict {'1':[(1,5),(2,5)...],'2':[...]...}
            if (i[0] in self.userDict):
                self.userDict[i[0]].append(temp)
            else:
                self.userDict[i[0]] = [temp]
            # 计算ItemUser {'1',[1,2,3..],...}
            if (i[1] in self.ItemUser):
                self.ItemUser[i[1]].append(i[0])
            else:
                self.ItemUser[i[1]] = [i[0]]

    # 找到某用户的相邻用户
    def getNearestNeighbor(self, userId):
        neighbors = []
        temp_neighbors = []  # dist，用户id
        # 获取userId评分的电影都有那些用户也评过分
        for i in self.userDict[userId]:
            for j in self.ItemUser[i[0]]:
                if (j != userId and j not in neighbors):
                    neighbors.append(j)  # 用户id
        # 计算这些用户与userId的相似度并排序
        for i in neighbors:
            dist = self.getCost(userId, i)
            temp_neighbors.append([dist, i])  # 用户id，[dist，用户id]
        # 排序默认是升序，reverse=True表示降序
        temp_neighbors.sort(reverse=True)
        temp_neighbors = temp_neighbors[:self.k]
        return temp_neighbors

    # 格式化userDict数据
    def formatuserDict(self, userId, l):
        user = {}
        for i in self.userDict[userId]:
            user[i[0]] = [i[1], 0]  # {'电影id':[电影的评分，0]}
        for j in self.userDict[l]:
            if (j[0] not in user):
                user[j[0]] = [0, j[1]]  # 若l用户的电影没有在user中，则{'电影id':[0，l用户的评分]}
            else:
                user[j[0]][1] = j[1]  # 若l用户的电影在user中，则{'电影id':[电影的评分，l用户的评分]}
        return user

    # 计算余弦距离
    def getCost(self, userId, l):
        # 获取用户userId和l评分电影的并集
        # {'电影ID'：[userId的评分，l的评分]} 没有评分为0
        user = self.formatuserDict(userId, l)
        x = 0.0
        y = 0.0
        z = 0.0
        for k, v in user.items():
            x += float(v[0]) * float(v[0])
            y += float(v[1]) * float(v[1])
            z += float(v[0]) * float(v[1])
        if (z == 0.0):
            return 0
        return z / sqrt(x * y)


# -------------------------开始-------------------------------
start = time.clock()
info = {'address':'localhost',
        'username':'root',
        'passwd':'114210',
        'basename':'learningrecommend'}
ddio = databaseIo.DatabaseIo(info)
ddio.open()
sql_dr = """select *          from course_dr"""
sql_course = """select id , system_course_id from course_info"""
sql_user = """select user_id from user_basic_info"""
result_dr = ddio.read(sql_dr)
result_course = ddio.read(sql_course)
result_user = ddio.read(sql_user)
course_length = len(result_course)
user_length = len(result_user)
range_length = len(result_dr)
movies = result_course

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
sorted(course_mdic,key=lambda x: course_mdic[x])
# 再建立反向字典
course_mdicr = {0: 1}
index = 0
for key in course_mdic:
    course_mdicr[index] = key
    index += 1


# 建立字典，实现用户id和索引序号之间的映射，方便后续工作
user_mdic = {1:0}
user_mdic = {}
index = 0
for row in range(len(result_list2)):
    user_mdic[int(result_list2[row][0])] = index
    index += 1
sorted(user_mdic,key=lambda x: user_mdic[x])
# 再建立反向字典
user_mdicr = {0: 1}
index = 0
for key in user_mdic:
    user_mdicr[index] = key
    index += 1

result = []
for j in range(range_length):
    w = []
    w.append(user_mdic[k[j][0]]+1)
    w.append(k[j][1])
    w.append(5 * k[j][2])
    result.append(w)

ratings = result
print('ratings')
print(ratings)
demo = CF(movies, ratings, course_length, user_length, k=10)
demo.recommendByUser()
print("训练集的数据为%d条" % (len(demo.trans_data)))
print("测试集的数据为%d条" % (len(demo.test_data)))
end = time.clock()
print("耗费时间： %f s" % (end - start))