#from __future__ import print_function 
import sys
from flask import Flask, render_template , jsonify ,request
from flask.ext.bootstrap import Bootstrap
from flask.ext.triangle import Triangle
from bson import json_util
import json

######### MONGO DB Related ###########
import pymongo
import datetime

from pymongo import MongoClient

client = MongoClient('localhost',27017)

db = client['disaster']
#overView = db['overView']
overView = db['overAll10MinuteAverage']
overViewAverageNew = db['overViewAverage']
realTimeCount10Sec = db['realTimeCount10Sec']
realTimeMLCount10Sec = db['realTimeMLCount10Sec']

Tweets = db['Tweets']
########## SPARK RELATED #############

#import pyspark
#import pymongo_spark
#pymongo_spark.activate()
#from pyspark import SparkContext, SparkConf
#conf = SparkConf().setAppName("pyspark test")
#sc = SparkContext(conf=conf)
#rdd = sc.mongoRDD('mongodb://localhost:27017/disaster.Tweets')

######################################

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

app = Flask(__name__)
Triangle(app)
app.config['SERVER_NAME'] = 'ec2-52-39-134-88.us-west-2.compute.amazonaws.com'

bootstrap = Bootstrap(app)

@app.route('/home',methods=['GET', 'POST'])
def hello_world():
  #return 'Hello from Flask!'
  return render_template('newIndex.html')


