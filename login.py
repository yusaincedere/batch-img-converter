from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import messagebox
import hashlib
import pymysql


###FUNCTIONS


def get_dbcred():
    with open("/Users/yusai/Desktop/rdscred.txt","r") as file:
        data = file.read()
        lines = data.split("\n")
        return lines


def get_cred():
    with open("userinfo.txt") as file:
        data = file.read()
        lines = data.split("\n")
        return lines

def save_current_user(username,email):
    with open("userinfo.txt", "w") as text_file:
        text_file.write(f"{username}")
        text_file.write(email)


def encrypt_password(password):
    sha_signature = \
        hashlib.sha256(password.encode()).hexdigest()
    return sha_signature


def register_window():
    window.destroy()
    import register


def signin():
    if entryEmail.get() == '' or entryPassword.get()=='':
        messagebox.showerror("Error","All Fields Are Required")
    else:
        try:
            con = pymysql.connect(host=host,
                                  user=dbusername, password=dbpassword, database=dbname)
            cur = con.cursor()
            password = encrypt_password(entryPassword.get())
            sql = "SELECT * from user where email=%s and password = %s "
            values = (entryEmail.get(),password)
            cur.execute(sql,values)
            row = cur.fetchone()

            if row == None:
                messagebox.showerror("Error", "Invalid email or password")

            else:
                save_current_user(row[1],row[2])
                window.destroy()
                import main_window
            con.close()

        except Exception as e:
            messagebox.showerror("Error",e)



#RDS DATABASE CREDS
dbcreds = get_dbcred()
host = dbcreds[0]
dbusername = dbcreds[1]
dbpassword = dbcreds[2]
dbname = dbcreds[3]


### GUI
#Login Window
window = Tk()
window.geometry('500x500+150+100')
window.title('İMG-CON')
window.configure(bg="gray55")

#LoginFrame
loginFrame = Frame(window,width=400,height=400)
loginFrame.configure(bg="gray55")
loginFrame.place(x=50,y=50)



#Email Label
emailLabel = Label(loginFrame,text='Email',font=('arial',11,'bold'),fg='white',bg ='gray55')
emailLabel.place(x=150,y=110)
entryEmail = Entry(loginFrame,font=('arial',11,'bold'))
entryEmail.place(x=150,y=140)


#Password Label
passwordLabel = Label(loginFrame,text='Password',font=('arial',11,'bold'),fg='white',bg ='gray55')
passwordLabel.place(x=150,y=170)
entryPassword = Entry(loginFrame,font=('arial',11,'bold'),show='*')
entryPassword.place(x=150,y=200)




#Register Button
registerButton = Button(loginFrame,bg='gray30',text="Register",fg="white"
                     ,activebackground='gray30', command=register_window)
registerButton.place(x=150,y=250)



#Login Button

loginButton = Button(loginFrame,bg='gray30',text="Login",fg="white"
                     ,activebackground='gray30',command=signin)
loginButton.place(x=250,y=250)



window.mainloop()

