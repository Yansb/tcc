import urllib.request
from bs4  import BeautifulSoup as bs
import spacy
from bertopic import BERTopic

pln = spacy.load("pt_core_news_md")

def coletaTexto(url):
  pagina = urllib.request.urlopen(url)
  conteudoLimpo = bs(pagina, features='html5lib')
  documento = pln(conteudoLimpo.text)

  tokens = []
  for token in documento:
    if token.pos_ == "VERB" and token.is_alpha and not(token.is_stop):
      tokens.append(str.lower(token.lemma_))
    elif not(token.pos_ == "VERB") and token.is_alpha and not(token.is_stop):
      tokens.append(str.lower(token.text))
  return tokens

tokens = coletaTexto('https://pt.wikipedia.org/wiki/Python')

modelagem = BERTopic(language="portuguese")
modelagem.fit_transform(tokens)

topicos = modelagem.get_topic_info()

for idTopico, contagem, conteudo in topicos.values:
  print("###########################")
  print(f"Id do Tópico: {idTopico}")
  print(f"Contagem: {contagem}")
  print(f"Conteúdo: {conteudo}")
