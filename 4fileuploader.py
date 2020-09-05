import requests,json,os
path = os.getcwd()
extend = os.sep
merge = path + extend
filename = "info.json"

# Servis kontrolleri
bcvc = True
trlink = True
urlturk = True

# banner
def banner():
    ban = """
           █████▒▒█████   █    ██  ██▀███      ██░ ██  ▄▄▄       ▄████▄   ██ ▄█▀▓█████  ██▀███  ▒███████▒
         ▓██   ▒▒██▒  ██▒ ██  ▓██▒▓██ ▒ ██▒   ▓██░ ██▒▒████▄    ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒▒ ▒ ▒ ▄▀░
         ▒████ ░▒██░  ██▒▓██  ▒██░▓██ ░▄█ ▒   ▒██▀▀██░▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒░ ▒ ▄▀▒░ 
         ░▓█▒  ░▒██   ██░▓▓█  ░██░▒██▀▀█▄     ░▓█ ░██ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄    ▄▀▒   ░
         ░▒█░   ░ ████▓▒░▒▒█████▓ ░██▓ ▒██▒   ░▓█▒░██▓ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒▒███████▒
          ▒ ░   ░ ▒░▒░▒░ ░▒▓▒ ▒ ▒ ░ ▒▓ ░▒▓░    ▒ ░░▒░▒ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░░▒▒ ▓░▒░▒
          ░       ░ ▒ ▒░ ░░▒░ ░ ░   ░▒ ░ ▒░    ▒ ░▒░ ░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░░░▒ ▒ ░ ▒
          ░ ░   ░ ░ ░ ▒   ░░░ ░ ░   ░░   ░     ░  ░░ ░  ░   ▒   ░        ░ ░░ ░    ░     ░░   ░ ░ ░ ░ ░ ░
                    ░ ░     ░        ░         ░  ░  ░      ░  ░░ ░      ░  ░      ░  ░   ░       ░ ░    
                                                                ░                               ░        
                                                                             
                                @@@   @@@       @@@@@@@   @@@@@@   @@@@@@@   
                               @@@@   @@@       @@@@@@@@  @@@@@@@  @@@@@@@@  
                              @@!@!   @@!       @@!  @@@      @@@  @@!  @@@  
                             !@!!@!   !@!       !@!  @!@      @!@  !@!  @!@  
                            @!! @!!   @!!       @!@@!@!   @!@!!@   @!@!!@!   
                           !!!  !@!   !!!       !!@!!!    !!@!@!   !!@!@!    
                           :!!:!:!!:  !!:       !!:           !!:  !!: :!!   
                           !:::!!:::   :!:      :!:           :!:  :!:  !:!  
                                :::    :: ::::   ::       :: ::::  ::   :::  
                                :::   : :: : :   :         : : :    :   : :  
    """
    return ban
# info.json kontrolü
print(banner())
try:
    with open(filename, "r", encoding="utf-8") as bilgiler:
       info = bilgiler.read()
except:
    pass

def writeInfo(username, password, token, group_guid):
    newu = '"'+username+'"'
    newp = '"'+password+'"'
    newt = '"'+token+'"'
    newg = '"'+group_guid+'"'
    icerik = """
{
  "username": """+newu+""",
  "password": """+newp+""",
  "token": """+newt+""",
  "group_guid": """+newg+"""
}
"""
    with open(filename, "w", encoding="utf-8") as file1:
        file1.write(icerik)
        
def getToken(username, password):
    response_token = requests.post("https://api-ssl.bitly.com/oauth/access_token", auth=(username, password))
    if(response_token.status_code == 200):
        ttoken = response_token.content.decode()
        print("[+] Token: "+ttoken)
    else:
        print(f"[!] Token alınamadı ! Detaylar:\nStatus Code: {response_token.status_code}\nResponse: {response_token.text}")
    try:
        return ttoken
    except:
        return False
    
def getGuid(token):
    headers = {"Authorization": f"Bearer {token}"}
    groups_res = requests.get("https://api-ssl.bitly.com/v4/groups", headers=headers)
    if groups_res.status_code == 200:
        groups_data = groups_res.json()['groups'][0]
        guid = groups_data['guid']
        print("[+] Group Guid: "+guid)
    else:
        print(f"[!] Group Guid alınamadı ! Detaylar:\nStatus Code: {groups_res.status_code}\nResponse: {groups_res.text}")
    try:
        return guid
    except:
        return False
    
