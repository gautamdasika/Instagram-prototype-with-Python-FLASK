from flask import Flask,request,render_template,session,url_for,redirect
app = Flask(__name__)
from pymongo import MongoClient
import base64,os,sys,time
from bson.objectid import ObjectId

maxsize=200000
app.secret_key = "secretkey"
MONGODB_HOST = '104.197.29.113'
MONGODB_PORT = 27017
MONGODB_ADDRESS = 'mongodb://104.197.29.113:27017/'
'''
client = MongoClient('mongodb://104.197.29.113:27017/')
    db = client.mydb
    post = {"author": "Mike",
            "text": "My first blog post!"}

    posts = db.mycollection
    post_id = posts.insert_one(post).inserted_id
    print "postid = {}".format(post_id)
'''
@app.route('/')
def hello_world():
    #if 'username' in session:
    #   return render_template("home.html")
    print time.clock()
    return render_template("login.html")

@app.route('/signup',methods=["POST"])
def signup():
    uname=request.form['uname']
    pwd=request.form['pwd']
    grp=request.form['grp']
    client = MongoClient(MONGODB_ADDRESS)
    db = client.mydb
    post = {"username": uname,
            "password": pwd,
            "group": grp}

    users = db.users
    post_id = users.insert_one(post).inserted_id
    print post_id
    return render_template("login.html")


@app.route('/search',methods=["POST"])
def search():
    k=request.form['keyword']
    st = time.time()
    images = []
    ids = []
    comments = []
    dbs = time.time()
    client = MongoClient(MONGODB_ADDRESS)
    db = client.mydb
    # result = db.images.find({"username": "anonymous"})
    result = db.images.find().limit(int(k))
    dbd = time.time() - dbs
    for image in result:
        images.append(image['image'])
        ids.append(str(image['_id']))
        print image['_id']
    result1 = db.comments.find()
    for comment in result1:
        comments.append(comment)
    # decode = base64.b64decode(image_cont)
    # img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(image_cont)
    delay = time.time() - st
    return render_template("images.html", images=zip(images, ids), comments=comments, delay=delay, dbd=dbd)

@app.route('/login',methods=["POST"])
def login():
    st=time.time()
    uname = request.form['uname']
    pwd = request.form['pwd']
    dbs=time.time()
    client = MongoClient(MONGODB_ADDRESS)
    db = client.mydb
    result = db.users.find({"username": uname, "password": pwd})
    dbd=time.time()-dbs
    if result:
        for row in result:
            session['username']=uname
            session['group']=row['group']
            print session['group']
            delay =time.time()-st
            return render_template("home.html", delay=delay, dbd=dbd)

    return "failure"
@app.route('/upload1',methods=["GET","POST"])
def upload1():
    st=time.time()
    ufile=request.files['ufile']
    ct=time.time()
    #filesize = os.stat(ufile.filename).st_size
    #num=db.images.find({"username": session['username']}).count()
    #print num
    #if num>5:
    #    return "exceeded max no. of files"
    #print filesize
    #if filesize>maxsize:
     #   return "image too big"
    with open(ufile.filename, "rb") as new:
        tstring = new.read()
    post = {"text": tstring}
    dbs=time.time()
    client = MongoClient(MONGODB_ADDRESS)
    db = client.mydb
    post_id = db.texts.insert_one(post).inserted_id
    dbd=time.time()-dbs
    print post_id
    #decode = encoded_string.decode()
    #img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(decode)
    delay=time.time()-st
    return tstring+str(delay)+"is total delay"+str(dbd)+"is db delay"
@app.route('/upload',methods=["GET","POST"])
def upload():
    st=time.time()
    ufile=request.files['ufile']
    ct=time.time()
    #filesize = os.stat(ufile.filename).st_size
    #num=db.images.find({"username": session['username']}).count()
    #print num
    #if num>5:
    #    return "exceeded max no. of files"
    #print filesize
    #if filesize>maxsize:
     #   return "image too big"
    with open(ufile.filename, "rb") as new:
        encoded_string = base64.b64encode(new.read())
    post = {"image": encoded_string,
            "username": session['username'],
            "time": ct,
            "group": session['group']}
    dbs=time.time()
    client = MongoClient(MONGODB_ADDRESS)
    db = client.mydb
    post_id = db.images.insert_one(post).inserted_id
    dbd=time.time()-dbs
    print post_id
    decode = encoded_string.decode()
    img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(decode)
    delay=time.time()-st
    return img_tag+str(delay)+"is total delay"+str(dbd)+"is db delay"
@app.route('/gettext',methods=["GET","POST"])
def gettext():
    k=request.form['key']
    print "key is"
    print k
    st=time.time()
    texts=[]
    times=[]
    dbs=time.time()
    t1=time.time()
    client = MongoClient(MONGODB_ADDRESS)
    db = client.mydb
    #result = db.images.find({"username": "anonymous"})
    result = db.texts.find()
    te1=time.time()-t1
    t11=time.time()
    for t in result:
        t2=time.time()
        print "text is "
        print t
        if k in t['text']:
            texts.append(t['text'])
            te2=time.time()-t2
            times.append(te2)
    te3=time.time()-t11

    return render_template("texts.html", texts=texts, te1=te1, times=times, te3=te3)
