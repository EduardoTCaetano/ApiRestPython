from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine,text
from json import dumps

db_connect = create_engine('mysql+mysqlconnector://root@localhost/fatec')

app = Flask(__name__)
api = Api(app)

class Test(Resource):
    def get(self):
        return('{"message":"Servidor funcionando corretamente"}')

class Users(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute(text('select * from alunos order by nome'))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

    def post(self):
        conn = db_connect.connect()
        nome = request.json['nome']
        email = request.json['email']
        conn.execute(text("insert into alunos (nome, email) values ('{0}', '{1}')".format(nome, email)))
        conn.commit()
        query = conn.execute(text('select * from alunos order by nome'))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)
    
    def put(self):
        conn = db_connect.connect()
        id = request.json['id']
        nome = request.json['nome']
        email = request.json['email']
        conn.execute(text("update alunos set nome ='" + str(nome) +"', email ='" + str(email) + "'where id =%d " % int(id)))
        conn.commit()
        query = conn.execute(text('select * from alunos order by id'))
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        return jsonify(result)

class UsersById(Resource):
    def delete(self, id):
        conn = db_connect.connect()
        conn.execute( text("delete from alunos where id=%d "(id)))
        conn.commit()
        return {"status": "success" }

    def get(self, id ):
        conn = db_connect.connect()
        query = conn.execute(text("select * from alunos where id = %d "%int(id)))
        result = [dict(zip(tuple(query.keys()), i))for i in query.cursor]
        return jsonify(result)
    
api.add_resource(Test, '/test')
api.add_resource(Users, '/users')
api.add_resource(UsersById, '/users/<id>')

if __name__ == '__main__':
    app.run()