import re
from flask import Flask, render_template, request, redirect, session, jsonify
from sklearn.ensemble import RandomForestClassifier

import classify
from DBConnection import Db
static_path="D:\\project\\vishnupriya\\food_recognition\\food_recognition\\static\\"
app = Flask(__name__)
app.secret_key="hai"



@app.route('/')
def ad_login():
    return render_template("login.html")

@app.route('/login_post',methods=["post"])
def login_post():
    username=request.form["textfield"]
    password=request.form["textfield2"]
    db = Db()
    qry = "select * from login where user_name='"+username+"' AND password='"+password+"'"
    res=db.selectOne(qry)
    if res is not None:
        if res["user_type"]=="admin":
            return render_template("admin/admin_home.html")
    else:
        return render_template("login.html")

@app.route('/ahome')
def ahome():
    return render_template("admin/admin_home.html")



@app.route('/food_add')
def food_add():
    return render_template("admin/fooditemadd.html")


@app.route('/food_add_post',methods=["post"])
def food_add_post():
    name=request.form["textfield"]
    Description=request.form["textarea"]
    photo=request.files["fileField"]

    photo.save(static_path+"food\\"+photo.filename)
    path="static/food/"+photo.filename

    db=Db()
    qry="insert into fooditem(name,image,description)values('"+name+"','"+path+"','"+Description+"')"

    db.insert(qry)
    return render_template("admin/fooditemadd.html")

@app.route('/foodview')
def foodview():
    db=Db()
    qry="select * from fooditem"
    res1=db.select(qry)
    return render_template("foodview.html",data=res1)

@app.route('/edit_fud/<id>')
def edit_fud(id):
    db=Db()
    qry="select * from fooditem where food_id='"+str(id)+"'"
    res=db.selectOne(qry)
    session['idd']=id
    return render_template('fooditem2.html',data=res)

@app.route('/food_edit_post',methods=["post"])
def food_edit_post():

    fid=request.form["fid"]
    Name=request.form["textfield"]

    Description=request.form["textarea"]


    if 'fileField' in request.files:
        Photo = request.files["fileField"]
        if Photo.filename!='':
            print("1")

            Photo.save(static_path+"food\\"+Photo.filename)
            path="static/"+Photo.filename

            db=Db()
            qry="update fooditem  set Name='"+Name+"',image='"+path+"',description='"+Description+"' where food_id='"+fid+"'"
            print(qry)

            db.update(qry)
        else:
            print("11")
            db = Db()
            qry = "update fooditem  set Name='" + Name + "',description='" + Description + "' where food_id='"+ fid+"'"


            db.update(qry)


    else:
        print("111")
        db = Db()
        qry = "update fooditem  set Name='"+Name+"',description='"+Description+"' where food_id='"+fid+"'"

        db.update(qry)
    return foodview()

@app.route('/del_fud/<id>')
def del_fud(id):
    db=Db()
    qry="delete from fooditem where food_id='"+str(id)+"'"
    db.delete(qry)
    return foodview()

@app.route('/food_search')
def food_search():
    return render_template("fooditem3.html")

@app.route('/food_search_post',methods=["post"])
def food_search_post():
    Name1=request.form["textfield"]

    db=Db()
    qry="select food_id,name,image from fooditem"

    db.select(qry)
    return render_template("fooditem3.html")

@app.route('/ad_upload')
def ad_upload():
    return render_template("admin/admin_upload.html",k=0)

@app.route('/ad_upload_post',methods=["post"])
def ad_upload_post():
    
    photo=request.files["fileField"]
    photo.save(static_path+"History\\"+photo.filename)
    result,score=classify.check(static_path+"History\\"+photo.filename)
    path="static/History/"+photo.filename
    db=Db()
    qry="insert into history(user_id,image,date,result)values(0,'"+path+"',curdate(),'"+str(result)+"')"
    db.insert(qry)
    import nutrition as nt
    ss = nt.view(str(result))
    return render_template("admin/admin_upload.html",Result=result,Path=path,Score=score, calories=ss[1], serving=ss[2], totalfat=ss[3],
                   saturatedfate=ss[4], protein=ss[5], sodium=ss[6], pottassium=ss[7], cholesterol=ss[8],
                   carbohydrates=ss[9], fibre=ss[10], sugar=ss[11],k=1)


@app.route('/food_userview')
def food_userview():
    db=Db()
    qry="select * from user"
    res1=db.select(qry)
    return render_template("viewuser.html",data=res1)
@app.route('/food_userview_post',methods=["post"])
def food_userview_post():
    db=Db()
    search=request.form['textfield']
    qry="select * from user where name like '%"+search+"%'"
    res1 = db.select(qry)
    return render_template("viewuser.html",data=res1)

