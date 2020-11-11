from pyfiglet import Figlet
from tabulate import tabulate
import re

import mysql.connector
mydb = mysql.connector.connect(
host="localhost",
user="root",
passwd="123qwe",
database='MY_DB'
)
print(mydb)

myCursor = mydb.cursor()

print (Figlet(font='speed').renderText("Airport DBMS"))

print("Welcome to this Shit Airline!\n")

while(True):
    User = input("Username: ")
    Pass = input("Password: ")
    if User == "admin" and Pass == "admin":
        print("Admin is here")

        while True:
            print("1. Add a new flight record, with the required details.")
            print("2. Update details of an existing flight record.")
            print("3. View every table of the database in tabular form")
            print("4. Cancel a particular flight record.")
            print("5. View all flights landing and taking off for a particular airport on that day")

            menu_choice = input("Select an Option: ")
            if menu_choice == "1" or menu_choice=="2":
                try:
                    olf_fid = ""
                    if menu_choice == "2":
                        old_fid = input("Enter the flight_id you want to modify: ")
                        if len(old_fid) !=5:
                            raise Exception("Invalid Flight ID") 
                        myCursor.execute("SELECT FLIGHT_ID FROM FLIGHT WHERE FLIGHT_ID=%s", (old_fid, ))
                        myCursor.fetchall()
                        if myCursor.rowcount==0:
                            print("No Such Flight Exists")
                            continue
                        else:
                            print("Enter the new Flight Details")

                    flight_id = input("FlightID: ")
                    if len(flight_id) !=5:
                        raise Exception("Invalid Flight ID")
                    dep = input("Departure Airport: ")
                    arr = input("Arrival Airport: ")
                    if len(dep)!=3 or len(arr)!=3:
                        raise Exception("Invalid Airport Entry")
                    departure_time = input("Departure Time: ")
                    arrival_time = input("Arrival Time: ")
                    if not (re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',departure_time) or re.match(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}',arrival_time)):
                        raise Exception("Invalid Time")
                    
                    airp = input("Airplane: ")
                    fare = int(input("Fare: "))

                    if(menu_choice == "1"):
                        query = "INSERT INTO FLIGHT(FLIGHT_ID, DEPARTURE_AIRPORT, ARRIVAL_AIRPORT, DEPARTURE_TIME, ARRIVAL_TIME, AIRPLANE, FARE) VALUES(%s, %s, %s, %s, %s, %s, %s)"
                        values = (flight_id, dep, arr, departure_time, arrival_time, airp, fare)
                        myCursor.execute(query, values)
                        mydb.commit()
                    else:
                        query = "UPDATE FLIGHT SET FLIGHT_ID=%s, DEPARTURE_AIRPORT=%s, ARRIVAL_AIRPORT=%s, DEPARTURE_TIME=%s, ARRIVAL_TIME=%s, AIRPLANE=%s, FARE=%s WHERE FLIGHT_ID=%s "
                        values = (flight_id, dep, arr, departure_time, arrival_time, airp, fare, old_fid)
                        myCursor.execute(query, values)
                        mydb.commit()


                except Exception as Ex:
                    print(Ex)
                    continue
            elif menu_choice=="3":
                myCursor.execute("SELECT * FROM FLIGHT")
                flight = myCursor.fetchall()
                myCursor.execute("SELECT * FROM PASSENGER1")
                p1 = myCursor.fetchall()
                myCursor.execute("SELECT * FROM PASSENGER2")
                p2 = myCursor.fetchall()
                myCursor.execute("SELECT * FROM TICKET")
                ticket = myCursor.fetchall()

                print("=========================Flight=========================")
                print(tabulate(flight, headers=['FLIGHT_ID', "DEPARTURE_AIRPORT", "ARRIVAL_AIRPORT", "DEPARTUE_TIME", "ARRIVAL_TIME","AIRPLANE","FARE" ]))
                print("=========================PASSENGERS_PARENT=========================")
                print(tabulate(p2, headers=["CNIC", "NATIONALITY", "NAME", "PHONE", "ADDRESS"]))
                print("=========================PASSENGERS_CHILD=========================")
                print(tabulate(p1, headers=["P_ID", "CNIC", "NATIONALITY"]))
                print("=========================TICEKT=========================")
                print(tabulate(ticket, headers=["TICKET_ID", "FLIGHT_ID", "CNIC", "NATIONALITY"]))

            elif menu_choice == "4":
                flight_id = input('Enter the Flight ID to be cancelled: ')
                myCursor.execute('DELETE FROM FLIGHT WHERE FLIGHT_ID=%s',(flight_id,))
                mydb.commit()
        
            elif menu_choice =="5":
                arrival_airport  = input('Enter arrival aiport IATA code : ')
                day = input('Enter the Day(YYYY-MM-DD): ')
                if len(arrival_airport)!=3:
                    print('======Invalid Iata code!=====') 
                    continue
                if not ( re.match(r'\d{4}-\d{2}-\d{2}', day)):
                    print('Invalid Day!')
                    continue
                initTime = day + ' 00:00:00'
                finishTime = day + ' 23:59:59'
                myCursor.execute('SELECT * FROM FLIGHT WHERE ARRIVAL_AIRPORT=%s and DEPARTURE_TIME>=%s and DEPARTURE_TIME<=%s',(arrival_airport, initTime, finishTime))
                result = myCursor.fetchall()
                if myCursor.rowcount == 0:
                    print('No Such Flight Exists')
                    continue
                for i in result:
                    print('Flight ID : '+ str(i[0]) + ' Departure Airport: '+ str(i[1]) + ' Arrival Airport: '+ str(i[2]) + ' Departure Time: '+ str(i[3]) + ' Arrival Time: '+ str(i[4]) + ' Airplane: '+ str(i[5]) + ' Fare: '+ str(i[6]) )
        
    elif User == "Rec" and Pass == "Rec":
        print("Receptioninsty is here")

        while True:
            print("1. Create a new passenger record, with the required personal details.")
            print("2. Update details of an existing passenger Record!")
            print("3. Using departure airport IATA code and arrival airport IATA code, view all available flights in a particular time period.")
            print("4. Generate ticket record for a particular passenger for a particular flight.")
            print("5. Using departure airport IATA code and arrival airport IATA code, view the cheapest flight.")
            print("6. View flight history of a particular passenger")
            print("7. Cancel a particular ticket record.")
            menu_choice = input("Select an option: ")

            if menu_choice =="1" or menu_choice=="2":
                try:
                    if menu_choice=="2":
                        print("Please Write your current details!")
                    
                    CNIC = input("Please Enter CNIC: ")
                    if CNIC.__len__()!=1 or not int(CNIC):
                        raise Exception("Invalid CNIC")
                    else:
                        CNIC = int(CNIC) 
                    Nationality = input("Please Enter your nationality: ")
                    if menu_choice == "1":
                        Name = input("Please Enter full Name: ")                    
                        Phone = input("Please Enter your Phone Number: ")
                        if not int(Phone) or Phone.__len__()!=1:
                            raise Exception("Invalid Phone")
                        else:
                            Phone = int(Phone)
                        Address = input("Please Enter your address: ")
                
                        # Menu Choice = 1 means that I need to insert the record
                        query = "INSERT INTO PASSENGER2 (NATIONALITY, CNIC, NAME, PHONE, ADDRESS) VALUES(%s, %s, %s, %s, %s)"
                        vals = (Nationality, CNIC, Name, Phone, Address)
                        myCursor.execute(query, vals)
                        query = "INSERT INTO PASSENGER1 (NATIONALITY, CNIC) VALUES(%s, %s)"
                        vals = (Nationality, CNIC)
                        myCursor.execute(query, vals)
                        mydb.commit()
                        print("Comitted!")
                    # Menu Choice = 2 means that I need to update a record!
                    else:
                        print("Enter New Details!")
                        NName = input("Please Enter Name: ")
                        NCNIC = input("Please Enter CNIC: ")
                        if NCNIC.__len__()!=1 or not int(NCNIC):
                            raise Exception("Invalid CNIC")
                        else:
                            NCNIC = int(NCNIC)
                        NPhone = input("Please Enter your Phone Number: ")
                        if not int(NPhone) or NPhone.__len__()!=1:
                            raise Exception("Invalid Phone")
                        else:
                            NPhone = int(NPhone)
                        NAddress = input("Please Enter your address: ")
                        NNationality = input("Please Enter your nationality: ")
                        
                        query = "UPDATE PASSENGER2 SET NAME=%s, CNIC=%s, PHONE=%s, ADDRESS=%s, NATIONALITY=%s WHERE CNIC=%s AND NATIONALITY=%s"
                        vals = (NName, NCNIC, NPhone, NAddress, NNationality, CNIC, Nationality)
                        myCursor.execute(query, vals)
                        mydb.commit()

                except Exception as Error:
                    print("Except")
                    print(Error)
                    continue
            
            elif menu_choice == "3":
                code1 = input("IATA code 1:")
                code2 = input("IATA code 2:")
                query = "SELECT FLIGHT_ID, DEPARTURE_AIRPORT, ARRIVAL_AIRPORT, DEPARTURE_TIME, ARRIVAL_TIME, AIRPLANE, FARE FROM FLIGHT WHERE DEPARTURE_AIRPORT=%s AND ARRIVAL_AIRPORT=%s"
                vals = (code1, code2)
                myCursor.execute(query, vals)
                rows = myCursor.fetchall()
                for r in rows:
                    print("FlightId:{}  Departure:{}  Arrival:{}  DepartureTime:{}  ArrivalTime:{}  Airplane:{}  Fare:{}".format(r[0],r[1],r[2],r[3],r[4],r[5],r[6]))
            elif menu_choice == "4":
                try:
                    flight_id = input("Please Enter your flight id: ")
                    cnic = input("Please Enter your cnic: ")
                    if cnic.__len__()!=1 or not int(cnic):
                        raise Exception("Invalid CNIC")
                    else:
                        cnic = int(cnic)
                    national = input("Nationality: ")
                    myCursor.execute("SELECT FLIGHT_ID FROM FLIGHT WHERE FLIGHT_ID=%s", (flight_id, ))
                    flights = myCursor.fetchall()
                    if myCursor.rowcount!=0:
                        myCursor.execute("SELECT CNIC, NATIONALITY FROM PASSENGER1 WHERE CNIC=%s AND NATIONALITY=%s", (cnic, national))
                        nation = myCursor.fetchall()
                        if myCursor.rowcount!=0:
                            query = "INSERT INTO TICKET (CNIC,FLIGHT_ID,NATIONALITY) VALUES(%s,%s,%s)"
                            vals = (cnic, flight_id, national)
                            myCursor.execute(query, vals)
                            mydb.commit()
                        else:
                            print("Register yourself first!")

                    else:
                        print("No Such Flight Exists!")
                        continue

                except Exception as Bug:
                    print(Bug)

            elif menu_choice=="5":
                departure = input("Departure Airport:")
                arrival = input("Arrival Airport:")
                if arrival.__len__()!=3 or departure.__len__()!=3:
                    print("Invalid IATA")
                    continue
                
                myCursor.execute("SELECT MIN(FARE) FROM FLIGHT WHERE ARRIVAL_AIRPORT=%s AND DEPARTURE_AIRPORT=%s",(arrival, departure))
                rows = myCursor.fetchall()
                if len(rows) == 0:
                    print("No Flight b/w thses APS\n")
                    continue
                
                min_fare = rows[0][0]

                myCursor.execute("SELECT * FROM FLIGHT WHERE ARRIVAL_AIRPORT=%s AND DEPARTURE_AIRPORT=%s AND FARE=%s",(arrival, departure, min_fare))
                rows = myCursor.fetchall()
                if len(rows) == 0:
                    print("No flight b/w these Airports!")
                for r in rows:
                    print("f_id:{} Dep:{} Arr:{} DepT:{} ArrT:{} Airplane:{} Fare:{}\n".format(r[0],r[1],r[2],r[3],r[4],r[5],r[6]))




            elif menu_choice=="6":
                try:
                    cnic = input("Please Enter your cnic: ")
                    if cnic.__len__()!=1 or not int(cnic):
                        raise Exception("Invalid CNIC")
                    else:
                        cnic = int(cnic)
                    national = input("Enter your Nationality: ")

                    myCursor.execute("SELECT CNIC, NATIONALITY FROM PASSENGER1 WHERE CNIC=%s AND NATIONALITY=%s", (cnic, national))
                    rows = myCursor.fetchall()
                    if len(rows) != 0:
                        myCursor.execute("SELECT TICKET_ID, FLIGHT_ID from TICKET WHERE NATIONALITY=%s AND CNIC=%s", (national, cnic))
                        rows = myCursor.fetchall()
                        for r in rows:
                            print("Nationality:{}  CNIC:{}  TICKET_ID:{}  FLIGHT_ID:{}".format(national, cnic, r[0], r[1]))
                    else:
                        print("Register yourself first!")
                        continue
                
                except Exception as Exec:
                    print(Exec)
            
            elif menu_choice=="7":
                try:
                    ticket = int(input("Enter Ticket Number: "))
                    myCursor.execute("DELETE FROM TICKET WHERE TICKET_ID=%s", (ticket, ))
                    mydb.commit()

                except:
                    print("Invalid Ticket")

