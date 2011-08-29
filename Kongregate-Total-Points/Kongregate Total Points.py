from urllib import urlopen

url = "http://www.kongregate.com/accounts/"+raw_input("Username: ")+"/rewards"
available = True

#points
bdg = 0
botd = 0
gRate = 0
aRate = 0
ref = 0
other = 0

def getText(text, firstExp, lastExp):
    x1 = text.find(firstExp)+len(firstExp)
    # Check if firstExp does exist 
    if(x1<len(firstExp)):
        return
    
    if(lastExp == None):
        x2 = len(text)
    else:
        x2 = text.find(lastExp,x1)
        
    x = text[x1:x2]
    return x

def getLink(text):

    global available
    
    x = getText(text,'<li class="next"><a href="','" rel=')
    if(x == None):
        available = False
        print('NO LINK FOUND\n')
        return
    
    return x

def countText(text, Exp):
    index = 0
    n = 0
    while True:
        if(text.find(Exp, index)>0):
            index = text.find(Exp, index)+len(Exp)
            n += 1
        else:
            return n

def getEventsNumber(text):
    x = countText(text,"<tr")-3
    return x

def getBody(text):
    x = getText(text, '<table class="rewards"', '</table>')
    x = getText(x, '<tbody>','</tbody>')
    return x
    
def parseData(text):
    body = getBody(text)
    events = getEventsNumber(text)
    for i in range(events):
        e = getText(body,"<tr","</tr>")
        date = getText(e, "<td>","<td>")
        points = getText(e, date+"<td>", "</td>")
        if(points != ''):
            getReason(e, points)
            
        body = getText(body, e, None)

def getReason(text, points):

    global bdg
    global botd
    global gRate
    global aRate
    global ref
    global other

    points = int(points)
    
    if("Completed achievement" in text):
        bdg += points
    elif("Acquired badge of the day" in text):
        botd += points
    elif("Rated game" in text):
        gRate += points
    elif("Rated artwork" in text):
        aRate += points
    elif("Friend signed up" in text or "Referral bonus" in text):
        ref += points
    else:
        other += points
        
while True:
    raw_page = urlopen(url).read()
    parseData(raw_page)
    print("\n")
    p = getLink(raw_page)
    if(p == None):
        print("Badges: "+str(bdg)+"\nBadge of the day: "+str(botd)+"\nGames rated: "+str(gRate)+"\tArt rated: "+str(aRate)+"\nReferrals: "+str(ref)+"\nOther: "+str(other)+"\nTotal: "+str(bdg+botd+gRate+aRate+ref+other))
        break
    
    url = "http://www.kongregate.com"+p
    print(url)
    
