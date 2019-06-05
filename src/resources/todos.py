import itertools

from resources.resource import Resource
from models.route import Route

class Todos(Resource):
  def _get_page(self, email, start_pos):
    result = self.client.get("get-to-dos", {
      "email": email
    })
    todo_route_ids = result["toDos"]
    return self.client.routes.get_all(todo_route_ids)

  # Get all ticks by default
  def get(self, email, n=float("inf")):
    page_limit = 200      

    def page_generator():
      start_pos = 0
      num_results = 0
      while True:
        page = self._get_page(email, start_pos)
        yield page

        num_results += len(page)
        start_pos += 200

        if num_results >= n or len(page) < page_limit:
          return
  
    return list(itertools.chain.from_iterable(page_generator()))
    
