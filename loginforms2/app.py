import sqlite3
from flask import Flask,render_template,request, redirect, url_for,send_file,jsonify
from datetime import date
import base64
import io


app = Flask(__name__)


# Global variables
mark_list = []
LoggedIn=False

@app.route('/admins',methods=['GET','POST'])
def alogin():
    return render_template('adminlogin.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('logins.html')

@app.route("/faculty-login", methods=["POST"])
def flogin():
    if  request.method == 'POST':
        fusername = request.form.get('fusername')
        fpassword = request.form.get("fpassword")
        connection = sqlite3.connect('logins2.db')
        cursor = connection.cursor()
        print(fusername, fpassword)
        query = "SELECT facid, fname, fusername, fpassword FROM Facultyss WHERE fusername = ? AND fpassword = ?"
        cursor.execute(query, (fusername, fpassword))
        results = cursor.fetchall()
        cursor.close()
        print(results)
        
        if len(results) == 0:
            error_message = "Invalid Fusername or Password"  # Set an error message
            return render_template('logins.html', error_message=error_message)  # Pass the message to the template
        else:
        # return render_template('welcomefact.htpps',fname=results[0][1], name=results[0][2], facid=results[0][0])
            
            return redirect(url_for('getprofile',fname=results[0][1], name=results[0][2], facid=results[0][0]))
    return redirect(url_for('login'))
    
@app.route("/getprofile")
def getprofile():
    fname = request.args.get("fname")
    name = request.args.get("name")
    facid = request.args.get("facid")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    # Use parameterized query to prevent SQL injection
    query = f"SELECT * FROM Facultyss WHERE facid={facid}"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    fimage=results[0][-1]
    fimage_base64=base64.b64encode(fimage).decode('utf-8')
    
    return render_template('welcomefact.html', name=name,facid=facid, fname=fname,  is_profile=True, profileresults=results,fimgres=fimage_base64)

@app.route('/inserts-data', methods=['POST','GET'])
def insertsData():
    if request.method == 'POST':
        sid=request.form.get('sid')
        username=request.form.get('susername') 
        password=request.form.get('spassword')
        name = request.form.get('sname')
        fathername = request.form.get('sfathername')
        mothername=request.form.get('smothername')
        mobilenumber=request.form.get('smobilenumber')
        pmobilenumber=request.form.get('pmobilenumber')
        dob=request.form.get('dob')
        gender=request.form.get('gender')
        email=request.form.get('semail')
        course=request.form.get('scourse')
        year=request.form.get('stuyear')
        sscmarks=request.form.get('sscmarks')
        intermarks=request.form.get('sintermarks')
        aadharnumber=request.form.get('saadharnumber')
        address=request.form.get('address')
        city=request.form.get('city')
        state=request.form.get('state')
        country=request.form.get('country')
        registrationapproved=request.form.get('regapproved')
        image = request.files['image']
        conn = sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Studentss(sid,username,password,name,fathername,mothername,mobilenumber,pmobilenumber,dob,gender,email,course,year,sscmarks,intermarks, aadharnumber,address,city,state,country,registrationapproved,image) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (sid,username,password,name,fathername,mothername,mobilenumber,pmobilenumber,dob,gender,email,course,year,sscmarks,intermarks,aadharnumber,address,city,state,country,registrationapproved,image.read()))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('studentdetails.html')


# @app.route("/admin-login")
# def adminlogin():
#     if request.method=='POST':
#         ausername=request.form.get('ausername')
#         apassword=request.form.get('apassword')
#         if ausername=="admin" and apassword=="admin123":
#             return redirect(url_for('insertsData'))
#     return render_template('adminlogin.htpps')
@app.route("/admin-login", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        ausername = request.form.get('ausername')
        apassword = request.form.get('apassword')
        if ausername == "admin" and apassword == "admin123":
            return redirect('/welcomeadmin')
        else:
            aerror_message = "Invalid Adminusername or Password"  # Set an error message
            return  render_template('adminlogin.html', aerror_message=aerror_message) # Pass the message to the template
    return render_template('adminlogin.html')

@app.route('/welcomeadmin')
def welcomeadmin():
    return render_template('welcomeadmin.html')








@app.route('/insertf-data', methods=['POST','GET'],endpoint='insert_data')
def insert_data():
    if request.method == 'POST':
        facid=request.form.get('facid')
        fusername=request.form.get('fusername')
        fpassword=request.form.get('fpassword')
        fnames = request.form.get('fname')
        fdepartment = request.form.get('fdepartment')
        fdesignation=request.form.get('fdesignation')
        fmobile=request.form.get('fmobilenumber')
        femail=request.form.get('femail')
        fspecification=request.form.get('fspecification')
        faddress=request.form.get('faddress')
        fimage = request.files['fimage']
        conn = sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Facultyss(facid,fusername,fpassword,fname, fdepartment,fdesignation,fmobile,femail,fspecification,faddress,image) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (facid,fusername,fpassword,fnames,fdepartment,fdesignation,fmobile,femail,fspecification,faddress,fimage.read()))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('facultydetails.html')

@app.route('/student-login',methods=['POST'])
def stulogin():
    if  request.method == 'POST':
        username=request.form.get("susername")
        password=request.form.get("spassword")
        connection=sqlite3.connect('logins2.db')
        cursor=connection.cursor()
        print(username,password)
        query = "SELECT *  FROM Studentss WHERE username = ? AND password = ?"
        # query="SELECT username,password FROM students where  username="+username+" password="+password+";"
        cursor.execute(query, (username, password))
        results=cursor.fetchall()
        cursor.close()
        if(results):
            LoggedIn=True
        print(results)
        if(len(results)==0):
            serror_message = "Invalid Susername or Password"  # Set an error message
            return render_template('logins.html', serror_message=serror_message)
        else:
            if(LoggedIn):
                
                return redirect(url_for('spdisplay', sid=results[0][0],suser=results[0][1],sfull=results[0][3]))
            # return render_template('welcomestudent.htpps',student=results[0])
    return redirect(url_for('login'))

@app.route('/logout', methods=['GET'])
def logout():
    LoggedIn=False
    if request.method=="GET":
        # return render_template('logins.htpps')
        return redirect(url_for('login'))


@app.route("/spdisplay")
def spdisplay():
    sid = request.args.get("sid")
    connection=sqlite3.connect('logins2.db')
    cursor=connection.cursor()
    query = "SELECT *  FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid, ))
    results=cursor.fetchall()
    cursor.close()
    image=results[0][-2]
    image_base64=base64.b64encode(image).decode('utf-8')
    if(len(results)==0):
        error_message = "Invalid Username or Password"  # Set an error message
        return render_template('logins.html', error_message=error_message)
    else:
        return render_template('welcomestudent.html',student=results[0], is_profile=True,imgres=image_base64)

@app.route("/smdisplay")
def smdisplay():
    sid = request.args.get("sid")
    connection=sqlite3.connect('logins2.db')
    cursor=connection.cursor()
    query = "SELECT *  FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid, ))
    results=cursor.fetchall()
    query = "SELECT * FROM Markss WHERE sid = ?"
    cursor.execute(query, (sid, ))
    marks = cursor.fetchall()
    cursor.close()
    if(len(results)==0):
        print("please provide valid login details")
    else:
        return render_template('welcomestudent.html',student=results[0], is_marks=True, marks=marks)
    
@app.route("/sadisplay")
def sadisplay():
    susername=request.args.get("suser")
    sid = request.args.get("sid")
    connection=sqlite3.connect('logins2.db')
    cursor=connection.cursor()
    query = "SELECT *  FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid, ))
    results=cursor.fetchall()
    cursor.close()
    if(len(results)==0):
        print("please provide valid login details")
    else:
        return render_template('welcomestudent.html',student=results[0], is_attendance=True,susername=susername)


@app.route("/sndisplay")
def sndisplay():
    sid = request.args.get("sid")
    connection=sqlite3.connect('logins2.db')
    cursor=connection.cursor()
    query = "SELECT *  FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid, ))
    results=cursor.fetchall()
    query = "SELECT * FROM notes"
    cursor.execute(query)
    notes = cursor.fetchall()
    cursor.close()
    if(len(results)==0):
        print("please provide valid login details")
    else:
        return render_template('welcomestudent.html',student=results[0], is_notes=True, notes=notes)

@app.route("/scdisplay")
def scdisplay():
    sid = request.args.get("sid")
    connection=sqlite3.connect('logins2.db',timeout=30)
    cursor=connection.cursor()
    query = "SELECT *  FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid, ))
    results=cursor.fetchall()
    query = "SELECT * FROM jobborad"
    cursor.execute(query)
    jobs = cursor.fetchall()
    cursor.close()
    if(len(results)==0):
        print("please provide valid login details")
    else:
        return render_template('welcomestudent.html',student=results[0], is_career=True, jobs=jobs)

@app.route('/admin-addmarks',methods=['GET','POST'])
def aaddmarks():
    if request.method=="POST":
        sid=request.form.get('sid')
        syear=request.form.get('syear')
        ppsinternal=request.form.get('ppsint')
        ppsexternal=request.form.get('ppsext')
        ppstotal=request.form.get('ppstotal')
        ppsgrade=request.form.get('ppsgrade')
        cdinternal=request.form.get('cdint')
        cdexternal=request.form.get('cdext')
        cdtotal=request.form.get('cdtotal')
        cdgrade=request.form.get('cdgrade')
        slinternal=request.form.get('slint')
        slexternal=request.form.get('slext')
        sltotal=request.form.get('sltotal')
        slgrade=request.form.get('slgrade')
        dppminternal=request.form.get('dppmint')
        dppmexternal=request.form.get('dppmext')
        dppmtotal=request.form.get('dppmtotal')
        dppmgrade=request.form.get('dppmgrade')
        cgpa=request.form.get('cgpa')
        gpa=request.form.get('gpa')
        conn=sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Markss(sid,semister,ppsinternal,ppsexternal,ppstotal,ppsgrade,cdinternal,cdexternal,cdtotal,cdgrade,slinternal,slexternal,sltotal,slgrade,dppminternal,dppmexternal,dppmtotal,dppmgrade,cgpa,gpa) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(sid,syear,ppsinternal,ppsexternal,ppstotal,ppsgrade,cdinternal,cdexternal,cdtotal,cdgrade,slinternal,slexternal,sltotal,slgrade,dppminternal,dppmexternal,dppmtotal,dppmgrade,cgpa,gpa))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('faddmarks.htpps')
    
