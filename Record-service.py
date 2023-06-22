# importing inbuilt modules csv,sqlite3
import csv
import sqlite3

# connecting to Record database
connection = sqlite3.connect('Record.db')
# creating a cursor object to execute SQL queries on  a database table
cursor = connection.cursor()

# defining table Control from control-table.csv
# (which is required for finding Confedance in Ticker table)
# mentioning the names of Columns and specifying their
# datatypes
create_Table = '''CREATE TABLE Control(
A TEXT,
B TEXT,
C TEXT)'''
# creating table Control in database
cursor.execute(create_Table)
# copying the contents of control-table.csv to contents
file = open('./Control/control-table.csv')
contents = csv.reader(file)

# SQL query to insert data into Control table
insert_records = '''INSERT INTO Control (A , B , C)
VALUES(? , ? , ?)'''

# Importing the contents  into  Control table
cursor.executemany(insert_records, contents)

# SQL query to retrieve all data from the Control table
# so that we can access and make computations on data
select_all = "SELECT * FROM Control"
controls = cursor.execute(select_all).fetchall()

list_controls = [[]]  # declaring a 2d list list_controls
temp_list = []        # declaring an 1d list temp_list
count = 0             # iniializing count as 0

# creating a list list_industries having types of industries in Control table
list_industry = ['Finance - General', 'Auto Ancillaries', 'Ceramics & Granite']

# obtaining the values in constraints of Control table B column
for row in controls:
    init_str = str(row[1])
    new_str = init_str.strip('<,< ,>=,=,%,> , ')
    length = len(new_str)
    temp_list = list(temp_list)
    if(length < 5):
        constraint1 = float(new_str)
        constraint2 = 0
        temp_list = [constraint1]
        # making a list of (constriant1,constraint2,corresponding confedance)
        temp_list.append(float(0))
        temp_list.append(0)
        temp_list.append(row[2])
    else:
        temp_list = [float(new_str[0])]
        temp_list.append(float(new_str[length - 1]))
        temp_list.append(1)
        temp_list.append(row[2])
    if(count > 0):
        # appending each list of (constriant1,constraint2,corresponding
        # confedance) to list list_controls
        list_controls.append(temp_list)
    else:
        list_controls = [temp_list]
    del(temp_list)
    temp_list = []
    count = count + 1
# correcting the constraints wherever required
for var in range(count):
    if(list_controls[var][2] == 1):
        list_controls[var][1] = list_controls[var + 1][0]

# defining table Day_1
# mentioning the names of Columns and specifying their datatypes
create_table = '''CREATE TABLE Day_1(
Company_Name TEXT,
Industry TEXT,
Last_Price REAL);'''
# creating table Day_1 in database
cursor.execute(create_table)
# copying the contents of 2021101006-20-05-2022.csv to contents
file = open('./Record/2021101006-20-05-2022.csv')
contents = csv.reader(file)
# SQL query to insert data into Day_1 table
insert_records = '''INSERT INTO Day_1 (
Company_Name, Industry,Last_Price)
VALUES(?, ?, ?)'''
# Importing the contents into  Day_1 table
cursor.executemany(insert_records, contents)

# SQL query to retrieve all data from the Day_1 table
# so that we can access and make computations on data
select_all = "SELECT * FROM Day_1"
rows = cursor.execute(select_all).fetchall()
final_list = [[[]]]  # declaring a 3d list final_list
sub_list1 = [[]]     # creating a 2d list sub_list1
count = 0            # initializing count as 0

# making a list temp_list from each row of table
# and  making list sub_list1 of all such lists
for row in rows:
    temp_list = row
    temp_list = list(temp_list)
    if(count > 0):
        sub_list1.append(temp_list)
    else:
        sub_list1 = [temp_list]
        count = count + 1
final_list = [sub_list1]  # adding sub_list1 to final_list

