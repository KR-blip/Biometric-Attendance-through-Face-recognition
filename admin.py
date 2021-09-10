import sys, cv2, os.path
import numpy as np
import csv,random
from pathlib import Path
from recog import rec
from flask import Blueprint, render_template
from openpyxl import Workbook
from flask import Blueprint, render_template, redirect, url_for, request, flash

admin = Blueprint('admin', __name__)




@admin.route('/train')
def atten():
    return render_template('train.html')

@admin.route('/train',methods=['POST'])
def train():
    name=request.form['name']
    email=request.form['email']
    dob=request.form['dob']
    doj=request.form['doj']

    id=str(random.randint(1,200))
    skip=0
    face_data=[]
    dataset_path ='./data/'   #store faces here
    u_id=name+id
    u_id=str(u_id)

    my_data = [name,u_id,email,dob,doj]

    #for each row append it to our CSV file
    
    
    my_file = Path("./testregister.csv")
    if my_file.is_file():
        with open ('testregister.csv','a', newline='') as my_file:
            csv_writter = csv.writer(my_file)
            csv_writter.writerow(my_data)
      
    else:
        from datetime import date
        today = date.today()
        date=today.strftime("%B %d, %Y")

        with open ('testregister.csv','a', newline='') as my_file:
            csv_writter = csv.writer(my_file)
            csv_writter.writerow(["Name", "uid","email","dob","doj"])
            csv_writter.writerow(my_data)
        
    
    
               
    rows=(name,u_id,email,dob,doj)
    
    #initialize camera

    cap=cv2.VideoCapture(0)
    

    face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


    
    count=0        
    while True:
        ret,frame=cap.read()
        
        if ret ==False:
            continue
        
        #convert our iage to gray sacle
        gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(frame,1.3,5)
        #print(faces)  # x,y,width,height
        
        
        #we have used lamda function and done sorting
        #f[2]=w
        #f[3]=h
        #w*h gives the area captured
        faces=sorted(faces,key=lambda f:f[2]*f[3])
        
    
        for face in faces[-1:]: #pick the last face as it is largest   
            x,y,w,h =face
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            
        
        #extract(crop out the required face): region of interest
        # we will slice it
        # by default first is y axis and second is x axis
        #add offset of 10 pixel in all direction of the face
            x,y,w,h =face
            offset=10
            #slicing
            face_section=frame[y-offset:y+h+offset,x-offset:x+w+offset]
            face_section=cv2.resize(face_section,(100,100)) #new size
            
            cv2.imshow("Face Section",face_section) #face section
        
        #we will store only 10th frame
            skip+=1 #after evry 10th frame we increase the counter  by one
            
            if skip%1==0:
                #store the 10th face
                face_data.append(face_section)
                print(len(face_data))  #how many faces have i captured so far
        
        
        cv2.imshow("Face Training",frame) #frame
        
        if len(face_data)==120:
            break
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

            #convert our face list array into a numpy array

    face_data=np.asarray(face_data) #converted python list to numpy array
    face_data = face_data.reshape((face_data.shape[0],-1))

    #number of rows=number of faces
    #number of column automatically will be set
    
    #save this data into file system
    
    np.save(dataset_path +u_id+'.npy',face_data) #(path,file you want to save)
    print("Data Successfully save at"+dataset_path+name+'.npy') #npy=numpy file

    cap.release()
     
    cv2.destroyAllWindows()


    flash('Your face is trained.')
    return render_template('train.html',value=u_id)

@admin.route('/ad_down')
def ad_down():
    return render_template('ad_down.html')
    

@admin.route('/ad_down', methods=['POST'])
def ad_downn():
    flag=0
    empid=request.form['empid']
    e_time=request.form['e_time']
    l_time=request.form['l_time']
    datee=request.form['daate']
    day_s=request.form['day_s']
    a=open('test.csv','r')
    csv_f=csv.reader(a)
    for row in csv_f:
        if row[0]==empid:
            flag=1
    if flag==0:
        flash('Incorrect Employee-ID.')
        return render_template('ad_down.html')
    else:
        with open('test.csv',newline="") as csv_file:
            data=csv.reader(csv_file)
            first_line = True
            check=0
            places = []
            for row in data:
                if not first_line:
                    if row[0]==empid:
                        if row[1]==datee:
                            check=1
                            places.append({
                            "Employee-ID": row[0],
                            "Date": row[1],
                            "Time": row[2],
                            "Day": row[3],
                            "Leaving Time": l_time
                            })
                        else:
                            places.append({
                            "Employee-ID": row[0],
                            "Date": row[1],
                            "Time": row[2],
                            "Day": row[3],
                            "Leaving Time": row[4]
                            })

                        
                    else:
                        places.append({
                        "Employee-ID": row[0],
                        "Date": row[1],
                        "Time": row[2],
                        "Day": row[3],
                        "Leaving Time": row[4]
                        })
                else:
                        first_line = False
            if check==0:
                places.append({
                    "Employee-ID": empid,
                    "Date": datee,
                    "Time": e_time,
                    "Day": day_s,
                    "Leaving Time": l_time
                            })
        keys = places[0].keys()
        with open('test.csv', 'w', newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(places)
        flash('Updated details.')
        return render_template('ad_down.html')
        