@app.route('/getimages',methods=["GET","POST"])
def getimages():
    st=time.time()
    images=[]
    ids=[]
    comments=[]
    dbs=time.time()
    client = MongoClient(MONGODB_ADDRESS)
    db = client.mydb
    #result = db.images.find({"username": "anonymous"})
    result = db.images.find()
    dbd=time.time()-dbs
    for image in result:
        images.append(image['image'])
        ids.append(str(image['_id']))
        print image['_id']
    result1 = db.comments.find()
    for comment in result1:
        comments.append(comment)
    #decode = base64.b64decode(image_cont)
    #img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(image_cont)
    delay=time.time()-st
    return render_template("images.html", images=zip(images,ids), comments=comments, delay=delay, dbd=dbd)

@app.route('/userimages',methods=["GET","POST"])
def userimages():
    images=[]
    ids=[]
    comments=[]
    client = MongoClient(MONGODB_ADDRESS)
    db = client.mydb
    uname=request.form['username']
    #result = db.images.find({"username": "anonymous"})
    result = db.images.find({"username": uname})
    for image in result:
        images.append(image['image'])
        ids.append(str(image['_id']))
        print image['_id']
    result1 = db.comments.find()
    for comment in result1:
        comments.append(comment)
    #decode = base64.b64decode(image_cont)
    #img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(image_cont)
    return render_template("images.html", images=zip(images,ids), comments=comments)

@app.route('/manageimage',methods=["GET","POST"])
def manageimage():
    client = MongoClient(MONGODB_ADDRESS)
    db = client.mydb
    if request.form['action']=="delete":
        id=request.form['imid']
        print id
        result = db.images.delete_one({"_id": ObjectId(id),"username": session['username']})
        result1 = db.comments.delete_many({"imageid": id, "username": session['username']})
        return str(result.deleted_count)+str(result1.deleted_count)
    elif request.form['action']=="comment":
        comment=request.form['comment']
        print comment
        id=request.form['imid']
        print id
        post={"imageid":id,"comment":comment, "username":session['username']}
        result=db.comments.insert_one(post).inserted_id
        return redirect(url_for('getimages'))

@app.route('/deletecmt',methods=["GET","POST"])
def deletecmt():
    client = MongoClient(MONGODB_ADDRESS)
    db = client.mydb
    id = request.form['id']
    result = db.comments.delete_one({"_id": ObjectId(id), "username": session['username']})
    return redirect(url_for('getimages'))


@app.route('/changegroup',methods=["GET","POST"])
def changegroup():
    return "reached"

@app.route('/groupimages',methods=["GET","POST"])
def groupimages():
    if request.form['action']=="GET GROUP IMAGES":
        images = []
        ids = []
        grps=[]
        time=[]
        comments = []
        client = MongoClient(MONGODB_ADDRESS)
        db = client.mydb
        grp = request.form['grp']
        # result = db.images.find({"username": "anonymous"})
        result = db.images.find({"group": grp})
        for image in result:
            images.append(image['image'])
            ids.append(str(image['_id']))
            grps.append(str(image['group']))
            time.append(str(image['time']))
            print image['_id']
        result1 = db.comments.find()
        for comment in result1:
            comments.append(comment)
        # decode = base64.b64decode(image_cont)
        # img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(image_cont)
        return render_template("group.html", images=zip(images, ids, grps, time), comments=comments)
    else:
        client = MongoClient(MONGODB_ADDRESS)
        db = client.mydb
        grp = request.form['grp']
        session['group'] = grp
        result = db.users.update_one({"username": session['username']},
                                     {
                                         "$set": {
                                             "group": session['group']
                                         }}
                                     )
        return render_template("home.html")

@app.route('/deleteimage', methods=["GET", "POST"])
def deleteimages():
    st=time.time()
    images = []
    ids = []
    grps = []
    times = []
    comments = []
    ct=request.form['mins']
    grp = request.form['grp']
    dbs=time.time()
    client = MongoClient(MONGODB_ADDRESS)
    db = client.mydb
    # result = db.images.find({"username": "anonymous"})
    result = db.images.find({"group": grp})
    for image in result:
        if int(image['time']) - int(time.time()) < ct:
            result = db.images.delete_one({"_id": ObjectId(image['_id'])})
            continue
        images.append(image['image'])
        ids.append(str(image['_id']))
        grps.append(str(image['group']))
        times.append(str(image['time']))
        print image['_id']
    dbd=time.time()-dbs
    result1 = db.comments.find()
    for comment in result1:
        comments.append(comment)
    # decode = base64.b64decode(image_cont)
    # img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(image_cont)
    delay=time.time()-st
    return render_template("group.html", images=zip(images, ids, grps, times), comments=comments, delay=delay,dbd=dbd)
#@app.route('/changegrp',methods=["GET","POST"])
def changegrp():

    grp=request.form['grp']
    session['group']=grp
    result = db.users.update_one({"username": session['username']},
        {
            "$set": {
                "group": session['group']
            }}
    )
    return render_template("home.html")
@app.route('/logout')
def logout():
    st=time.time()
    session.pop('username', None)
    session.pop('group', None)
    delay = time.time()-st
    print delay
    return render_template("login.html",delay=delay)
if __name__ == '__main__':
    app.run()
