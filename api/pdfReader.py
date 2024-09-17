from pdfquery import pdfquery
from pdfquery.cache import FileCache
from pypdf import PdfReader
import pymupdf

def read_pdf(file_path):
  metadata = {
    "discente": "",
    "titulo": "",
    "orientador": "",
    "resumo": "",
    "palavras_chave": "",
    "ano": "",
  }
  document = pymupdf.open(filename=file_path)
  pdf = pdfquery.PDFQuery(file_path, parse_tree_cacher=FileCache("temp/"))
  pdf.load()
  metadata = pdf.extract( [
     ('with_parent','LTPage[pageid=\'2\']'),
     ('with_formatter', 'text'),

     ('discente', 'LTTextBoxHorizontal[index=\'0\']'),
     ('titulo', 'LTTextBoxHorizontal[index=\'1\']', lambda match: match.text()),
     ('ano', 'LTTextBoxHorizontal[index=\'6\']'),

      ('with_parent','LTPage[pageid=\'3\']'),
      ('orientador', f'LTTextLineHorizontal:contains("Orientador")', lambda match: match.text()),
  ])
  palavras_chave_element = pdf.pq(f'LTTextLineHorizontal:contains("chave:")')

  if not(palavras_chave_element.parent().attr('page_index')):
    palavras_chave_element = pdf.pq(f'LTTextLineHorizontal:contains("Chave:")')

  resumo_index = int(palavras_chave_element.parent().attr('page_index'))

  reader = PdfReader(file_path)
  page = reader.pages[resumo_index]

  extractedAbstract = page.extract_text().split("Resumo")

  if not(extractedAbstract):
    metadata['resumo'] = extractedAbstract[1].split("Chave:")[0].replace('\n', '').replace('\r', '').strip()
  else:
    metadata['resumo'] = page.extract_text().split("RESUMO")[1].split("palavras-chave:")[0].replace('\n', '').replace('\r', '').strip()

  metadata['palavras_chave'] = list(filter(None,map(str.strip, page.extract_text().split("Chave: ")[1].replace('.', ';').replace(',', ';').split(';'))))

  return metadata