# defining table Day_2
# mentioning the names of Columns and specifying their datatypes
create_table = '''CREATE TABLE Day_2(Company_Name TEXT,
Industry TEXT,
Last_Price REAL);'''
# creating table Day_2 in database
cursor.execute(create_table)
# copying the contents of 2021101006-21-05-2022.csv to contents
file = open('./Record/2021101006-21-05-2022.csv')
contents = csv.reader(file)
# SQL query to insert data into Day_2 table
insert_records = '''INSERT INTO Day_2 (
Company_Name, Industry,Last_Price)
VALUES(?, ?, ?)'''
# Importing the contents  into  Day_2 table
cursor.executemany(insert_records, contents)
# SQL query to retrieve all data from the Day_2 table
# so that we can access and make computations on data
select_all = "SELECT * FROM Day_2"
rows = cursor.execute(select_all).fetchall()
sub_list2 = [[]]  # defining a 2d list sub_list2
count = 0         # initializing count as 0

# making a list temp_list from each row of table
# appending the values of previousdayprice,change in price% to temp_list
# appending the values of confedance(found based on values(constraints)
# and corresponding confedance values stored in list list_controls)
# and  making list sub_list2 of all such lists
for row in rows:
    temp_list = row
    temp_list = list(temp_list)
    temp_list[2] = sub_list1[count][2]
    temp_list.append(row[2])
    temp_list.append((temp_list[3] - temp_list[2]) * 100 / temp_list[2])
    if(temp_list[1] == list_industry[0]):
        if (temp_list[4] < list_controls[0][0]):
            temp_list.append(list_controls[0][3])
        elif list_controls[1][0] <= temp_list[4] <= list_controls[1][1]:
            temp_list.append(list_controls[1][3])
        elif(temp_list[4] > list_controls[2][0]):
            temp_list.append(list_controls[2][3])
    elif(temp_list[1] == list_industry[1]):
        if(temp_list[4] < list_controls[3][0]):
            temp_list.append(list_controls[3][3])
        elif list_controls[4][0] <= temp_list[4] <= list_controls[4][1]:
            temp_list.append(list_controls[4][3])
        elif(temp_list[4] > list_controls[5][0]):
            temp_list.append(list_controls[5][3])
    elif(temp_list[1] == list_industry[2]):
        if(temp_list[4] < list_controls[6][0]):
            temp_list.append(list_controls[6][3])
        elif list_controls[7][0] <= temp_list[4] <= list_controls[7][1]:
            temp_list.append(list_controls[7][3])
        elif(temp_list[4] > list_controls[8][0]):
            temp_list.append(list_controls[8][3])
    if(count > 0):
        sub_list2.append(temp_list)
    else:
        sub_list2 = [temp_list]
    count = count + 1
final_list.append(sub_list2)  # adding sub_list2 to final_list

# defining table Day_3
# mentioning the names of Columns and specifying their datatypes
create_table = '''CREATE TABLE Day_3(Company_Name TEXT,
Industry TEXT,
Last_Price REAL);'''
# creating table Day_3 in database
cursor.execute(create_table)
# copying the contents of 2021101006-22-05-2022.csv to contents
file = open('./Record/2021101006-22-05-2022.csv')
contents = csv.reader(file)
# SQL query to insert data into Day_3 table
insert_records = '''INSERT INTO Day_3 (
Company_Name, Industry,Last_Price)
VALUES(?, ?, ?)'''
# Importing the contents  into  Day_3 table
cursor.executemany(insert_records, contents)
# SQL query to retrieve all data from the Day_3 table
# so that we can access and make computations on data
select_all = "SELECT * FROM Day_3"
rows = cursor.execute(select_all).fetchall()
sub_list3 = [[]]  # defining a 2d list sub_list3
count = 0         # initializing count as 0

