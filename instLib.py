import requests
import re
from time import sleep

class Profile:

    def __init__(self, login):

        self.__login = login
        url = "https://www.instagram.com/" + self.__login + "/?__a=1"
        s = requests.Session()
        while True:
            try:
                request = requests.get(url)
                break
            except:
                print ("Bad Connection page")
                sleep(3)

        try:
            data = request.json()
            self.__numFoll = int(data["user"]["followed_by"]["count"])
            self.__id = int(data["user"]["id"])
            self.__isPrivate = data["user"]["is_private"]
            self.__photo=data["user"]["biography"]["profile_pic_url"]
        except:
            raise "404"


    def get_photo(self):

        p=requests.get(self.__photo)
        out=open("D/photos","wb")
        out.write(p.content)
        out.close()

    def countFollowers(self):

        return self.__numFoll

    def __procText(self, text, tagDict):
        pattern = r"#[\S]*"
        result = re.findall(pattern, text)
        for word in result:
            if tagDict.get(word)== None:
                tagDict.update({word : 1})
            else:
                tagDict[word]+=1

        return tagDict


    def getTagList(self):
        if self.__isPrivate=="true":
            raise "PRIVATE_ERROR"
        lastMedia = ""

        tagDict = dict()
        count=0
        while True:
            url='https://www.instagram.com/graphql/query/?query_id=17888483320059182&variables={"id":"'+str(self.__id)+'","first":12,"after":"'+lastMedia+'"}'
            s = requests.Session()
            while True:
                try:
                    request = requests.get(url)
                    re = request.json()
                    lastMedia = re["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
                    break
                except:
                    print("Bad connection media")
                    sleep(3)
            for i in range(12):
                try:
                    imgUrl = re["data"]["user"]["edge_owner_to_timeline_media"]["edges"][i]["node"]["shortcode"]
                    while True:
                        try:
                            imgHTMLanswer = (requests.get(("https://www.instagram.com/p/" + imgUrl+"/?__a=1")))
                            try:
                                imgHTML= imgHTMLanswer.json()
                            except:
                                print("Photo was deleted")
                                imgHTML=""
                            break
                        except:
                            print("Bad Connection Img")
                            sleep(3)
                    count += 1
                    print(count)
                    try:
                        text= imgHTML["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"]
                    except:
                        text=""
                    tagDict = self.__procText(text, tagDict)

                except:
                    break
            if str(re["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["has_next_page"])!="True":
                break
        return tagDict