@app.route('/f-addmarks',methods=['GET','POST'])
def faddmarks():
    fname = request.args.get("fname")
    name = request.args.get("name")
    facid = request.args.get("facid")
    if request.method=="POST":
        sid=request.form.get('sid')
        semister=request.form.get('syear1')
        eninternal=request.form.get('enint')
        enexternal=request.form.get('enext')
        entotal=request.form.get('entotal')
        engrade=request.form.get('engrade')
        m1internal=request.form.get('m1int')
        m1external=request.form.get('m1ext')
        m1total=request.form.get('m1total')
        m1grade=request.form.get('m1grade')
        beeinternal=request.form.get('beeint')
        beeexternal=request.form.get('beeext')
        beetotal=request.form.get('beetotal')
        beegrade=request.form.get('beegrade')
        cheminternal=request.form.get('chemint')
        chemexternal=request.form.get('chemext')
        chemtotal=request.form.get('chemtotal')
        chemgrade=request.form.get('chemgrade')
        syear2=request.form.get('syear2')
        apinternal=request.form.get('apint')
        apexternal=request.form.get('apext')
        aptotal=request.form.get('aptotal')
        apgrade=request.form.get('apgrade')
        ppsinternal=request.form.get('ppsint')
        ppsexternal=request.form.get('ppsext')
        ppstotal=request.form.get('ppstotal')
        ppsgrade=request.form.get('ppsgrade')
        m2internal=request.form.get('m2int')
        m2external=request.form.get('m2ext')
        m2total=request.form.get('m2total')
        m2grade=request.form.get('m2grade')
        engfinternal=request.form.get('engfint')
        engfexternal=request.form.get('engfext')
        engftotal=request.form.get('engftotal')
        engfgrade=request.form.get('engfgrade')
        syear3=request.form.get('syear3')
        dbmsinternal=request.form.get('dbmsint')
        dbmsexternal=request.form.get('dbmsext')
        dbmstotal=request.form.get('dbmstotal')
        dbmsgrade=request.form.get('dbmsgrade')
        javainternal=request.form.get('javaint')
        javaexternal=request.form.get('javaext')
        javatotal=request.form.get('javatotal')
        javagrade=request.form.get('javagrade')
        osinternal=request.form.get('osint')
        osexternal=request.form.get('osext')
        ostotal=request.form.get('ostotal')
        osgrade=request.form.get('osgrade')
        seinternal=request.form.get('seint')
        seexternal=request.form.get('seext')
        setotal=request.form.get('setotal')
        segrade=request.form.get('segrade')
        syear4=request.form.get('syear4')
        pyinternal=request.form.get('pyint')
        pyexternal=request.form.get('pyext')
        pytotal=request.form.get('pytotal')
        pygrade=request.form.get('pygrade')
        msfinternal=request.form.get('msfint')
        msfexternal=request.form.get('msfext')
        msftotal=request.form.get('msftotal')
        msfgrade=request.form.get('msfgrade')
        befainternal=request.form.get('befaint')
        befaexternal=request.form.get('befaext')
        befatotal=request.form.get('befatotal')
        befagrade=request.form.get('befagrade')
        dsinternal=request.form.get('dsint')
        dsexternal=request.form.get('dsext')
        dstotal=request.form.get('dstotal')
        dsgrade=request.form.get('dsgrade')
        syear5=request.form.get('syear5')
        mlinternal=request.form.get('mlint')
        mlexternal=request.form.get('mlext')
        mltotal=request.form.get('mltotal')
        mlgrade=request.form.get('mlgrade')
        cdinternal=request.form.get('cdint')
        cdexternal=request.form.get('cdext')
        cdtotal=request.form.get('cdtotal')
        cdgrade=request.form.get('cdgrade')
        slinternal=request.form.get('slint')
        slexternal=request.form.get('slext')
        sltotal=request.form.get('sltotal')
        slgrade=request.form.get('slgrade')
        dppminternal=request.form.get('dppmint')
        dppmexternal=request.form.get('dppmext')
        dppmtotal=request.form.get('dppmtotal')
        dppmgrade=request.form.get('dppmgrade')
        cgpa=request.form.get('cgpa')
        gpa=request.form.get('gpa')
        conn=sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Markss(sid,semister,eninternal,enexternal,entotal,engrade,m1internal,m1external,m1total,m1grade,beeinternal,beeexternal,beetotal,beegrade,cheinternal,chemexternal,chemtotal,chemgrade,semister2,apinternal,apexternal,aptotal,apgrade,ppsinternal,ppsexternal,ppstotal,ppsgrade,m2internal,m2external,m2total,m2grade,enginternal,engexternal,engtotal,enggrade,semister3,dbmsinternal,dbmsexternal,dbmstotal,dbmsgrade,javainternal,javaexternal,javatotal,javagrade,osinternal,osexternal,osgrade,ostotal,seinternal,seexternal,setotal,segrade,semister4,pyinternal,pyexternal,pytotal,pygrade,msfinternal,msfexternal,msftotal,msfgrade,befainternal,befaexternal,befatotal,befagrade,dsinternal,dsexternal,dstotal,dsgrade,semister5,mlinternal,mlexternal,mltotal,mlgrade,cdinternal,cdexternal,cdtotal,cdgrade,slinternal,slexternal,sltotal,slgrade,dppminternal,dppmexternal,dppmtotal,dppmgrade,cgpa,gpa) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(sid,semister,eninternal,enexternal,entotal,engrade,m1internal,m1external,m1total,m1grade,beeinternal,beeexternal,beetotal,beegrade,cheminternal,chemexternal,chemtotal,chemgrade,syear2,apinternal,apexternal,aptotal,apgrade,ppsinternal,ppsexternal,ppstotal,ppsgrade,m2internal,m2external,m2total,m2grade,engfinternal,engfexternal,engftotal,engfgrade,syear3,dbmsinternal,dbmsexternal,dbmstotal,dbmsgrade,javainternal,javaexternal,javatotal,javagrade,osinternal,osexternal,ostotal,osgrade,seinternal,seexternal,setotal,segrade,syear4,pyinternal,pyexternal,pytotal,pygrade,msfinternal,msfexternal,msftotal,msfgrade,befainternal,befaexternal,befatotal,befagrade,dsinternal,dsexternal,dstotal,dsgrade,syear5,mlinternal,mlexternal,mltotal,mlgrade,cdinternal,cdexternal,cdtotal,cdgrade,slinternal,slexternal,sltotal,slgrade,dppminternal,dppmexternal,dppmtotal,dppmgrade,cgpa,gpa))
        results=cursor.fetchall()
        print(results)
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('welcomefact.html', fname=fname, name=name,facid=facid, add_marks=True)
    # return render_template('faddmarks.html')

@app.route('/getmarks',methods=['GET','POST'])
def getmarks():
    fname = request.args.get("fname")
    if request.method=="POST":
        sid=request.form.get("sid")
        conn=sqlite3.connect('logins2.db')
        cursor=conn.cursor()
        query="select * from Markss where sid="+sid+";"
        cursor.execute(query)
        results=cursor.fetchall()   
        conn.commit()
        cursor.close()
        conn.close()
        print(list[results])
        if(len(results)==0):
            print("invalid number provided ")
        else:
            return render_template('displaymarks.html', fname=fname, sid=sid, results=results)
    return render_template('getmarks.html')



@app.route("/aadd_attendance", methods=["GET", "POST"])
def aadd_attendance():
    global mark_list
    today = date.today()
    def total_days():
        start_date = date(2023, 9, 7)
        return int((today-start_date).days)
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    # Use parameterized query to prevent SQL injection
    query = "SELECT sid, attendance, name FROM Studentss"
    cursor.execute(query)
    students = cursor.fetchall()
    if request.method=="POST":
        for student in students:
            is_present = request.form.get(str(student[0]))
            
            no_of_days_present = (student[1] * (total_days()-1)) / 100
            if is_present=="1":
                no_of_days_present += 1
            new_attendance = int((no_of_days_present / total_days())*100)
            
            query = "UPDATE Studentss SET attendance=? WHERE sid=?"
            cursor.execute(query, (new_attendance, student[0]))
            connection.commit()
            mark_list.append(today)
    cursor.close()
    connection.close()
    if date.today() in mark_list:
        is_completed = True
    else:
        is_completed = False
            
    return render_template("add_attendance.html", students=students, is_completed=is_completed, today=today)



@app.route("/add_attendance", methods=["GET", "POST"])
def add_attendance():
    global mark_list
    today = date.today()
    def total_days():
        start_date = date(2023, 9, 7)
        return int((today-start_date).days)
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    # Use parameterized query to prevent SQL injection
    query = "SELECT sid, attendance, name FROM Studentss"
    cursor.execute(query)
    students = cursor.fetchall()
    if request.method=="POST":
        for student in students:
            is_present = request.form.get(str(student[0]))
            
            no_of_days_present = (student[1] * (total_days()-1)) / 100
            if is_present=="1":
                no_of_days_present += 1
            new_attendance = int((no_of_days_present / total_days())*100)
            
            query = "UPDATE Studentss SET attendance=? WHERE sid=?"
            cursor.execute(query, (new_attendance, student[0]))
            connection.commit()
            mark_list.append(today)
    cursor.close()
    connection.close()
    if date.today() in mark_list:
        is_completed = True
    else:
        is_completed = False
            
    return render_template("add_attendance.html", students=students, is_completed=is_completed, today=today)


@app.route("/aadd_notes",methods=["GET","POST"])
def aadd_notes():
   
    if request.method=="POST":
        subcode=request.form.get('subcode')
        subname=request.form.get('subname')
        sublink=request.form.get('sublink')
        conn=sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes(subcode,subname,sublink) values(?,?,?)',(subcode,subname,sublink))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('insertnotes.html')
 

 
@app.route("/add_notes",methods=["GET","POST"])
def add_notes():
    fname = request.args.get("fname")
    name = request.args.get('name')
    facid = request.args.get("facid")
    if request.method=="POST":
        facname=request.form.get('facname')
        subcode=request.form.get('subcode')
        subname=request.form.get('subname')
        sublink=request.form.get('sublink')
        conn=sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes(facname,subcode,subname,sublink) values(?,?,?,?)',(facname,subcode,subname,sublink))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('welcomefact.html',add_notes=True, name=name, fname=fname, facid=facid)


@app.route('/aadd_jobs',methods=["GET","POST"], endpoint='aadd_jobs')
def aaddjobs():
    if request.method=="POST":
        companyname=request.form.get('companyname')  
        email=request.form.get('email')
        jobposition=request.form.get('jobposition')
        location=request.form.get('location')
        requriments=request.form.get('requriments')
        url=request.form.get('url')
        conn = sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO jobborad(Company_Name,email,JOB_POSITION,location,Requriments,url) VALUES (?,?,?,?,?,?)', (companyname,email,jobposition,location,requriments,url))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('insertjobs.html')
@app.route('/insert_parentdata',methods=["GET","POST"])
def insertpdata():
    if request.method=="POST":
        pid=request.form.get('pid')
        pusername=request.form.get('pusername')
        ppassword=request.form.get('ppassword')
        ssid=request.form.get('ssid')
        conn=sqlite3.connect('logins2.db')
        cursor=conn.cursor()
        cursor.execute('INSERT INTO parents(pid,pusername,ppassword,STUID) VALUES (?,?,?,?)', (pid,pusername,ppassword,ssid))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('insertparentdetails.html')

@app.route('/p_login',methods=['GET','POST'])
def plogin():
    if  request.method == 'POST':
        pusername=request.form.get('pusername')
        ppassword=request.form.get("ppassword")
        connection=sqlite3.connect('logins2.db')
        cursor=connection.cursor()
        print(pusername,ppassword)
        query = "SELECT * FROM parents WHERE pusername = ? AND ppassword = ?"
        # query="SELECT username,password FROM students where  username="+username+" password="+password+";"
        cursor.execute(query, (pusername, ppassword))
        results=cursor.fetchall()
        if(len(results)==0):
            perror_message = "Invalid Pusername or Password"  # Set an error message
            return render_template('logins.html', perror_message=perror_message)
        else:
            return redirect(url_for('ppdisplay', pid=results[0][0],pusername=pusername,stuid=results[0][3]))
            # return render_template('welcomeparent.htpps',pid=results[0][0],pusername=pusername,results=results[0],stuid=results[0][3])
    return redirect(url_for('login'))
       
    
@app.route("/ppdisplay")
def ppdisplay():
    stuid = request.args.get("stuid")
    pusername = request.args.get("pusername")
    conn = sqlite3.connect('logins2.db')
    cursor = conn.cursor()
    query = "SELECT * from Studentss WHERE sid = ?"
    cursor.execute(query, (stuid, ))
    results = cursor.fetchall()
    print(results)
    if(len(results)==0):
        print("No results please try again")
    else:
        return render_template('welcomeparent.html', stuid=stuid, results = results[0], is_profile=True, pusername=pusername)

@app.route('/pmdisplay')
def pmdisplay():
    pid = request.args.get("pid")
    stuid=request.args.get("stuid")
    pusername=request.args.get("pusername")
    # pusername=request.form.get('pusername')
    # stuid=request.form.get('stuid')
    # pid=request.form.get('pid')
    conn=sqlite3.connect('logins2.db')
    cursor = conn.cursor()
    query = "SELECT * From  Markss WHERE sid = ?"
    cursor.execute(query,(stuid,))
    markss=cursor.fetchall()
    print(markss)
    if(len(markss)==0):
        print("no results please try again")
    else:
        return render_template('welcomeparent.html',stuid=stuid,pid=pid,marks=markss[0],pusername=pusername,is_smarks=True)
    
   
@app.route("/padisplay")
def padisplay():
    stuid = request.args.get("stuid")
    pusername=request.args.get("pusername")
    conn=sqlite3.connect('logins2.db')
    cursor = conn.cursor()
    query = "SELECT sid, attendance FROM Studentss WHERE sid = ?"
    cursor.execute(query,(stuid,))
    results=cursor.fetchall()
    if(len(results)==0):
        print("No results please try again")
    else:
        return render_template('welcomeparent.html', stuid=stuid, results = results[0], is_attendance=True, pusername=pusername)

@app.route("/stuprofac",methods=['POST','GET'])
def stuprofac():
    if request.method=='POST':
        facid = request.args.get("facid")
        sids=request.form.get('sids')
        sfull=request.form.get('sfull')
        connection=sqlite3.connect('logins2.db')
        cursor=connection.cursor()
        query="SELECT * from Studentss where sid=? and name=?"
        cursor.execute(query,(sids,sfull))
        results=cursor.fetchall()
        print(results)
        query="select * from Markss where sid=?"
        cursor.execute(query,(sids,))
        marksresults=cursor.fetchall()
        print(marksresults)
        query="select attendance FROM studentss WHERE sid=?"
        cursor.execute(query,(sids,))
        attresults=cursor.fetchall()
        print(attresults)
        query="select * from Facultyss where facid=?"
        cursor.execute(query,(facid,))
        fresults=cursor.fetchall()
        print(fresults)
        if(len(results))==0:
            search_error = "Invalid Sid or UserName"  # Set an error message
            return render_template('searchstudent.html', search_error=search_error)  # Pass the message to the template
        else:
            return render_template('viewstudentdata.html',results=results,sids=results[0][0],marks=marksresults,attendance=attresults[0][0])
    return render_template('searchstudent.html')

@app.route("/ttable")
def ttable():
    susername=request.form.get("susername")
    connection=sqlite3.connect('logins2.db')
    cursor=connection.cursor()
    query = "SELECT *  FROM Studentss WHERE username = ?"
    cursor.execute(query, (susername, ))
    results=cursor.fetchall()
    print(results)
    cursor.close()
    return render_template('timetable.html',susername=susername,results=results)

@app.route("/ttimg")
def ttimg():
    return render_template('dsatimetable.html')

