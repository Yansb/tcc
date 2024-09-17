from fileinput import filename
import pathlib
from flask import *
from uuid import uuid4

from pdfReader import read_pdf
from models.models import db, PDF, University, Course, Topics
from topics.modeling import model_topics, fit_topics

app = Flask(__name__)

db.connect()
db.create_tables([PDF, University, Course, Topics])


@app.route('/')
def main():
  return jsonify({
    'health': True
  })

@app.route('/seed')
def seed():
  university = University.create(
    id=uuid4(),
    name='Universidade do Estado da Bahia'
  )
  course = Course.create(
    id=uuid4(),
    name='Sistemas de Informação',
    university=university
  )
  return jsonify({
    'message': 'Data seeded successfully',
    'course': {
      'id': course.id,
      'name': course.name,
      'university': {
        'id': course.university.id,
        'name': course.university.name
      }
    }
  })

@app.route('/upload', methods=['POST'])
def upload():
  file = request.files['file']
  courseId = request.form['course_id']
  pdfAlreadyExists = PDF.select().where(PDF.filename == file.filename).exists()
  if pdfAlreadyExists:
    return app.response_class(
      content_type='application/json',
      status=400,
      response='{"message": "File already exists"}'
    )
  file.save('temp/' + file.filename)
  metadata = read_pdf('temp/' + file.filename)
  file.close()
  pathlib.Path.unlink('temp/' + file.filename)

  PDF.insert({
    PDF.id: uuid4(),
    PDF.titulo: metadata['titulo'],
    PDF.discente: metadata['discente'],
    PDF.orientador: metadata['orientador'],
    PDF.resumo: metadata['resumo'],
    PDF.palavras_chave: metadata['palavras_chave'],
    PDF.ano: metadata['ano'],
    PDF.filename: file.filename,
    PDF.course: courseId
  }).execute()


  return jsonify({
      'message': 'File uploaded successfully',
      'metadata': metadata
    })



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

@app.route('/fit-topics', methods=['PUT'])
def call_fit_topics():
    pdfs = PDF.select()
    resumos = [pdf.resumo for pdf in pdfs if isinstance(pdf.resumo, str) and pdf.resumo.strip()]
    message, status =  fit_topics(resumos)
    return jsonify({
        'message': message
    }), status


if __name__ == '__main__':
  app.run(debug=True)

