from mountainproject.resources.resource import Resource
from mountainproject.models.user import User

class Users(Resource):
  def find(self, email):
    return User(
      email,
      self.client.get("get-user", {
        "email": email
      }),
      self.client
    )

  def get(self, user_id):
    return User(
      "unknown",
      self.client.get("get-user", {
        "userId": str(user_id)
      }),
      self.client
    )
    