@app.route("/todos")
def todos():
    return render_template('todos.html')

@app.route("/pcomplaint",methods=['POST','GET'])
def pcomplaint():
    sid = request.args.get("sid")
    conn = sqlite3.connect('logins2.db')
    cursor = conn.cursor()
    query = "SELECT * FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid,))
    results = cursor.fetchall()
    if request.method=="POST":
        cid=request.form.get("cid")
        cname=request.form.get("cname")
        cdepartment=request.form.get("cdepartment")
        csection=request.form.get("csection")
        ccategory=request.form.get("ccategory")
        cpriority=request.form.get("cpriority")
        cdescription=request.form.get("cdescription")
        cimage= request.files['cimage']
        cursor.execute('INSERT INTO pcomplaints(crollno,cname,cdepartment,csection,ccategeory,cpriority,descriptions,cimage) VALUES (?,?,?,?,?,?,?,?)', (cid,cname,cdepartment,csection,ccategory,cpriority,cdescription,cimage.read()))
        conn.commit()
        cursor.close()
        conn.close()

    print("Helloo", results, len(results))
    return render_template('welcomestudent.html',student=results[0] if results else None, is_pcomt=True)

@app.route("/hodcom",methods=['POST','GET'])
def hodcom():
    sid = request.args.get("sid")
    conn = sqlite3.connect('logins2.db')
    cursor = conn.cursor()
    query = "SELECT * FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid,))
    results = cursor.fetchall()
    if request.method=="POST":
        hodid=request.form.get("hodid")
        hodname=request.form.get("hodname")
        hoddepartment=request.form.get("hoddepartment")
        hodsection=request.form.get("hodsection")
        hodcategory=request.form.get("hodcategory")
        hodpriority=request.form.get("hodpriority")
        hoddescription=request.form.get("hoddescription")
        hodimage= request.files['hodimage']
        cursor.execute('INSERT INTO hodcomp(hodid,hodname,hoddepartment,hodsection,hodcategory,hodpriority,hoddescription,hodimage) VALUES (?,?,?,?,?,?,?,?)', (hodid,hodname,hoddepartment,hodsection,hodcategory,hodpriority,hoddescription,hodimage.read()))
        conn.commit()
        cursor.close()
        conn.close()
        
    return render_template('welcomestudent.html',student=results[0] if results else None, is_hod=True)

@app.route("/plcom", methods=['POST', 'GET'])
def plcom():
    sid = request.args.get("sid")
    conn = sqlite3.connect('logins2.db')
    cursor = conn.cursor()
    query = "SELECT * FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid,))
    results = cursor.fetchall()
    if request.method == "POST":
        plid = request.form.get("plid")
        plname = request.form.get("plname")
        pldepartment = request.form.get("pldepartment")
        plsection = request.form.get("plsection")
        plcategory = request.form.get("plcategory")
        plpriority = request.form.get("plpriority")
        pldescription = request.form.get("pldescription")
        plimage = request.files['plimage']
        cursor.execute('INSERT INTO plcomp(plid, plname, pldepartment, plsection, plcategory, plpriority, pldescription, plimage) VALUES (?,?,?,?,?,?,?,?)', (plid, plname, pldepartment, plsection, plcategory, plpriority, pldescription, plimage.read()))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('welcomestudent.html',sid=sid, student=results[0] if results else None, is_plcomt=True)

@app.route("/complaintgroup")
def complaintgroup():
    sid = request.args.get("sid")
    connection=sqlite3.connect('logins2.db')
    cursor=connection.cursor()
    query = "SELECT * FROM Studentss WHERE sid = ?"
    cursor.execute(query, (sid, ))
    results=cursor.fetchall()
    cursor.close()
    connection.close()
    print(results)
    if(len(results)==0):
        return "please provide valid login details"
    else:
        return render_template('welcomestudent.html',student=results[0],is_comps=True)
    
    
  

@app.route("/getpcomplaints")
def getpcomplaints():
    name = request.args.get("name")
    facid = request.args.get("facid")
    fname = request.args.get("fname")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM pcomplaints"
    cursor.execute(query)
    results = cursor.fetchall()
    cimage = results[0][-1]
    compresultss = [{'cid': cid, 'cname': cname, 'cdepartment': cdepartment, 'csection': csection,
                     'ccategory': ccategory, 'cpriority': cpriority, 'cdescription': cdescription,'cimage':base64.b64encode(cimage).decode('utf-8')} for
                    cid, cname, cdepartment, csection, ccategory, cpriority, cdescription,cimage in results]
    cursor.close()
    return render_template('welcomefact.html',fname=fname,name=name,compresultss=compresultss, is_pcomplaints=True,facid=facid,cimage=cimage)

@app.route("/getplcomplaints")
def getplcomplaints():
    tpusername=request.args.get("tpusername")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM plcomp"
    cursor.execute(query)
    results = cursor.fetchall()
    plimage = results[0][-1]
    complresultss = [{'cid': plid, 'cname': plname, 'cdepartment': pldepartment, 'csection': plsection,
                     'ccategory': plcategory, 'cpriority': plpriority, 'cdescription': pldescription,'cimage':base64.b64encode(plimage).decode('utf-8')} for
                    plid, plname, pldepartment, plsection, plcategory, plpriority, pldescription,plimage in results]
    cursor.close()
    return render_template('welcometp.html',complresultss=complresultss,is_plcomplaints=True,plimage=plimage,tpusername=tpusername)

@app.route("/deligates")
def deligates():
    return render_template('deligates.html')
@app.route("/tp_login",methods=['GET','POST'])
def tp_login():
    if request.method=="POST":
        tpusername=request.form.get("tpusername")
        tppassword=request.form.get("tppassword")
        print(tpusername,tppassword)
        if(tpusername=="placement" and tppassword=="placement123"):
            return redirect(url_for('alldepartments',tpusername=tpusername))
        else:
            return render_template('deligates.html')
    return redirect(url_for('deligates'))

# @app.route("/ds_students")
# def ds_students():
#         connection=sqlite3.connect('logins2.db')
#         cursor=connection.cursor()
#         query="SELECT * FROM Studentss WHERE course ='ECE';"
#         cursor.execute(query,)
#         results=cursor.fetchall()
#         connection.commit()
#         dsimage=results[0][-2]
#         dsresultss=[{'SID':sid,'SFULLNAME':name,'SFATHERNAME':fathername,'S-MOBNUMBER':mobilenumber,'SGENDER':gender,'SEMAIL':email,'SCOURSE':course,'SSSC':sscmarks,'SINTER':intermarks,'SGPA':aadhaarnumber,'SCITY':city,'SIMAGE':base64.b64encode(dsimage).decode('utf-8')}
#                    for sid,name,fathername,mobilenumber,gender,email,course,sscmarks,intermarks,aadhaarnumber,city,dsimage in results]
#         cursor.close()
#         return render_template('dsstudents.html',ds_students=results[0],dsresultss=dsresultss,dsimage=dsimage)
@app.route("/alldepartments")
def alldepartments():
    tpusername=request.args.get("tpusername")
    return render_template('welcometp.html',is_alldepartments=True,tpusername=tpusername)
    
@app.route("/ds_students")
def ds_students():
    tpusername=request.args.get("tpusername")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course = 'DATASCIENCE';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    dsresultss = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11],'YEAR':row[12],'SSSC': row[13], 'SINTER': row[14], 'SGPA': row[15],'address':row[16],'city':row[17],'state':row[18],'country': row[19],'approvedby':row[20],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[-1]} for row in results]
    cursor.close()
    return render_template('welcometp.html',ds_students=results[0],dsresultss=dsresultss,is_dstp=True,tpusername=tpusername)
@app.route("/ece_students")
def ece_students():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course = 'ECE';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    eceresultss = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html', ece_students=results[0], eceresultss=eceresultss,is_ecetp=True)
@app.route("/aiml_students")
def aiml_students():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course = 'AIML';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    aimlresultss = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html', aiml_students=results[0], aimlresultss=aimlresultss,is_aimltp=True)

@app.route("/civil_students")
def civil_students():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course = 'CIVIL';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    civilresultss = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html', civil_students=results[0], civilresultss=civilresultss,is_civiltp=True)
@app.route("/mech_students")
def mech_students():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course = 'MECHANICAL';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    mechresultss = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html', mech_students=results[0], mechresultss=mechresultss,is_mechtp=True)

@app.route("/cse_students")
def cse_students():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course = 'COMPUTERSCIENCE';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cseresultss = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html', cse_students=results[0], cseresultss=cseresultss,is_csetp=True)

@app.route("/alldepartments_pp")
def alldepartments_pp():
    tpusername=request.args.get("tpusername")
    return render_template('welcomeprincipal.html',is_alldepartments=True,tpusername=tpusername)
    
@app.route("/ds_students_pp")
def ds_students_pp():
    tpusername=request.args.get("tpusername")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course = 'DATASCIENCE';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    dsresultss = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcomeprincipal.html',ds_students=results[0],dsresultss=dsresultss,is_dstp=True,tpusername=tpusername)
@app.route("/ece_students_pp")
def ece_students_pp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course = 'ECE';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    eceresultss = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcomeprincipal.html', ece_students=results[0], eceresultss=eceresultss,is_ecetp=True)
@app.route("/aiml_students_pp")
def aiml_students_pp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course = 'AIML';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    aimlresultss = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcomeprincipal.html', aiml_students=results[0], aimlresultss=aimlresultss,is_aimltp=True)

@app.route("/civil_students_pp")
def civil_students_pp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course = 'CIVIL';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    civilresultss = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcomeprincipal.html', civil_students=results[0], civilresultss=civilresultss,is_civiltp=True)
@app.route("/mech_students_pp")
def mech_students_pp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course = 'MECHANICAL';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    mechresultss = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcomeprincipal.html', mech_students=results[0], mechresultss=mechresultss,is_mechtp=True)

@app.route("/cse_students_pp")
def cse_students_pp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course = 'COMPUTERSCIENCE';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cseresultss = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcomeprincipal.html', cse_students=results[0], cseresultss=cseresultss,is_csetp=True)




















@app.route("/get_spec_students")
def get_spec_students():
    return render_template('welcometp.html',is_get_spec_students=True)

@app.route("/getspecfper")
def getspecfper():
    firstper = float(request.args.get("firstper"))
    secondper = float(request.args.get("secondper"))
    sdepart=request.args.get("sdepart")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course=? AND aadharnumber BETWEEN ? AND ?;"
    cursor.execute(query, (sdepart,firstper, secondper))
    results = cursor.fetchall()
    specfiedress = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html', cse_students=results, specfiedress=specfiedress, is_specress=True)

@app.route("/topten")
def topten():
    sdepart=request.args.get("sdepart")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course=? ORDER BY aadharnumber DESC LIMIT 10;"
    cursor.execute(query, (sdepart,))
    results = cursor.fetchall()
    toptenress = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html', cse_students=results,toptenress=toptenress, is_topten=True)


@app.route("/toptwenty")
def toptwenty():
    sdepart=request.args.get("sdepart")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course=? ORDER BY aadharnumber DESC LIMIT 20;"
    cursor.execute(query, (sdepart,))
    results = cursor.fetchall()
    toptwentyress = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html', cse_students=results,toptwentyress=toptwentyress, is_toptwenty=True)

@app.route("/bottomten")
def bottomten():
    sdepart = request.args.get("sdepart")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course=? ORDER BY aadharnumber ASC LIMIT 10;"
    cursor.execute(query, (sdepart,))
    results = cursor.fetchall()
    bottomtenress = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html',bottomtenress=bottomtenress, is_bottomten=True)

@app.route("/bottomtwenty")
def bottomtwenty():
    sdepart = request.args.get("sdepart")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course=? ORDER BY aadharnumber ASC LIMIT 20;"
    cursor.execute(query, (sdepart,))
    results = cursor.fetchall()
    bottomtwentyress = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html',bottomtwentyress=bottomtwentyress, is_bottomtwenty=True)



@app.route("/bottomsix")
def bottomsix():
    sdepart = request.args.get("sdepart")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course=? AND aadharnumber >=6.0 ORDER BY aadharnumber DESC;"
    cursor.execute(query, (sdepart,))
    results = cursor.fetchall()
    bottom_six_results = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html', bottom_six_results=bottom_six_results, is_bottom_six=True)

@app.route("/bottomseven")
def bottomseven():
    sdepart = request.args.get("sdepart")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course=? AND aadharnumber >=7.0 ORDER BY aadharnumber DESC ;"
    cursor.execute(query, (sdepart,))
    results = cursor.fetchall()
    bottom_seven_results = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html', bottom_seven_results=bottom_seven_results, is_bottom_seven=True)

@app.route("/bottomeight")
def bottomeight():
    sdepart = request.args.get("sdepart")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course=? AND aadharnumber >=8.0 ORDER BY aadharnumber DESC;"
    cursor.execute(query, (sdepart,))
    results = cursor.fetchall()
    bottom_eight_results = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html', bottom_eight_results=bottom_eight_results, is_bottom_eight=True)

