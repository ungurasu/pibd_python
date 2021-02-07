import mysql.connector
import tkinter as tk
from tkscrolledframe import ScrolledFrame


class DatabaseHandler:
    def fail_window(self, text):
        print(text)
        failwindow = tk.Tk()
        failwindow.resizable(False, False)
        failwindow.title("Error")
        faillabel = tk.Label(master=failwindow, text=text, fg="red")
        faillabel.grid(column=0, row=0, pady=5, padx=5)
        failbutton = tk.Button(master=failwindow, text="Okay :(", command=failwindow.destroy)
        failbutton.grid(column=0, row=1, pady=10, padx=5)

    def success_window(self, text):
        print(text)
        successwindow = tk.Tk()
        successwindow.resizable(False, False)
        successwindow.title("Success")
        successlabel = tk.Label(master=successwindow, text=text, fg="green")
        successlabel.grid(column=0, row=0, pady=5, padx=5)
        successbutton = tk.Button(master=successwindow, text="Okay", command=successwindow.destroy)
        successbutton.grid(column=0, row=1, pady=10, padx=5)

    def insert(self, table, columns, nullable, fields):
        if self.isConnected:
            self.repeat_login()
            index = 0
            insertable = True
            for x in fields:
                if not nullable[index] and not x.get():
                    insertable = False
            if insertable:
                values = list()
                strvalues = list()
                for x in fields:
                    values.append(x.get())
                    strvalues.append("%s")

                strcolumns = ", ".join(columns)
                strvalues = ", ".join(strvalues)
                sqlcommand = str(f"INSERT INTO {table} ({strcolumns}) VALUES ({strvalues});")

                print(strcolumns)
                print(strvalues)
                print(sqlcommand)
                try:
                    self.mycursor.execute(sqlcommand, values)
                except mysql.connector.Error as err:
                    self.fail_window(err)
                else:
                    try:
                        self.mydb.commit()
                    except:
                        self.fail_window("Failed to commit: credentials?")
                    else:
                        self.success_window(f"1 record inserted with ID: {self.mycursor.lastrowid}")
            else:
                self.fail_window("Nonnullable fields null!")
        else:
            self.fail_window("Can not operate without connection!")

    def insert_window(self, table):
        if self.isConnected:
            self.repeat_login()
            print(table)
            try:
                self.mycursor.execute(f"SHOW COLUMNS FROM {table};")
            except mysql.connector.Error as err:
                self.fail_window(err)
            else:
                columns = list()
                nullable = list()
                for x in self.mycursor:
                    if x[5] != "auto_increment":
                        columns.append(x[0])
                        if x[2] == 'YES':
                            nullable.append(True)
                        else:
                            nullable.append(False)

                insertwindow = tk.Tk()
                insertwindow.resizable(False, False)
                insertwindow.title("Insert row")
                myrow = 0

                entrycolumn = list()
                for x in columns:
                    try:
                        self.mycursor.execute(f"SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = 'madeByPython' AND TABLE_NAME = '{table}' AND COLUMN_NAME = '{x}';")
                    except mysql.connector.Error as err:
                        self.fail_window(err)
                    else:
                        myresult = self.mycursor.fetchall()
                        if not myresult:
                            labelcolumn = tk.Label(master=insertwindow, text=f"column: {x}", justify="left")
                        else:
                            labelcolumn = tk.Label(master=insertwindow, text=f"column: {x}\nconstrained to: {myresult[0][3]} -> {myresult[0][4]}", justify="left")
                        if nullable[myrow] == False:
                            labelcolumn["fg"] = "red"
                        entrycolumn.append(tk.Entry(master=insertwindow, width=20))
                        labelcolumn.grid(column=0, row=myrow, pady=5, padx=5, sticky="w")
                        entrycolumn[myrow].grid(column=1, row=myrow, pady=5, padx=5, sticky="w")
                        myrow += 1

                buttoninsert = tk.Button(master=insertwindow, text="Insert", command=lambda: [self.insert(table, columns, nullable, entrycolumn), insertwindow.destroy()])
                buttoninsert.grid(column=0, row=myrow, pady=5, padx=5)
        else:
            self.fail_window("Can not operate without connection!")

    def select_all(self, table, column, equals):
        if self.isConnected:
            self.repeat_login()
            try:
                self.mycursor.execute(f"SHOW COLUMNS FROM {table};")
            except mysql.connector.Error as err:
                self.fail_window(err)
            else:
                selectedwindow = tk.Tk()
                selectedwindow.title(table)

                scroll = ScrolledFrame(master=selectedwindow, width=720, height=720)
                scroll.pack()
                scrollframe = scroll.display_widget(tk.Frame)

                othercolumns = list()
                othertables = list()
                currentcolumns = list()
                restraints = list()
                constrained = False

                for x in self.mycursor:
                    currentcolumns.append(x[0])

                for x in currentcolumns:
                    self.mycursor.execute(f"SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = 'animalute' AND TABLE_NAME = '{table}' AND COLUMN_NAME = '{x}';")
                    myresult = self.mycursor.fetchall()
                    if myresult and othertables.count(myresult[0][3]) == 0:
                        self.mycursor.execute(f"SHOW COLUMNS FROM {myresult[0][3]}")
                        for y in self.mycursor:
                            othertables.append(myresult[0][3])
                            othercolumns.append(y[0])
                    if myresult:
                        restraints.append([table,x,myresult[0][3],myresult[0][4]])
                        constrained = True

                print(othertables)
                print(othercolumns)
                print(currentcolumns)
                print(restraints)

                sql = "SELECT "
                if constrained:
                    index = 0
                    for x in othertables:
                        sql += f"{x}.{othercolumns[index]}, "
                        index += 1
                for x in currentcolumns:
                    sql += f"{table}.{x}, "
                sql = sql[0:(len(sql)-2)]
                sql += f" FROM {table} "
                if constrained:
                    for x in restraints:
                        sql += f"INNER JOIN {x[2]} ON {x[0]}.{x[1]} = {x[2]}.{x[3]} "
                if column:
                    sql += f" WHERE {table}.{column} = '{equals.get()}'"
                    print(column)
                    print(equals.get())

                print(sql)
                mycolumn = 0
                for x in othercolumns:
                    frame = tk.Frame(master=scrollframe, relief="groove", borderwidth=1, bg="crimson")
                    label = tk.Label(master=frame, text=x, bg="crimson", fg="white")
                    frame.grid(column=mycolumn, row=0, sticky="ew")
                    label.pack()
                    mycolumn += 1
                for x in currentcolumns:
                    frame = tk.Frame(master=scrollframe, relief="groove", borderwidth=1, bg="crimson")
                    label = tk.Label(master=frame, text=x, bg="crimson", fg="white")
                    frame.grid(column=mycolumn, row=0, sticky="ew")
                    label.pack()
                    mycolumn += 1

                myrow = 1
                try:
                    self.mycursor.execute(sql)
                except mysql.connector.Error as err:
                    self.fail_window(err)
                else:
                    myresult = self.mycursor.fetchall()
                    for y in myresult:
                        mycolumn = 0
                        for x in y:
                            frame = tk.Frame(master=scrollframe, relief="groove", borderwidth=1)
                            label = tk.Label(master=frame, text=x)
                            if myrow % 2:
                                frame["bg"] = "aliceblue"
                                label["bg"] = "aliceblue"
                            else:
                                frame["bg"] = "white"
                                label["bg"] = "white"
                            frame.grid(column=mycolumn, row=myrow, sticky="ew")
                            label.pack()
                            mycolumn += 1
                        myrow += 1
        else:
            self.fail_window("Can not operate without connection!")

    def filter_window(self, table):
        if self.isConnected:
            self.repeat_login()
            try:
                self.mycursor.execute(f"SHOW COLUMNS FROM {table};")
            except mysql.connector.Error as err:
                self.fail_window(err)
            else:
                filterwindow = tk.Tk()
                filterwindow.title("Filtering")
                filterwindow.resizable(False, False)

                frameup = tk.Frame(master=filterwindow)
                framedown = tk.Frame(master=filterwindow)
                frameup.pack()
                framedown.pack()
                instructions = tk.Label(master=frameup, text=f"Search in {table} where column equals:")
                instructions.pack()

                myrow = 0
                for x in self.mycursor:
                    columnlabel = tk.Label(master=framedown, text=x[0])
                    columnentry = tk.Entry(master=framedown, width=50)
                    columnbutton = tk.Button(master=framedown, text="EQUALS", command=lambda entry=columnentry, column=x[0]: [self.select_all(table, column, entry), filterwindow.destroy()])
                    columnlabel.grid(column=0, row=myrow, pady=5, padx=5, sticky="w")
                    columnentry.grid(column=2, row=myrow, pady=5, padx=5)
                    columnbutton.grid(column=1, row=myrow, pady=5, padx=5)
                    myrow += 1
        else:
            self.fail_window("Can not operate without connection!")

    def select_window(self, table):
        if self.isConnected:
            self.repeat_login()
            selectwindow = tk.Tk()
            selectwindow.title("Selecting")
            selectwindow.resizable(False, False)

            instructions = tk.Label(master=selectwindow, text=f"From {table} would you like to select:")
            buttonall = tk.Button(master=selectwindow, text="ALL", command=lambda: [self.select_all(table, 0, 0), selectwindow.destroy()], width=15)
            buttonfilter = tk.Button(master=selectwindow, text="FILTER", command=lambda: [self.filter_window(table), selectwindow.destroy()], width=15)

            instructions.grid(column=0, row=0, pady=5, padx=5)
            buttonall.grid(column=0, row=1, pady=5, padx=5)
            buttonfilter.grid(column=0, row=2, pady=5, padx=5)
        else:
            self.fail_window("Can not operate without connection!")

    def update(self, table, primary, primaryvalue, columns, columnentries):
        if self.isConnected:
            self.repeat_login()
            sql = f"UPDATE {table} SET "
            for x in range(len(columns)):
                sql += f"{columns[x]} = '{columnentries[x].get()}', "
            sql = sql[0:(len(sql)-2)]
            sql += f" WHERE {primary} = '{primaryvalue}'"
            print(sql)
            try:
                self.mycursor.execute(sql)
            except mysql.connector.Error as err:
                self.fail_window(err)
            else:
                try:
                    self.mydb.commit()
                except mysql.connector.Error as err:
                    self.fail_window(err)
                else:
                    self.success_window(f"Updated in {table} row with {primary} = {primaryvalue}.")
        else:
            self.fail_window("Can not operate without connection!")

    def update_window(self, table, primary, primaryentry):
        if self.isConnected:
            self.repeat_login()
            try:
                self.mycursor.execute(f"SHOW COLUMNS FROM {table};")
            except mysql.connector.Error as err:
                self.fail_window(err)
            else:
                primaryvalue = primaryentry.get()

                updatewindow = tk.Tk()
                updatewindow.title(f"Update in {table}")
                updatewindow.resizable(False, False)

                frameup = tk.Frame(master=updatewindow, pady=5, padx=5)
                framedown = tk.Frame(master=updatewindow, pady=5, padx=5)
                frameup.pack()
                framedown.pack()

                entries = list()
                columns = list()
                for x in self.mycursor:
                    if x[3] != "PRI":
                        columns.append(x[0])
                allcolumns = ", ".join(columns)
                try:
                    self.mycursor.execute(f"SELECT {allcolumns} FROM {table} WHERE {primary} = '{primaryentry.get()}';")
                except mysql.connector.Error as err:
                    self.fail_window(err)
                    updatewindow.destroy()
                else:
                    myresult = self.mycursor.fetchall()
                    if myresult:
                        myrow = 0
                        for x in myresult[0]:
                            labelcolumn = tk.Label(master=frameup, text=columns[myrow])
                            entrycolumn = tk.Entry(master=frameup, width=30)
                            entrycolumn.insert(0, x)

                            labelcolumn.grid(column=0, row=myrow)
                            entrycolumn.grid(column=1, row=myrow)
                            entries.append(entrycolumn)
                            myrow += 1
                        buttonupdate = tk.Button(master=framedown, text="UPDATE", command=lambda: [self.update(table, primary, primaryvalue, columns, entries), updatewindow.destroy()])
                        buttonupdate.pack()
                    else:
                        self.fail_window("Tried to update non-existing row!")
                        updatewindow.destroy()
        else:
            self.fail_window("Can not operate without connection!")

    def delete(self, table, primary, primaryentry):
        if self.isConnected:
            self.repeat_login()
            try:
                self.mycursor.execute(f"DELETE FROM {table} WHERE {primary} = '{primaryentry.get()}'")
            except mysql.connector.Error as err:
                self.fail_window(err)
            else:
                try:
                    self.mydb.commit()
                except mysql.connector.Error as err:
                    self.fail_window(err)
                else:
                    self.success_window(f"Deleted in {table} row with {primary} = {primaryentry.get()}.")
        else:
            self.fail_window("Can not operate without connection!")

    def findbypk_window(self, table, task):
        if self.isConnected:
            self.repeat_login()
            try:
                self.mycursor.execute(f"SHOW COLUMNS from {table};")
            except mysql.connector.Error as err:
                self.fail_window(err)
            else:
                findbypkwindow = tk.Tk()
                findbypkwindow.title(f"{task} in {table}")
                findbypkwindow.resizable(False, False)

                frameup = tk.Frame(master=findbypkwindow)
                framemiddle = tk.Frame(master=findbypkwindow)
                framedown = tk.Frame(master=findbypkwindow, pady=5, padx=5)

                frameup.pack()
                framemiddle.pack()
                framedown.pack()
                instructions = tk.Label(master=frameup, text=f"Find by PK value to perform {task} in {table}", pady=5, padx=5)
                instructions.pack()

                for x in self.mycursor:
                    if x[3] == "PRI":
                        print(x[0])
                        primary = x[0]

                labelprimary = tk.Label(master=framemiddle, text=primary)
                entryprimary = tk.Entry(master=framemiddle)
                labelprimary.grid(column=0, row=0, pady=5, padx=5)
                entryprimary.grid(column=1, row=0, pady=5, padx=5)

                if task == "update":
                    buttontask = tk.Button(master=framedown, text="FIND", command=lambda: [self.update_window(table, primary, entryprimary), findbypkwindow.destroy()])
                elif task == "delete":
                    buttontask = tk.Button(master=framedown, text="FIND", command=lambda: [self.delete(table, primary, entryprimary), findbypkwindow.destroy()])
                buttontask.pack()
        else:
            self.fail_window("Can not operate without connection!")

    def get_tables(self, task):
        if self.isConnected:
            self.repeat_login()
            print("All is good")
            tables = list()
            try:
                self.mycursor.execute("SHOW TABLES;")
            except mysql.connector.Error as err:
                self.fail_window(err)
            else:
                for x in self.mycursor:
                    x = str(x)
                    tables.append(x[2:(len(x)-3)])
                for x in tables:
                    print(x)

                tableselector = tk.Tk()
                tableselector.title("Available tables")
                tableselector.resizable(False, False)
                frameup = tk.Frame(master=tableselector)
                framedown = tk.Frame(master=tableselector)
                frameup.grid(column=0, row=0, pady=5, padx=5)
                framedown.grid(column=0, row=1, pady=5, padx=5)
                labelmessage = tk.Label(master=frameup, text="Found the following tables in the given database:")
                labelmessage.pack()

                myrow = 0
                for x in tables:
                    labeltable = tk.Label(master=framedown, text=x)
                    if task == "insert":
                        buttontable = tk.Button(master=framedown, text=f"{task} here", command=lambda current=x: [self.insert_window(current), tableselector.destroy()])
                    elif task == "select":
                        buttontable = tk.Button(master=framedown, text=f"{task} here", command=lambda current=x: [self.select_window(current), tableselector.destroy()])
                    elif task == "update":
                        buttontable = tk.Button(master=framedown, text=f"{task} here", command=lambda current=x: [self.findbypk_window(current, task), tableselector.destroy()])
                    elif task == "delete":
                        buttontable = tk.Button(master=framedown, text=f"{task} here", command=lambda current=x: [self.findbypk_window(current, task), tableselector.destroy()])
                    labeltable.grid(column=0, row=myrow, pady=5, padx=5)
                    buttontable.grid(column=1, row=myrow, pady=5, padx=5)
                    myrow += 1

        else:
            self.fail_window("Can not operate without connection!")

    def repeat_login(self):
        if self.isConnected:
            try:
                self.mydb = mysql.connector.connect(host=self.address, user=self.user, password=self.password, database="animalute")
            except mysql.connector.Error as err:
                self.fail_window(err)
                self.labelconnectedstatus["text"] = "offline"
                self.labelconnectedstatus["fg"] = "red"
                self.labelusername["text"] = "none"
                self.isConnected = False
            else:
                self.mycursor = self.mydb.cursor()
                print("Connected successfuly!")
                self.labelconnectedstatus["text"] = "online"
                self.labelconnectedstatus["fg"] = "green"
                self.labelusername["text"] = self.user
                self.isConnected = True

    def attempt_login(self, address, user, password):
        try:
            self.mydb = mysql.connector.connect(host=address.get(), user=user.get(), password=password.get(), database="animalute")
        except mysql.connector.Error as err:
            self.fail_window(err)
            self.labelconnectedstatus["text"] = "offline"
            self.labelconnectedstatus["fg"] = "red"
            self.labelusername["text"] = "none"
            self.isConnected = False
        else:
            self.address = address.get()
            self.user = user.get()
            self.password = password.get()
            self.mycursor = self.mydb.cursor()
            print("Connected successfuly!")
            self.labelconnectedstatus["text"] = "online"
            self.labelconnectedstatus["fg"] = "green"
            self.labelusername["text"] = user.get()
            self.isConnected = True

    def login_screen(self):
        loginwindow = tk.Tk()
        loginwindow.title("Log in")
        loginwindow.resizable(False, False)
        addresslabel = tk.Label(master=loginwindow, text="Address:")
        addressentry = tk.Entry(master=loginwindow, width=20)
        userlabel = tk.Label(master=loginwindow, text="User:")
        userentry = tk.Entry(master=loginwindow, width=20)
        passwordlabel = tk.Label(master=loginwindow, text="Password:")
        passwordentry = tk.Entry(master=loginwindow, width=20, show="*")

        loginbutton = tk.Button(master=loginwindow, text="Log in", command=lambda: [self.attempt_login(addressentry, userentry, passwordentry), loginwindow.destroy()], pady=5, padx=5)
        addresslabel.grid(column=0, row=0, pady=5, padx=5, sticky="w")
        addressentry.grid(column=1, row=0, pady=5, padx=5)
        userlabel.grid(column=0, row=1, pady=5, padx=5, sticky="w")
        userentry.grid(column=1, row=1, pady=5, padx=5)
        passwordlabel.grid(column=0, row=2, pady=5, padx=5, sticky="w")
        passwordentry.grid(column=1, row=2, pady=5, padx=5)

        loginbutton.grid(column=0, row=3, pady=5, padx=5)

    def logout(self):
        self.address = str()
        self.password = str()
        self.user = str()
        self.isConnected = False
        self.mydb = 0
        self.mycursor = 0
        self.labelconnectedstatus["text"] = "offline"
        self.labelconnectedstatus["fg"] = "red"
        self.labelusername["text"] = "none"

    def __init__(self):
        self.address = str()
        self.password = str()
        self.user = str()
        self.isConnected = False
        self.mydb = 0
        self.mycursor = 0

        window = tk.Tk()
        window.title("Smart Database Handler")
        window.resizable(False, False)
        frameStatus = tk.Frame(master=window)
        frameButtons = tk.Frame(master=window)
        frameStatus.grid(column=0, row=0)
        frameButtons.grid(column=0, row=1, pady=5, padx=5)

        labelconnected = tk.Label(master=frameStatus, text="Connection status:")
        self.labelconnectedstatus = tk.Label(master=frameStatus, text="offline",fg="red")
        labeluser = tk.Label(master=frameStatus, text="User:")
        self.labelusername = tk.Label(master=frameStatus, text="none")

        labelconnected.grid(column=0, row=0, sticky="w", padx=5, pady=5)
        self.labelconnectedstatus.grid(column=1, row=0, sticky="w", padx=5, pady=5)
        labeluser.grid(column=0, row=1, sticky="w", padx=5, pady=5)
        self.labelusername.grid(column=1, row=1, sticky="w", padx=5, pady=5)

        loginButton = tk.Button(master=frameButtons, text="Log In", command=self.login_screen, width=15)
        logoutButton = tk.Button(master=frameButtons, text="Log Out", command=self.logout, width=15)
        insertButton = tk.Button(master=frameButtons, text="Insert", command=lambda: [self.get_tables("insert")], width=15)
        updateButton = tk.Button(master=frameButtons, text="Update", command=lambda: [self.get_tables("update")], width=15)
        selectButton = tk.Button(master=frameButtons, text="Select", command=lambda: [self.get_tables("select")], width=15)
        deleteButton = tk.Button(master=frameButtons, text="Delete", command=lambda: [self.get_tables("delete")], width=15)

        loginButton.grid(column=0, row=0, padx=2, pady=2)
        logoutButton.grid(column=1, row=0, padx=2, pady=2)
        insertButton.grid(column=0, row=1, padx=2, pady=2)
        updateButton.grid(column=1, row=1, padx=2, pady=2)
        selectButton.grid(column=0, row=2, padx=2, pady=2)
        deleteButton.grid(column=1, row=2, padx=2, pady=2)
        window.mainloop()


dbh = DatabaseHandler()
