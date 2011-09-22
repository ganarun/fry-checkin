import cgi
import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db


#there are 2 different programmes in this code:

#The first programme has 3 classes called: Sign_in, MainPage, and Sign_in_book.
#This programme is used for users to sign in their name at a certain time and date.


# The Sign_in class contains 'content' and 'date'. The 'content' is to register the name and 'date' is to register the time and date at which the user signs in at.

class Sign_in(db.Model) :
    content = db.StringProperty()
    date= db.DateTimeProperty(auto_now_add=True)


# The MainPage class i

class MainPage(webapp.RequestHandler) :
    def get(self):
        self.response.out.write("""
     <html>
       
        <title>FRY CHECK-IN</title>
       
          <body> <b>FRY CHECK-IN</b>             
            <form action="/sign" method="post">
              <div><input name="content" width="50"></input></div>
              <div><input type="submit" value="Please key in your name"><div>
            </form>
            <a href="/macaddress">Configure your mac addresses</a>
          </body>
      </html> """)
        sign_in_names=Sign_in.gql(
                            "WHERE date > :1 "
                            "ORDER BY date DESC LIMIT 10",
                            datetime.datetime.now() - datetime.timedelta(minutes=15))

        for sign_in in sign_in_names:

            if sign_in.content:
                self.response.out.write(
                    "<p><b><font size=5>%s signed in @ %s</font></b></t></p>"
                    %(sign_in.content, sign_in.date))

class Sign_in_book(webapp.RequestHandler) :
    def post(self) :
        self.response.out.write("<html><body><pre>")
        self.response.out.write(cgi.escape(self.request.get("content")))
        self.response.out.write("</pre></body></html>")

        sign_in = Sign_in()

        sign_in.content = self.request.get('content')
        sign_in.put()
        self.redirect('/')

# The second programme has 3 classes called: Mac_address, MacPage, and Macaddress_users.
# This programme is used to enter and save: the user's name, the name and model number of the user's device, and the Mac-address of the device.


# The Mac_Address class consists of owner, device, and mac_add

class Mac_address(db.Model) :
    owner = db.StringProperty()
    device= db.StringProperty()
    mac_add = db.StringProperty()

#The MacPage class


class MacPage(webapp.RequestHandler):
    def get(self):                                                  
        self.response.out.write("""
    <html>
        <body><h1><a href="/">FRY-IT USER CHECK IN</a></h1>        
                    <div><table border = "2">
                    <tr>
                    <th>User's Name</th>
                    <th>Name and Model of User's Device</th>
                    <th>Mac Address of the Device</th>
                    </tr>""")

        the_users = Mac_address.all()

        
        for mac_address in the_users:
            if mac_address.owner:

                self.response.out.write("""

                   <tr>
                   <td><font size=4>%s</font></td>
                   <td><font size=4>%s</font></td>
                   <td><font size=4>%s</font></td>
                   </tr>"""%(mac_address.owner, mac_address.device, mac_address.mac_add))

        self.response.out.write(           
        """</table>"""
                )

        self.response.out.write("""                   
            <form action="/macaddress_users" method="post">
              <title>FRY-IT USER CHECK IN</title>
              <body><p>Please fill in the following information:</p></body>
              <div><label>Your Name:</label><input name="owner" width="50"></input></div>
              <div><label>Device Name:</label><input name="device" width="50"></input></div>
              <div><label>Mac Address of the Device:</label><input name="mac_add" width="50"></input></div>
              <div><p><input type="submit" value="SUBMIT"></p><div>
            </form>                
        </body>
    </html>
           """)

class Macaddress_users (webapp.RequestHandler) :
    def post(self) :
        
        self.response.out.write("<html><body><pre>")
        self.response.out.write("</pre></body></html>")

        mac_address = Mac_address()

        mac_address.owner = self.request.get('owner')
        mac_address.device = self.request.get('device')
        mac_address.mac_add = self.request.get('mac_add')
        mac_address.put()
        self.redirect('/macaddress')
               



application = webapp.WSGIApplication([   #url bar
    ('/', MainPage),   
    ('/sign', Sign_in_book),
    ('/macaddress', MacPage),
    ('/macaddress_users', Macaddress_users)], debug=True)


def main():
    run_wsgi_app(application)

if __name__== "__main__":
    main()








