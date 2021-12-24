from flask_mysqldb import MySQL
from flask import jsonify, make_response




class Registration:
    

    def newuser(data,mysql):

        username=data.get("username")
        email=data.get("email")
        FirstName=data.get("firstname")
        LastName=data.get("lastname")
        accnt_no=data.get("accountno")

        cur=mysql.connection.cursor()
        new_value = cur.execute("SELECT * FROM user WHERE accountno =%s", [accnt_no])
        if new_value> 0 :
            return make_response(jsonify({"message": "User already exists"}), 400)

        cur.execute("INSERT INTO user(username,firstname,lastname,email,accountno) VALUES (%s,%s,%s,%s,%s)",(username,FirstName,LastName,email,accnt_no))
        mysql.connection.commit()
        cur.close()    
        return make_response(jsonify({"message": "User details registered"}), 200)


        print(FirstName)

        
        
