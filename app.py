
from flask import Flask
from flask import request
import os
import json
import time

app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

@app.route('/')
def test():
    return '服务器正常运行!!!'



#此方法处理用户注册
# @app.route('/register',methods=['POST'])
# def register():
#     username=request.form['username']
#     password=request.form['password']
#
#     print('username:'+username)
#     print('password:'+password)
#     return '连接成功'

@app.route('/connect',methods=['GET'])
def connect():
    print("服务器连接成功")
    return '服务器连接成功'

@app.route('/upload',methods=['POST'])
def func():
    datajson = request.form['datajson']

    print('datajson:' + datajson)
    return 'json接收成功'

@app.route('/upOneSample',methods=['POST'])
def func1():
    onesamplejson=request.form['oneSample']
    data= eval(onesamplejson)
    key=data["key"]
    seed=data["hashseed"]
    print("key:",key,"hashseed:",seed)
    time.sleep(5)

    candidate=[8,21,2,48,101,11,30,28,18,17,15,6,3,67,7,89,29,1,98,13,64,92,66,4,1973,88,32,10,63,49,52,83,23,19,93,57,
               2285,142,40,20]
    index=[i+1 for i in range(len(candidate))]
    returndate=(dict(zip(index,candidate)))
    returnjson=json.dumps(returndate)
    print(returnjson)
    return returnjson


if __name__ == '__main__':
    app.run(debug=True)