@app.route("/bottomnine")
def bottomnine():
    sdepart = request.args.get("sdepart")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE course=? AND aadharnumber >=9.0 ORDER BY aadharnumber DESC;"
    cursor.execute(query, (sdepart,))
    results = cursor.fetchall()
    bottom_nine_results = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html', bottom_nine_results=bottom_nine_results, is_bottom_nine=True)

@app.route("/eachstudent")
def eachstudent():
    esid=request.args.get("esid")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Studentss WHERE sid =?;"
    cursor.execute(query, (esid,))
    results = cursor.fetchall()
    eachsturesults = [{'SID': row[0], 'susername':row[1],'password':row[2],'SFULLNAME': row[3], 'SFATHERNAME': row[4], 'S-MOBNUMBER': row[6],'p-mobilenumber':row[7],'dob':row[8],'SGENDER': row[9], 'SEMAIL': row[10], 'SCOURSE': row[11], 'SSSC': row[12], 'SINTER': row[13], 'SGPA': row[14],'address':row[15],'city':row[16],'state':row[17],'country': row[18],'approvedby':row[19],'SIMAGE': base64.b64encode(row[-2]).decode('utf-8'),'sttend':row[20]} for row in results]
    cursor.close()
    return render_template('welcometp.html',eachsturesults=eachsturesults, is_eachsid=True)



@app.route('/add_jobs',methods=["GET","POST"], endpoint='add_jobs')
def addjobs():
    if request.method=="POST":
        postingdate=request.form.get("posting_date")
        companyname=request.form.get('companyname')  
        email=request.form.get('email')
        jobposition=request.form.get('jobposition')
        jobtype=request.form.get('jjob_type')
        location=request.form.get('location')
        jobdescription=request.form.get('job_description')
        requriments=request.form.get('requriments')
        deadline=request.form.get('application_deadline')
        url=request.form.get('url')
        contactinfo=request.form.get('jcontact_information')
        conn = sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO jobborad(postingdate,Company_Name,email,JOB_POSITION,jobtype,location,jobdescription,Requriments,deadline,url,contactinfo) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (postingdate,companyname,email,jobposition,jobtype,location,jobdescription,requriments,deadline,url,contactinfo))
        conn.commit()
        cursor.close()
        conn.close()
    return render_template('welcometp.html',add_jobs=True)


@app.route('/view_alumini')
def view_alumini():
    return render_template('welcometp.html',add_aluminis=True)


@app.route('/add_alumini',methods=['GET','POST'])
def add_alumini():
    if request.method=="POST":
        alname=request.form.get('alname')
        graduation_year=request.form.get('graduation_year')
        location=request.form.get('location')
        current_job_position=request.form.get('current_job_position')
        internship_experience=request.form.get('internship_experience')
        company_name=request.form.get('company_name')
        professional_certifications=request.form.get('professional_certifications')
        github=request.form.get('github')
        linkedin=request.form.get('linkedin')
        hackerrank=request.form.get('hackerrank')
        interview_questions=request.form.get('interview_questions')
        salary_range=request.form.get('salary_range')
        success_story=request.form.get('success_story')
        work_life_balance_tips=request.form.get('work_life_balance_tips')
        conn = sqlite3.connect('logins2.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO alumini  
                        (name, graduation_year, location, current_job_position, 
                        internship_experience, company_name, professional_certifications, 
                        github, linkedin, hackerrank, interview_questions, 
                        salary_range, success_story, work_life_balance_tips) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (alname, graduation_year, location,current_job_position, 
                        internship_experience, company_name, professional_certifications, 
                        github, linkedin, hackerrank, interview_questions, 
                        salary_range, success_story, work_life_balance_tips))
        conn.commit()
        conn.close()
    return render_template('welcometp.html',add_aluminis=True)

@app.route("/principal_login",methods=['GET','POST'])
def principal_login():
    if request.method=="POST":
        plusername=request.form.get("plusername")
        plpassword=request.form.get("plpassword")
        print("username and password are",plusername,plpassword)
        if(plusername=="principal" and plpassword=="principal123"):
            return redirect(url_for('palldepartments'))
        else:
            return "please check the login credentials"
    return render_template('deligates.html')

@app.route("/palldepartments")
def palldepartments():
    plusername=request.args.get("plusername")
    return render_template('welcomeprincipal.html',is_allpdepartments=True,plusername=plusername)

@app.route("/ds_faculty")
def ds_faculty():
    plusername=request.args.get("plusername")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Facultyss WHERE fdepartment = 'DATASCIENCE';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    dsfacultyres = [{'facid': row[0], 'fusername':row[1],'fpassword':row[2],'fname': row[3], 'fdepartment': row[4], 'fdesignation': row[5],'fmobile':row[6],'femail':row[7],'fspecification': row[8], 'faddress': row[9], 'FIMAGE': base64.b64encode(row[-1]).decode('utf-8')} for row in results]
    return render_template('welcomeprincipal.html',ds_faculty=results[0],dsfacultyres=dsfacultyres,is_dsfp=True,plusernam=plusername)

@app.route("/ece_faculty")
def ece_faculty():
    plusername = request.args.get("plusername")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Facultyss WHERE fdepartment = 'ECE';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    ecefacultyres = [{'facid': row[0], 'fusername': row[1], 'fpassword': row[2], 'fname': row[3], 'fdepartment': row[4], 'fdesignation': row[5], 'fmobile': row[6], 'femail': row[7], 'fspecification': row[8], 'faddress': row[9], 'FIMAGE': base64.b64encode(row[-1]).decode('utf-8')} for row in results]
    return render_template('welcomeprincipal.html', ece_faculty=results[0], ecefacultyres=ecefacultyres, is_ecefp=True, plusername=plusername)

@app.route("/cse_faculty")
def cse_faculty():
    plusername = request.args.get("plusername")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Facultyss WHERE fdepartment = 'CSE';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    csefacultyres = [{'facid': row[0], 'fusername': row[1], 'fpassword': row[2], 'fname': row[3], 'fdepartment': row[4], 'fdesignation': row[5], 'fmobile': row[6], 'femail': row[7], 'fspecification': row[8], 'faddress': row[9], 'FIMAGE': base64.b64encode(row[-1]).decode('utf-8')} for row in results]
    return render_template('welcomeprincipal.html', cse_faculty=results[0], csefacultyres=csefacultyres, is_csefp=True, plusername=plusername)

@app.route("/civil_faculty")
def civil_faculty():
    plusername = request.args.get("plusername")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Facultyss WHERE fdepartment = 'CIVIL';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    civilfacultyres = [{'facid': row[0], 'fusername': row[1], 'fpassword': row[2], 'fname': row[3], 'fdepartment': row[4], 'fdesignation': row[5], 'fmobile': row[6], 'femail': row[7], 'fspecification': row[8], 'faddress': row[9], 'FIMAGE': base64.b64encode(row[-1]).decode('utf-8')} for row in results]
    return render_template('welcomeprincipal.html', civil_faculty=results[0], civilfacultyres=civilfacultyres, is_civilfp=True, plusername=plusername)

@app.route("/aiml_faculty")
def aiml_faculty():
    plusername = request.args.get("plusername")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Facultyss WHERE fdepartment = 'AIML';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    aimlfacultyres = [{'facid': row[0], 'fusername': row[1], 'fpassword': row[2], 'fname': row[3], 'fdepartment': row[4], 'fdesignation': row[5], 'fmobile': row[6], 'femail': row[7], 'fspecification': row[8], 'faddress': row[9], 'FIMAGE': base64.b64encode(row[-1]).decode('utf-8')} for row in results]
    return render_template('welcomeprincipal.html', aiml_faculty=results[0], aimlfacultyres=aimlfacultyres, is_aimlfp=True, plusername=plusername)

@app.route("/mech_faculty")
def mech_faculty():
    plusername = request.args.get("plusername")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM Facultyss WHERE fdepartment = 'MECH';"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    mechfacultyres = [{'facid': row[0], 'fusername': row[1], 'fpassword': row[2], 'fname': row[3], 'fdepartment': row[4], 'fdesignation': row[5], 'fmobile': row[6], 'femail': row[7], 'fspecification': row[8], 'faddress': row[9], 'FIMAGE': base64.b64encode(row[-1]).decode('utf-8')} for row in results]
    return render_template('welcomeprincipal.html', mech_faculty=results[0], mechfacultyres=mechfacultyres, is_mechfp=True, plusername=plusername)


@app.route("/pviewstudentdata",methods=['POST','GET'])
def pviewstudentdata():
    if request.method=='POST':
        plusername = request.args.get("plusername")
        sidp=request.form.get('sidp')
        sfullp=request.form.get('sfullp')
        connection=sqlite3.connect('logins2.db')
        cursor=connection.cursor()
        query="SELECT * from Studentss where sid=? and name=?"
        cursor.execute(query,(sidp,sfullp))
        psresults=cursor.fetchall()
        query="select * from Markss where sid=?"
        cursor.execute(query,(sidp,))
        psmarksresults=cursor.fetchall()
        query="select attendance FROM studentss WHERE sid=?"
        cursor.execute(query,(sidp,))
        psattresults=cursor.fetchall()
        image=psresults[0][-2]
        image_base64=base64.b64encode(image).decode('utf-8')
        if(len(psresults))==0:
            search_error = "Invalid Sid or UserName"
            return render_template('psearchstudent.html', search_error=search_error)
        else:
            return render_template('pviewstudentdata.html',results=psresults,sids=psresults[0][0],marks=psmarksresults,attendance=psattresults[0][0],plusername=plusername,image_base64=image_base64)
    return render_template('psearchstudent.html')

@app.route("/psearch_student")
def psearch_student():
    return render_template('welcomeprincipal.html',is_psearchstudent=True)

@app.route("/is_psearchall")
def is_psearchall():
    return render_template('welcomeprincipal.html',is_psearchall=True)

@app.route("/notification_raiser")
def notification_raiser():
    return render_template('welcomeprincipal.html',is_notification=True)

@app.route("/tpnotification_raiser")
def tpnotification_raiser():
    return render_template('welcometp.html',is_notificationtp=True)

@app.route("/all_years_stu_tp")
def all_years_stu_tp():
    return render_template('welcometp.html',is_all_years_stu=True)

@app.route("/all_years_stu")
def all_years_stu():
    return render_template('welcomeprincipal.html',is_all_years_stu=True)

@app.route("/year1branchs")
def year1branchs():
    return render_template('welcomeprincipal.html',is_year1branchs=True)


@app.route("/year2branchs")
def year2branchs():
    return render_template('welcomeprincipal.html',is_year2branchs=True)


@app.route("/year3branchs")
def year3branchs():
    return render_template('welcomeprincipal.html',is_year3branchs=True)


@app.route("/year4branchs")
def year4branchs():
    return render_template('welcomeprincipal.html',is_year4branchs=True)


@app.route("/year1branchs_tp")
def year1branchs_tp():
    return render_template('welcometp.html',is_year1branchs=True)


@app.route("/year2branchs_tp")
def year2branchs_tp():
    return render_template('welcometp.html',is_year2branchs=True)


@app.route("/year3branchs_tp")
def year3branchs_tp():
    return render_template('welcometp.html',is_year3branchs=True)


@app.route("/year4branchs_tp")
def year4branchs_tp():
    return render_template('welcometp.html',is_year4branchs=True)




@app.route("/getds1mails")
def getds1mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'DATASCIENCE' AND year=1;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getds1mails=True,ds1emailresults=results)

@app.route("/getds2mails")
def getds2mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'DATASCIENCE' AND year=2;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getds2mails=True,ds2emailresults=results)

@app.route("/getds3mails")
def getds3mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'DATASCIENCE' AND year=3;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getds3mails=True,ds3emailresults=results)

@app.route("/getds4mails")
def getds4mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'DATASCIENCE' AND year=4;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getds4mails=True,ds4emailresults=results)


@app.route("/getds1emailscat")
def getds1emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ds1eresults = []  # Initialize the variables outside the conditions
    top10ds1eresults = []
    bottom10ds1eresults = []
    totalds1eresults=[]
    ds1secaeresults =[]
    ds1secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalds1eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ds1secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ds1secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email,fathername,pmobilenumber FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ds1eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ds1eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'DATASCIENCE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ds1eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getds1emailscat=True,ds1secaeresults=ds1secaeresults,totalds1eresults=totalds1eresults,ds1secberesults=ds1secberesults,top3ds1eresults=top3ds1eresults,top10ds1eresults=top10ds1eresults,bottom10ds1eresults=bottom10ds1eresults)
    

@app.route("/getds2emailscat")
def getds2emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ds2eresults = []  # Initialize the variables outside the conditions
    top10ds2eresults = []
    bottom10ds2eresults = []
    totalds2eresults=[]
    ds2secaeresults =[]
    ds2secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalds2eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ds2secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ds2secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ds2eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ds2eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'DATASCIENCE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ds2eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getds2emailscat=True,ds2secaeresults=ds2secaeresults,totalds2eresults=totalds2eresults,ds2secberesults=ds2secberesults,top3ds2eresults=top3ds2eresults,top10ds2eresults=top10ds2eresults,bottom10ds2eresults=bottom10ds2eresults)
    
