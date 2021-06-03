from flask import jsonify
from flask import request
from app import app
import mariadb
import sys


def always():
    try:
        con = mariadb.connect(user="root", password="7h8g2cc", host="localhost", port=3306)
        print("Connected")
        return con
    except mariadb.Error as e:
        print(f" Error connecting to Mariadb Server: {e}")
        sys.exit(1)


@app.route('/api_v1', methods=['POST'])
def add_user():
    global cursor, cur
    try:
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        if _name and _email and request.method == 'POST':
            query = "insert into  walexfab_blogs.User_reg1(name,email) values (?,?)"
            bind_data = (_name, _email)
            cur = always()
            cursor = cur.cursor()
            cursor.execute(query, bind_data)
            cur.commit()
            respones = jsonify('POST  successfully !')
            respones.status_code = 200
            return respones
        else:
            return not_found()
    except Exception as es:
        print(es)
    finally:
        cursor.close()
        cur.close()


@app.route('/api_pv2')
def pull_member():
    global cur, con
    try:
        con = always()
        cur = con.cursor()
        cur.execute("select * from walexfab_blogs.User_reg1")
        res = [dict((cur.description[i][0], value)
                    for i, value in enumerate(row))
               for row in cur.fetchall()]
        respones = jsonify(res)
        respones.status_code = 200
        return respones
    except Exception as er:
        print(er)
    finally:
        cur.close()
        con.close()


@app.route('/api_pv3/<int:id>')
def pull_single_user(id):
    global con, cur
    try:
        con = always()
        cur = con.cursor()
        cur.execute("select * from walexfab_blogs.User_reg1 where id= " + str(id))
        res = [dict((cur.description[i][0], value)
                    for i, value in enumerate(row))
               for row in cur.fetchall()]
        respones = jsonify(res)
        respones.status_code = 200
        return respones

    except Exception as ew:
        print(ew)
    finally:
        cur.close()
        con.close()


@app.route('/api_pv4', methods=['PUT'])
def update_column():
    global cursor, conn
    try:
        _json = request.json
        _id = _json['id']
        _name = _json['name']
        _email = _json['email']
        if _name and _email and request.method == 'PUT':
            query = "update walexfab_blogs.User_reg1 set name=?, email=? where id=?"
            bind_data = (_name, _email, _id,)
            conn = always()
            cursor = conn.cursor()
            cursor.execute(query, bind_data)
            conn.commit()
            respones = jsonify('PUT successfully !')
            respones.status_code = 200
            return respones
        else:
            return not_found()
    except Exception as ew:
        print(ew)
    finally:
        conn.close()
        cursor.close()


@app.route('/api_pv5/<int:id>', methods=['DELETE'])
def drop(id):
    global cur, cursor
    try:
        cur = always()
        cursor = cur.cursor()
        cursor.execute("Delete from walexfab_blogs.User_reg1 where id = ?",  (id, ))
        cur.commit()
        respones = jsonify("Deleted Successfully ! ")
        respones.status_code = 200
        return respones
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        cur.close()


@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404, 'message': 'Record not found' + request.url, }
    respone = jsonify(message)
    respone.status_code = 404
    return respone


if __name__ == "__main__":
    app.debug = True
    app.run()
