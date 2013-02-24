import urllib2
import json
import cgi
import datetime
import urllib
import webapp2
import httplib2


from twilio.rest import TwilioRestClient

account = ""
token = ""
client = TwilioRestClient(account, token)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("""
          <html>
            <body>

<h3>Get yesterday's precip SMS alert for your fields! </h3>
<div class="highlight-box">
<p>Enter your phone number (this format: +18182443677) and lat/long (this format: 37.8,-122.4). If you're really crafty you can put in a state and major city ("CA/Los Angeles")
instead of lat/long.</p>

              <form action="/submitted" method="post">
               <b> Phone Number: <input type="text" name="phone"><br>
                Lat / Long: <input type="text" name="latlong"></b>
            
                <div><input type="submit" value="Submit"></div>
              </form><p> </body>
          </html>
            """)



class Submitted(webapp2.RequestHandler):


# get phone number and lat/long


    def weathertext(self,recphone,location):



# pull lat/long rain for yesterday, parse response

        f = urllib2.urlopen('http://api.wunderground.com/api/XXXX/yesterday/q/'+location+'.json')

        json_string = f.read()
        parsed_json = json.loads(json_string)
#print(parsed_json)
        damnlist = parsed_json['history']['observations']

        rain_list = [str(item['rain']) for item in damnlist]

        rain_in = max([int(item) for item in rain_list])


        print "Yesterday's rain was: %s" % (rain_in)
        f.close()







#send text
        message = client.sms.messages.create(to="%s" % recphone, from_="+YYYYYYYYYYY",
                                             body="Hello there! It rained %s inches on \
                                             your field at %s" % (rain_in,location))

        return(rain_in)


    def post(self):
        #?
        latlong = self.request.get('latlong')
        recphone = self.request.get('phone')
        #submission.put()
                
        self.response.out.write('<html><body>Thanks! We will text you shortly at this number: <pre>')
        self.response.out.write(cgi.escape(self.request.get('phone')))
        self.response.out.write('</pre></body></html>')

        self.weathertext(recphone,latlong)
        







app = webapp2.WSGIApplication([('/', MainPage),
                              ('/submitted', Submitted)],
                              debug=True)