@app.route("/getds3emailscat")
def getds3emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ds3eresults = []  # Initialize the variables outside the conditions
    top10ds3eresults = []
    bottom10ds3eresults = []
    totalds3eresults=[]
    ds3secaeresults =[]
    ds3secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalds3eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ds3secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ds3secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ds3eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ds3eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'DATASCIENCE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ds3eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getds3emailscat=True,ds3secaeresults=ds3secaeresults,totalds3eresults=totalds3eresults,ds3secberesults=ds3secberesults,top3ds3eresults=top3ds3eresults,top10ds3eresults=top10ds3eresults,bottom10ds3eresults=bottom10ds3eresults)
    

@app.route("/getds4emailscat")
def getds4emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ds4eresults = []  # Initialize the variables outside the conditions
    top10ds4eresults = []
    bottom10ds4eresults = []
    totalds4eresults=[]
    ds4secaeresults =[]
    ds4secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalds4eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ds4secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ds4secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ds4eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ds4eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'DATASCIENCE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ds4eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getds4emailscat=True,ds4secaeresults=ds4secaeresults,totalds4eresults=totalds4eresults,ds4secberesults=ds4secberesults,top3ds4eresults=top3ds4eresults,top10ds4eresults=top10ds4eresults,bottom10ds4eresults=bottom10ds4eresults)
    



@app.route("/getece1mails")
def getece1mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'ECE' AND year=1;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getece1mails=True,ece1emailresults=results)
@app.route("/getece2mails")
def getece2mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'ECE' AND year=2;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getece2mails=True,ece2emailresults=results)
@app.route("/getece3mails")
def getece3mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'ECE' AND year=3;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getece3mails=True,ece3emailresults=results)
@app.route("/getece4mails")
def getece4mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'ECE' AND year=4;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getece4mails=True,ece4emailresults=results)


@app.route("/getece1emailscat")
def getece1emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ece1eresults = []  # Initialize the variables outside the conditions
    top10ece1eresults = []
    bottom10ece1eresults = []
    totalece1eresults=[]
    ece1secaeresults =[]
    ece1secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalece1eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ece1secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ece1secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ece1eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ece1eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'ECE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ece1eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getece1emailscat=True,ece1secaeresults=ece1secaeresults,totalece1eresults=totalece1eresults,ece1secberesults=ece1secberesults,top3ece1eresults=top3ece1eresults,top10ece1eresults=top10ece1eresults,bottom10ece1eresults=bottom10ece1eresults)
    
    
@app.route("/getece2emailscat")
def getece2emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ece2eresults = []  # Initialize the variables outside the conditions
    top10ece2eresults = []
    bottom10ece2eresults = []
    totalece2eresults=[]
    ece2secaeresults =[]
    ece2secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalece2eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ece2secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ece2secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ece2eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ece2eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'ECE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ece2eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getece2emailscat=True,ece2secaeresults=ece2secaeresults,totalece2eresults=totalece2eresults,ece2secberesults=ece2secberesults,top3ece2eresults=top3ece2eresults,top10ece2eresults=top10ece2eresults,bottom10ece2eresults=bottom10ece2eresults)
    
@app.route("/getece3emailscat")
def getece3emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ece3eresults = []  # Initialize the variables outside the conditions
    top10ece3eresults = []
    bottom10ece3eresults = []
    totalece3eresults=[]
    ece3secaeresults =[]
    ece3secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalece3eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ece3secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ece3secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ece3eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ece3eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'ECE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ece3eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getece3emailscat=True,ece3secaeresults=ece3secaeresults,totalece3eresults=totalece3eresults,ece3secberesults=ece3secberesults,top3ece3eresults=top3ece3eresults,top10ece3eresults=top10ece3eresults,bottom10ece3eresults=bottom10ece3eresults)
    
@app.route("/getece4emailscat")
def getece4emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ece4eresults = []  # Initialize the variables outside the conditions
    top10ece4eresults = []
    bottom10ece4eresults = []
    totalece4eresults=[]
    ece4secaeresults =[]
    ece4secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalece4eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ece4secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ece4secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ece4eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ece4eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'ECE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ece4eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getece4emailscat=True,ece4secaeresults=ece4secaeresults,totalece4eresults=totalece4eresults,ece4secberesults=ece4secberesults,top3ece4eresults=top3ece4eresults,top10ece4eresults=top10ece4eresults,bottom10ece4eresults=bottom10ece4eresults)
    
@app.route("/getcivil1mails")
def getcivil1mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CIVIL' AND year=1;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getcivil1mails=True,civil1emailresults=results)

@app.route("/getcivil2mails")
def getcivil2mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CIVIL' AND year=2;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getcivil2mails=True,civil2emailresults=results)

@app.route("/getcivil3mails")
def getcivil3mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CIVIL' AND year=3;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getcivil3mails=True,civil3emailresults=results)

@app.route("/getcivil4mails")
def getcivil4mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CIVIL' AND year=4;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getcivil4mails=True,civil4emailresults=results)


@app.route("/getcivil1emailscat")
def getcivil1emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3civil1eresults = []  # Initialize the variables outside the conditions
    top10civil1eresults = []
    bottom10civil1eresults = []
    totalcivil1eresults=[]
    civil1secaeresults =[]
    civil1secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcivil1eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        civil1secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        civil1secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3civil1eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10civil1eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CIVIL' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10civil1eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getcivil1emailscat=True,civil1secaeresults=civil1secaeresults,totalcivil1eresults=totalcivil1eresults,civil1secberesults=civil1secberesults,top3civil1eresults=top3civil1eresults,top10civil1eresults=top10civil1eresults,bottom10civil1eresults=bottom10civil1eresults)
    
    
@app.route("/getcivil2emailscat")
def getcivil2emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3civil2eresults = []  # Initialize the variables outside the conditions
    top10civil2eresults = []
    bottom10civil2eresults = []
    totalcivil2eresults=[]
    civil2secaeresults =[]
    civil2secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcivil2eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        civil2secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        civil2secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3civil2eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10civil2eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CIVIL' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10civil2eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getcivil2emailscat=True,civil2secaeresults=civil2secaeresults,totalcivil2eresults=totalcivil2eresults,civil2secberesults=civil2secberesults,top3civil2eresults=top3civil2eresults,top10civil2eresults=top10civil2eresults,bottom10civil2eresults=bottom10civil2eresults)
    
@app.route("/getcivil3emailscat")
def getcivil3emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3civil3eresults = []  # Initialize the variables outside the conditions
    top10civil3eresults = []
    bottom10civil3eresults = []
    totalcivil3eresults=[]
    civil3secaeresults =[]
    civil3secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcivil3eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        civil3secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        civil3secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3civil3eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10civil3eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CIVIL' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10civil3eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getcivil3emailscat=True,civil3secaeresults=civil3secaeresults,totalcivil3eresults=totalcivil3eresults,civil3secberesults=civil3secberesults,top3civil3eresults=top3civil3eresults,top10civil3eresults=top10civil3eresults,bottom10civil3eresults=bottom10civil3eresults)
    

@app.route("/getcivil4emailscat")
def getcivil4emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3civil4eresults = []  # Initialize the variables outside the conditions
    top10civil4eresults = []
    bottom10civil4eresults = []
    totalcivil4eresults=[]
    civil4secaeresults =[]
    civil4secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcivil4eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        civil4secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        civil4secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3civil4eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10civil4eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10civil4eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getcivil4emailscat=True,civil4secaeresults=civil4secaeresults,totalcivil4eresults=totalcivil4eresults,civil4secberesults=civil4secberesults,top3civil4eresults=top3civil4eresults,top10civil4eresults=top10civil4eresults,bottom10civil4eresults=bottom10civil4eresults)
    

@app.route("/getmech1mails")
def getmech1mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'MECH' AND year=1;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getmech1mails=True,mech1emailresults=results)

@app.route("/getmech2mails")
def getmech2mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'MECH' AND year=2;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getmech2mails=True,mech2emailresults=results)

@app.route("/getmech3mails")
def getmech3mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'MECH' AND year=3;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getmech3mails=True,mech3emailresults=results)

@app.route("/getmech4mails")
def getmech4mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'MECH' AND year=4;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getmech4mails=True,mech4emailresults=results)

@app.route("/getmech1emailscat")
def getmech1emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3mech1eresults = []  # Initialize the variables outside the conditions
    top10mech1eresults = []
    bottom10mech1eresults = []
    totalmech1eresults=[]
    mech1secaeresults =[]
    mech1secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY name ASC;"
        cursor.execute(query,)
        totalmech1eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        mech1secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        mech1secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3mech1eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10mech1eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'MECH' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10mech1eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getmech1emailscat=True,mech1secaeresults=mech1secaeresults,totalmech1eresults=totalmech1eresults,mech1secberesults=mech1secberesults,top3mech1eresults=top3mech1eresults,top10mech1eresults=top10mech1eresults,bottom10mech1eresults=bottom10mech1eresults)
    

@app.route("/getmech2emailscat")
def getmech2emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3mech2eresults = []  # Initialize the variables outside the conditions
    top10mech2eresults = []
    bottom10mech2eresults = []
    totalmech2eresults=[]
    mech2secaeresults =[]
    mech2secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY name ASC;"
        cursor.execute(query,)
        totalmech2eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        mech2secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        mech2secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3mech2eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10mech2eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'MECH' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10mech2eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getmech2emailscat=True,mech2secaeresults=mech2secaeresults,totalmech2eresults=totalmech2eresults,mech2secberesults=mech2secberesults,top3mech2eresults=top3mech2eresults,top10mech2eresults=top10mech2eresults,bottom10mech2eresults=bottom10mech2eresults)
    

@app.route("/getmech3emailscat")
def getmech3emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3mech3eresults = []  # Initialize the variables outside the conditions
    top10mech3eresults = []
    bottom10mech3eresults = []
    totalmech3eresults=[]
    mech3secaeresults =[]
    mech3secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY name ASC;"
        cursor.execute(query,)
        totalmech3eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        mech3secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        mech3secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3mech3eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10mech3eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'MECH' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10mech3eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getmech3emailscat=True,mech3secaeresults=mech3secaeresults,totalmech3eresults=totalmech3eresults,mech3secberesults=mech3secberesults,top3mech3eresults=top3mech3eresults,top10mech3eresults=top10mech3eresults,bottom10mech3eresults=bottom10mech3eresults)
    

@app.route("/getmech4emailscat")
def getmech4emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3mech4eresults = []  # Initialize the variables outside the conditions
    top10mech4eresults = []
    bottom10mech4eresults = []
    totalmech4eresults=[]
    mech4secaeresults =[]
    mech4secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY name ASC;"
        cursor.execute(query,)
        totalmech4eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        mech4secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        mech4secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3mech4eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10mech4eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'MECH' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10mech4eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getmech4emailscat=True,mech4secaeresults=mech4secaeresults,totalmech4eresults=totalmech4eresults,mech4secberesults=mech4secberesults,top3mech4eresults=top3mech4eresults,top10mech4eresults=top10mech4eresults,bottom10mech4eresults=bottom10mech4eresults)
    


@app.route("/getaiml1mails")
def getaiml1mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'AIML' AND year=1;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getaiml1mails=True,aiml1emailresults=results)

@app.route("/getaiml2mails")
def getaiml2mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'AIML' AND year=2;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getaiml2mails=True,aiml2emailresults=results)

@app.route("/getaiml3mails")
def getaiml3mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'AIML' AND year=3;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getaiml3mails=True,aiml3emailresults=results)


@app.route("/getaiml4mails")
def getaiml4mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'AIML' AND year=4;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getaiml4mails=True,aiml4emailresults=results)

@app.route("/getaiml1emailscat")
def getaiml1emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3aiml1eresults = []  # Initialize the variables outside the conditions
    top10aiml1eresults = []
    bottom10aiml1eresults = []
    totalaiml1eresults=[]
    aiml1secaeresults =[]
    aiml1secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY name ASC;"
        cursor.execute(query,)
        totalaiml1eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml1secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml1secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3aiml1eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10aiml1eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'AIML' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10aiml1eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getaiml1emailscat=True,aiml1secaeresults=aiml1secaeresults,totalaiml1eresults=totalaiml1eresults,aiml1secberesults=aiml1secberesults,top3aiml1eresults=top3aiml1eresults,top10aiml1eresults=top10aiml1eresults,bottom10aiml1eresults=bottom10aiml1eresults)
    

@app.route("/getaiml2emailscat")
def getaiml2emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3aiml2eresults = []  # Initialize the variables outside the conditions
    top10aiml2eresults = []
    bottom10aiml2eresults = []
    totalaiml2eresults=[]
    aiml2secaeresults =[]
    aiml2secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY name ASC;"
        cursor.execute(query,)
        totalaiml2eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml2secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml2secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3aiml2eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10aiml2eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'AIML' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10aiml2eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getaiml2emailscat=True,aiml2secaeresults=aiml2secaeresults,totalaiml2eresults=totalaiml2eresults,aiml2secberesults=aiml2secberesults,top3aiml2eresults=top3aiml2eresults,top10aiml2eresults=top10aiml2eresults,bottom10aiml2eresults=bottom10aiml2eresults)
    
