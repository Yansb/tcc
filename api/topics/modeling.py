from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired


representation_model = KeyBERTInspired()

topic_model = BERTopic(language="multilingual", representation_model=representation_model, min_topic_size=2)
def model_topics(abstract):
  topics, probs = topic_model.fit(abstract)
  print(topic_model.get_topics())



def fit_topics(resumos):
  try:
      topics, probs = topic_model.fit_transform(resumos)
      fig = topic_model.get_topics()
      print(fig)
  except ValueError as e:
      return e.args[0], 500
  return "Topics fitted successfully", 200