# making a list temp_list from each row of table
# appending the values of previousdayprice,change in price% to temp_list
# appending the values of confedance(found based on values(constraints)
# and corresponding confedance values stored in list list_controls)
# and  making list sub_list3 of all such lists
for row in rows:
    temp_list = row
    temp_list = list(temp_list)
    temp_list[2] = sub_list2[count][3]
    temp_list.append(row[2])
    temp_list.append((temp_list[3] - temp_list[2]) * 100 / temp_list[2])
    if(temp_list[1] == list_industry[0]):
        if(temp_list[4] < list_controls[0][0]):
            temp_list.append(list_controls[0][3])
        elif list_controls[1][0] <= temp_list[4] <= list_controls[1][1]:
            temp_list.append(list_controls[1][3])
        elif(temp_list[4] >= list_controls[2][0]):
            temp_list.append(list_controls[2][3])
    elif(temp_list[1] == list_industry[1]):
        if(temp_list[4] < list_controls[3][0]):
            temp_list.append(list_controls[3][3])
        elif list_controls[4][0] <= temp_list[4] <= list_controls[4][1]:
            temp_list.append(list_controls[4][3])
        elif(temp_list[4] >= list_controls[5][0]):
            temp_list.append(list_controls[5][3])
    elif(temp_list[1] == list_industry[2]):
        if(temp_list[4] < list_controls[6][0]):
            temp_list.append(list_controls[6][3])
        elif list_controls[7][0] <= temp_list[4] <= list_controls[7][1]:
            temp_list.append(list_controls[7][3])
        elif(temp_list[4] >= list_controls[8][0]):
            temp_list.append(list_controls[8][3])
    if(count > 0):
        sub_list3.append(temp_list)
    else:
        sub_list3 = [temp_list]
    count = count + 1
final_list.append(sub_list3)  # adding sub_list3 to final_list

# defining table Day_4
# mentioning the names of Columns and specifying their datatypes
create_table = '''CREATE TABLE Day_4(Company_Name TEXT,
Industry TEXT,
Last_Price REAL);'''
# creating table Day_4 in database
cursor.execute(create_table)
# copying the contents of 2021101006-23-05-2022.csv to contents
file = open('./Record/2021101006-23-05-2022.csv')
contents = csv.reader(file)
# SQL query to insert data into Day_4 table
insert_records = '''INSERT INTO Day_4 (
Company_Name, Industry,Last_Price)
VALUES(?, ?, ?)'''
# Importing the contents into  Day_4 table
cursor.executemany(insert_records, contents)
# SQL query to retrieve all data from the Day_4 table
# so that we can access and make computations on data
select_all = "SELECT * FROM Day_4"
rows = cursor.execute(select_all).fetchall()
sub_list4 = [[]]  # defining a 2d list sub_list4
count = 0         # initializing count as 0

# making a list temp_list from each row of table
# appending the values of previousdayprice,change in price% to temp_list
# appending the values of confedance(found based on values(constraints)
# and corresponding confedance values stored in list list_controls)
# and  making list sub_list4 of all such lists
for row in rows:
    temp_list = row
    temp_list = list(temp_list)
    temp_list[2] = sub_list3[count][3]
    temp_list.append(row[2])
    temp_list.append((temp_list[3] - temp_list[2]) * 100 / temp_list[2])
    if(temp_list[1] == list_industry[0]):
        if(temp_list[4] < list_controls[0][0]):
            temp_list.append(list_controls[0][3])
        elif list_controls[1][0] <= temp_list[4] <= list_controls[1][1]:
            temp_list.append(list_controls[1][3])
        elif(temp_list[4] >= list_controls[2][0]):
            temp_list.append(list_controls[2][3])
    elif(temp_list[1] == list_industry[1]):
        if(temp_list[4] < list_controls[3][0]):
            temp_list.append(list_controls[3][3])
        elif list_controls[4][0] <= temp_list[4] <= list_controls[4][1]:
            temp_list.append(list_controls[4][3])
        elif(temp_list[4] >= list_controls[5][0]):
            temp_list.append(list_controls[5][3])
    elif(temp_list[1] == list_industry[2]):
        if(temp_list[4] < list_controls[6][0]):
            temp_list.append(list_controls[6][3])
        elif list_controls[7][0] <= temp_list[4] <= list_controls[7][1]:
            temp_list.append(list_controls[7][3])
        elif(temp_list[4] >= list_controls[8][0]):
            temp_list.append(list_controls[8][3])
    if(count > 0):
        sub_list4.append(temp_list)
    else:
        sub_list4 = [temp_list]
    count = count + 1
final_list.append(sub_list4)  # adding sub_list4 to final_list

