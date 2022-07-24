"""
Author: Rahil Amit Shah
Aim: To create a billing system using python
Libraries used for GUI: tkinter
"""

# importing some required libraries
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmsg
import os
import time

#===================Python Variables=======================
menu_category = ["Pens","Pencils","Print","Paper","Other","Seasonal"]  # These are the menu categories

menu_category_dict = {"Pens":"pens.txt","Pencils":"pencils.txt",
                "Print":"print.txt","Paper":"paper.txt",
                "Other":"other.txt","Seasonal":"seasonal.txt"}
# Menu category dictionary, gives the value of a particular key when pressed on the GUI


order_dict = {}
for i in menu_category:
    order_dict[i] = {}

# defines the releative path of the file where these text files of the menu are stored.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
#====================Backend Functions===========================

# loads menu from the text files stored above
def load_menu():
    menuCategory.set("")
    menu_tabel.delete(*menu_tabel.get_children())
    menu_file_list = os.listdir("Menu")
    # The below for loop reads every text file and stores it as python variables for use 
    for file in menu_file_list:
        # opens a particular file when a menu is selected on the GUI
        f = open("Menu\\" + file , "r")
        category=""
        while True:
            line = f.readline()
            if(line==""):
                # Thsi indicates that the file is now finished and one should move ahead
                menu_tabel.insert('',END,values=["","",""])
                break
            elif (line=="\n"):
                # This means that the line has finished and now we need to move to the next line to read data
                continue
            elif(line[0]=='#'):
                # This indicates the category in which the menu needs to be stored
                category = line[1:-1]
                name = "\t\t"+line[:-1]
                price = ""
            elif(line[0]=='*'):
                # This indicates the material that is not available currently.
                name = line[:-1]
                price = ""
            else:
                # This reads the name of the item in the menu and it's price.
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ")+1:-3]
            
            # Inserts the name, price and category into the menu table.
            menu_tabel.insert('',END,values=[name,price,category])
        

# loads the order into the python and stores it as variables and writes it onto the bill
# it loads the values selected by the customer and stores and writes it into the bill (order_table)
### Please check once



def load_order():
    # takes the already stored values of the order from dictionary (order_dict) to the tabel
    order_tabel.delete(*order_tabel.get_children())
    for category in order_dict.keys():
        if order_dict[category]:
            for lis in order_dict[category].values():
                order_tabel.insert('',END,values=lis)
    update_total_price()


# This function adds the item that is required when a button is pressed
def add_button_operation():

    name = itemName.get()   # name of the item
    rate = itemRate.get()   # rate to show on window
    category = itemCategory.get()   # category of the item
    quantity = itemQuantity.get()   # quantity of the item

    # If an item is taken 2 times it shows an error 
    # To overcome here and reduce redundancy this was provided
    # One needs to increase the quantity of the item rather than adding it again
    if name in order_dict[category].keys():
        tmsg.showinfo("Error", "Item already exist in your order")
        return
    if not quantity.isdigit():
        # if the quantity entered is not a whole number than this shows an error
        tmsg.showinfo("Error", "Please Enter Valid Quantity")
        return
    lis = [name,rate,quantity,str(int(rate)*int(quantity)),category]
    # stores all the collected data of the order and it's price in order_dict dictionary
    order_dict[category][name] = lis
    # calling the function to load the order
    load_order()
    
# loads item form the menu    
def load_item_from_menu(event):
    # gives the focus to menu_table widget
    cursor_row = menu_tabel.focus()
    # adds item to the menu_table to the contents
    contents = menu_tabel.item(cursor_row)
    row = contents["values"]
    itemName.set(row[0])
    itemRate.set(row[1])
    itemCategory.set(row[2]) 
    itemQuantity.set("1")

def load_item_from_order(event):
    cursor_row = order_tabel.focus()        # focuses on order_tabel
    contents = order_tabel.item(cursor_row) # adds to order_table
    row = contents["values"]    

    # puts the description of the item in order_tabel
    itemName.set(row[0])
    itemRate.set(row[1])
    itemQuantity.set(row[2])
    itemCategory.set(row[4])

