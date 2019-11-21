import pymongo
def MongoDBLink(host,port):
    #host = localhost,port = 27017
    #myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    client = pymongo.MongoClient(host,port)
    return client

def LinkDB(dbname,client):
    #若该DB不存在则创建
    #若存在则返回该DB
    #dbname is a string
    db = client[dbname]
    return db

def PrintDBList(client):
    dblist = client.database_names()
    print(dblist)

def LinkSet(setname,db):
    #若该集合不存在则创建
    myset = db[setname]
    return myset

def PrintSetList(db):
    setList = db.list_collection_names()
    print(setList)

def InsertDoc(doc,myset):
    #doc是字典列表
    myset.insert_many(doc)

def UpdateDoc(myset,myquery,newquery):
    myset.update_one(myquery,newquery)

def PrintAllDoc(myset):
    for doc in myset.find():
        print(doc)

def PrintSelectedDoc(myset,dict2,dict1={}):
    #dict1是要查找符合的内容
    #dict2指定字段为0则不显示,为1则打印,如只看name和level则seledict2 = {"_id":0,"name":1,"level":1}
    for doc in myset.find(dict1,dict2):
        print(doc)

def DeleteDoc(doc,myset):
    #doc is a dictionary
    myset.delete_one(doc)

def DeleteSet(myset):
    myset.drop()

def LinkStartPage():
    #输入host和port
    for i in range(0,20):
        if i != 19:
            print("*",end="*")
        else :
            print("**")
    host = input("***     请输入您的MongoDB的host:")
    port = int(input("***     请输入您的MongoDB的port:"))
    return host,port


def DBCoopPage():
    for i in range(0,20):
        if i != 19:
            print("*",end="*")
        else :
            print("**")
    while True:
        print("****          1.创建(连接)数据库         ****")
        print("****          2.删除数据库               ****")
        print("****          3.显示数据库列表           ****")
        print("****          4.断开MongoDB连接          ****")
        choice = int(input("***           请输入您的选择(1-3):"))
        if choice not in range(1,5):
            print("输入有误,请重新输入")
            continue
        else :
            break
    return choice

def SetCoopPage():
    for i in range(0,20):
        if i != 19:
            print("*",end="*")
        else :
            print("**")
    while True:
        print("****          1.创建(连接)集合         ****")
        print("****          2.删除集合               ****")
        print("****          3.显示集合列表           ****")
        print("****          4.返回                  ****")
        choice = int(input("***           请输入您的选择(1-4):"))
        if choice not in range(1,5):
            print("输入有误,请重新输入")
            continue
        else :
            break
    return choice

def DocCoopPage():
    for i in range(0,20):
        if i != 19:
            print("*",end="*")
        else :
            print("**")
    while True:
        print("****          1.插入文档          ****")
        print("****          2.删除文档          ****")
        print("****          3.修改文档          ****")
        print("****          4.查询文档          ****")
        print("****          5.显示文档列表            ****")
        print("****          6.返回")
        choice = int(input("***           请输入您的选择(1-6):"))
        if choice not in range(1,7):
            print("输入有误,请重新输入")
            continue
        else :
            break
    return choice