# defining table Day_5
# mentioning the names of Columns and specifying their datatypes
create_table = '''CREATE TABLE Day_5(Company_Name TEXT,
Industry TEXT,
Last_Price REAL);'''
# creating table Day_5 in database
cursor.execute(create_table)
# copying the contents of 2021101006-24-05-2022.csv to contents
file = open('./Record/2021101006-24-05-2022.csv')
contents = csv.reader(file)
# SQL query to insert data into Day_5 table
insert_records = '''INSERT INTO Day_5 (
Company_Name, Industry,Last_Price)
VALUES(?, ?, ?)'''
# Importing the contents  into  Day_5 table
cursor.executemany(insert_records, contents)
# SQL query to retrieve all data from the Day_5 table
# so that we can access and make computations on data
select_all = "SELECT * FROM Day_5"
rows = cursor.execute(select_all).fetchall()
sub_list5 = [[]]  # defining a 2d list sub_list5
count = 0         # initializing count as 0

# making a list temp_list from each row of table
# appending the values of previousdayprice,change in price% to temp_list
# appending the values of confedance(found based on values(constraints)
# and corresponding confedance values stored in list l)
# and  making list sub_list5 of all such lists
for row in rows:
    temp_list = row
    temp_list = list(temp_list)
    temp_list[2] = sub_list4[count][3]
    temp_list.append(row[2])
    temp_list.append((temp_list[3] - temp_list[2]) * 100 / temp_list[2])
    if(temp_list[1] == list_industry[0]):
        if(temp_list[4] < list_controls[0][0]):
            temp_list.append(list_controls[0][3])
        elif list_controls[1][0] <= temp_list[4] <= list_controls[1][1]:
            temp_list.append(list_controls[1][3])
        elif(temp_list[4] >= list_controls[2][0]):
            temp_list.append(list_controls[2][3])
    elif(temp_list[1] == list_industry[1]):
        if(temp_list[4] < list_controls[3][0]):
            temp_list.append(list_controls[3][3])
        elif list_controls[4][0] <= temp_list[4] <= list_controls[4][1]:
            temp_list.append(list_controls[4][3])
        elif(temp_list[4] >= list_controls[5][0]):
            temp_list.append(list_controls[5][3])
    elif(temp_list[1] == list_industry[2]):
        if(temp_list[4] < list_controls[6][0]):
            temp_list.append(list_controls[6][3])
        elif list_controls[7][0] <= temp_list[4] <= list_controls[7][1]:
            temp_list.append(list_controls[7][3])
        elif(temp_list[4] >= list_controls[8][0]):
            temp_list.append(list_controls[8][3])
    if(count > 0):
        sub_list5.append(temp_list)
    else:
        sub_list5 = [temp_list]
    count = count + 1
final_list.append(sub_list5)  # adding sub_list4 to final_list

# defining table Ticker
# mentioning the names of Columns and specifying their datatypes
Create_table = '''CREATE TABLE Ticker(
Date BLOB,
Company_Name TEXT,
Industry TEXT,
PreviousDay_Price REAL,
Current_Price REAL,
Change_in_Price_Percentage REAL,
Confidance TEXT);'''

# creating table Ticker in database
cursor.execute(Create_table)
# copying contents of list final_list[0] to contents
contents = final_list[0]
# SQL query to insert data Ticker
insert_records = '''INSERT INTO Ticker (
Date,Company_Name,Industry,PreviousDay_Price,Current_Price,
Change_in_Price_Percentage,Confidance)
VALUES('20-05-2022', ?, ?, 'NA', ?,'NA','Listed New')'''
# Importing the contents into Ticker table
cursor.executemany(insert_records, contents)
# SQL query to retrieve all data from the Ticker table(added till now)
# so that we can access and make computations on data
select_all = "SELECT * FROM Ticker;"
firstday_data = cursor.execute(select_all).fetchall()
# copying contents of list final_list[1] to contents
contents = final_list[1]
# SQL query to insert data Ticker
records = '''INSERT INTO Ticker (
Date,Company_Name,Industry,PreviousDay_Price,Current_Price,
Change_in_Price_Percentage,Confidance)
VALUES('21-05-2022', ?, ? ,?, ?, ?, ?)'''
# Importing the contents into Ticker table
cursor.executemany(records, contents)