def checkInfoFile(file):
    global bitlytoken,bitlyguid

    if os.path.exists(merge+file):
        print(f"[+] {file} bulundu !")
        bitly = json.loads(info)
        bitlytoken = bitly["token"]
        bitlyguid = bitly["group_guid"]
    else:
        print(f"[!] {file} bulunamadı !")
        user = input("Bit.ly kullanıcı adı: ")
        pwd = input("Bit.ly parola: ")
        token = getToken(username=user,password=pwd)
        guid = getGuid(token=token)
        writeInfo(username=user,password=pwd,token=token,group_guid=guid)
        with open(filename, "r", encoding="utf-8") as bilgiler:
            info1 = bilgiler.read()
        bitlyverileri = json.loads(info1)
        bitlytoken = bitlyverileri["token"]
        bitlyguid = bitlyverileri["group_guid"]
        
checkInfoFile(file=filename)
dosya = input("Dosya: ")
files = {
    'file': (str(dosya), open(str(dosya), 'r',encoding="utf-8")),
}
headers = {"Authorization": f"Bearer {bitlytoken}"}
print(f"{dosya} dosyası upload ediliyor...")

# Dosyayı uplaod etme

response = requests.post('https://api.anonfiles.com/upload', files=files)

# Gelen değeri JSON a dönüştürüp ayıklama işlemi

veriler = json.loads(response.text)
status = veriler["status"]
filename = veriler["data"]["file"]["metadata"]["name"]
full = veriler["data"]["file"]["url"]["full"]
short = veriler["data"]["file"]["url"]["short"]
size = veriler["data"]["file"]["metadata"]["size"]["bytes"]

# other.json daki verileri işleme
try:
    with open("other.json", "r", encoding="utf-8") as other:
        icerik = other.read()
    otherjson = json.loads(icerik)
except FileNotFoundError:
    print("[!] other.json bulunamadı !")

try:
    bcvcapi = otherjson["bcvc"]
    bcvcuid = otherjson["bcvcuid"]
except:
    print("[!] Bc.vc API bulunamadı !")
    bcvc = False
try:
    trlinkapi = otherjson["trlink"]
except:
    print("[!] Tr.link API bulunamadı !")
    trlink = False
try:
    urlturkapi = otherjson["urlturk"]
except:
    print("[!] Urlturk API bulunamadı !")
    urlturk = False
# Kısaltılabilir linkler

if bcvc == True:
    bcvcshortablelink = f"https://bc.vc/api.php?key={bcvcapi}&uid={bcvcuid}&url=" + short
else:
    pass
if trlink == True:
    trlinkshortablelink = f"https://ay.link/api/?api={trlinkapi}&url={short}&ct=1"
else:
    pass
if urlturk == True:
    urlturkshortablelink = f" https://urlturk.com/api?api={urlturkapi}&url={short}"
pass

# bc.vc kısaltma isteği

if bcvc == True:
    r = requests.get(url=bcvcshortablelink)
else:
    pass

# tr.link kısaltma isteği ve verileri ayıklama

if trlink == True:
    trlinkresponse = requests.get(url=trlinkshortablelink)
    trlink1 = json.loads(trlinkresponse.text)
else:
    pass

# bitly

bitlyshortablelink = requests.post("https://api-ssl.bitly.com/v4/shorten", json={"group_guid": bitlyguid, "long_url": short}, headers=headers)
bitlylink = bitlyshortablelink.json().get("link")

# urlturk

if urlturk == True:
    urlturk_res = requests.get(url=urlturkshortablelink)
else:
    pass

# Sonucu ekrana bastırma

if str(status).lower() != "true":
    print("Upload başarısız!")
    print(f"Detaylar:\n{veriler}")
else:
    print("Upload başarılı!")
    print(f"{status}")
    print(f"Dosya adı: {filename}")
    print(f"Full link: {full}")
    print(f"Kısaltılmış link: {short}")
    print(f"Dosya boyutu {size} bytes")
    print("*******************************************")
    if bcvc == True:
        print(f"Bc.vc kısaltılmış link: {r.text}")
    else:
        print("Bc.vc seçilmedi !")
        
    print(f"Bit.ly kısaltılmış link: {bitlylink}")
    
    if urlturk == True:
        if str(urlturk_res.json()["status"]).lower() == "success":
            urll = urlturk_res.json().get("shortenedUrl")
            print("Urlturk kısaltılmış link: " + str(urll).replace('\\', ''))
        else:
            print("Urlturk link kısaltılamadı ! Detaylar:\n" + urlturk_res.json()["status"] + " " + urlturk_res.json()[
                "message"])
    else:
        print("Urlturk seçilmedi !")
        
    if trlink == True:
        if str(trlink1["status"]).lower() == "success":
            print("Tr.link (ay.link) kısaltılmış link: " + str(trlink1['shortenedUrl']).replace('\\', ''))
        else:
            print("Tr.link (ay.link) link kısaltılamadı ! Detaylar:\n" + trlink1["status"] + " " + trlink1["message"])
    else:
        print("Trlink seçilmedi !")
