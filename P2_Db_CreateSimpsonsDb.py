import sqlite3

print '*************PART ONE: CREATING DATABASE****************'
conn = sqlite3.connect('simpsons.db')
conn.execute("DROP TABLE IF EXISTS simpson_info;")
conn.execute("CREATE TABLE simpson_info(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, gender TEXT, age INT, occupation TEXT);")
conn.execute("INSERT INTO simpson_info (name, gender, age, occupation) VALUES ('Bart Simpson', 'Male', 10, 'Student');")
conn.commit()
changes = conn.total_changes
print 'Number of changes: ', changes
conn.execute("INSERT INTO simpson_info (name, gender, age, occupation) VALUES ('Homer Simpson', 'Male', 40, 'Nuclear Plant');")
conn.execute("INSERT INTO simpson_info (name, gender, age, occupation) VALUES ('Lisa Simpson', 'Female', 8, 'Student');")
conn.commit()
changes = conn.total_changes
print 'Number of changes: ', changes
cursor = conn.execute("SELECT id, name, gender, age, occupation FROM simpson_info;")
rows = cursor.fetchall()
print rows
print '--------'
cursor = conn.execute("SELECT * FROM simpson_info WHERE name = 'Homer Simpson';")
row = cursor.fetchall()
print row
print '--------'
conn.execute("DELETE FROM simpson_info WHERE id=2;")
cursor = conn.execute("SELECT id, name, gender, age, occupation FROM simpson_info;")
rows = cursor.fetchall()
print rows
print '--------'
conn.execute("INSERT INTO simpson_info (name, gender, age, occupation) VALUES ('Homer Simpson', 'Male', 40, 'Nuclear Plant');")
cursor = conn.execute("SELECT id, name, gender, age, occupation FROM simpson_info;")
rows = cursor.fetchall()
print rows
print '--------'
conn.execute("UPDATE simpson_info SET age=41 WHERE name='Homer Simpson';")
cursor = conn.execute("SELECT id, name, gender, age, occupation FROM simpson_info;")
rows = cursor.fetchall()
print rows
print '--------'


print '*************PART TWO****************'

def mainLoop():
    inLoop = True
    while inLoop == True:
        options()
        again = raw_input('\nWould you like to do something else? (y/n) ')
        if again != 'y':
            inLoop = False

def options():
    print '\n What would you like to do?'
    print '1. Add a new character'
    print '2. View all characters'
    print '3. Search for a character'
    print '4. Delete a character'
    print '5. Quit'
    response = raw_input('Enter number: ')
    if response == '1':
        newCharacter()
    elif response == '2':
        viewAll()
    elif response == '3':
        viewDetails()
    elif response == '4':
        deleteCharacter()
    else:
        return

def printData(data):
    for row in data:
        print 'ID:', row[0]
        print 'Name:', row[1]
        print 'Gender:', row[2]
        print 'Age', row[3]
        print 'Occupation:', row[4], '\n'

def newCharacter():
    print '\nAdding a new character...'
    name = raw_input('Name: ')
    gender = raw_input('Gender: ')
    age = raw_input('Age: ')
    occupation = raw_input('Occupation: ')
                           
    valStr = "'{}', '{}', '{}', '{}'".format(name, gender, age, occupation)
    sqlStr = "INSERT INTO simpson_info (name, gender, age, occupation) VALUES ({});".format(valStr)
                           
    conn.execute(sqlStr)
    conn.commit()

def viewAll():
    sqlStr = "SELECT * FROM simpson_info"
    cursor = conn.execute(sqlStr)
    rows = cursor.fetchall()
    print rows

def viewDetails():
    print '\nViewing character details'
    name = raw_input("Enter the character's name: ")
    sqlStr = "SELECT * FROM simpson_info WHERE name='{}'".format(name)
    cursor = conn.execute(sqlStr)
    rows = cursor.fetchall()
    if len(rows) == 0:
        print 'No records found.'
        return
    else:
        printData(rows)

def deleteCharacter():
    print '\nDeleting a character'
    name = raw_input("Enter the character's name: ")
    sqlStr = "SELECT * FROM simpson_info WHERE name='{}'".format(name)
    cursor = conn.execute(sqlStr)
    rows = cursor.fetchall()
    if len(rows) == 0:
        print 'No records found.'
        return
    elif len(rows) == 1:
        print 'One record found'
        printData(rows)
        deleteID = rows[0][0]                   
    else:
        print 'More than one record found...'
        printData(rows)
        deleteID = raw_input("Type the ID of the character to delete: ")
        
    really = raw_input("Confirm delete character (y/n) ")
    if really == 'y':
        sqlStr = "DELETE FROM simpson_info WHERE id={}".format(deleteID)
        conn.execute(sqlStr)
        conn.commit()
        print 'number of records changed: ', conn.total_changes
    else:
        return


mainLoop()

