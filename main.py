import webapp2
import re

form="""
<!DOCTYPE html>

<html>
    <head>
        <style>
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
    <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="%(username)s" required>
                    </td>
                        <td class="error">%(error_username)s</td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password" required>
                    </td>
                        <td class="error">%(error_password)s</td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password" required>
                    </td>
                        <td class="error">%(error_verify)s</td>
                    </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="%(email)s">
                    </td>
                    <td class="error">%(error_email)s</td>

                </tr>
            </table>
            <input type="submit">
        </form>
    </body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error_username="", error_password="", error_verify="", error_email="", username="", email=""):
        self.response.write(form % {"username": username,
                                    "email": email,
                                    "error_username": error_username,
                                    "error_password": error_password,
                                    "error_verify": error_verify,
                                    "error_email": error_email})

    def get(self):
        self.write_form()

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""

        if not valid_username(username):
            error_username = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            error_password = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            error_verify = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            error_email= "That's not a valid email."
            have_error = True

        if have_error:
            self.write_form(error_username, error_password, error_verify, error_email, username, email)
        else:
            self.response.write("Welcome " + username + "!")


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