# adds the button to menu 
def show_button_operation():
    category = menuCategory.get()       # returns entry as string

    # if category is not in menu then we need to show an error
    if category not in menu_category:
        tmsg.showinfo("Error", "Please select valid Choice")
    else:
        # this function reads the text files and adds button to the menu
        menu_tabel.delete(*menu_tabel.get_children())
        f = open("Menu\\" + menu_category_dict[category] , "r")
        while True:
            line = f.readline()
            if(line==""):
                # end of the file
                break
            if (line[0]=='#' or line=="\n"):
                # start or end of the line hence, need to be skipped
                continue
            if(line[0]=='*'):
                # reads the line and makes it's button
                name = "\t"+line[:-1]
                menu_tabel.insert('',END,values=[name,"",""])
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ")+1:-3]
                menu_tabel.insert('',END,values=[name,price,category])
# removes the button from the order tabel
def clear_button_operation():
    # makes all the buttons in the order tabel blank
    itemName.set("")
    itemRate.set("")
    itemQuantity.set("")
    itemCategory.set("")

# cancel operation during billing or before billing
def cancel_button_operation():
    names = []
    for i in menu_category:
        names.extend(list(order_dict[i].keys()))
    if len(names)==0:
        # the order was already empty
        tmsg.showinfo("Error", "Your order list is Empty")
        return
    # asking to confirm if the customer wants to cancel the order
    ans = tmsg.askquestion("Cancel Order", "Are You Sure to Cancel Order?")
    if ans=="no":
        return
    order_tabel.delete(*order_tabel.get_children())     # removes the whole order
    
    # again inititates the order
    for i in menu_category:
        order_dict[i] = {}
    clear_button_operation()        # clears the widget showing the bills
    update_total_price()            # updates the total price 

# updates button when there is a change in quantity of the item
def update_button_operation():
    name = itemName.get()
    rate = itemRate.get()
    category = itemCategory.get()
    quantity = itemQuantity.get()

    if category=="":
        return
    # name is not there in the order dictionary hence need to show an error
    if name not in order_dict[category].keys():
        tmsg.showinfo("Error", "Item is not in your order list")
        return
    # if there is no change in the quantity then we need to show an error
    # as a change in quantity was bound to happen here
    if order_dict[category][name][2]==quantity:
        tmsg.showinfo("Error", "No changes in Quantity")
        return
    # updating the quantity
    order_dict[category][name][2] = quantity
    order_dict[category][name][3] = str(int(rate)*int(quantity))
    # loading the order
    load_order()

def remove_button_operation():
    # removing an item displayed on the order widget
    name = itemName.get()
    category = itemCategory.get()

    
    if category=="":
        return
    # if name is not in order then we need to show an error
    if name not in order_dict[category].keys():
        tmsg.showinfo("Error", "Item is not in your order list")
        return
    # deletes the item corresponding to the one that needs to be deleted
    del order_dict[category][name]
    # load the rest of the order
    load_order()

def update_total_price():
    # up=dates the price everytime
    price = 0
    # the below loop calculates the total price
    for i in menu_category:
        for j in order_dict[i].keys():
            price += int(order_dict[i][j][3])
    # displays the price on the widget
    if price == 0:
        totalPrice.set("")
    else:
        totalPrice.set("Rs. "+str(price)+"  /-")

