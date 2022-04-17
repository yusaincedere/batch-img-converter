from tkinter import *
import os
import os.path
from tkinter import filedialog,ttk,messagebox
from PIL import Image,ImageTk
import pymysql
import boto3

IMAGEPAGE2 =""
IMAGEDIR = ""
OLDIMAGE = ""
SAVELOC = ""
CURRENTFRAME = 2
ENTRYSTATE = 1

#FUNCTIONS


def logout():
    open('userinfo.txt', 'w').close()
    mainWindow.destroy()
    import login


def get_s3cred():
    with open("/Users/yusai/Desktop/s3cred.txt","r") as file:
        data = file.read()
        lines = data.split("\n")
        return lines

def get_dbcred():
    with open("/Users/yusai/Desktop/rdscred.txt","r") as file:
        data = file.read()
        lines = data.split("\n")
        return lines


def get_user_id():
    try:
        con = pymysql.connect(host=host,
                              user=dbusername, password=dbpassword, database=dbname)
        cur = con.cursor()
        sql = "SELECT id from user where email=%s"
        values = (userinfo[1])
        cur.execute(sql, values)
        row = cur.fetchone()

        if row == None:
            messagebox.showerror("Error", "USER NOT FOUND")

        else:
            print(row)
            return row[0]

        con.close()

    except Exception as e:
        messagebox.showerror("Error", e)

