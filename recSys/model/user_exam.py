userExamlist = [[1,1,30,60],[1,2,60,150],[2,1,100,100],[2,2,50,70]]
resultList = []
len = len(userExamlist)
for i in range(len):
    "评分为成绩/满分"
    socre = userExamlist[i][2]/userExamlist[i][3]
    list = [userExamlist[i][0],userExamlist[i][1],round(socre,3)]
    resultList.append(list)
print(resultList)
print(userExamlist)