@app.route("/getaiml3emailscat")
def getaiml3emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3aiml3eresults = []  # Initialize the variables outside the conditions
    top10aiml3eresults = []
    bottom10aiml3eresults = []
    totalaiml3eresults=[]
    aiml3secaeresults =[]
    aiml3secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY name ASC;"
        cursor.execute(query,)
        totalaiml3eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml3secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml3secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3aiml3eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10aiml3eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'AIML' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10aiml3eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getaiml3emailscat=True,aiml3secaeresults=aiml3secaeresults,totalaiml3eresults=totalaiml3eresults,aiml3secberesults=aiml3secberesults,top3aiml3eresults=top3aiml3eresults,top10aiml3eresults=top10aiml3eresults,bottom10aiml3eresults=bottom10aiml3eresults)
    

@app.route("/getaiml4emailscat")
def getaiml4emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3aiml4eresults = []  # Initialize the variables outside the conditions
    top10aiml4eresults = []
    bottom10aiml4eresults = []
    totalaiml4eresults=[]
    aiml4secaeresults =[]
    aiml4secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY name ASC;"
        cursor.execute(query,)
        totalaiml4eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml4secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml4secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3aiml4eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10aiml4eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'AIML' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10aiml4eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getaiml4emailscat=True,aiml4secaeresults=aiml4secaeresults,totalaiml4eresults=totalaiml4eresults,aiml4secberesults=aiml4secberesults,top3aiml4eresults=top3aiml4eresults,top10aiml4eresults=top10aiml4eresults,bottom10aiml4eresults=bottom10aiml4eresults)
    






@app.route("/getcse1mails")
def getcse1mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CSE' AND year=1;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getcse1mails=True,cse1emailresults=results)
@app.route("/getcse2mails")
def getcse2mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CSE' AND year=2;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getcse2mails=True,cse2emailresults=results)
@app.route("/getcse3mails")
def getcse3mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CSE' AND year=3;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getcse3mails=True,cse3emailresults=results)
@app.route("/getcse4mails")
def getcse4mails():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CSE' AND year=4;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getcse4mails=True,cse4emailresults=results)


@app.route("/getcse1emailscat")
def getcse1emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3cse1eresults = []  # Initialize the variables outside the conditions
    top10cse1eresults = []
    bottom10cse1eresults = []
    totalcse1eresults=[]
    cse1secaeresults =[]
    cse1secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcse1eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        cse1secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        cse1secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3cse1eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10cse1eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CSE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10cse1eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getcse1emailscat=True,cse1secaeresults=cse1secaeresults,totalcse1eresults=totalcse1eresults,cse1secberesults=cse1secberesults,top3cse1eresults=top3cse1eresults,top10cse1eresults=top10cse1eresults,bottom10cse1eresults=bottom10cse1eresults)
    
@app.route("/getcse2emailscat")
def getcse2emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3cse2eresults = []  # Initialize the variables outside the conditions
    top10cse2eresults = []
    bottom10cse2eresults = []
    totalcse2eresults=[]
    cse2secaeresults =[]
    cse2secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcse2eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        cse2secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        cse2secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3cse2eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10cse2eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CSE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10cse2eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getcse2emailscat=True,cse2secaeresults=cse2secaeresults,totalcse2eresults=totalcse2eresults,cse2secberesults=cse2secberesults,top3cse2eresults=top3cse2eresults,top10cse2eresults=top10cse2eresults,bottom10cse2eresults=bottom10cse2eresults)
    
@app.route("/getcse3emailscat")
def getcse3emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3cse3eresults = []  # Initialize the variables outside the conditions
    top10cse3eresults = []
    bottom10cse3eresults = []
    totalcse3eresults=[]
    cse3secaeresults =[]
    cse3secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcse3eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        cse3secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        cse3secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3cse3eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10cse3eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CSE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10cse3eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getcse3emailscat=True,cse3secaeresults=cse3secaeresults,totalcse3eresults=totalcse3eresults,cse3secberesults=cse3secberesults,top3cse3eresults=top3cse3eresults,top10cse3eresults=top10cse3eresults,bottom10cse3eresults=bottom10cse3eresults)
    
@app.route("/getcse4emailscat")
def getcse4emailscat():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3cse4eresults = []  # Initialize the variables outside the conditions
    top10cse4eresults = []
    bottom10cse4eresults = []
    totalcse4eresults=[]
    cse4secaeresults =[]
    cse4secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcse4eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        cse4secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        cse4secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3cse4eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10cse4eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CSE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10cse4eresults=cursor.fetchall()
    connection.close()
    return render_template('welcomeprincipal.html',is_getcse4emailscat=True,cse4secaeresults=cse4secaeresults,totalcse4eresults=totalcse4eresults,cse4secberesults=cse4secberesults,top3cse4eresults=top3cse4eresults,top10cse4eresults=top10cse4eresults,bottom10cse4eresults=bottom10cse4eresults)





@app.route("/getds1mails_tp")
def getds1mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'DATASCIENCE' AND year=1;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getds1mails=True,ds1emailresults=results)

@app.route("/getds2mails_tp")
def getds2mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'DATASCIENCE' AND year=2;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getds2mails=True,ds2emailresults=results)

@app.route("/getds3mails_tp")
def getds3mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'DATASCIENCE' AND year=3;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getds3mails=True,ds3emailresults=results)

@app.route("/getds4mails_tp")
def getds4mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'DATASCIENCE' AND year=4;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getds4mails=True,ds4emailresults=results)





@app.route("/getds1emailscat_tp")
def getds1emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ds1eresults = []  # Initialize the variables outside the conditions
    top10ds1eresults = []
    bottom10ds1eresults = []
    totalds1eresults=[]
    ds1secaeresults =[]
    ds1secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalds1eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ds1secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ds1secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email,fathername,pmobilenumber FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ds1eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ds1eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'DATASCIENCE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ds1eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getds1emailscat=True,ds1secaeresults=ds1secaeresults,totalds1eresults=totalds1eresults,ds1secberesults=ds1secberesults,top3ds1eresults=top3ds1eresults,top10ds1eresults=top10ds1eresults,bottom10ds1eresults=bottom10ds1eresults)
    

@app.route("/getds2emailscat_tp")
def getds2emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ds2eresults = []  # Initialize the variables outside the conditions
    top10ds2eresults = []
    bottom10ds2eresults = []
    totalds2eresults=[]
    ds2secaeresults =[]
    ds2secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalds2eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ds2secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ds2secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ds2eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ds2eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'DATASCIENCE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ds2eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getds2emailscat=True,ds2secaeresults=ds2secaeresults,totalds2eresults=totalds2eresults,ds2secberesults=ds2secberesults,top3ds2eresults=top3ds2eresults,top10ds2eresults=top10ds2eresults,bottom10ds2eresults=bottom10ds2eresults)
    
@app.route("/getds3emailscat_tp")
def getds3emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ds3eresults = []  # Initialize the variables outside the conditions
    top10ds3eresults = []
    bottom10ds3eresults = []
    totalds3eresults=[]
    ds3secaeresults =[]
    ds3secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalds3eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ds3secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ds3secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ds3eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ds3eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'DATASCIENCE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ds3eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getds3emailscat=True,ds3secaeresults=ds3secaeresults,totalds3eresults=totalds3eresults,ds3secberesults=ds3secberesults,top3ds3eresults=top3ds3eresults,top10ds3eresults=top10ds3eresults,bottom10ds3eresults=bottom10ds3eresults)
    

@app.route("/getds4emailscat_tp")
def getds4emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ds4eresults = []  # Initialize the variables outside the conditions
    top10ds4eresults = []
    bottom10ds4eresults = []
    totalds4eresults=[]
    ds4secaeresults =[]
    ds4secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalds4eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ds4secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ds4secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ds4eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='DATASCIENCE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ds4eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'DATASCIENCE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ds4eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getds4emailscat=True,ds4secaeresults=ds4secaeresults,totalds4eresults=totalds4eresults,ds4secberesults=ds4secberesults,top3ds4eresults=top3ds4eresults,top10ds4eresults=top10ds4eresults,bottom10ds4eresults=bottom10ds4eresults)
    



@app.route("/getece1mails_tp")
def getece1mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'ECE' AND year=1;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getece1mails=True,ece1emailresults=results)
@app.route("/getece2mails_tp")
def getece2mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'ECE' AND year=2;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getece2mails=True,ece2emailresults=results)
@app.route("/getece3mails_tp")
def getece3mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'ECE' AND year=3;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getece3mails=True,ece3emailresults=results)
@app.route("/getece4mails_tp")
def getece4mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'ECE' AND year=4;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getece4mails=True,ece4emailresults=results)


@app.route("/getece1emailscat_tp")
def getece1emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ece1eresults = []  # Initialize the variables outside the conditions
    top10ece1eresults = []
    bottom10ece1eresults = []
    totalece1eresults=[]
    ece1secaeresults =[]
    ece1secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalece1eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ece1secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ece1secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ece1eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ece1eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'ECE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ece1eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getece1emailscat=True,ece1secaeresults=ece1secaeresults,totalece1eresults=totalece1eresults,ece1secberesults=ece1secberesults,top3ece1eresults=top3ece1eresults,top10ece1eresults=top10ece1eresults,bottom10ece1eresults=bottom10ece1eresults)
    
    
@app.route("/getece2emailscat_tp")
def getece2emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ece2eresults = []  # Initialize the variables outside the conditions
    top10ece2eresults = []
    bottom10ece2eresults = []
    totalece2eresults=[]
    ece2secaeresults =[]
    ece2secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalece2eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ece2secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ece2secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ece2eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ece2eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'ECE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ece2eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getece2emailscat=True,ece2secaeresults=ece2secaeresults,totalece2eresults=totalece2eresults,ece2secberesults=ece2secberesults,top3ece2eresults=top3ece2eresults,top10ece2eresults=top10ece2eresults,bottom10ece2eresults=bottom10ece2eresults)
    
@app.route("/getece3emailscat_tp")
def getece3emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ece3eresults = []  # Initialize the variables outside the conditions
    top10ece3eresults = []
    bottom10ece3eresults = []
    totalece3eresults=[]
    ece3secaeresults =[]
    ece3secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalece3eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ece3secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ece3secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ece3eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ece3eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'ECE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ece3eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getece3emailscat=True,ece3secaeresults=ece3secaeresults,totalece3eresults=totalece3eresults,ece3secberesults=ece3secberesults,top3ece3eresults=top3ece3eresults,top10ece3eresults=top10ece3eresults,bottom10ece3eresults=bottom10ece3eresults)
    
@app.route("/getece4emailscat_tp")
def getece4emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3ece4eresults = []  # Initialize the variables outside the conditions
    top10ece4eresults = []
    bottom10ece4eresults = []
    totalece4eresults=[]
    ece4secaeresults =[]
    ece4secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalece4eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        ece4secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='ECE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        ece4secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3ece4eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='ECE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10ece4eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'ECE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10ece4eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getece4emailscat=True,ece4secaeresults=ece4secaeresults,totalece4eresults=totalece4eresults,ece4secberesults=ece4secberesults,top3ece4eresults=top3ece4eresults,top10ece4eresults=top10ece4eresults,bottom10ece4eresults=bottom10ece4eresults)
    
@app.route("/getcivil1mails_tp")
def getcivil1mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CIVIL' AND year=1;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getcivil1mails=True,civil1emailresults=results)

@app.route("/getcivil2mails_tp")
def getcivil2mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CIVIL' AND year=2;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getcivil2mails=True,civil2emailresults=results)

@app.route("/getcivil3mails_tp")
def getcivil3mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CIVIL' AND year=3;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getcivil3mails=True,civil3emailresults=results)

@app.route("/getcivil4mails_tp")
def getcivil4mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CIVIL' AND year=4;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getcivil4mails=True,civil4emailresults=results)


@app.route("/getcivil1emailscat_tp")
def getcivil1emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3civil1eresults = []  # Initialize the variables outside the conditions
    top10civil1eresults = []
    bottom10civil1eresults = []
    totalcivil1eresults=[]
    civil1secaeresults =[]
    civil1secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcivil1eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        civil1secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        civil1secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3civil1eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10civil1eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CIVIL' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10civil1eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getcivil1emailscat=True,civil1secaeresults=civil1secaeresults,totalcivil1eresults=totalcivil1eresults,civil1secberesults=civil1secberesults,top3civil1eresults=top3civil1eresults,top10civil1eresults=top10civil1eresults,bottom10civil1eresults=bottom10civil1eresults)
    
    
@app.route("/getcivil2emailscat_tp")
def getcivil2emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3civil2eresults = []  # Initialize the variables outside the conditions
    top10civil2eresults = []
    bottom10civil2eresults = []
    totalcivil2eresults=[]
    civil2secaeresults =[]
    civil2secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcivil2eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        civil2secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        civil2secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3civil2eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10civil2eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CIVIL' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10civil2eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getcivil2emailscat=True,civil2secaeresults=civil2secaeresults,totalcivil2eresults=totalcivil2eresults,civil2secberesults=civil2secberesults,top3civil2eresults=top3civil2eresults,top10civil2eresults=top10civil2eresults,bottom10civil2eresults=bottom10civil2eresults)
    