# bills the order:- generates, saves and prints the bill
def bill_button_operation():
    # takes all the required data from the dictionary and displays it in bill
    customer_name = customerName.get()
    customer_contact = customerContact.get()
    names = []
    for i in menu_category:
        names.extend(list(order_dict[i].keys()))
    if len(names)==0:
        tmsg.showinfo("Error", "Your order list is Empty")
        return
    if customer_name=="" or customer_contact=="":
        tmsg.showinfo("Error", "Customer Details Required")
        return
    if not customerContact.get().isdigit():
        tmsg.showinfo("Error", "Invalid Customer Contact")
        return   
    ans = tmsg.askquestion("Generate Bill", "Are You Sure to Generate Bill?")
    ans = "yes"
    # The below generates the bill
    if ans=="yes":
        bill = Toplevel()
        bill.title("Bill")
        bill.geometry("670x500+300+100")
        bill.wm_iconbitmap("pen.ico")
        bill_text_area = Text(bill, font=("arial", 12))
        st = "\t\t\t\tStationary\n\t\t\Prahladnagar, 380015\n"
        st += "\t\t\tGST.NO:- 27AHXPP3379HIZH\n"
        st += "-"*61 + "BILL" + "-"*61 + "\nDate:- "

        #Date and time
        # uses date time library to show the time output
        t = time.localtime(time.time())
        week_day_dict = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",
                            6:"Sunday"}
        st += f"{t.tm_mday} / {t.tm_mon} / {t.tm_year} ({week_day_dict[t.tm_wday]})"
        st += " "*10 + f"\t\t\t\t\t\tTime:- {t.tm_hour} : {t.tm_min} : {t.tm_sec}"

        #Customer Name & Contact
        st += f"\nCustomer Name:- {customer_name}\nCustomer Contact:- {customer_contact}\n"
        st += "-"*130 + "\n" + " "*4 + "DESCRIPTION\t\t\t\t\tRATE\tQUANTITY\t\tAMOUNT\n"
        st += "-"*130 + "\n"

        #List of Items
        # shows the list of items present in the order
        for i in menu_category:
            for j in order_dict[i].keys():
                lis = order_dict[i][j]
                name = lis[0]
                rate = lis[1]
                quantity = lis[2]
                price = lis[3]
                st += name + "\t\t\t\t\t" + rate + "\t      " + quantity + "\t\t  " + price + "\n\n"
        st += "-"*130

        #Total Price
        st += f"\n\t\t\tTotal price : {totalPrice.get()}\n"
        st += "-"*130

        #display bill in new window
        bill_text_area.insert(1.0, st)

        #write into file
        # saves the file in the folder
        folder = f"{t.tm_mday},{t.tm_mon},{t.tm_year}"
        if not os.path.exists(f"Bill Records\\{folder}"):
            os.makedirs(f"Bill Records\\{folder}")
        file = open(f"Bill Records\\{folder}\\{customer_name+customer_contact}.txt", "w")
        file.write(st)
        file.close()
        


        # After billing and saving the data all the previous data needs to be deleted,
        # for the fresh entries
        #Clear operaitons
        order_tabel.delete(*order_tabel.get_children())
        for i in menu_category:
            order_dict[i] = {}
        clear_button_operation()
        update_total_price()
        customerName.set("")
        customerContact.set("")

        bill_text_area.pack(expand=True, fill=BOTH)
        bill.focus_set()
        
        
        #========Storing data in csv format===============
        import csv
        data = open('data_f1.csv', 'w')
        writer = csv.DictWriter(data, fieldnames=['name', 'phone', 'product','quantity','day','month','year','time','rate'])
        writer.writeheader()
        for i in menu_category:
            for j in order_dict[i].keys():
                lis = order_dict[i][j]
                name = lis[0]
                rate = lis[1]
                quantity = lis[2]
                price = lis[3] 
                writer.writerow([customer_name,totalPrice.get(),name ,quantity,t.tm_mday,t.tm_mon,t.tm_year,t.tm_hour,rate])
        data.close()
        
        
        #data_2 = open('data_test.csv', 'w')
        #write = csv.Dictwritwer(data_2, fieldnames=['name'])
        #write.writeheader()
        #write.writerow({'name': 'rahil'})
        #data_2.close()



#==================Backend Code Ends===============

#================Frontend Code Start==============
# using tkinter
root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight() # setting width and height of tkinter window

