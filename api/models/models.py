from peewee import *

db = SqliteDatabase('teste.db')
class BaseModel(Model):
    id = UUIDField(primary_key=True)
    class Meta:
        database = db



class University(BaseModel):
    name = CharField()
    class Meta:
        table_name = 'universities'

class Course(BaseModel):
    name = CharField()
    university = ForeignKeyField(University, backref='courses')
    class Meta:
        table_name = 'courses'



class PDF(BaseModel):
    titulo = CharField()
    discente = CharField()
    orientador = CharField()
    resumo = CharField(max_length=5000)
    palavras_chave = CharField()
    ano = CharField()
    filename = CharField()
    course = ForeignKeyField(Course, backref='pdfs')
    class Meta:
        table_name = 'pdfs'

class Topics(BaseModel):
    name = CharField()
    pdf = ForeignKeyField(PDF, backref='topics')
    class Meta:
        table_name = 'topics'
