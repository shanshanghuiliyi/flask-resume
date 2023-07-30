import base64

import requests
from flask import Flask, render_template, request, jsonify, Response, json, abort, make_response, redirect, session
from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'
CORS(app, supports_credentials=True)

# 登录状态标志
logged_in = False


# @app.route('/')
# def name():
#     return render_template('name.html')


# @app.route('/a1', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # 获取表单数据
#         email = request.form.get('email')
#         password = request.form.get('password')
#         code = request.form.get('code')
#         # 合并数据并提交到接口
#         data = {"username": email,"password": password}
#         print(data)
#         headers = {
#             "Content-Type": "application/json"
#         }
#         response = requests.post('http://8.130.26.106:8080/login', params=data, headers=headers)
#         return jsonify(response.json())
#     return render_template('11111.html')

# 检查登录状态的中间件函数
@app.before_request
def check_login():
    # 获取当前请求的路径
    path = request.path

    # 如果未登录，并且当前路径不是登录页，则跳转到登录页
    if not logged_in and path != '/login':
        return redirect('/login')


@app.route('/jianli', methods=['POST', 'GET'])
def jianli():
    if request.method == 'POST':
        name = request.form['Name']
        job = request.form['Job']
        return render_template("jianli.html", name=name, job=job)


@app.route('/detail', methods=['POST', 'GET'])
def detail():
    if request.method == 'POST':
        resumeid = request.get_data()
        return render_template("picture_detail.html", resumeid=resumeid)
    else:
        return make_response("Request method not supported", 405)


@app.route('/write')
def write():
    return render_template('jianli.html')


@app.route('/')
def form():
    return render_template('index.html')


@app.route('/login')
def login():
    global logged_in
    logged_in = True
    return render_template('login.html')


@app.route('/before')
def before():
    return render_template('before.html')


@app.route('/after')
def after():
    return render_template('after.html')


@app.route('/manage')
def manage():
    return render_template('manage.html')


@app.route('/client')
def client():
    return render_template('client.html')


@app.route('/hr')
def hr():
    return render_template('hr.html')


@app.route('/fit')
def fit():
    return render_template('fit.html')


@app.route('/chief')
def chief():
    return render_template('chief.html')


@app.route('/organize')
def organize():
    return render_template('organize.html')


@app.route('/picture')
def picture():
    return render_template('picture.html')


@app.route('/picture_detail')
def picture_detail():
    return render_template('picture_detail.html')


@app.route('/pie_nest_data')
def pie_nest_data():
    data_list = {}
    data1 = ['公众号：Python研究者', '直达', '营销广告', '搜索引擎', '邮件营销', '联盟广告', '视频广告', '百度', '谷歌',
             '必应', '其他']
    data_list['data1'] = data1
    data2 = [
        {'value': 2000, 'name': 'Python研究者', 'selected': True},
        {'value': 1548, 'name': '搜索引擎'},
        {'value': 775, 'name': '直达'},
        {'value': 679, 'name': '营销广告'}
    ]
    data_list['data2'] = data2
    data3 = [
        {'value': 1048, 'name': '百度'},
        {'value': 335, 'name': '直达'},
        {'value': 310, 'name': '邮件营销'},
        {'value': 251, 'name': '谷歌'},
        {'value': 234, 'name': '联盟广告'},
        {'value': 147, 'name': '必应'},
        {'value': 135, 'name': '视频广告'},
        {'value': 102, 'name': '其他'}
    ]
    data_list['data3'] = data3
    return Response(json.dumps(data_list), mimetype='application/json')


@app.route('/pie-nest')
def pie_nest():
    return render_template('pie-nest.html')


@app.route('/data', methods=['GET', 'POST'])  # 路由
def data():
    global json_re
    global num
    '''receive data'''
    recv_data = request.get_data()
    if recv_data:
        json_re = json.loads(recv_data)
        print(json_re)
    else:
        print("receive data is empty")

    '''send data'''
    return json.dumps('保存成功')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.after_request
def after(resp):
    '''
    被after_request钩子函数装饰过的视图函数
    ，会在请求得到响应后返回给用户前调用，也就是说，这个时候，
    请求已经被app.route装饰的函数响应过了，已经形成了response，这个时
    候我们可以对response进行一些列操作，我们在这个钩子函数中添加headers，所有的url跨域请求都会允许！！！
    '''
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


# 反向代理：所有/api开头的请求，去除/api前缀后，都会被转发到http://8.130.26.106:5000/
# 例如/api/user/login会被转发到http://8.130.26.106:5000/user/login
SITE_NAME = 'http://8.130.26.106:8080'


# @app.route捕获所有/api开头的请求
@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    print(path)
    print(f'{SITE_NAME}/{path}')
    # global SITE_NAME
    # headers = {"User-Agent": f"{request.user_agent}"}
    # 遍历请求头，复制请求头转发到目标网站
    headers = {key: value for (key, value) in request.headers if key != 'Host'}
    print(headers)

    if request.method == 'GET':
        # 请求目标网站，携带请求头和参数
        resp = requests.get(f'{SITE_NAME}/{path}', headers=headers, params=request.args)
        # 复制响应头，转发到客户端
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        # 构建响应。将请求后端的响应内容，响应状态码和响应头，复制到新的响应对象中
        response = Response(resp.content, resp.status_code, headers)
        print(request.user_agent)
        print(request.path)
        # 返回响应
        return response
    if request.method == 'POST':
        print(request.get_data())
        # 请求目标网站，携带请求头和参数，包括表单参数（request.get_data就是表单）
        resp = requests.post(f'{SITE_NAME}/{path}', headers=headers, data=request.get_data())
        # 复制响应头，转发到客户端
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        # 构建响应。将请求后端的响应内容，响应状态码和响应头，复制到新的响应对象中
        response = Response(resp.content, resp.status_code, headers)
        print(request.user_agent)
        print(request.path)
        return response
    if request.method == 'PUT':
        # 请求目标网站，携带请求头和参数，包括表单参数（request.get_data就是表单）
        resp = requests.put(f'{SITE_NAME}/{path}', headers=headers, data=request.get_data())
        # 复制响应头，转发到客户端
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        # 构建响应。将请求后端的响应内容，响应状态码和响应头，复制到新的响应对象中
        response = Response(resp.content, resp.status_code, headers)
        print(request.user_agent)
        print(request.path)
        return response
    if request.method == 'DELETE':
        # 请求目标网站，携带请求头和参数，包括表单参数（request.get_data就是表单）
        resp = requests.delete(f'{SITE_NAME}/{path}', headers=headers, data=request.get_data())
        # 复制响应头，转发到客户端
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        # 构建响应。将请求后端的响应内容，响应状态码和响应头，复制到新的响应对象中
        response = Response(resp.content, resp.status_code, headers)
        print(request.user_agent)
        print(request.path)
        return response


if __name__ == '__main__':
    app.run(debug=True)