# setting the geometry of tkinter window
root.geometry("%dx%d+0+0" % (w, h))
# shows the title of the tkinter window
root.title("AIRAS")
# sets the icon for tkinter window
# the pencil icon looks good as a tkinter symbol
root.wm_iconbitmap("pencil.ico")
#root.attributes('-fullscreen', True)
#root.resizable(0, 0)

#================Title==============
# making the title of the tkinter window
style_button = ttk.Style()
style_button.configure("TButton",font = ("arial",10,"bold"),
   background="lightgreen")

# setting the geometry and shape of the title
title_frame = Frame(root, bd=8, bg="yellow", relief=GROOVE)
title_frame.pack(side=TOP, fill="x")

# putting the text in the title label
title_label = Label(title_frame, text="Stationary", 
                    font=("times new roman", 20, "bold"),bg = "yellow", fg="red", pady=5)

title_label.pack()

#==============Customer=============
# making the customer frame to store his/her details
customer_frame = LabelFrame(root,text="Customer Details",font=("times new roman", 15, "bold"),
                            bd=8, bg="lightblue", relief=GROOVE)
customer_frame.pack(side=TOP, fill="x")

# name is displayed in the widget
customer_name_label = Label(customer_frame, text="Name", 
                    font=("arial", 15, "bold"),bg = "lightblue", fg="blue")
customer_name_label.grid(row = 0, column = 0)

# takes input the name of the customer as a string
customerName = StringVar()
customerName.set("")
customer_name_entry = Entry(customer_frame,width=20,font="arial 15",bd=5,
                                textvariable=customerName)
customer_name_entry.grid(row = 0, column=1,padx=50)

# sets up the customer contact label
customer_contact_label = Label(customer_frame, text="Contact", 
                    font=("arial", 15, "bold"),bg = "lightblue", fg="blue")
customer_contact_label.grid(row = 0, column = 2)

# takes the customer contact number as a string
customerContact = StringVar()
customerContact.set("")
customer_contact_entry = Entry(customer_frame,width=20,font="arial 15",bd=5,
                                textvariable=customerContact)
customer_contact_entry.grid(row = 0, column=3,padx=50)

#===============Menu===============
# Setting up the menu in the tkinter window

# sets up the geometry of the menu frame
menu_frame = Frame(root,bd=8, bg="lightgreen", relief=GROOVE)
menu_frame.place(x=0,y=125,height=585,width=680)

# label of the menu
menu_label = Label(menu_frame, text="Menu", 
                    font=("times new roman", 20, "bold"),bg = "lightgreen", fg="red", pady=0)
menu_label.pack(side=TOP,fill="x")

# forms the menu category frame
menu_category_frame = Frame(menu_frame,bg="lightgreen",pady=10)
menu_category_frame.pack(fill="x")

