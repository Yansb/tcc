from pdfquery import pdfquery
from pdfquery.cache import FileCache
from pypdf import PdfReader
def read_pdf(file_path):
  metadata = {
    "discente": "",
    "titulo": "",
    "orientador": "",
    "resumo": "",
    "palavras_chave": "",
    "ano": "",
  }
  pdf = pdfquery.PDFQuery(file_path, parse_tree_cacher=FileCache("./temp"))
  pdf.load()
  metadata = pdf.extract( [
     ('with_parent','LTPage[pageid=\'2\']'),
     ('with_formatter', 'text'),

     ('discente', 'LTTextBoxHorizontal[index=\'0\']'),
     ('titulo', 'LTTextBoxHorizontal[index=\'1\']'),
     ('ano', 'LTTextBoxHorizontal[index=\'6\']'),

      ('with_parent','LTPage[pageid=\'3\']'),
      ('orientador', f'LTTextLineHorizontal:contains("Orientador")', lambda match: match.text().split(":")[1]),
  ])
  resumo_element = pdf.pq('LTTextLineHorizontal:contains("RESUMO")')
  resumo_index = int(resumo_element.parent().attr('page_index'))

  reader = PdfReader(file_path)
  page = reader.pages[resumo_index]

  metadata['resumo'] = page.extract_text().split("RESUMO")[1].split("Palavras-chave")[0].replace('\n', '').replace('\r', '')
  metadata['palavras_chave'] = page.extract_text().split("Palavras-chave: ")[1].split('.')

  return metadata
