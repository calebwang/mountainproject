import itertools

from resources.resource import Resource
from models.route import Route
from util.util import paginate

class Todos(Resource):
  def _get_page(self, email, start_pos):
    result = self.client.get("get-to-dos", {
      "email": email
    })
    todo_route_ids = result["toDos"]
    return self.client.routes.get_all(todo_route_ids)

  # Get all todos by default
  def get(self, email, n=float("inf")):
    page_limit = 200
    return paginate(
      lambda start_pos: self._get_page(email, start_pos),
      page_limit,
      n
    )