def MongoDBclient():
    host,port = LinkStartPage()
    myclient = MongoDBLink(host,port)
    print("---->MongoDB连接成功!")
    
    while True:
        print("=====    当前处于MongoDB页面    ====")
        choice1 = DBCoopPage()#选择MongoDB数据库操作
        if choice1 == 4:
            print("---->"+host+"MongoDB连接已断开!")
            break
        elif choice1 == 1:#当前host创建数据库
            dbname = input("***请输入您的数据库名:")
            mydb = LinkDB(dbname,myclient)
            print("---->"+dbname+"连接成功!")
            while True:
                print("====    当前处于"+dbname+"数据库页面    ====")
                choice2 = SetCoopPage()#选择当前数据库操作
                if choice2 == 4:#返回至MongoDB页面
                    break
                elif choice2 == 1:#当前数据库创建(连接)集合
                    setname =input("***请输入您的集合名:")
                    myset = LinkSet(setname,mydb)
                    print("---->"+setname+"连接成功!")
                    while True:
                        print("====    当前处于"+setname+"集合页面    ====")
                        choice3 = DocCoopPage()#选择当前集合操作
                        if choice3 == 6:#返回至数据库页面
                            break
                        elif choice3 == 1:#当前集合插入文档
                            dictlist = []
                            DocNum = int(input("***请输入要插入的文档数:"))
                            for i in range(1,DocNum+1):
                                DocDict={}
                                DocKVNum = int(input("***请输入第"+str(i)+"个文档的键值对数:"))
                                for j in range(1,DocKVNum+1):
                                    KV = input("***请输入第"+str(j)+"个键值对(用空格分隔):")
                                    key,val = KV.split()[0],KV.split()[1]
                                    DocDict[key] = val
                                dictlist.append(DocDict)
                            InsertDoc(dictlist,myset)
                            print("---->文档插入成功!")
                        elif choice3 == 2:#当前集合删除文档
                            ###删除demo,只能一次删除一个
                            KV = input("***请输入要删除的文档的某个字段的键值对(以空格分隔):")
                            key,val = KV.split()[0],KV.split()[1]
                            dict3={}
                            dict3[key] =val
                            DeleteDoc(dict3,myset)
                            print("---->文档删除成功!")
                        elif choice3 == 3:#当前集合修改文档
                            ###修改demo
                            keyval =input("***请输入要修改的文档的某个字段的键值对(以空格分隔):")
                            key,val = keyval.split()[0],keyval.split()[1]
                            myquery = {key:val}
                            newkyval = input("***请输入要增加或修改的键值对(以空格分隔)")
                            nkey,nval = newkyval.split()[0],newkyval.split()[1]
                            newquery = {"$set":{nkey:nval}}
                            UpdateDoc(myset,myquery,newquery)
                            print("---->文档修改成功!")
                        elif choice3 == 4:#当前集合查询文档
                            ###查询文档demo,MongoDB的ID一般不需要查看,默认置0
                            dict1 = {}
                            dict2 = {"_id":0}
                            checkKey=input("***请输入要查看的字段名(以空格分隔)")
                            checkeCount =len(checkKey.split())
                            for  i in range(0,checkeCount):
                                dict2[checkKey.split()[i]] = 1
                            
                            PrintSelectedDoc(myset,dict2,dict1)
                        elif choice3 == 5:
                            PrintAllDoc(myset)
                
                elif choice2 == 2:#当前数据库删除集合
                    setname =input("***请输入您要删除的集合名:")
                    if setname  in mydb.list_collection_names():
                        YoN = int(input("***您确定要删除集合"+setname+"?(输入1则确定,2则取消):"))
                        if YoN == 1:
                            myset = LinkSet(setname,mydb)
                            DeleteSet(myset)
                            print("---->"+setname+"删除成功!")
                        else :
                            print(setname+"取消删除")
                    else:
                        print("***该集合不存在,无法删除!")
                
                elif choice2 == 3:#当前数据库显示集合列表
                    PrintSetList(mydb)
                    
        
        elif choice1 == 2:#当前host删除数据库
             dbname = input("***请输入您要删除的数据库:")
             dblist = myclient.list_database_names()
             if dbname in dblist:
                 mydb = LinkDB(dbname,myclient)
                 print("当前数据库有以下集合,是否全部删除:")
                 PrintSetList(mydb)
                 confirm = int(input("若确定,则输入1,若取消,则输入2:"))
                 if confirm == 1:
                     setlist = mydb.list_collection_names()
                     length = len(setlist)

                     for i in range(0,length):
                         myset = LinkSet(setlist[i],mydb)
                         DeleteSet(myset)
                     print("--->集合全部删除,数据库已清空!")
                 else:
                     print("***删除数据库操作已取消!")
                     
             else:
                 print("***该数据库不存在,无法删除！")
                     


        elif choice1 == 3:#当前host显示数据库列表
            PrintDBList(myclient)
        
MongoDBclient()





'''
myclient = MongoDBLink("localhost",27017)
PrintDBList(myclient)
mydb = LinkDB("company",myclient)
PrintSetList(mydb)
mytable = LinkSet("admins",mydb)
#PrintAllDoc(mytable)
a ="name"
myquery = {a:"Kelly"}
newquery = {"$set":{"level":"3"}}
mytable.update_one(myquery,newquery)
PrintAllDoc(mytable)

print("****          1.创建(连接)数据库          ****")
        print("****          2.创建(连接)集合            ****")
        print("****          3.插入文档            ****")
        print("****          4.显示数据库列表       ****")
        print("****          5.显示集合列表         ****")
        print("****          6.显示文档列表         ****")
        print("****          7.删除数据库          ****")
        print("****          8.删除集合            ****")
        print("****          9.删除文档            ****")
mydb = myclient["company"]
mytable = mydb["admins"]
mydict ={"name":"BOB","sex":"man","level":"3"}
mydict2 = {"name":"kelly","sex":"woman"}
mytable.insert_one(mydict2)
'''