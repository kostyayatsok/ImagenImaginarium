def make_new_picture_from_two_embeddings(text_embeddings_1,text_embeddings_2, how_many_we_can_union):
  alf = 1 - how_many_we_can_union
  omega = alf * text_embeddings_1 + (1-alf) * text_embeddings_2
  return omega