# flask server run
# 1. app.run() < localhost(127.0.0.1)
# 2. app.run("ipv4") > ipv4 > 10.10.141.xx > 10.10.141 에 있는 모두 접속가능
# 3. app.run("0.0.0.0") > 나를 바라볼 수 있는 누구나 (local, ipv4)


# harman2 폴더 내 > server 폴더 내 > exam_01.py
# 프롬프트 server 폴더로 바꿔야함

# Client > Server : request
# Server > Client : response

# Python server
# 1. flask  : 마이크로 웹 프레임워크 (코드가 작고 가볍고 간단, 12,000 line)
# 2. Django : 모든 기능이 포함(풀패키지), flask보다 10~20배 무겁다.

# 가상환경 변경
# (우측 하단 3.9.13 버전 클릭) or (ctrl + shift + P : 인터프리터 검색 > 인터프리터 선택) => (harman) 선택

# ctrl + L : Terminal Clear

# import sys
# print(sys.executable)


# 필요한 기능만 Custom해서 사용한다. = 가볍고 간단하게
# from flask import Flask, render_template > ,로 구분 가능

from flask import Flask               # route 경로, run 서버 실행 (대문자>클래스)
from flask import render_template     # html load               (소문자>함수)
from flask import request             # 사용자가 보낸 정보 관련 
from flask import redirect            # 페이지 이동
from flask import make_response       # 페이지 이동 시 정보 유지

# 파일 이름 보안처리 라이브러리
from werkzeug.utils import secure_filename



# aws.py안에 detect 함수만 load
from aws import detect_labels_local_file
from aws import compare_faces as cf         # 얼굴 비교


import os
# static 폴더가 없다면 만들어라
if not os.path.exists("static"):
    os.mkdir("static")


#////////////////////////////////////////////////////////////////////////////
app = Flask(__name__) # 전달인자: __name__
@app.route("/")

def index():
    #return '<h1 style="color:red;">Hello World</h1>'
    #return render_template("exam01.html")
    #return "Moon Web Page"
    return render_template("index.html")

    # flask는 templates, static folder > 딱 2개만 경로를 잡을 수 있다.


#////////////////////////////////////////////////////////////////////////////
@app.route("/compare", methods=["POST"])
def compare_faces():
    # /detect 와 거의 동일하다. (file이 2개가 됐을뿐)
    # 1. compare로 오는 file1, 2를 받아서 static 폴더에 save.
    if request.method == "POST":
        file1 = request.files["file1"]
        file2 = request.files["file2"]

        file1_filename = secure_filename(file1.filename)
        file2_filename = secure_filename(file2.filename)

        file1.save("static/"+ file1_filename)
        file2.save("static/"+ file2_filename)

    # 2. 이 때, secure_filename 사용해서 aws.py 얼굴 비교 aws 코드 사용
    # 이 결과를 웹페이지에 "동일 인물일 확률 ~% 입니다." 출력
    # 3. aws.py안에 함수를 불러오기

        r = cf("static/" + file1_filename, "static/" + file2_filename)
                
    return r


#////////////////////////////////////////////////////////////////////////////
@app.route("/detect", methods=["POST"])
def detect_label():
    #flask에서 보안 규칙상 파일 이름을 secure처리 필요

    if request.method == "POST":
        file = request.files["file"]
        # file을 static 폴더에 secure 처리 후 file_name에 저장하고, 
        file_name = secure_filename(file.filename)
        file.save("static/" + file_name)
        
        # 해당 경로를 detect 함수에 전달
        r = detect_labels_local_file("static/" + file_name)

    return r



#////////////////////////////////////////////////////////////////////////////
@app.route("/secret", methods=["POST"])
def box():
    try:
        if request.method == "POST":
            # get방식 > args[key], post방식 > form[key]
            hidden = request.form["hidden"]
            return f"비밀 정보: {hidden}"
    except:
        return "데이터 전송 실패" # 이거 작동 안함, Finally도 안됨 > Method Not Allowed 뜸



#////////////////////////////////////////////////////////////////////////////
@app.route("/login", methods=["GET"])
def login():
    if request.method == "GET":

        # 페이지가 이동하더라도 정보를 남겨 사용하자

        login_id = request.args["login_id"]
        login_pw = request.args["login_pw"]

        if login_id == "moon" and login_pw == "1234":
            # 로그인 성공
            response = make_response(redirect("/login/success"))
            # 페이지 이동시 login_id 정보를 유지하기 위해 make_response를 쓴다.
            response.set_cookie("user", login_id)
            return response

        else:
            # 로그인 실패
            return redirect("/")

#////////////////////////////////////////////////////////////////////////////
@app.route("/login/success", methods=["GET"])
def login_success():
    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다."


if __name__ == "__main__":
    app.run(host="0.0.0.0") # 내 로컬 IP가 들어감 


# 127.0.0.1 뜨면 성공, Ctrl + Click하면 server로 이동