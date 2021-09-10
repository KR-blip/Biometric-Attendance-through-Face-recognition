from flask import Blueprint, render_template, redirect, url_for, request, flash
import numpy as np
import cv2
import os
import pandas as pd
import csv
from datetime import date 
from datetime import datetime
from pathlib import Path

def rec():
    #knn algorithm
    def distance(v1,v2):
        #eucledian
        return np.sqrt(((v1-v2)**2).sum())

    def knn(train,test,k=5):
        dist=[]
        
        for i in range(train.shape[0]):
            #get vector and label
            ix=train[i,:-1]
            iy=train[i,-1]
            
            #compute the distance from test point
            
            d=distance(test,ix)
            dist.append([d,iy])
        
        #sort based on distance and get top k
        dk=sorted(dist,key=lambda x:x[0])[:k]
        
        #retrieve only the label
        ouput=np.array(dk)[:,-1]
        
        #get frequency of each label
        output=np.unique(labels,return_counts=True)
        
        #Find max frequency and correspondng label 
        index=np.argmax(output[1])
        return output[0][index]
    #initialize camera

    cap=cv2.VideoCapture(0)

    face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    skip=0
    face_data=[]  #this is your training data  #x-value of our data
    dataset_path ='./data/'   #store faces here
    labels=[]  #y value of our data

    class_id=0  #labels for the give file
    names={} #Mapping between id and name,i.e name will be mapped to an id

    #load training data

    # data preparation
    #iterate directory

    for fx in os.listdir(dataset_path):  #will get all the fileswhich are in the folder
        if fx.endswith('.npy'):
            #create mapping between class_id and name
            names[class_id]=fx[:-4]
            print("Loaded"+fx)
            data_item=np.load(dataset_path+fx)  #this will load the file
            face_data.append(data_item)
            
            #create labels for class
            target=class_id*np.ones((data_item.shape[0],)) #arrray of ones of size npy
            class_id +=1 # every time id incremented
            labels.append(target)
            
    #concatinate all items in list into single list
    face_dataset=np.concatenate(face_data,axis=0)
    face_labels=np.concatenate(labels,axis=0).reshape((-1,1))
    print(face_dataset.shape)
    print(face_labels.shape)

    #concatinate both x and y values into a single training set
    # as our knn excepts one training matrix in which we have x data and y data combined in a single matrix
    trainset=np.concatenate((face_dataset,face_labels),axis=1)
    print(trainset.shape)


    #Testing
    while True:
        ret,frame=cap.read()
        
        if ret ==False:
            continue
        
        faces=face_cascade.detectMultiScale(frame,1.3,5)
        #print(faces)  # x,y,width,height
        
        #extract(crop out the required face): region of interest
        # by default first is y axis and second is x axis
        #add offset of 10 pixel in all direction of the face
        for face in faces: #pick the last face as it is largest   
            x,y,w,h =face
            offset=10
            #slicing
            face_section=frame[y-offset:y+h+offset,x-offset:x+w+offset]
            face_section=cv2.resize(face_section,(100,100))
        
            out=knn(trainset,face_section.flatten())
            
            #Display on screem the name and rectange around it
            pred_name=names[int(out)]
            
            cv2.putText(frame,pred_name,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            
        
        cv2.imshow("Press q to quit",frame) #frame
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    cv2.destroyAllWindows()

    
   

    now = datetime.now()
    
    
    current_time = now.strftime("%H:%M:%S")
    today=str(date.today())

    dayy=datetime.today().strftime('%A')
    

    #open the file or create it if it doesnt exist

    
    my_file = Path("./test.csv")
    flag=0
    if my_file.is_file():
        with open('test.csv',newline="") as csv_file:
            data=csv.reader(csv_file)
            first_line = True
            places = []
            for row in data:
                if not first_line:
                    if row[0]==pred_name:
                        if row[1]==today:
                            flag=1
                            if row[4]=="-": 
                                                             
                                places.append({
                                "Employee-ID": row[0],
                                "Date": row[1],
                                "Time": row[2],
                                "Day": row[3],
                                "Leaving Time": current_time
                                })
                            else:
                                return "Nope"
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
        if flag==0:
            places.append({
            "Employee-ID": pred_name,
            "Date": today,
            "Time": current_time,
            "Day": dayy,
            "Leaving Time": "-"
            })
        keys = places[0].keys()
        with open('test.csv', 'w', newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(places)
    else:
        with open ('test.csv','a', newline='') as my_file:
            csv_writter = csv.writer(my_file)
            csv_writter.writerow(["Employee-ID", "Date","Time","Day","Leaving Time"])
            my_data = [pred_name,today,current_time,dayy,"-"]
            csv_writter.writerow(my_data)

    return pred_name
    