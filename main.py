from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# configurando o local da nossa base de dados
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# criar modelo para armazenar os videos
class VideoModel(db.Model):
    # declarar os campos que dentro do modelo de videos
    id = db.Column(db.Integer, primary_key=True)
    # quantidade de caracteres, nullable = False == esse campo precisar ter algo nele
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"

#criando a base de dados
# depois que rodamos o código 1 vez, nos comentamos essa linha para ele não sobbrescrever os dados
# db.create_all()

# "válida" para ver se o dado que passamos está correto
video_put_args = reqparse.RequestParser()

video_put_args.add_argument("name", type=str, help="Nome do video é obrigatório", required=True)
video_put_args.add_argument("views", type=int, help="Informe a qantidade de view", required=True)
video_put_args.add_argument("likes", type=int, help="Informe a quantidade de likes", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Nome do video é obrigatório")
video_update_args.add_argument("views", type=int, help="Informe a qantidade de view")
video_update_args.add_argument("likes", type=int, help="Informe a quantidade de likes")


resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer,
}


class Video(Resource):
    # serializar os dados do "return result" de acordo com o "resource_field"
    @marshal_with(resource_fields)
    # video_id é passado como parametro para podermos acessarmos ele no api.add_resources
    # retorna
    def get(self, video_id):
        # filtrar todos os videos por ID, retornando a primeira resposta
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Não foi possivel encontrar o video...")
        return result

    # criar 
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="O video já existe...")

        video = VideoModel(id=video_id, name=args["name"], views=args["views"], likes=args["likes"])
        # adicionar temporariamente o video para a base de dados
        db.session.add(video)
        # confirmar as mudanças e torna-las permanentes
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video não existe, não foi possivel atualizar..")
        # se tivermos um resultado, atualizar ele
        if args['name']:
            result.name= args["name"]
        if args['views']:
            result.views= args["views"]
        if args['likes']:
            result.likes= args["likes"]
       
        db.session.commit()

        return result
    
    # def delete(self, video_id): 
    #     if_video_id_doesnt_exist(video_id)
    #     del videos[video_id]
    #     # 204 => deletado com sucesso
    #     return '', 204

# adicionaro "resource" declarado, onde passamos o "resource" e o endpoint
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__": 
        app.run(debug=True)