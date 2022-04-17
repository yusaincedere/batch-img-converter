from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
import hashlib
import pymysql





### FUNCTIONS


def get_dbcred():
    with open("/Users/yusai/Desktop/rdscred.txt","r") as file:
        data = file.read()
        lines = data.split("\n")
        return lines


def login_window():
    root.destroy()
    import login


def clear():
    entryName.delete(0,END)
    entryEmail.delete(0,END)
    entryPassword.delete(0,END)
    entryPasswordConfirm.delete(0,END)


def encrypt_password(password):
    sha_signature = \
        hashlib.sha256(password.encode()).hexdigest()
    return sha_signature


def register():
    if entryName.get()=='' or entryEmail.get() ==''\
        or entryPassword.get()=='' or entryPasswordConfirm.get()=='':
        messagebox.showerror('Error','All Fields Are Required')


    elif entryPassword.get() != entryPasswordConfirm.get():
        messagebox.showerror('Error', 'Password Mismatch')

    else:
        try:
            con = pymysql.connect(host=host,
                            user=dbusername,password=dbpassword,database=dbname)
            cur = con.cursor()
            cur.execute("SELECT * FROM user WHERE email=%s",entryEmail.get())
            row = cur.fetchone()
            if row!=None:
                messagebox.showerror("Error","User Already Exists")
                con.close()
            else:
                sql = "INSERT INTO user (name, email,password) VALUES (%s, %s, %s)"
                password = encrypt_password(password=entryPassword.get())
                values = (entryName.get(),entryEmail.get(),password)
                cur.execute(sql,values)
                con.commit()
                con.close()
                messagebox.showinfo("Success","Registration is succesfull")
                clear()
                root.destroy()
                import login

        except Exception as e:
            messagebox.showerror("Error",e)



#RDS DATABASE CREDS
dbcreds = get_dbcred()
host = dbcreds[0]
dbusername = dbcreds[1]
dbpassword = dbcreds[2]
dbname = dbcreds[3]



### GUI
#Register Window
root = Tk()
root.geometry('500x500+150+100')
root.title('İMG-CON')
root.configure(bg="gray55")

#Register Frame
registerFrame = Frame(root,width=400,height=400)
registerFrame.configure(bg="gray55")
registerFrame.place(x=50,y=50)


#Title Label
titleLabel = Label(registerFrame,text="Sign Up",font=('arial',22,'bold'),fg='white',bg='gray55')
titleLabel.place(x=10,y=5)

#Name Label
nameLabel = Label(registerFrame,text='Name',font=('arial',11,'bold'),fg='white',bg ='gray55')
nameLabel.place(x=10,y=80)
entryName = Entry(registerFrame,font=('arial',11,'bold'))
entryName.place(x=10,y=110)

#Email Label
emailLabel = Label(registerFrame,text='Email',font=('arial',11,'bold'),fg='white',bg ='gray55')
emailLabel.place(x=10,y=140)
entryEmail = Entry(registerFrame,font=('arial',11,'bold'))
entryEmail.place(x=10,y=170)

#Password Label
passwordLabel = Label(registerFrame,text='Password',font=('arial',11,'bold'),fg='white',bg ='gray55')
passwordLabel.place(x=10,y=200)
entryPassword = Entry(registerFrame,font=('arial',11,'bold'),show='*')
entryPassword.place(x=10,y=230)


#PasswordConfirm Label
passwordConfirmLabel = Label(registerFrame,text='Confirm Password',font=('arial',11,'bold'),fg='white',bg ='gray55')
passwordConfirmLabel.place(x=10,y=260)
entryPasswordConfirm = Entry(registerFrame,font=('arial',11,'bold'),show='*')
entryPasswordConfirm.place(x=10,y=290)

#Login Button

loginButton = Button(registerFrame,bg='gray30',text="Login",fg="white"
                     ,activebackground='gray30',command=login_window)
loginButton.place(x=100,y=350)


#Register Button
registerButton = Button(registerFrame,bg='gray30',text="Register",fg="white"
                     ,activebackground='gray30', command=register)
registerButton.place(x=10,y=350)

root.mainloop()