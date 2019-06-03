import itertools

def chunk(iterable, n):
  it = iter(iterable)
  cls = list
  chunk = cls(itertools.islice(it, n))
  while chunk:
    yield chunk
    chunk = cls(itertools.islice(it, n))

def map_chunk(iterable, n, f_chunk):
  """
  Map over iterable in chunks of size n, applying f_chunk to 
  each chunk, and then flattening the result back into the original
  shape of iterable
  """
  cls = iterable.__class__
  it_result = itertools.chain(
    *(f_chunk(c) for c in chunk(iterable, n))
  )
  return cls(it_result)

  