@app.route('/about',methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/realTimeSpark1',methods=['GET', 'POST'])
def realTimeSpark1():
    return render_template('sparkRealTime.html')


@app.route('/realTimeStorm1',methods=['GET', 'POST'])
def realTimeStorm1():
    return render_template('stormRealTime.html')


@app.route('/getTotalCount',methods=['GET', 'POST'])
def getTotalCount():
    count = int(db.Tweets.count()) + 131351916
    #count  = ""
    #with open("/home/ec2-user/Disaster-Analysis/totalCount","r") as text_file:
    #    count = str(text_file.readlines()[0])
    return str(count)


@app.route('/', defaults={'KeyWord': None})
def test(KeyWord):
    if( KeyWord == None ): 
        return render_template('newIndex.html')#,count=count)
    
@app.route('/realTimeSpark', defaults={'KeyWord': None})
def realTimeSpark(KeyWord):
    if( KeyWord == None ):
        return render_template('sparkRealTime.html')

@app.route('/realTimeStorm', defaults={'KeyWord': None})
def realTimeStorm(KeyWord):
    if ( KeyWord == None ):
        return render_template('stormRealTime.html')

@app.route('/realTimeChart')
def realTimeChart():
    return render_template('chartRealTime.html')

@app.route('/getJSON/', defaults={'KeyWord': None})
@app.route('/getJSON/<KeyWord>')
def test1(KeyWord):
    content = list(overView.find({},{'_id': 0,'date': 1,'average.'+KeyWord:1}))
    content1 = []
    for x in content:
        content1.append([x['date'] , x['average'][KeyWord]])
    return json_util.dumps(content1)


@app.route('/getRealJSON/', defaults={'KeyWord': None})
@app.route('/getRealJSON/<KeyWord>')
def getRealTimeSpark(KeyWord):
    content = list(overViewAverageNew.find({'average.'+KeyWord: { "$not": { "$type": 10},"$exists" : "true"   } },{'_id': 0,'date': 1,'average.'+KeyWord:1}))
    #print content
    content1 = []
    for x in content:
	content1.append([x['date'] , x['average'][KeyWord]])
    return json_util.dumps(content1)



@app.route('/getRealSecondJSON/', defaults={'KeyWord': None})
@app.route('/getRealSecondJSON/<KeyWord>')
def getRealTimeStorm(KeyWord):
    #print "Content: " ,list(realTimeCount10Sec.find({},{'_id': 0,'date': 1,'count.'+KeyWord:1}).sort('data',pymongo.DESCENDING))[0:12]
    content = list(realTimeCount10Sec.find({},{'_id': 0,'date': 1,'count.'+KeyWord:1}).sort('date',pymongo.DESCENDING))[0:1]
    content1 = []
    for x in content:
        # print x['date']
        content1.append([x['date'] , x['count'][KeyWord]])
    return json_util.dumps(content1)


@app.route('/getRealSecondJSONML/', defaults={'KeyWord': None})
@app.route('/getRealSecondJSONML/<KeyWord>')
def getRealTimeStormML(KeyWord):
    #print "Content: " ,list(realTimeCount10Sec.find({},{'_id': 0,'date': 1,'count.'+KeyWord:1}).sort('data',pymongo.DESCENDING))[0:12]
    content = list(realTimeMLCount10Sec.find({},{'_id': 0,'date': 1,'count.'+KeyWord:1}).sort('date',pymongo.DESCENDING))[0:1]
    content1 = []
    for x in content:
       # print x['date']
        content1.append([x['date'] , x['count'][KeyWord]])
    return json_util.dumps(content1)


@app.route('/getRealSecondJSON20/', defaults={'KeyWord': None})
@app.route('/getRealSecondJSON20/<KeyWord>')
def getRealTimeStorm20(KeyWord):
    #print "Content: " ,list(realTimeCount10Sec.find({},{'_id': 0,'date': 1,'count.'+KeyWord:1}).sort('data',pymongo.DESCENDING))[0:12]
    content = list(realTimeCount10Sec.find({},{'_id': 0,'date': 1,'count.'+KeyWord:1}).sort('date',pymongo.DESCENDING))[0:20][::-1]
    content1 = []
    for x in content:
       # print x['date']
        content1.append([x['date'] , x['count'][KeyWord]])
    return json_util.dumps(content1)


@app.route('/getRealSecondJSONforAll')
def getRealSecondJSONforAll():
    content = list(realTimeCount10Sec.find({},{'_id': 0,'date': 1,'count':1}).sort('date',pymongo.DESCENDING))[0:1]
    #print content[0]['count'].items()
    return json_util.dumps(content[0]['count'].items())


@app.route('/getRealSecondJSON20ML/', defaults={'KeyWord': None})
@app.route('/getRealSecondJSON20ML/<KeyWord>')
def getRealTimeStorm20ML(KeyWord):
    #print "Content: " ,list(realTimeCount10Sec.find({},{'_id': 0,'date': 1,'count.'+KeyWord:1}).sort('data',pymongo.DESCENDING))[0:12]
    content = list(realTimeMLCount10Sec.find({},{'_id': 0,'date': 1,'count.'+KeyWord:1}).sort('date',pymongo.DESCENDING))[0:20][::-1]
    content1 = []
    for x in content:
        #print x['date']
        content1.append([x['date'] , x['count'][KeyWord]])
    return json_util.dumps(content1)


@app.route('/getCount/',methods=['GET', 'POST'])
def getCount():
#    print request
    if request.method == 'GET':
        #content = json.dumps(,default=json_util.default)
        content = list(overView.find({},{'_id': 0}))[0]['count']
        #return jsonify(data=content)
        #return json.dumps({"auth":"1"})
        return render_template('displayGraphs.html', content=content)
        #print content
        #return jsonify(data="hello")
    	#return jsonify()
    if request.method == 'POST':
	#print json.loads(request.data.decode())
        #count = rdd.count()
        #print count
	count = 1
	return jsonify(data=count)
	#return json.loads(request.data.decode())['search']
	#return jsonify(data="hello")	


@app.route('/getCountHourly/',methods=['GET'])
def getHourlyCount():
    content = list(overView.find({},{'_id': 0}))
    listCreation =  [[0 for x in range(6)] for x in range(222)]
    totalCount = 0
    for i in content[-6:]:
        count = 0
        for j in i['count']:
            listCreation[count][totalCount] = i['count'][j]    
            count += 1
        totalCount += 1 
    return render_template('displayGraphHourly.html', content=listCreation)

@app.route('/team/', methods=['GET', 'POST'])
def team():
    return render_template('team.html')
if __name__ == '__main__':
  app.debug = True
  app.run(debug=True,host=app.config['SERVER_NAME'], port=80)
  #app.run(debug=True)