# sets up combolababel for the label
# this is in the menu frame and sets up the type of the item
combo_lable = Label(menu_category_frame,text="Select Type", 
                    font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
combo_lable.grid(row=0,column=0,padx=10)

# sets up menu category
menuCategory = StringVar()
combo_menu = ttk.Combobox(menu_category_frame,values=menu_category,
                            textvariable=menuCategory)
combo_menu.grid(row=0,column=1,padx=30)

# shows the button of for category grame
show_button = ttk.Button(menu_category_frame, text="Show",width=10,
                        command=show_button_operation)
show_button.grid(row=0,column=2,padx=60)

# this shows all the items availabel in the menu when clicked over it
show_all_button = ttk.Button(menu_category_frame, text="Show All",
                        width=10,command=load_menu)
show_all_button.grid(row=0,column=3)

############################# Menu Tabel ##########################################
# Moving on to menu 

# setting up the menu frame
menu_tabel_frame = Frame(menu_frame)
menu_tabel_frame.pack(fill=BOTH,expand=1)

# setting the scrollbar for x and y axis
scrollbar_menu_x = Scrollbar(menu_tabel_frame,orient=HORIZONTAL)
scrollbar_menu_y = Scrollbar(menu_tabel_frame,orient=VERTICAL)

# displays the items as an ordered tabel and setting up the font for it
style = ttk.Style()
style.configure("Treeview.Heading",font=("arial",13, "bold"))
style.configure("Treeview",font=("arial",12),rowheight=25)

# this sets up the all the items in the menu tabel
menu_tabel = ttk.Treeview(menu_tabel_frame,style = "Treeview",
            columns =("name","price","category"),xscrollcommand=scrollbar_menu_x.set,
            yscrollcommand=scrollbar_menu_y.set)

# displaying the name, price of the items
menu_tabel.heading("name",text="Name")
menu_tabel.heading("price",text="Price")
menu_tabel["displaycolumns"]=("name", "price")
menu_tabel["show"] = "headings"
menu_tabel.column("price",width=50,anchor='center')

# sets up scrollbar in x and y axis
scrollbar_menu_x.pack(side=BOTTOM,fill=X)
scrollbar_menu_y.pack(side=RIGHT,fill=Y)

scrollbar_menu_x.configure(command=menu_tabel.xview)
scrollbar_menu_y.configure(command=menu_tabel.yview)

menu_tabel.pack(fill=BOTH,expand=1)

# loads up the menu
load_menu()
menu_tabel.bind("<ButtonRelease-1>",load_item_from_menu)

###########################################################################################

#===============Item Frame=============
# setting up the item frame
# setting the geometry of the item frame
item_frame = Frame(root,bd=8, bg="lightgreen", relief=GROOVE)
item_frame.place(x=680,y=125,height=230,width=680)

# label of title and it's font style
item_title_label = Label(item_frame, text="Item", 
                    font=("times new roman", 20, "bold"),bg = "lightgreen", fg="red")
item_title_label.pack(side=TOP,fill="x")

# item frame 2 for putting up the items in it
item_frame2 = Frame(item_frame, bg="lightgreen")
item_frame2.pack(fill=X)

# labels the item name
item_name_label = Label(item_frame2, text="Name", 
                    font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
item_name_label.grid(row=0,column=0)

# stores the item category
itemCategory = StringVar()
itemCategory.set("")

# stores the item name
# later this varibale is filled by names of different items
itemName = StringVar()
itemName.set("")
item_name = Entry(item_frame2, font="arial 12",textvariable=itemName,state=DISABLED, width=25)
item_name.grid(row=0,column=1,padx=10)

# labels the rate of the item 
item_rate_label = Label(item_frame2, text="Rate", 
                    font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
item_rate_label.grid(row=0,column=2,padx=40)

# stores the item rate as a string value
itemRate = StringVar()
itemRate.set("")
item_rate = Entry(item_frame2, font="arial 12",textvariable=itemRate,state=DISABLED, width=10)
item_rate.grid(row=0,column=3,padx=10)

# sets up the quantity of the label
item_quantity_label = Label(item_frame2, text="Quantity", 
                    font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
item_quantity_label.grid(row=1,column=0,padx=30,pady=15)

# item quantity of the label
itemQuantity = StringVar()
itemQuantity.set("")
item_quantity = Entry(item_frame2, font="arial 12",textvariable=itemQuantity, width=10)
item_quantity.grid(row=1,column=1)

# item frame for add item in the bill
item_frame3 = Frame(item_frame, bg="lightgreen")
item_frame3.pack(fill=X)

# adds the button to the menu
add_button = ttk.Button(item_frame3, text="Add Item"
                        ,command=add_button_operation)
add_button.grid(row=0,column=0,padx=40,pady=30)

# adds the remove button to remove the item 
# calls the remove_button_operation function to remove the item
remove_button = ttk.Button(item_frame3, text="Remove Item"
                        ,command=remove_button_operation)
remove_button.grid(row=0,column=1,padx=40,pady=30)

# adds the update button
update_button = ttk.Button(item_frame3, text="Update Quantity"
                        ,command=update_button_operation)
update_button.grid(row=0,column=2,padx=40,pady=30)

# clears the menu
clear_button = ttk.Button(item_frame3, text="Clear",
                        width=8,command=clear_button_operation)
clear_button.grid(row=0,column=3,padx=40,pady=30)

#==============Order Frame=====================
# setting up the order frame

# geometry
order_frame = Frame(root,bd=8, bg="lightgreen", relief=GROOVE)
order_frame.place(x=680,y=335,height=370,width=680)

# sets up the title of the label
order_title_label = Label(order_frame, text="Your Order", 
                    font=("times new roman", 20, "bold"),bg = "lightgreen", fg="red")
order_title_label.pack(side=TOP,fill="x")

############################## Order Tabel ###################################
# order tabel 

# sets up the order table frame
order_tabel_frame = Frame(order_frame)
order_tabel_frame.place(x=0,y=40,height=260,width=680)

# adding scrollbar on x and y axis
scrollbar_order_x = Scrollbar(order_tabel_frame,orient=HORIZONTAL)
scrollbar_order_y = Scrollbar(order_tabel_frame,orient=VERTICAL)

# A treeview wiidget allows to store the data in tabular form  
order_tabel = ttk.Treeview(order_tabel_frame,
            columns =("name","rate","quantity","price","category"),xscrollcommand=scrollbar_order_x.set,
            yscrollcommand=scrollbar_order_y.set)

# adding the variables name, rate, quantity, price to be displayed on the order tabel
order_tabel.heading("name",text="Name")                     # creating the heading of the order_table
order_tabel.heading("rate",text="Rate")
order_tabel.heading("quantity",text="Quantity")
order_tabel.heading("price",text="Price")


order_tabel["displaycolumns"]=("name", "rate","quantity","price")         # defining columns
order_tabel["show"] = "headings"                                        # defining headings

# setting the geopmetry of different columns in columns
order_tabel.column("rate",width=100,anchor='center', stretch=NO)        
order_tabel.column("quantity",width=100,anchor='center', stretch=NO)
order_tabel.column("price",width=100,anchor='center', stretch=NO)

# sets up button to load the order
order_tabel.bind("<ButtonRelease-1>",load_item_from_order)

# setting the scrollbar on the right and the bottom side
scrollbar_order_x.pack(side=BOTTOM,fill=X)
scrollbar_order_y.pack(side=RIGHT,fill=Y)

scrollbar_order_x.configure(command=order_tabel.xview)
scrollbar_order_y.configure(command=order_tabel.yview)

# frame fills the space fully
order_tabel.pack(fill=BOTH,expand=1)


###########################################################################################

# finds the total price and it's geometry
total_price_label = Label(order_frame, text="Total Price", 
                    font=("arial", 12, "bold"),bg = "lightgreen", fg="blue")
total_price_label.pack(side=LEFT,anchor=SW,padx=20,pady=10)

# sets up the total price as a string variable and updates the price 
# as and when the items are added in the order tabel
totalPrice = StringVar()
totalPrice.set("")
total_price_entry = Entry(order_frame, font="arial 12",textvariable=totalPrice,state=DISABLED, 
                            width=10)
total_price_entry.pack(side=LEFT,anchor=SW,padx=0,pady=10)

# making a bill button to bill the order by a customer
bill_button = ttk.Button(order_frame, text="Bill",width=8,
                        command=bill_button_operation)
bill_button.pack(side=LEFT,anchor=SW,padx=80,pady=10)

# setting up a cancel button to cancel the order
cancel_button = ttk.Button(order_frame, text="Cancel Order",command=cancel_button_operation)
cancel_button.pack(side=LEFT,anchor=SW,padx=20,pady=10)

# It will loop forever until the user exits the window
root.mainloop()
#====================Frontend code ends=====================

# Thanks for reading till the end, I hope that you have understood this code fully
#====================Thank     You=====================
