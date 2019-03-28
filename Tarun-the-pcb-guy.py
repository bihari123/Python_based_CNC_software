from tkinter import *
import re
import os
import warnings
import serial
import serial.tools.list_ports
import time
import re
import getpass

arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if re.search(r'ttyACM.','ttyACM0').group() or re.search(r'ttyS.','ttyS0').group()
]
if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')

print("Please Enter Your Computer's Password (it is neccessary for giving permission to the board):")

sudoPassword = "tjinthejungle"


command = 'sudo chmod 666 '+arduino_ports[0]
os.system('echo %s|sudo -S %s' % (sudoPassword, command))



arduino = serial.Serial(arduino_ports[0],9600)
print(arduino)

servo_position = 0

def isPendown(servo_position):
    if(servo_position == 0):
        return True
    else:
        return False


def isPenup(servo_position):
    if(servo_position == 90):
        return True
    else:
        return False

def pen_down():
    global servo_position
    time.sleep(1)
    go="D"
    arduino.write(go.encode())
    time.sleep(2)
    servo_position=0
    print("pen down")

def pen_up():
    global servo_position
    time.sleep(1)
    go="U"
    arduino.write(go.encode())
    time.sleep(2)
    servo_position=90
    print("pen up")
    


def fixRes(x,a):
    for n in range(len(a)):
        if(x> a[0] and x < a[len(a)-1]):
            if (x>a[n] and x<a[n+1]):
                if (x <= (a[n] + a[n+1])/2):
                    x=a[n]
                else:
                    x=a[n+1]

        else:
            if(x<a[0]):
                x=a[0]
            elif(x>a[len(a)-1]):
                x=a[len(a)-1]

    return x 





def movement(xi,yi,xf,yf):
    if(xi == xf and yi != yf):
         moveY(yi,yf)
    elif(yi == yf and xi != xf):
         moveX(xi,xf)
    else:
         move_diagonal(xi,yi,xf,yf)

    return
        


def moveY(yi,yf):
    if (yi>yf):
        moveUp(yi - yf)
    else:
        moveDown(yf - yi)

def moveX(xi,xf):
    if (xi>xf):
        moveLeft(xi - xf)
    else:
        moveRight(xf - xi)
    

def move_diagonal(xi,yi,xf,yf):
    if (xi>xf and yi>yf):
        #move_diagonal_lift_up(xi-xf, yi-yf)
        time.sleep(1)
        steps=xi-xf    
        if((steps/20)<10):
            go="DXNYP"+"0"+str(int(steps/20))
        else:
            go="DXNYP"+str(int(steps/20))
        
        print(go)
        arduino.write(go.encode())
        time.sleep(5)    

    elif(xi<xf and yi > yf):
        #move_diagonal_right_up(xf-xi, yi-yf)
        time.sleep(1)
        arduino.write('B'.encode())
        time.sleep(60)
       
    elif(xi > xf and yi < yf):
        #move_diagonal_down_left(xi-xf, yf-yi)
        time.sleep(1)
        arduino.write('C'.encode())
        time.sleep(60)
    elif(xi<xf and yi < yf):
        #move_diagonal_down_right(xf-xi, yf-yi)
        time.sleep(1)
        arduino.write('D'.encode())
        time.sleep(60)




def moveUp(steps):
    time.sleep(1)

    if((steps/20)<10):
        go="YP"+"0"+str(int(steps/20))
    else:
        go="YP"+str(int(steps/20))
        
    print(go)
    arduino.write(go.encode())
    print("up here")
    time.sleep(5)
    






def moveDown(steps):
    time.sleep(1)
    
    if((steps/20)<10):
        go="YN"+"0"+str(int(steps/20))
    else:
        go="YN"+str(int(steps/20))
        
    print(go)
    arduino.write(go.encode())
    print("down here")
    time.sleep(5)
    

    




def moveRight(steps):
    time.sleep(1)
    
    if((steps/20)<10):
        go="XP"+"0"+str(int(steps/20))
    else:
        go="XP"+str(int(steps/20))
        
    print(go)
    arduino.write(go.encode())
    print("right here")
    time.sleep(1)






def moveLeft(steps):
    time.sleep(1)
    
    if((steps/20)<10):
        go="XN"+"0"+str(int(steps/20))
    else:
        go="XN"+str(int(steps/20))
        
    print(go)
    arduino.write(go.encode())
    print("left here")    
    time.sleep(1)











# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):
    # number of displacements
    disp_count=0
    i=0
    j=0
    # Stores current drawing tool used
    drawing_tool = "line"
    
    # Tracks whether left mouse is down
    left_but = "up"
    
    # x and y positions for drawing with pencil
    x_pos, y_pos = None, None
    x_points=[]
    y_points=[]
    # Tracks x & y when the mouse is clicked and released
    x1_line_pt, y1_line_pt, x2_line_pt, y2_line_pt = None, None, None, None
    coordinates=[[None for _ in range(4)] for _ in range(50)]
    

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()

    #Creation of init_window
    def init_window(self):
        
        # changing the title of our master widget      
        self.master.title("Tarun2.0 - The PCB Designer")

        # allowing the widget to take the full space of the root window
        self.pack()

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)
        file.add_command(label="Open", command=self.__openFile)
        file.add_command(label="New", command=self.__newFile)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Exit", command=self.client_exit)

        
        #added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # create the file object)
        edit = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        edit.add_command(label="Undo")

        #added "file" to our menu
        menu.add_cascade(label="Edit", menu=edit)

        about = Menu(menu)
        about.add_command(label="Application", command=self.__showAbout)
        menu.add_cascade(label="About", menu=about)

        widget1 = Entry(root, show="*", width=15).pack()
        counter=0
        self.widget2 = Text(root,height=1, width=8,name="widget2")
        self.widget2.pack()
        self.widget2.insert(1.0,str(counter))
                        
        increase = Button(root,text='Increase',command=self.__increase).pack()
        decrease = Button(root,text='Decrease',command=self.__decrease).pack() 

        #print(widget)

        drawing_area = Canvas(root,bg="white",width=360,height=360)
        drawing_area.pack()
        drawing_area.bind("<Motion>", self.motion)
        drawing_area.bind("<ButtonPress-1>", self.left_but_down)
        drawing_area.bind("<ButtonRelease-1>", self.left_but_up)


        for x in range(10,360,20):
            for y in range (10,360,20):
                drawing_area.create_rectangle(x-1, y-1, x + 1, y + 1,fill="midnight blue")
                self.x_points.append(x)
                self.y_points.append(y)
                #print("x = " + str(x) + " and y = " + str(y) + "  ", end=" ")

            #print("\n")    

        btn2 = Button(root,text='Run', command=self.run_grid).pack()   

    
        
    def __openFile(self):
        root=self.master
        T = Text(root, height=30, width=50)
        T.pack()
        filename = filedialog.askopenfilename()
        with open(filename, 'r') as f_gcode:
            for line in f_gcode:
                
                try:
                    str(line)
                
                    s=line.split(" ")
                    for item in range(len(s)):
                   
                        r_string_and_num_unsigned = re.compile("([a-zA-Z]+)([0.0-9.9]+)").match(s[item])
                        r_string_and_num_signed = re.compile("([a-zA-Z]+)([-+]+)([0.0-9.9]+)").match(s[item])
                        if r_string_and_num_unsigned:
                            print(r_string_and_num_unsigned.groups())
                            T.insert(1.0,r_string_and_num_unsigned.groups())
                            T.insert(1.0,"\n ")
                        elif r_string_and_num_signed:
                            print(r_string_and_num_signed.groups())
                            T.configure(text=r_string_and_num_signed.groups())
                            T.insert(1.0,r_string_and_num_signed.groups())
                            T.insert(1.0," \n")
                        
                except:
                    pass



        btn1 = Button(root,text='Run', command=self.__run_gcode).pack()       
                
                
    def __newFile(self): 
        self.master.title("Untitled - Tarun2.0")
        self.__file = None
    def __increase(self):
        counter=int(self.widget2.get(1.0,END))
        counter=counter+1
        self.widget2.delete(1.0)
        self.widget2.insert(1.0,str(counter))
        arduino.write("u".encode())
        
        '''if counter == 1: 
            time.sleep(1) 
            arduino.write('A'.encode()) 
            
        elif counter == 2:
            time.sleep(1) 
            arduino.write('B'.encode())
        elif counter == 3:
            time.sleep(1) 
            arduino.write('C'.encode())
        elif counter == 4:
            time.sleep(1) 
            arduino.write('D'.encode())
        elif counter == 5:
            time.sleep(1) 
            arduino.write('E'.encode())
        elif counter == 6 or counter == 0:
            time.sleep(1) 
            arduino.write("A10".encode())          
            
        else:
            print ("Sorry..type another thing..!")'''

    def __decrease(self):
        counter=int(self.widget2.get(1.0,END))
        counter=counter-1
        self.widget2.delete(1.0)
        self.widget2.insert(1.0,str(counter))
        arduino.write("d".encode()) 
        print("the elements of the coordinates list are")
        for k in range(self.i):
            for l in range(4):
                print(str(self.coordinates[k][l]) + " ",end="")

            print("\n")       
                
                
        '''
        if counter == 1: 
            time.sleep(1) 
            arduino.write("u".encode()) 
            
        elif counter == 2:
            time.sleep(1) 
            arduino.write("B".encode())
        elif counter == 3:
            time.sleep(1) 
            arduino.write("C".encode())
        elif counter == 4:
            time.sleep(1) 
            arduino.write("D".encode())
        elif counter == 5 or counter == 0:
            time.sleep(1) 
            arduino.write("E".encode())
        elif counter == 6 or counter == 0:
            time.sleep(1) 
            arduino.write("A10".encode())          
            
        else:
            print ("Sorry..type another thing..!")        
        '''

    def __showAbout(self): 
        messagebox.showinfo("Tarun2.0","Tarun Thakur")

    # ---------- CATCH MOUSE UP ----------
    def left_but_down(self, event=None):
        self.left_but = "down"
 
        # Set x & y when mouse is clicked
        self.x1_line_pt = event.x
        self.y1_line_pt = event.y

        self.x1_line_pt =fixRes(self.x1_line_pt,self.x_points)
        self.y1_line_pt =fixRes(self.y1_line_pt,self.y_points)
  
        self.coordinates[self.i][0]= self.x1_line_pt
        self.coordinates[self.i][1]= self.y1_line_pt
        #event.widget.create_rectangle(self.x1_line_pt, self.y1_line_pt, self.x1_line_pt + 5, self.y1_line_pt + 5,fill="midnight blue")   
        print("x1 = " + str(self.x1_line_pt)+"\n y1 = "+str(self.y1_line_pt))

    # ---------- CATCH MOUSE UP ----------
 
    def left_but_up(self, event=None):
        self.left_but = "up"
 
        # Reset the line
        self.x_pos = None
        self.y_pos = None
 
        # Set x & y when mouse is released
        self.x2_line_pt = event.x
        self.y2_line_pt = event.y
        
        self.x2_line_pt =fixRes(self.x2_line_pt,self.x_points)
        self.y2_line_pt =fixRes(self.y2_line_pt,self.y_points)
        self.disp_count= self.disp_count +1
        
        self.coordinates[self.i][2]= self.x2_line_pt
        self.coordinates[self.i][3]= self.y2_line_pt
        self.i = self.i + 1
        #event.widget.create_rectangle(self.x2_line_pt, self.y2_line_pt, self.x2_line_pt + 5, self.y2_line_pt + 5,fill="midnight blue")
        print("x2 = " + str(self.x2_line_pt)+"\n y2 = "+str(self.y2_line_pt))
         
        # If mouse is released and line tool is selected
        # draw the line
        if self.drawing_tool == "line":
            self.line_draw(event)

 
    # ---------- CATCH MOUSE MOVEMENT ----------
 
    def motion(self, event=None):
 
        if self.drawing_tool == "pencil":
            self.pencil_draw(event)


  # ---------- DRAW LINE ----------
 
    def line_draw(self, event=None):
 
        # Shortcut way to check if none of these values contain None
        if None not in (self.x1_line_pt, self.y1_line_pt, self.x2_line_pt, self.y2_line_pt):
            event.widget.create_line(self.x1_line_pt, self.y1_line_pt, self.x2_line_pt, self.y2_line_pt, smooth=TRUE, fill="green")
 




    def run_grid(self):
        del self.coordinates[self.disp_count : ]
        print(str(len(self.coordinates)))
        for k in range(-1,len(self.coordinates)):
            print(str(k))

            
            if k == -1:
                print("")
            elif k == 0:
                print("moving")
                #if ( not isPendown(servo_position)):
                #pen_down()# under if
                movement(self.coordinates[k][0],self.coordinates[k][1],self.coordinates[k][2],self.coordinates[k][3])
                print("X1 = " + str(self.coordinates[k][0])+"Y1 = " + str(self.coordinates[k][1]) + "X2 = " + str(self.coordinates[k][2]) + "Y2 = " + str(self.coordinates[k][3]))
                    
            else:
                if self.coordinates[k][0] == self.coordinates[k-1][2] and self.coordinates[k][1] == self.coordinates[k-1][3] :
                    print("moving")
                  #  if ( not isPendown(servo_position)):
                  #  pen_down()# under if
                    print("servo position" + str(servo_position))

                    movement(self.coordinates[k][0],self.coordinates[k][1],self.coordinates[k][2],self.coordinates[k][3])
                   
                    print("X1 = " + str(self.coordinates[k][0])+"Y1 = " + str(self.coordinates[k][1]) + "X2 = " + str(self.coordinates[k][2]) + "Y2 = " + str(self.coordinates[k][3]))
 
                else:
                    # if ( not isPenup(servo_position)):
                    pen_up()#under if
                    #print("servo position" + str(servo_position))
                    print("problem is here \n")
                    movement(self.coordinates[k-1][2],self.coordinates[k-1][3],self.coordinates[k][0],self.coordinates[k][1])
                    print("k-1 = " +str(k-1)+"k"+str(k))
                    print("X1 = " + str(self.coordinates[k-1][2])+"Y1 = " + str(self.coordinates[k-1][3]) + "X2 = " + str(self.coordinates[k][0]) + "Y2 = " + str(self.coordinates[k][1]))
                    pen_down()
                    print("servo position" + str(servo_position))
                    movement(self.coordinates[k][0],self.coordinates[k][1],self.coordinates[k][2],self.coordinates[k][3])
                    print("X1 = " + str(self.coordinates[k][0])+"Y1 = " + str(self.coordinates[k][1]) + "X2 = " + str(self.coordinates[k][2]) + "Y2 = " + str(self.coordinates[k][3]))
                    print("k= "+str(k))


    
       
   
    def client_exit(self):
        exit()



        

        
# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

root.geometry("1200x700")

#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()  







