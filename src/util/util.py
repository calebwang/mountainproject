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
  it_result = itertools.chain.from_iterable(
    f_chunk(c) for c in chunk(iterable, n)
  )
  return cls(it_result)

def paginator(page_getter, page_limit, n):
  start_pos = 0
  num_results = 0
  while True:
    page = page_getter(start_pos)
    yield page

    page_size = len(page)
    num_results += page_size
    start_pos += page_size

    if num_results >= n or page_size < page_limit:
      return  

def paginate(page_getter, page_limit, n):
  return list(itertools.chain.from_iterable(paginator(page_getter, page_limit, n)))
