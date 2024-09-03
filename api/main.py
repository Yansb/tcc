from fileinput import filename
import pathlib
from flask import *
from uuid import uuid4

from pdfReader import read_pdf
from models.models import db, PDF

app = Flask(__name__)

db.connect()
db.create_tables([PDF])

@app.route('/')
def main():
  return jsonify({
    'health': True
  })

@app.route('/upload', methods=['POST'])
def upload():
  file = request.files['file']
  file.save('temp/' + file.filename)
  metadata = read_pdf('temp/' + file.filename)
  file.close()
  pathlib.Path.unlink('temp/' + file.filename)
  pdfAlreadyExists = PDF.select().where(PDF.titulo == metadata['titulo'], PDF.discente == metadata['discente']).exists()
  if pdfAlreadyExists:
    return app.response_class(
      content_type='application/json',
      status=400,
      response='{"message": "File already exists"}'
    )
  res = PDF.insert({
    PDF.id: uuid4(),
    PDF.titulo: metadata['titulo'],
    PDF.discente: metadata['discente'],
    PDF.orientador: metadata['orientador'],
    PDF.resumo: metadata['resumo'],
    PDF.palavras_chave: metadata['palavras_chave'],
    PDF.ano: metadata['ano'],
    PDF.filename: file.filename
    }).execute()


  return app.response_class(
    content_type='application/json',
    status=200,
    response='{"message": "File uploaded"}'
  )


@app.route('/pdfs', methods=['GET'])
def pdfs():
  pdfs = PDF.select()
  return jsonify([{
    'id': pdf.id,
    'titulo': pdf.titulo,
    'discente': pdf.discente,
    'orientador': pdf.orientador,
    'resumo': pdf.resumo,
    'palavras_chave': pdf.palavras_chave,
    'ano': pdf.ano,
    'filename': pdf.filename
  } for pdf in pdfs])

if __name__ == '__main__':
  app.run(debug=True)
