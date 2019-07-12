userCounrselist = [[1,1,300,True,True,4],[1,2,20,True,False,3],[2,1,8,False,False,2],[2,2,300,False,True,5]]
resultList = []
len = len(userCounrselist)
for i in range(len):
    "10min以上1分，否则为0"
    if userCounrselist[i][2]>=10:
        time = 1
    else:
        time = 0
    "有评论1.5分，否则为0"
    if userCounrselist[i][3]==True:
        commit = 1.5
    else:
        commit = 0
    "收藏1分，否则为0"
    if userCounrselist[i][4]==True:
        collect = 1
    else:
        collect = 0
    "评分三分以上1分，否则为0"
    if userCounrselist[i][5]>=3:
        score = 1
    else:
        score = 0
    count = (3*time+2*commit+collect+score)/8
    list = [userCounrselist[i][0],userCounrselist[i][1],round(count,3)]
    resultList.append(list)
print(resultList)
print(userCounrselist)
