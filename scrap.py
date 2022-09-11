from bs4 import BeautifulSoup
from dotenv import load_dotenv

import requests
import time
load_dotenv()




def main():
    response=requests.get("https://minecraft-server-list.com/")
    if response:
        ign=input("Enter ign: ")
        html_doc=response.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        #Get all columns with the server title and link in it
        td=soup.findAll("td",{"class":"n2"})
        #Extract Server name and vote URL
        for i in td:
            head=i.find("h2",{"class":"column-heading"})
            print(head.find("a").find(text=True),end=" , ")
            print("https:"+head.find("a")['href']+"vote")
            url="https:"+head.find("a")['href']+"vote"
            iden=url.split("/")[-2]
            captchabypassurl=f"http://2captcha.com/in.php?key={APIKEY}&method=userrecaptcha&version=v3&action=vote&min_score=0.3&googlekey={GOOGLEKEY}&pageurl={url}"

            session = requests.Session()
            
            voteresp=session.get(url)
            capresp=requests.get(captchabypassurl)
            respid=capresp.text.split("|")[1]
            captcharespurl=f"http://2captcha.com/res.php?key={APIKEY}&action=get&id={respid}"
            tries=0
            gcap=""
            while tries<3:
                respcap=requests.get(captcharespurl)
                if respcap.text.split("|")[0]=="OK":
                    gcap=respcap.text.split("|")[1]
                    break
                tries+=1
                time.sleep(5)
            if not gcap=="":
                votesoup=BeautifulSoup(voteresp.text,"html.parser")
                form=votesoup.find(id="voteform")
                mitcheck=form.find("input",{"class":"buttonsmall"})["onclick"]
                mitcheck=mitcheck.split("(")[1]
                mitcheck=mitcheck.split(")")[0]
                ipennn=form.find("input",{"name":"ipennn"})["value"]

                
                #print(form.find("input",{"class":"buttonsmall"})["onclick"])
                print("Loading...")
                payload=f"ipennn={ipennn}&iden={iden}&ignn={ign}&g-recaptcha-response={gcap}"
                headers = {
                'Host': 'minecraft-server-list.com',
                'Content-Length': '532',
                'Sec-Ch-Ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Sec-Ch-Ua-Mobile': '?0',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Origin': 'https://minecraft-server-list.com',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Dest': 'empty',
                'Referer': url,
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9',
                'Cookie': f'PHPSESSID={session.cookies["PHPSESSID"]}'
                }
                lastresp=requests.request("POST", f"https://minecraft-server-list.com/servers/voter10.php?voteses={mitcheck}", headers=headers, data=payload)
                print(lastresp,lastresp.text)
            else:
                print("Captcha Error")
                
            
            break
        
    else:
        print("Connection Error")
if __name__=="__main__":
    main()