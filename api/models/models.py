from peewee import *

db = SqliteDatabase('teste.db')

class PDF(Model):
    id = UUIDField(primary_key=True)
    titulo = CharField()
    discente = CharField()
    orientador = CharField()
    resumo = CharField(max_length=5000)
    palavras_chave = CharField()
    ano = CharField()
    filename = CharField()
    class Meta:
        database = db
        table_name = 'pdfs'