@app.route("/getcivil3emailscat_tp")
def getcivil3emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3civil3eresults = []  # Initialize the variables outside the conditions
    top10civil3eresults = []
    bottom10civil3eresults = []
    totalcivil3eresults=[]
    civil3secaeresults =[]
    civil3secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcivil3eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        civil3secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        civil3secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3civil3eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10civil3eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CIVIL' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10civil3eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getcivil3emailscat=True,civil3secaeresults=civil3secaeresults,totalcivil3eresults=totalcivil3eresults,civil3secberesults=civil3secberesults,top3civil3eresults=top3civil3eresults,top10civil3eresults=top10civil3eresults,bottom10civil3eresults=bottom10civil3eresults)
    

@app.route("/getcivil4emailscat_tp")
def getcivil4emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3civil4eresults = []  # Initialize the variables outside the conditions
    top10civil4eresults = []
    bottom10civil4eresults = []
    totalcivil4eresults=[]
    civil4secaeresults =[]
    civil4secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcivil4eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        civil4secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CIVIL' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        civil4secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3civil4eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10civil4eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CIVIL' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10civil4eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getcivil4emailscat=True,civil4secaeresults=civil4secaeresults,totalcivil4eresults=totalcivil4eresults,civil4secberesults=civil4secberesults,top3civil4eresults=top3civil4eresults,top10civil4eresults=top10civil4eresults,bottom10civil4eresults=bottom10civil4eresults)
    

@app.route("/getmech1mails_tp")
def getmech1mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'MECH' AND year=1;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getmech1mails=True,mech1emailresults=results)

@app.route("/getmech2mails_tp")
def getmech2mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'MECH' AND year=2;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getmech2mails=True,mech2emailresults=results)

@app.route("/getmech3mails_tp")
def getmech3mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'MECH' AND year=3;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getmech3mails=True,mech3emailresults=results)

@app.route("/getmech4mails_tp")
def getmech4mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'MECH' AND year=4;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getmech4mails=True,mech4emailresults=results)

@app.route("/getmech1emailscat_tp")
def getmech1emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3mech1eresults = []  # Initialize the variables outside the conditions
    top10mech1eresults = []
    bottom10mech1eresults = []
    totalmech1eresults=[]
    mech1secaeresults =[]
    mech1secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY name ASC;"
        cursor.execute(query,)
        totalmech1eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        mech1secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        mech1secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3mech1eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10mech1eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'MECH' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10mech1eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getmech1emailscat=True,mech1secaeresults=mech1secaeresults,totalmech1eresults=totalmech1eresults,mech1secberesults=mech1secberesults,top3mech1eresults=top3mech1eresults,top10mech1eresults=top10mech1eresults,bottom10mech1eresults=bottom10mech1eresults)
    

@app.route("/getmech2emailscat_tp")
def getmech2emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3mech2eresults = []  # Initialize the variables outside the conditions
    top10mech2eresults = []
    bottom10mech2eresults = []
    totalmech2eresults=[]
    mech2secaeresults =[]
    mech2secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY name ASC;"
        cursor.execute(query,)
        totalmech2eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        mech2secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        mech2secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3mech2eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10mech2eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'MECH' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10mech2eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getmech2emailscat=True,mech2secaeresults=mech2secaeresults,totalmech2eresults=totalmech2eresults,mech2secberesults=mech2secberesults,top3mech2eresults=top3mech2eresults,top10mech2eresults=top10mech2eresults,bottom10mech2eresults=bottom10mech2eresults)
    

@app.route("/getmech3emailscat_tp")
def getmech3emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3mech3eresults = []  # Initialize the variables outside the conditions
    top10mech3eresults = []
    bottom10mech3eresults = []
    totalmech3eresults=[]
    mech3secaeresults =[]
    mech3secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY name ASC;"
        cursor.execute(query,)
        totalmech3eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        mech3secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        mech3secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3mech3eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10mech3eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'MECH' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10mech3eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getmech3emailscat=True,mech3secaeresults=mech3secaeresults,totalmech3eresults=totalmech3eresults,mech3secberesults=mech3secberesults,top3mech3eresults=top3mech3eresults,top10mech3eresults=top10mech3eresults,bottom10mech3eresults=bottom10mech3eresults)
    

@app.route("/getmech4emailscat_tp")
def getmech4emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3mech4eresults = []  # Initialize the variables outside the conditions
    top10mech4eresults = []
    bottom10mech4eresults = []
    totalmech4eresults=[]
    mech4secaeresults =[]
    mech4secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY name ASC;"
        cursor.execute(query,)
        totalmech4eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        mech4secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='MECH' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        mech4secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3mech4eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='MECH' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10mech4eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'MECH' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10mech4eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getmech4emailscat=True,mech4secaeresults=mech4secaeresults,totalmech4eresults=totalmech4eresults,mech4secberesults=mech4secberesults,top3mech4eresults=top3mech4eresults,top10mech4eresults=top10mech4eresults,bottom10mech4eresults=bottom10mech4eresults)
    

@app.route("/getaiml1mails_tp")
def getaiml1mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'AIML' AND year=1;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getaiml1mails=True,aiml1emailresults=results)

@app.route("/getaiml2mails_tp")
def getaiml2mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'AIML' AND year=2;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getaiml2mails=True,aiml2emailresults=results)

@app.route("/getaiml3mails_tp")
def getaiml3mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'AIML' AND year=3;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getaiml3mails=True,aiml3emailresults=results)


@app.route("/getaiml4mails_tp")
def getaiml4mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'AIML' AND year=4;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getaiml4mails=True,aiml4emailresults=results)

@app.route("/getaiml1emailscat_tp")
def getaiml1emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3aiml1eresults = []  # Initialize the variables outside the conditions
    top10aiml1eresults = []
    bottom10aiml1eresults = []
    totalaiml1eresults=[]
    aiml1secaeresults =[]
    aiml1secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY name ASC;"
        cursor.execute(query,)
        totalaiml1eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml1secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml1secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3aiml1eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10aiml1eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'AIML' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10aiml1eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getaiml1emailscat=True,aiml1secaeresults=aiml1secaeresults,totalaiml1eresults=totalaiml1eresults,aiml1secberesults=aiml1secberesults,top3aiml1eresults=top3aiml1eresults,top10aiml1eresults=top10aiml1eresults,bottom10aiml1eresults=bottom10aiml1eresults)
    

@app.route("/getaiml2emailscat_tp")
def getaiml2emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3aiml2eresults = []  # Initialize the variables outside the conditions
    top10aiml2eresults = []
    bottom10aiml2eresults = []
    totalaiml2eresults=[]
    aiml2secaeresults =[]
    aiml2secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY name ASC;"
        cursor.execute(query,)
        totalaiml2eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml2secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml2secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3aiml2eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10aiml2eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'AIML' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10aiml2eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getaiml2emailscat=True,aiml2secaeresults=aiml2secaeresults,totalaiml2eresults=totalaiml2eresults,aiml2secberesults=aiml2secberesults,top3aiml2eresults=top3aiml2eresults,top10aiml2eresults=top10aiml2eresults,bottom10aiml2eresults=bottom10aiml2eresults)
    
@app.route("/getaiml3emailscat_tp")
def getaiml3emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3aiml3eresults = []  # Initialize the variables outside the conditions
    top10aiml3eresults = []
    bottom10aiml3eresults = []
    totalaiml3eresults=[]
    aiml3secaeresults =[]
    aiml3secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY name ASC;"
        cursor.execute(query,)
        totalaiml3eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml3secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml3secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3aiml3eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10aiml3eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'AIML' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10aiml3eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getaiml3emailscat=True,aiml3secaeresults=aiml3secaeresults,totalaiml3eresults=totalaiml3eresults,aiml3secberesults=aiml3secberesults,top3aiml3eresults=top3aiml3eresults,top10aiml3eresults=top10aiml3eresults,bottom10aiml3eresults=bottom10aiml3eresults)
    

@app.route("/getaiml4emailscat_tp")
def getaiml4emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3aiml4eresults = []  # Initialize the variables outside the conditions
    top10aiml4eresults = []
    bottom10aiml4eresults = []
    totalaiml4eresults=[]
    aiml4secaeresults =[]
    aiml4secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY name ASC;"
        cursor.execute(query,)
        totalaiml4eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml4secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='AIML' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        aiml4secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3aiml4eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='AIML' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10aiml4eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'AIML' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10aiml4eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getaiml4emailscat=True,aiml4secaeresults=aiml4secaeresults,totalaiml4eresults=totalaiml4eresults,aiml4secberesults=aiml4secberesults,top3aiml4eresults=top3aiml4eresults,top10aiml4eresults=top10aiml4eresults,bottom10aiml4eresults=bottom10aiml4eresults)
    


@app.route("/getcse1mails_tp")
def getcse1mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CSE' AND year=1;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcomeprincipal.html',is_getcse1mails=True,cse1emailresults=results)
@app.route("/getcse2mails_tp")
def getcse2mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CSE' AND year=2;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getcse2mails=True,cse2emailresults=results)
@app.route("/getcse3mails_tp")
def getcse3mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CSE' AND year=3;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getcse3mails=True,cse3emailresults=results)
@app.route("/getcse4mails_tp")
def getcse4mails_tp():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT email FROM Studentss WHERE  course = 'CSE' AND year=4;"
    cursor.execute(query)
    results = cursor.fetchall()
    connection.commit()
    cursor.close()
    return render_template('welcometp.html',is_getcse4mails=True,cse4emailresults=results)


@app.route("/getcse1emailscat_tp")
def getcse1emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3cse1eresults = []  # Initialize the variables outside the conditions
    top10cse1eresults = []
    bottom10cse1eresults = []
    totalcse1eresults=[]
    cse1secaeresults =[]
    cse1secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcse1eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        cse1secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        cse1secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3cse1eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10cse1eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CSE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10cse1eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getcse1emailscat=True,cse1secaeresults=cse1secaeresults,totalcse1eresults=totalcse1eresults,cse1secberesults=cse1secberesults,top3cse1eresults=top3cse1eresults,top10cse1eresults=top10cse1eresults,bottom10cse1eresults=bottom10cse1eresults)
    
@app.route("/getcse2emailscat_tp")
def getcse2emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3cse2eresults = []  # Initialize the variables outside the conditions
    top10cse2eresults = []
    bottom10cse2eresults = []
    totalcse2eresults=[]
    cse2secaeresults =[]
    cse2secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcse2eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        cse2secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        cse2secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3cse2eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10cse2eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CSE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10cse2eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getcse2emailscat=True,cse2secaeresults=cse2secaeresults,totalcse2eresults=totalcse2eresults,cse2secberesults=cse2secberesults,top3cse2eresults=top3cse2eresults,top10cse2eresults=top10cse2eresults,bottom10cse2eresults=bottom10cse2eresults)
    
@app.route("/getcse3emailscat_tp")
def getcse3emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3cse3eresults = []  # Initialize the variables outside the conditions
    top10cse3eresults = []
    bottom10cse3eresults = []
    totalcse3eresults=[]
    cse3secaeresults =[]
    cse3secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcse3eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        cse3secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        cse3secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3cse3eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10cse3eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CSE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10cse3eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getcse3emailscat=True,cse3secaeresults=cse3secaeresults,totalcse3eresults=totalcse3eresults,cse3secberesults=cse3secberesults,top3cse3eresults=top3cse3eresults,top10cse3eresults=top10cse3eresults,bottom10cse3eresults=bottom10cse3eresults)
    
@app.route("/getcse4emailscat_tp")
def getcse4emailscat_tp():
    pcateogery = request.args.get("dsp")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    top3cse4eresults = []  # Initialize the variables outside the conditions
    top10cse4eresults = []
    bottom10cse4eresults = []
    totalcse4eresults=[]
    cse4secaeresults =[]
    cse4secberesults=[]
    if pcateogery=="1":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY name ASC;"
        cursor.execute(query,)
        totalcse4eresults = cursor.fetchall()
    elif pcateogery=="2":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='A' ORDER BY name ASC;"
        cursor.execute(query,)
        cse4secaeresults = cursor.fetchall()  
    elif pcateogery=="4":
        query = "SELECT name, mobilenumber,course,email FROM Studentss WHERE course='CSE' AND city='B' ORDER BY name ASC;"
        cursor.execute(query,)
        cse4secberesults = cursor.fetchall()    
    elif pcateogery=="3":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 3;"
        cursor.execute(query,)
        top3cse4eresults = cursor.fetchall()
    elif pcateogery == "10":
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course='CSE' ORDER BY aadharnumber DESC LIMIT 10;"
        cursor.execute(query,)
        top10cse4eresults=cursor.fetchall()
    else:
        query = "SELECT name,mobilenumber,course,email FROM Studentss WHERE course= 'CSE' ORDER BY aadharnumber ASC LIMIT 10;"
        cursor.execute(query,)
        bottom10cse4eresults=cursor.fetchall()
    connection.close()
    return render_template('welcometp.html',is_getcse4emailscat=True,cse4secaeresults=cse4secaeresults,totalcse4eresults=totalcse4eresults,cse4secberesults=cse4secberesults,top3cse4eresults=top3cse4eresults,top10cse4eresults=top10cse4eresults,bottom10cse4eresults=bottom10cse4eresults)


