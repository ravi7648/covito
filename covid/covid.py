import urllib.request, urllib.parse, urllib.error
import json
import ssl

def covidSummary():
    url = 'https://api.covid19api.com/summary'
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print('Retrieving the report...',)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')
    js = json.loads(data)

    try:
        js = json.loads(data)
    except:
        js = None

    if not js :
        print('==== Failure To Retrieve ====')
        print(data)
    else:
        try:
            rep = (js['Global']['NewConfirmed'], js['Global']['TotalConfirmed'], js['Global']['NewDeaths'], js['Global']['TotalDeaths'], js['Global']['NewRecovered'], js['Global']['TotalRecovered'])
            # print(rep)
            return rep
        except:
            print("Sorry! some error occured")
def covidCountry(country):
    print(country)
    url = 'https://api.covid19api.com/summary'
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print('Retrieving the report...',)
    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters')
    js = json.loads(data)

    try:
        js = json.loads(data)
    except:
        js = None

    if not js :
        print('==== Failure To Retrieve ====')
        print(data)
    else:
        try:
            for count in js['Countries']:
                if count['Slug'] == country:
                    rep = (count['NewConfirmed'], count['TotalConfirmed'], count['NewDeaths'], count['TotalDeaths'], count['NewRecovered'], count['TotalRecovered'], count['Date'])
                    return rep
            
        except:
            print("Sorry! some error occured")