# copying contents of list final_list[2] to contents
contents = final_list[2]
# SQL query to insert data Ticker
records = '''INSERT INTO Ticker (
Date,Company_Name,Industry,PreviousDay_Price,Current_Price,
Change_in_Price_Percentage,Confidance)
VALUES('22-05-2022', ?, ? ,?, ?, ?, ?)'''
# Importing the contents into Ticker table
cursor.executemany(records, contents)

# copying contents of list final_list[3] to contents
contents = final_list[3]
# SQL query to insert data Ticker
records = '''INSERT INTO Ticker (
Date,Company_Name,Industry,PreviousDay_Price,Current_Price,
Change_in_Price_Percentage,Confidance)
VALUES('23-05-2022', ?, ? ,?, ?, ?, ?)'''
# Importing the contents into Ticker table
cursor.executemany(records, contents)

# copying contents of list final_list[4] to contents
contents = final_list[4]
# SQL query to insert data Ticker
records = '''INSERT INTO Ticker (
Date,Company_Name,Industry,PreviousDay_Price,Current_Price,
Change_in_Price_Percentage,Confidance)
VALUES('24-05-2022', ?, ? ,?, ?, ?, ?)'''
# Importing the contents into Ticker table
cursor.executemany(records, contents)

# SQL query to retrieve  data of Day 24-05-2022 from the Ticker table
# so that we can access and make computations on data
select_specific = "SELECT * FROM Ticker WHERE Date='24-05-2022';"
lastday_data = cursor.execute(select_specific).fetchall()
# SQL query to retrieve all data from the Ticker table
# so that we can access and make computations on data
select_all = "SELECT * FROM Ticker"
complete_data = cursor.execute(select_all).fetchall()

# creating a list of lists->kpi_metrics for storing contents of KPI column
# of metrics
kpi_metrics = [['Best listed Industry'], ['Best Company'], ['Gain %'],
               ['Worst listed Industry'], ['Worst Company'], ['Loss %']]

# initializing count as 0
count = 0

# initializing high_count1,high_count2,high_count3 as 0
# Here high_count1->Finance - General
# high_count2->Auto Ancillaries
# high_count3->Ceramics & Granite
high_count1 = 0
high_count2 = 0
high_count3 = 0
# initializing low_count1,low_count2,low_count3 as 0
# Here low_count1->Finance - General
# low_count2->Auto Ancillaries
# low_count3->Ceramics & Granite
low_count1 = 0
low_count2 = 0
low_count3 = 0

# calculating highcount1,highcount2,highcount3 and
# lowcount1,lowcount2,lowcount3 using the value in
# confedance column of each row
for row in complete_data:
    if(row[2] == list_industry[0]):
        if(row[6] == 'High'):
            high_count1 = high_count1 + 1
        elif(row[6] == 'Low'):
            low_count1 = low_count1 + 1
    if(row[2] == list_industry[1]):
        if(row[6] == 'High'):
            high_count2 = high_count2 + 1
        elif(row[6] == 'Low'):
            low_count2 = low_count2 + 1
    if(row[2] == list_industry[2]):
        if(row[6] == 'High'):
            high_count3 = high_count3 + 1
        elif(row[6] == 'Low'):
            low_count3 = low_count3 + 1
# creatings lists with counts obtained
list_highcounts = [high_count1, high_count2, high_count3]
list_lowcounts = [low_count1, low_count2, low_count3]

# finding the industry having maximum number of highs and lows
# based on the corresponding industry names in list lis
# and inserting the industry name into corresponding list of list kpi_metrics
if(max(list_highcounts) == high_count1):
    kpi_metrics[0].append(list_industry[0])
elif(max(list_highcounts) == high_count2):
    kpi_metrics[0].append(list_industry[1])
elif(max(list_highcounts) == high_count3):
    kpi_metrics[0].append(list_industry[2])
if(max(list_lowcounts) == low_count1):
    kpi_metrics[3].append(list_industry[0])
elif(max(list_lowcounts) == low_count2):
    kpi_metrics[3].append(list_industry[1])
elif(max(list_lowcounts) == low_count3):
    kpi_metrics[3].append(list_industry[2])