# @app.route('/add_plstudents', methods=['POST', 'GET'])
# def add_plstudents():
#     if request.method=='POST':
#         plstudent_id = request.form.get('plstudent_id')
#         plsname = request.form.get('plsname')
#         plemail = request.form.get('plsemail')
#         plsphone_number = request.form.get('plsphone_number')
#         plsgender = request.form.get('plsgender')
#         plsbranch = request.form.get('sbranched')
#         plsyear_of_passing = request.form.get('plsyear_of_passing')
#         plscompany_name = request.form.get('plscompany_name')
#         plsjob_title = request.form.get('plsjob_title')
#         plssalary_offered = request.form.get('plssalary_offered')
#         plsplacement_date = request.form.get('plsplacement_date')
#         plsplacement_status = request.form.get('plsplacement_status')
#         plsresume = request.files.get('plsresume')
#         plslinkedin = request.form.get('plslinkedin')
#         plsgithub = request.form.get('plsgithub')
#         plsskills = request.form.get('plsskills')
#         if plsresume:
#             pdf_data = plsresume.read()
#             pdf_data_base64 = base64.b64encode(pdf_data).decode('utf-8')
#             connection = sqlite3.connect('logins3.db')
#             cursor = connection.cursor()
#             cursor.execute('INSERT INTO addnewplstudent(plstudent_id,plsname, plemail, plsphone_number, plsgender, plsbranch, plsyear_of_passing, plscompany_name, plsjob_title, plssalary_offered, plsplacement_date, plsplacement_status, plsresume, plslinkedin, plsgithub, plsskills) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (plstudent_id, plsname, plemail, plsphone_number, plsgender, plsbranch, plsyear_of_passing, plscompany_name, plsjob_title, plssalary_offered, plsplacement_date, plsplacement_status, pdf_data_base64, plslinkedin, plsgithub, plsskills))
#             connection.commit()
#             cursor.close()
#             connection.close()
#     return render_template('welcometp.html', add_plstudents=True)


@app.route('/add_plstudents', methods=['POST', 'GET'])
def add_plstudents():
    success_message = None
    if request.method == 'POST':
        plstudent_id = request.form.get('plstudent_id')
        plsname = request.form.get('plsname')
        plemail = request.form.get('plsemail')
        plsphone_number = request.form.get('plsphone_number')
        plsgender = request.form.get('plsgender')
        plsbranch = request.form.get('sbranched')  # Fix the name here
        plsyear_of_passing = request.form.get('plsyear_of_passing')
        plscompany_name = request.form.get('plscompany_name')
        plsjob_title = request.form.get('plsjob_title')
        plssalary_offered = request.form.get('plssalary_offered')
        plsplacement_date = request.form.get('plsplacement_date')
        plsplacement_status = request.form.get('plsplacement_status')
        plsresume = request.files.get('plsresume')  # Correct file handling
        plslinkedin = request.form.get('plslinkedin')
        plsgithub = request.form.get('plsgithub')
        plsskills = request.form.get('plsskills')
        if plsresume:
            pdf_data = plsresume.read()
            pdf_data_base64 = base64.b64encode(pdf_data).decode('utf-8')
            connection = sqlite3.connect('logins2.db')
            cursor = connection.cursor()
            cursor.execute('INSERT INTO addplstudents(plstudent_id, plsname, plemail, plsphone_number, plsgender, plsbranch, plsyear_of_passing, plscompany_name, plsjob_title, plssalary_offered, plsplacement_date, plsplacement_status, plsresume, plslinkedin, plsgithub, plsskills) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (plstudent_id, plsname, plemail, plsphone_number, plsgender, plsbranch, plsyear_of_passing, plscompany_name, plsjob_title, plssalary_offered, plsplacement_date, plsplacement_status, pdf_data_base64, plslinkedin, plsgithub, plsskills))
            connection.commit()
            cursor.close()
            connection.close()
            success_message = "Data has been successfully added."
    return render_template('welcometp.html', add_plstudents=True,success_message=success_message)



@app.route('/display_plstudents_datascience')
def display_plstudents_datascience():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM addplstudents where plsbranch='DATASCIENCE';")
    plstudents = cursor.fetchall()
    cursor.close()
    connection.close()
    plstud_id=plstudents[0][0]
    print("the placed student id is ",plstud_id)
    return render_template('placed_students.html', plstudents=plstudents,plstudents_id=plstud_id)

@app.route('/display_plstudents_cse')
def display_plstudents_cse():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM addplstudents where plsbranch='COMPUTERSCIENCE';")
    plstudents = cursor.fetchall()
    cursor.close()
    connection.close()
    plstud_id=plstudents[0][0]
    print("the placed student id is ",plstud_id)
    return render_template('placed_students.html', plstudents=plstudents,plstudents_id=plstud_id)

@app.route('/display_plstudents_ece')
def display_plstudents_ece():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM addplstudents where plsbranch='ECE';")
    plstudents = cursor.fetchall()
    cursor.close()
    connection.close()
    plstud_id=plstudents[0][0]
    print("the placed student id is ",plstud_id)
    return render_template('placed_students.html', plstudents=plstudents,plstudents_id=plstud_id)

@app.route('/display_plstudents_civil')
def display_plstudents_civil():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM addplstudents where plsbranch='CIVIL';")
    plstudents = cursor.fetchall()
    cursor.close()
    connection.close()
    plstud_id=plstudents[0][0]
    print("the placed student id is ",plstud_id)
    return render_template('placed_students.html', plstudents=plstudents,plstudents_id=plstud_id)

@app.route('/display_plstudents_mech')
def display_plstudents_mech():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM addplstudents where plsbranch='MECH';")
    plstudents = cursor.fetchall()
    cursor.close()
    connection.close()
    plstud_id=plstudents[0][0]
    print("the placed student id is ",plstud_id)
    return render_template('placed_students.html', plstudents=plstudents,plstudents_id=plstud_id)

@app.route('/display_plstudents_aiml')
def display_plstudents_aiml():
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM addplstudents where plsbranch='AIML';")
    plstudents = cursor.fetchall()
    cursor.close()
    connection.close()
    plstud_id=plstudents[0][0]
    print("the placed student id is ",plstud_id)
    return render_template('placed_students.html', plstudents=plstudents,plstudents_id=plstud_id)

# @app.route('/get_pdf')
# def get_pdf():
#     connection = sqlite3.connect('logins2.db')
#     cursor = connection.cursor()
#     query_pdf = "SELECT plsresume FROM addplstudents" 
#     cursor.execute(query_pdf)
#     pdf_data_base64 = cursor.fetchone()
#     cursor.close()
#     connection.close()
#     if pdf_data_base64 and pdf_data_base64[0] is not None:
#         pdf_data = base64.b64decode(pdf_data_base64[0])
#         pdf_io = io.BytesIO(pdf_data)
#         return send_file(pdf_io, download_name='leave_pdf.pdf', mimetype='application/pdf')

# @app.route('/get_pdf')
# def get_pdf():
#     plstudent_id = request.args.get('plstudent_id')
#     connection = sqlite3.connect('logins2.db')
#     cursor = connection.cursor()
#     query_pdf = "SELECT plsresume FROM addplstudents WHERE plstudent_id = ?"
#     cursor.execute(query_pdf, (plstudent_id,))
#     pdf_data_base64 = cursor.fetchone()
#     cursor.close()
#     connection.close()
#     if pdf_data_base64 and pdf_data_base64[0] is not None:
#         pdf_data = base64.b64decode(pdf_data_base64[0])
#         pdf_io = io.BytesIO(pdf_data)
#         return send_file(pdf_io, download_name='leave_pdf.pdf', mimetype='application/pdf')
#     else:
#         return "PDF not found"  # Or any other appropriate response
@app.route('/get_resume')
def get_resume():
    return render_template('get_resume.html')

@app.route("/alldepartments_plstu")
def alldepartments_plstu():
    tpusername=request.args.get("tpusername")
    return render_template('welcometp.html',is_alldepartments_plstu=True,tpusername=tpusername)
    
@app.route("/alldepartments_ppl")
def alldepartments_ppl():
    tpusername=request.args.get("tpusername")
    return render_template('welcomeprincipal.html',is_alldepartments_ppl=True,tpusername=tpusername)
    
@app.route('/get_pdf')
def get_pdf():
    plstudents_id = request.args.get('plstudentsid')
    print("the student id from final is  is",plstudents_id)
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query_pdf = "SELECT plsresume FROM addplstudents WHERE plstudent_id = ?"
    cursor.execute(query_pdf, (plstudents_id,))
    pdf_data_base64 = cursor.fetchone()
    cursor.close()
    connection.close()
    if pdf_data_base64 and pdf_data_base64[0] is not None:
        pdf_data = base64.b64decode(pdf_data_base64[0])
        pdf_io = io.BytesIO(pdf_data)
        return send_file(pdf_io, download_name='student_resume.pdf', mimetype='application/pdf')
    else:
        return "PDF not found"  # Or any other appropriate response
  
# @app.route('/display_plstudents')
# def display_plstudents():
#     connection = sqlite3.connect('logins2.db')
#     cursor = connection.cursor()
#     cursor.execute('SELECT * FROM addplstudents')
#     plstudents = cursor.fetchall()
#     cursor.close()
#     connection.close()
#     plstud_id = plstudents[0][0]
#     print("the placed student id is ", plstud_id)
#     return render_template('placed_students.html', plstudents=plstudents, plstudents_id=plstud_id)

@app.route("/alldepartments_attends")
def alldepartments_attends():
    tpusername=request.args.get("tpusername")
    return render_template('welcomeprincipal.html',is_alldepartments_attends=True,tpusername=tpusername)
    


@app.route('/get_data_science_attendance')
def get_data_science_attendance():
    conn = sqlite3.connect('logins2.db') 
    cursor = conn.cursor()
    cursor.execute("SELECT sid, attendance FROM Studentss WHERE course ='DATASCIENCE';")
    data = cursor.fetchall()
    conn.close()
    return render_template('chart.html', data=data)

@app.route('/get_ece_attendance')
def get_ece_attendance():
    conn = sqlite3.connect('logins2.db') 
    cursor = conn.cursor()
    cursor.execute("SELECT sid, attendance FROM Studentss WHERE course ='ECE';")
    data = cursor.fetchall()
    conn.close()
    return render_template('chart.html', data=data)

@app.route('/get_aiml_attendance')
def get_aiml_attendance():
    conn = sqlite3.connect('logins2.db') 
    cursor = conn.cursor()
    cursor.execute("SELECT sid, attendance FROM Studentss WHERE course ='AIML';")
    data = cursor.fetchall()
    conn.close()
    return render_template('chart.html', data=data)

@app.route('/get_cse_attendance')
def get_cse_attendance():
    conn = sqlite3.connect('logins2.db') 
    cursor = conn.cursor()
    cursor.execute("SELECT sid, attendance FROM Studentss WHERE course ='CSE';")
    data = cursor.fetchall()
    conn.close()
    return render_template('chart.html', data=data)

@app.route('/get_civil_attendance')
def get_civil_attendance():
    conn = sqlite3.connect('logins2.db') 
    cursor = conn.cursor()
    cursor.execute("SELECT sid, attendance FROM Studentss WHERE course ='CIVIL';")
    data = cursor.fetchall()
    conn.close()
    return render_template('chart.html', data=data)

@app.route('/get_mech_attendance')
def get_mech_attendance():
    conn = sqlite3.connect('logins2.db') 
    cursor = conn.cursor()
    cursor.execute("SELECT sid, attendance FROM Studentss WHERE course ='MECH';")
    data = cursor.fetchall()
    conn.close()
    return render_template('chart.html', data=data)


@app.route('/payfees')
def payfees():
    return render_template('payments.html')

@app.route("/getprincipalcomplaints")
def getprincipalcomplaints():
    tpusername=request.args.get("plusername")
    connection = sqlite3.connect('logins2.db')
    cursor = connection.cursor()
    query = "SELECT * FROM pcomplaints"
    cursor.execute(query)
    results = cursor.fetchall()
    cimage = results[0][-1]
    pcompresultss = [{'cid': crollno, 'cname': cname, 'cdepartment': cdepartment, 'csection': csection,
                     'ccategory': ccategory, 'cpriority': cpriority, 'cdescription': descriptions,'cimage':base64.b64encode(cimage).decode('utf-8')} for
                    crollno, cname, cdepartment, csection, ccategory, cpriority, descriptions,cimage in results]
    cursor.close()
    return render_template('welcomeprincipal.html',pcompresultss=pcompresultss,is_pcompresultss=True,cimage=cimage,tpusername=tpusername)





if __name__ == '__main__':
    app.run(debug=True)