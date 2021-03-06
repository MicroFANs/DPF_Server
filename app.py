from flask import Flask
from flask import request
from flask import jsonify
import os
import json
import time
import xxhash
import random
import function.Server as lib
import function
import csv
import function
import numpy as np
import pandas as pd

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

epsilon = 3  # 隐私预算
channel = random.randint(0, 3)


@app.route('/')
def test():
    return '服务器正常运行!!!'


# 此方法处理用户注册
# @app.route('/register',methods=['POST'])
# def register():
#     username=request.form['username']
#     password=request.form['password']
#
#     print('username:'+username)
#     print('password:'+password)
#     return '连接成功'

@app.route('/connect', methods=['GET'])
def connect():
    '''

    :return: 返回
    '''
    ip = request.remote_addr
    user_id = (xxhash.xxh32(ip, seed=1)).intdigest()
    print("user_id为:" + ip + "连接成功")
    data = {'user_id': user_id, 'channel': channel, 'epsilon': epsilon}
    return jsonify(data)


@app.route('/upload', methods=['POST'])
def upload():
    datajson = request.form['datajson']

    print('datajson:' + datajson)
    return 'json接收成功'


# @app.route('/upOneSample',methods=['POST'])
# def func1():
#     onesamplejson=request.form['oneSample']
#     data= eval(onesamplejson)
#     key=data["key"]
#     seed=data["hashseed"]
#     print("key:",key,"hashseed:",seed)
#     time.sleep(5)
#
#     candidate=[8,21,2,48,101,11,30,28,18,17,15,6,3,67,7,89,29,1,98,13,64,92,66,4,1973,88,32,10,63,49,52,83,23,19,93,57,
#                2285,142,40,20]
#     index=[i+1 for i in range(len(candidate))]
#     returndate=(dict(zip(index,candidate)))
#     returnjson=json.dumps(returndate)
#     print(returnjson)
#     return returnjson

@app.route('/upOneSample', methods=['POST'])
def upOneSample():
    onesamplejson = request.form['OneSample']
    data = eval(onesamplejson)
    key = data["perturbed_key"]
    seed = data["seed"]
    print("perturbed_key:", key, "hash_seed:", seed)
    time.sleep(1)
    candidate = lib.getcandidate()
    index = [i + 1 for i in range(len(candidate))]
    returndate = (dict(zip(index, candidate)))
    returnjson = json.dumps(returndate)
    print(returnjson)
    return returnjson


@app.route('/upNumber', methods=['POST'])
def upNumber():
    numberjson = request.form['Number']
    data = eval(numberjson)
    num = data["perturbed_number"]
    print("perturbed_number:", num)
    time.sleep(1)
    padlength = 2
    return str(padlength)


@app.route('/upOneSampleUE', methods=['POST'])
def upOneSampleUE():
    numberjson = request.form['OneSampleUE']
    data = eval(numberjson)
    vector = data["perturbed_vector"]
    print("perturbed_vector:", vector)
    time.sleep(1)
    res = lib.getestimated()
    index = [i + 1 for i in range(len(res))]
    returndate = (dict(zip(index, res)))
    returnjson = json.dumps(returndate)
    print(returnjson)

    return returnjson

@app.route('/getLocation',methods=['GET'])
def getLocation():
    point_x=[]
    point_y=[]
    with open('function/data_normal.csv','r') as f:
        reader=csv.reader(f)
        for i in reader:
            point_x.append(float(i[0]))
            point_y.append(float(i[1]))
    index = [i + 1 for i in range(len(point_x))]
    label_x=(dict(zip(index,point_x)))
    label_y=(dict(zip(index,point_y)))
    return_x=json.dumps(label_x)
    return_y=json.dumps(label_y)
    print(return_x)
    print(return_y)
    dic={"label_x":return_x,"label_y":return_y}
    return jsonify(dic)

@app.route('/getCluster',methods=['GET'])
def getCluster():
    data=pd.read_csv('function/data_normal.csv',header=None)
    dataset=np.array(data)
    tp,label,sse,labels_list=lib.DPkmeans(dataset,k=5,iters=8,totalepslion=5,allocation=0)
    print(len(labels_list))
    index = [i + 1 for i in range(len(label))]
    dic={}
    for i in range(len(labels_list)):
        l=(dict(zip(index,labels_list[i])))
        dic[str(i)]=json.dumps(l)


    return jsonify(dic)

if __name__ == '__main__':
    app.run(debug=True)