def delete_s3():
    try:
        filename = listBoxPage2.get(listBoxPage2.curselection())
        s3 = boto3.resource(
            service_name=service_name,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        userId = get_user_id()
        obj = s3.Object("imgconb", f"{userId}/{filename}")
        obj.delete()
        listBoxPage2.delete(listBoxPage2.curselection())
        listBoxPage2.select_set(0)
    except Exception as e:
        print(e)



def download_s3():
    try:
        filename = listBoxPage2.get(listBoxPage2.curselection())
        s3 = boto3.resource(
            service_name=service_name,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        userId = get_user_id()
        downLoc = select_down_loc()
        result = s3.Bucket('imgconb').download_file(f'{userId}/{filename}',f'{downLoc}/{filename}')
        print(result)
    except Exception as e:
        print(e)

def upload_s3():
    s3 = boto3.resource(
        service_name=service_name,
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    userId = get_user_id()
    filename = listBox.get(listBox.curselection())
    result = s3.Bucket('imgconb').upload_file(f'{IMAGEDIR}//{filename}',f'{userId}/{filename}')
    print(result)



def show_page2():
    listBoxPage2.delete(0,END)
    s3 = boto3.resource(
        service_name=service_name,
        region_name= region_name,
        aws_access_key_id= aws_access_key_id,
        aws_secret_access_key= aws_secret_access_key
    )
    userId = str(get_user_id())
    s3_bucket = s3.Bucket("imgconb")
    files_in_s3 = [f.key.split(userId + "/")[1] for f in s3_bucket.objects.filter(Prefix=userId).all()]
    for filename in files_in_s3:
        listBoxPage2.insert(END,filename)
        print(filename)


def save_current_user(username,email):
    with open("userinfo.txt", "w") as text_file:
        text_file.write(f"{username}\n")
        text_file.write(email)

def update_user_info():
    if entryNamePage2.get() != '' or entryEmailPage2.get() != '':
        try:
            change_enrty_state()
            con = pymysql.connect(host=host,
                                  user=dbusername, password=dbpassword, database=dbname)
            cur = con.cursor()
            print(userinfo[1])
            sql = "UPDATE user SET name=%s where email=%s"
            values = (userinfo[0],userinfo[1])
            cur.execute(sql,values)
            con.commit()
            save_current_user(username=entryNamePage2.get(),email=userinfo[1])
            messagebox.showinfo("Succes","UPDATED")
            con.close()
        except Exception as e:
            messagebox.showerror("Error",e)
            con.close()





def change_enrty_state():
    global ENTRYSTATE
    if ENTRYSTATE == 1:
        entryNamePage2['state'] = NORMAL
        entryEmailPage2['state'] = NORMAL
        ENTRYSTATE = 2
    else:
        entryNamePage2['state'] = DISABLED
        entryEmailPage2['state'] = DISABLED
        ENTRYSTATE = 1

def raise_frame(frame):
    global CURRENTFRAME
    if frame == 1 and CURRENTFRAME == 2:
        CURRENTFRAME = 1
        frame1.tkraise()
    elif frame == 2 and CURRENTFRAME ==1:
        CURRENTFRAME = 2
        frame2.tkraise()



def read_user_info():
    with open("userinfo.txt") as file:
        data = file.read()
        lines = data.split("\n")
        return lines


def convert(filename,newextension):
    extension = os.path.splitext(filename)[1]
    filenamenoex =  os.path.splitext(filename)[0]
    valuex = int(xvalue.get())
    valuey = int(yvalue.get())
    if extension == ".png":
        if newextension == "JPG":
            img = Image.open(f"{IMAGEDIR}//{filename}")
            img = img.convert('RGB')
            if valuex != "" and valuey != "" and valuex != 0 and valuey != 0:
               img = img.resize((valuex,valuey),Image.ANTIALIAS)
            img.save(f"{SAVELOC}//{filenamenoex}.jpg",'jpeg')
        elif newextension == "WEBP":
            img = Image.open(f"{IMAGEDIR}//{filename}")
            img = img.convert('RGB')
            if valuex != "" and valuey != "" and valuex != 0 and valuey != 0:
                img = img.resize((valuex, valuey), Image.ANTIALIAS)
            img.save(f"{SAVELOC}//{filenamenoex}.webp", 'webp')
        elif newextension == "PNG":
            messagebox.showerror("Error","Same Format")
    elif extension == ".jpg":
        if newextension == "PNG":
            img = Image.open(f"{IMAGEDIR}//{filename}")
            img = img.convert('RGB')
            if valuex != "" and valuey != "" and valuex != 0 and valuey != 0:
               img = img.resize((valuex,valuey),Image.ANTIALIAS)
            img.save(f"{SAVELOC}//{filenamenoex}.png",'png')
        elif newextension == "WEBP":
            print("webp")
            img = Image.open(f"{IMAGEDIR}//{filename}")
            img = img.convert('RGB')
            if valuex != "" and valuey != "" and valuex != 0 and valuey != 0:
                img = img.resize((valuex, valuey), Image.ANTIALIAS)
            img.save(f"{SAVELOC}//{filenamenoex}.webp", 'webp')
        elif newextension == "JPG":
            messagebox.showerror("Error","Same Format")
    elif extension == ".webp":
        if newextension == "JPG":
            img = Image.open(f"{IMAGEDIR}//{filename}")
            img = img.convert('RGB')
            if valuex != "" and valuey != "" and valuex != 0 and valuey != 0:
               img = img.resize((valuex,valuey),Image.ANTIALIAS)
            img.save(f"{SAVELOC}//{filenamenoex}.jpg",'jpeg')
        elif newextension == "PNG":
            img = Image.open(f"{IMAGEDIR}//{filename}")
            img = img.convert('RGB')
            if valuex != "" and valuey != "" and valuex != 0 and valuey != 0:
                img = img.resize((valuex, valuey), Image.ANTIALIAS)
            img.save(f"{SAVELOC}//{filenamenoex}.png", 'png')
        elif newextension == "WEBP":
            messagebox.showerror("Error","Same Format")
    else:
        messagebox.showerror("Error","Invalid format  Valid formats(png,jpg,webp)")




def trace_x_value(*args):
    value = xvalue.get()
    if len(value) > 4: xvalue.set(value[:4])



def trace_y_value(*args):
    value = yvalue.get()
    if len(value) > 4: yvalue.set(value[:4])


def is_number(inStr,acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True


def show(event):
    global OLDIMAGE,NEWIMAGE
    if listBox.curselection() != ():
        n = listBox.curselection()
        imgname = listBox.get(n)
        image = Image.open(os.path.join(IMAGEDIR,imgname)).resize((400,250))
        img = ImageTk.PhotoImage(image)
        orimgLabel.config(image=img)
        orimgLabel.image = img






def selectFile():
    listBox.delete(0, END)
    global IMAGEDIR
    IMAGEDIR = ''
    directory = filedialog.askdirectory(initialdir=os.getcwd(),title="Select Image Folder")
    IMAGEDIR = directory
    extensionsToCheck = ('.jpg', '.png', '.webp','.jpeg')
    if directory != "":
        for filename in os.listdir(directory):
            if filename.endswith(extensionsToCheck):
                listBox.insert(END,filename)
                image = Image.open(os.path.join(IMAGEDIR, filename)).resize((400, 250))
                img = ImageTk.PhotoImage(image)
                orimgLabel.config(image=img)
                orimgLabel.image = img
                listBox.select_set(0)


def select_down_loc():
    directory = filedialog.askdirectory(initialdir=os.getcwd(),title="Select Download Location")
    if directory != "" :
        return directory


def select_save_loc():
    global SAVELOC
    SAVELOC = ''
    directory = filedialog.askdirectory(initialdir=os.getcwd(),title="Select Image Folder")
    SAVELOC = directory
    if directory != "" and IMAGEDIR !="":
        newextension = current_var.get()
        for item in listBox.get(0,END):
            convert(item,newextension)








#S3 STOREGE CREDS
s3creds = get_s3cred()
service_name = s3creds[0]
region_name = s3creds[1]
aws_access_key_id = s3creds[2]
aws_secret_access_key = s3creds[3]

#RDS DATABASE CREDS
dbcreds = get_dbcred()
host = dbcreds[0]
dbusername = dbcreds[1]
dbpassword = dbcreds[2]
dbname = dbcreds[3]






#GUI
mainWindow = Tk()

frame1 = Frame(mainWindow,width=500,height=500,bg="gray55")
frame1.place(x=0,y=0)
frame2 = Frame(mainWindow,width=500,height=500,bg="gray55")
frame2.place(x=0,y=0)



mainWindow.geometry('500x500+150+100')
mainWindow.title('İMG-CON')
mainWindow.configure(bg="gray55")


#  FRAME 1

convertPageButton = Button(frame1,text="Image Settings",command=lambda:raise_frame(1),bg="gray30",fg="white")
convertPageButton.place(x=0,y=0)

accountPageButton = Button(frame1,text="Account Settings",command=lambda:raise_frame(2),bg="gray30",fg="white")
accountPageButton.place(x=90,y=0)



userinfo = read_user_info()
usernameLabel = Label(frame1,text=f'{userinfo[0]}',font=('arial',8,'bold'),fg='white',bg ='gray55')
usernameLabel.place(x=450,y=0)


# Original image Frame
orimgFrame = Frame(frame1,width=400,height=250)
orimgFrame.configure(bg="gray55")
orimgFrame.place(x=50,y=50)
orimgLabel = Label(orimgFrame,width=400,height=250,bg="gray55",image=OLDIMAGE)
orimgLabel.place(x=0,y=0)




#Setting Frame
settingFrame = Frame(frame1,width=200,height=100)
settingFrame.configure(bg="gray55")
settingFrame.place(x=250,y=350)


sizeLabel = Label(settingFrame,text='Size:',font=('arial',8,'bold'),fg='white',bg ='gray55')
sizeLabel.place(x=0,y=0)
xvalue = StringVar()
xvalue.trace('w', trace_x_value)
entrySizeX = Entry(settingFrame,font=('arial',8,'bold'),width=4,validate="key",textvariable=xvalue)
entrySizeX['validatecommand'] = (entrySizeX.register(is_number),'%P','%d')
entrySizeX.place(x=60,y=0)

sizeLabel = Label(settingFrame,text='x',font=('arial',8,'bold'),fg='white',bg ='gray55')
sizeLabel.place(x=90,y=0)


yvalue = StringVar()
yvalue.trace('w', trace_y_value)
entrySizeY = Entry(settingFrame,font=('arial',8,'bold'),width=4,validate="key",textvariable=yvalue)
entrySizeY['validatecommand'] = (entrySizeY.register(is_number),'%P','%d')
entrySizeY.place(x=105,y=0)


#Format setting
FormatLabel = Label(settingFrame,text='Format:',font=('arial',8,'bold'),fg='white',bg ='gray55')
FormatLabel.place(x=0,y=40)
current_var = StringVar()
combobox = ttk.Combobox(settingFrame, textvariable=current_var,width=9)
combobox['state'] = 'readonly'
combobox['values']=('JPG','PNG','WEBP')
combobox.current(0)
combobox.place(x=60,y=40)

saveAllButton = Button(settingFrame,text="Save",command=select_save_loc,bg="gray30",fg="white")
saveAllButton.place(x=150,y=75)

uploadAllButton = Button(settingFrame,text="Upload",command=upload_s3,bg="gray30",fg="white")
uploadAllButton.place(x=80,y=75)


#List Box
listBox = Listbox(frame1)
listBox.bind("<<ListboxSelect>>",show)
listBox.place(x=50 ,y=350, height=100,width=150)

#Select File Button

selectFileButton = Button(frame1,text="Select File",command=selectFile,bg="gray30",fg="white")
selectFileButton.place(x=50,y=320)


logoutButton = Button(frame1,text="Logout",command=logout,bg="gray30",fg="white")
logoutButton.place(x=445,y=30)

# FRAME 2


convertPage2Button = Button(frame2,text="Image Settings",command=lambda:raise_frame(1),bg="gray30",fg="white")
convertPage2Button.place(x=0,y=0)

accountPage2Button = Button(frame2,text="Account Settings",command=lambda:raise_frame(2),bg="gray30",fg="white")
accountPage2Button.place(x=90,y=0)




editButton = Button(frame2,bg='gray30',text="Edit",fg="white"
                     ,activebackground='gray30',command=change_enrty_state)
editButton.place(x=205,y=100)


applyPage2Button = Button(frame2,text="Save",command=update_user_info,bg="gray30",fg="white")
applyPage2Button.place(x=190,y=210)





userNamePage2 = StringVar()
userNamePage2.set( userinfo[0])
userNamePage2abel = Label(frame2,text='Name:',font=('arial',8,'bold'),fg='white',bg ='gray55')
userNamePage2abel.place(x=50,y=150)
entryNamePage2 = Entry(frame2,font=('arial',8,'bold'),state=DISABLED,textvariable=userNamePage2)
entryNamePage2.place(x=100,y=150)

emailPage2 = StringVar()
emailPage2.set( userinfo[1])
emailPage2Label = Label(frame2,text='Email:',font=('arial',8,'bold'),fg='white',bg ='gray55')
emailPage2Label.place(x=50,y=180)
entryEmailPage2 = Entry(frame2,font=('arial',8,'bold'),state=DISABLED,textvariable=emailPage2)
entryEmailPage2.place(x=100,y=180)


showFilesPage2Button = Button(frame2,text="Show Files",command=show_page2,bg="gray30",fg="white")
showFilesPage2Button.place(x=50,y=320)


downloadPage2Button = Button(frame2,text="Download",command=download_s3,bg="gray30",fg="white")
downloadPage2Button.place(x=230,y=350)

deletePage2Button = Button(frame2,text="Delete",command=delete_s3,bg="gray30",fg="white")
deletePage2Button.place(x=230,y=400)

logoutPage2Button = Button(frame2,text="Logout",command=logout,bg="gray30",fg="white")
logoutPage2Button.place(x=445,y=30)

listBoxPage2 = Listbox(frame2)
listBoxPage2.place(x=50 ,y=350, height=100,width=150)



raise_frame(1)
mainWindow.mainloop()