@app.route('/and_login',methods=["post"])
def and_login():
    username=request.form["uname"]
    password=request.form["paswd"]
    db = Db()
    qry = "select * from login where user_name='"+username+"' AND password='"+password+"'"
    res=db.selectOne(qry)
    if res is not None:
        if res["user_type"]=="user":
            return jsonify(status='ok',lid=res['login_id'])
        else:
            return jsonify(status='No')
    else:
        return jsonify(status='No')


@app.route('/and_signup',methods=["post"])
def and_signup():
    Name=request.form["name"]
    Photo=request.form["photo"]
    Dob=request.form["dob"]
    Gender=request.form["gender"]
    Email=request.form["email"]
    Phone=request.form["phn"]
    Pin = request.form["pincode"]
    Place = request.form["place"]
    City=request.form["city"]
    State=request.form["stat"]

    Password=request.form["paswd"]
    import time
    import base64
    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)
    a = base64.b64decode(Photo)
    fh = open("D:\\project\\vishnupriya\\food_recognition\\food_recognition\\static\\User\\" + timestr + ".jpg", "wb")
    path = "/static/User/" + timestr + ".jpg"
    fh.write(a)
    fh.close()
    db = Db()
    qry2 = "insert into login(user_name,password,user_type)values('" + Email + "','" + Password + "','user')"
    print(qry2)
    lid=db.insert(qry2)
    qry1="insert into user (login_id,name,dob,gender,email,phone,pin,place,city,state,image)values('"+str(lid)+"','"+ Name+"','"+ Dob +"','"+Gender+"','"+Email+"','"+Phone+"','"+Pin +"','"+Place+"','"+City+"','"+State+"','"+path+"')"
    print(qry1)

    db.insert(qry1)

    return jsonify(status="OK")
    pass
@app.route('/and_fooditem',methods=["post"])
def and_fooditem():
    db=Db()
    qry1="select *from fooditem"
    res=db.select(qry1)
    return jsonify(status='ok',data=res)
@app.route('/and_profile',methods=["post"])
def andp():
    db=Db()
    lid=request.form["lid"]
    qry1="select *from user where login_id='"+lid+"'"
    res=db.select(qry1)
    return jsonify(status='ok',name=res['name'],dob=res['dob'],gender=res["gender"],email=res["email"],phone=res["phone"],pin=res["pin"],place=res["place"],city=res["city"],state=res["state"],image=res["image"])
@app.route('/and_history',methods=["post"])
def and_hstory():
    lid=request.form["lid"]
    db=Db()
    qry1="select * from history where user_id='"+lid+"'"
    res=db.select(qry1)
    return jsonify(status='ok',data=res)

@app.route('/and_upload',methods=["post"])
def and_upload():
    image=request.form['upimg']
    User_id=request.form['user_id']
    import time
    import base64
    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)
    a = base64.b64decode(image)
    fh = open(r"D:\project\vishnupriya\food_recognition\food_recognition\\static\\History\\" + timestr + ".jpg", "wb")
    path = "/static/History/" + timestr + ".jpg"
    fh.write(a)
    fh.close()
    db=Db()
    result, score = classify.check(static_path + "History\\" +  timestr + ".jpg")
    # qry1="insert into fooditem(name,image,description)values('"+name+"','"+path+"','"+Description+"')"
    qry2="insert into History(user_id,image,date)values('"+User_id+"','"+path+"',curdate())"
    print(qry2)
    db.insert(qry2)

    import nutrition as nt
    ss=nt.view(str(result))

    return jsonify(status='ok',result=str(result),score=str(score),calories=ss[1],serving=ss[2],totalfat=ss[3],saturatedfat=ss[4],protein=ss[5],sodium=ss[6],pottassium=ss[7],cholesterol=ss[8],carbohydrates=ss[9],fibre=ss[10],sugar=ss[11])


@app.route("/and_recommendation", methods=['post'])
def and_recommendation():
    height=request.form['height']
    weight=request.form['weight']
    bf_meals=request.form['bf_meals']
    af_meals=request.form['af_meals']
    fname=request.form['fname']
    print(fname)
    ftype=0
    if fname=="apple pie":
        ftype=0
    elif fname=="baby back ribs":
        ftype=1

    ar=[]
    ar.append(float(height))
    ar.append(float(weight))
    ar.append(float(bf_meals))
    ar.append(float(af_meals))
    ar.append(float(ftype))
    import numpy as np
    testval=np.array([ar])

    import pandas as pd
    data=pd.read_csv(r"D:\project\vishnupriya\food_recognition\food_recognition\static\dataset.csv")
    attributes=data.values[1:, :5]
    labels=data.values[1:, 5]
    clf=RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(attributes, labels)
    pred=clf.predict(testval)
    print("Attributes : ", testval)
    print("Prediction  :  ", pred)
    if pred[0]==0:
        return jsonify(status="ok", data=fname+ " Not Recommended")
    elif pred[0]==1:
        return jsonify(status="ok", data=fname + " Recommended")


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

