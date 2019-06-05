from resources.resource import Resource
import models.user

class Users(Resource):
  def _create_user_model(self, email, user_response):
    return models.user.User(
      email,
      user_response,
      self.client
    )

  def find(self, email):
    return self._create_user_model(
      email,
      self.client.get("get-user", {
        "email": email
      })
    )

  def get(self, user_id):
    return self._create_user_model(
      "unknown",
      self.client.get("get-user", {
        "userId": str(user_id)
      }),
    )
    
