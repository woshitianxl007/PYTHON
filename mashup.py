#coding:utf-8
import flickrapi
import urllib2,urllib
import json
import re

class Mashup:
    def __init__(self):
        #zip_code_key need crawling from https://www.zipcodeapi.com/API
        self.zip_code_key = self.Getzip_code_key()
        self.flikr_api_key = '613b51cbfd0269d111e952be1c994147'
        self.flikr_api_secret = '600124c95f7802db'
        self.google_api_key = 'AIzaSyAZaBhronbg2BVkohVlLNL233-P5CrDiVs'

    #the Crawler is used to get the zip_code_key and return
    def Getzip_code_key(self):
        #try to get the zip_code_key
        #except: return ""
        try:
            page = urllib.urlopen("https://www.zipcodeapi.com/API")
            html = page.read()
            reg = 'name="api_key" value=\"\w*\"'
            keyreg = re.compile(reg)
            keylist = re.findall(keyreg, html)
            key = keylist[0][22:][:-1]
            return key
        except :
            return ""

    #Program entry
    def Domain(self):
        #check the zip_code_key crawling success
        if self.zip_code_key == "":
            print "Failure to crawling zip_code_key!"
            return

        raw_input_A =raw_input("enter the zip code: ")
        #if city is exist then do next
        #else domain against
        if self.CheckInput(raw_input_A):
            self.CatchData(raw_input_A)
        else:
            self.Domain()
    #Check the input
    def CheckInput(self,raw_input_A):
        if len(raw_input_A) == 5:
            return True
        else:
            print "The input is worng length!"
            print "----------"
            return False

    #Check the target is not null?
    #yse:return true
    #no：domain()
    def IsNotNull(self, target):
        if target:
            return True
        else:
            self.Domain()
    # the analyzerfor's core
    # Get the city,state,latitude,longitude
    def CatchData(self,zipcode):
        self.url = "http://www.zipcodeapi.com/rest/" + self.zip_code_key + "/info.json/" + str(zipcode) + "/degrees"
        set = self.Http_Get()
        if self.IsNotNull(set):
            jo = json.loads(set)
            city = jo["city"]
            state = jo["state"]
            latitude = str(jo["lat"])
            longitude = str(jo["lng"])
            #print the Mapped city of zip code
            print "The city: " + city
            print "The state: " + state
            print "The earth's latitude and longitude:[" + latitude + "," + longitude + "]"
            #Get the photos
            photos = self.GetPhotos(city, latitude, longitude)
            self.PrintPhotos(photos)

    # Send a Get request to the server by urllib2
    def Http_Get(self):
        try:
            response = urllib2.urlopen(self.url)
            # Get the josn resopnse
            return response.read()
        except Exception:
            print "the zip code is not exist!"

    #Get the five picture about the city
    def GetPhotos(self, tag, latitude, longitude):
        if self.IsNotNull(tag):
            flickr = flickrapi.FlickrAPI(self.flikr_api_key,  self.flikr_api_secret, cache=False)
            try:
                #Get the collection of picture
                photos = flickr.walk(text="'"+tag+"'", tag_mode='all',
                    tags = "'"+tag+"'",
                    latitudes ="'"+latitude+"'",
                    longitude ="'"+longitude+"'",
                    pages = '1',
                    per_page='20',
                    extras='owner_name,tags,url_q,url_m,url_o')
                print "----------"
                print "Five picture about "+tag+" on Flikr:"
                return photos
            except Exception:
                print 'Get photos error'
                exit()

    #print the five picture of photos
    def PrintPhotos(self, photos):

        try:
            i = 0;
            for photo in photos:
                if(i==5):
                    break
                print "picture"+ str(i+1) + ":" + photo.get('title')
                print photo.get('url_m')
                print ""
                i = i+1
        except Exception,ex:
            print 'Print photos error'
            print Exception,':',ex

if __name__ == "__main__":
    m =Mashup()
    m.Domain()