list_extremes = [[]]  # declaring a 2d list list_estremes
count = 0              # initializing count as 0
# making  list temp_list having companyname and firstday price of each company
# and adding all those lists to list list_extremes
for row in firstday_data:
    temp_list = [row[1]]
    temp_list = list(temp_list)
    temp_list.append(row[4])
    if(count > 0):
        list_extremes.append(temp_list)
    else:
        list_extremes = [temp_list]
    count = count + 1
count = 0              # initializing count as 0
# adding lastdayprice of each company to corresponding list in list_extremes
for row in lastday_data:
    list_extremes[count].append(row[4])
    count = count + 1
# inserting change in price(last dayprice-firstdayprice) and change%
# and 'Loss'/'Gain' based on sign of change%
# of each company to corresponding list in list_extremes
for var in range(89):
    list_extremes[var].append(list_extremes[var][2] - list_extremes[var][1])
    list_extremes[var].append(
        list_extremes[var][3] *
        100 /
        list_extremes[var][1])
    if(list_extremes[var][4] < 0):
        list_extremes[var].append('Loss')
    else:
        list_extremes[var].append('Gain')

list_Gains = [[]]  # declaring a 2d list list_Gains
list_Losses = [[]]  # declaring a 2d list list_Gains
loss_count = 0     # initializing loss_count as 0
gain_count = 0     # initializing gain_count as 0

# inserting loss%,loss,companyname of companies
# having Loss into temp_list
# and adding all those lists to list_Losses
# and calculating number of companies having Loss
for var in range(89):
    if(list_extremes[var][5] == 'Loss'):
        loss_count = loss_count + 1
        temp_list = [list_extremes[var][4]]
        temp_list = list(temp_list)
        temp_list.append(list_extremes[var][3])
        temp_list.append(list_extremes[var][0])
        if(var > 0):
            list_Losses.append(temp_list)
        else:
            list_Losses = [temp_list]

# inserting gain%,gain,companyname of companies
# having Gain into temp_list
# and adding all those lists to list_Gains
# and calculating number of companies having Gain
for var in range(89):
    if(list_extremes[var][5] == 'Gain'):
        gain_count = gain_count + 1
        temp_list = [list_extremes[var][4]]
        temp_list = list(temp_list)
        temp_list.append(list_extremes[var][3])
        temp_list.append(list_extremes[var][0])
        if(var > 0):
            list_Gains.append(temp_list)
        else:
            list_Gains = [temp_list]

# sorting list_Losses list
list_Losses.sort()
# sorting list_Gainss list
list_Gains.sort()
count = 0  # initializing count as 0
# in case of same loss%,loss
# finding index of company which will be bottom as per alphabetical order
while(list_Losses[count][0] == list_Losses[count + 1][0] and list_Losses[count][1] == list_Losses[count + 1][1]):
        count = count + 1
# then adding the required company name and its loss% to
# corresponding lists of kpi_metrics
kpi_metrics[4].append(list_Losses[count][2])
kpi_metrics[5].append(list_Losses[count][0])

# initializing count as gain_count(obtained above)
count = gain_count
# in case of same loss%,loss
# finding index of company which will be top as per alphabetical order
while(list_Gains[count][0] == list_Gains[count - 1][0] and list_Gains[count][1] == list_Gains[count - 1][1]):
        count = count - 1
# then adding the required company name and its gain% to
# corresponding lists of kpi_metrics
kpi_metrics[1].append(list_Gains[count][2])
kpi_metrics[2].append(list_Gains[count][0])

# defining table Metrics
# mentioning the names of Columns and specifying their datatypes
Create_Table = '''CREATE TABLE Metrics(
            KPIs TEXT,
Metrics TEXT);
'''
# creating table Day_3 in database
cursor.execute(Create_Table)
# copying the contents of list kpi_metrics to contents
contents = kpi_metrics
# SQL query to insert data Ticker
records = '''INSERT INTO Metrics (KPIs,Metrics)
VALUES(?, ? )'''
# Importing the contents into Ticker table
cursor.executemany(records, contents)

# committing the changes
connection.commit()

# closing the database connection
connection.close()
