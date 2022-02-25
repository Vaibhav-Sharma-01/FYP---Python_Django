from django.shortcuts import render
import requests
from datetime import datetime, timedelta

Eids = []

# headers = {
#         'x-rapidapi-host': "livescore6.p.rapidapi.com",
#         'x-rapidapi-key': "2f7d4e24b8msh1eca7845910287cp1caff8jsnc9bd026ddb82"
#     }
headers = {
    'x-rapidapi-host': "livescore6.p.rapidapi.com",
    'x-rapidapi-key': "179f92de74msh12ff1e0eeed7f88p15465djsn09f3cb5c5863"
    }

def home(request):
    return render(request, 'home/HomePage.html')

def index(request):
    News = GetLatestCricketNews()
    Image = CricketGallery()
    Eids = GetCricketLiveMatches()
    url = "https://livescore6.p.rapidapi.com/matches/v2/detail"
    datas = []
    Team = []
    data = {}
    for i in Eids:
        querystring = {"Eid": i, "Category": "cricket", "LiveTable": "true"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = response.json()
        Team.append(res['Stg']['Snm'])
        length = len(res['SDInn'])
        for j in res['SDInn']:
            Teams = j['Ti']
            points = j['Pt']
            wickets = j['Wk']
            overs = j['Ov']
            InnNo = j['Inn']
            runrate = j['Rr']
            Extras = j['Ex']

            datas.append({
                "Teampl": Teams,
                "Total": points,
                "Wickets": wickets,
                "overs": overs,
                "runrate": runrate,
                "innings": InnNo,
                'Eid': i
            })
    data.__setitem__(length, datas)

    return render(request, 'home/index.html', {'data': data, 'news': News, 'MatchInfo': Team, 'Images': Image})

def widgets(request):

    # Upcoming Date
    Upcomingdate = UpcomingCricketMatches()

    # Previous Dates
    PastDate = PastCricketMatches()

    # Today's Date
    Today = CricketMatchesToday()

    # List By Date Url
    url = 'https://livescore6.p.rapidapi.com/matches/v2/list-by-date'

    # Find Live Cricket Matches but using list by Date
    LData = []
    Livedata = {}
    querystring = {"Category": "cricket", "Date": Today}
    responses = requests.request("GET", url, headers=headers, params=querystring)
    resu = responses.json()
    for i in resu['Stages']:
        Team = i['Snm']
        NEid = i['Events'][0]['Eid']
        LData.append({
            "Team": Team,
            "Eid": NEid
        })
    length = len(resu)
    Livedata.__setitem__(length, LData)
    # Finding Live matches Ends Here

    # Upcoming Matches
    LData = []
    datadic = {}
    querystring = {"Category":"cricket","Date":Upcomingdate}
    responses = requests.request("GET", url, headers=headers, params=querystring)
    resu = responses.json()
    for i in resu['Stages']:
        Team = i['Snm']
        LData.append({
            "Team": Team
        })
    length = len(resu)
    datadic.__setitem__(length, LData)
    # Upcoming Matches Ends Here

    # Previous Matches
    querystring = {"Category": "cricket", "Date": PastDate}
    responses = requests.request("GET", url, headers=headers, params=querystring)
    LData = []
    datadi = {}
    resu = responses.json()
    for i in resu['Stages']:
        Team = i['Snm']
        LData.append({
            "Team": Team
        })
    length = len(resu)
    datadi.__setitem__(length, LData)
    # Previous Matches Ends Here

    # Date Wise Matches
    Date = request.POST.get('dates', datetime.now().strftime('%Y%m%d'))
    date_time_obj = Date.replace("-","")
    LData = []
    datedata = {}
    querystrings = {"Category": "cricket", "Date": date_time_obj}
    resp = requests.request("GET", url, headers=headers, params=querystrings)
    result = resp.json()
    for i in result['Stages']:
        Team = i['Snm']
        Leagues = i['Cnm']
        LData.append({
            "Team": Team,
            "Leagues": Leagues
        })
    length = len(resu)
    datedata.__setitem__(length, LData)
    # Date Wise Matches Ends Here

    # Storing Eid from Index.html in session
    if(request.POST.get('Eid') != None):
        request.session['Eid'] = request.POST.get('Eid')
    # Storing Ends Here

    # Fetching Eid from Session
    Eid = request.session['Eid']
    # Fetching Ends Here

    # Finding Match Details for users choosed matches from index.html
    LData = []
    data = {}
    urls = "https://livescore6.p.rapidapi.com/matches/v2/detail"
    querystring = {"Eid": Eid, "Category": "cricket", "LiveTable": "true"}
    response = requests.request("GET", urls, headers=headers, params=querystring)
    print(response)
    res = response.json()
    Team = res['Stg']['Snm']
    Status = res['ECo']
    players = res['Prns']
    length = len(res['SDInn'])
    for j in res['SDInn']:
        Inn = j['Ti']
        Batting_info = j['Bat']
        for k in Batting_info:
            if 'B' in k.keys():
                balls = k['B']
            if 'R' in k.keys():
                runs = k['R']
            if '$4' in k.keys():
                four = k['$4']
            if '$6' in k.keys():
                sixes = k['$6']
            if k['LpTx'] == "did not bat" or k['LpTx'] == 'yet to bat':
                runs = 0
                four = 0
                sixes = 0
                extra = k['LpTx']

            for l in players:
                if k['Pid'] == int(l['Pid']):
                    player_name = l['Fn'] + " " + l['Ln']
                if k['Bid'] == int(l['Pid']):
                    bowler_name = l['Fn'] + " " + l['Ln']

            LData.append({
                "Stats": Status,
                "Team": Team,
                "Runs": runs,
                "fours": four,
                "sixes": sixes,
                "player_name": player_name,
                "bowler_name": bowler_name,
                'balls': balls,
                'Innings': Inn,
            })
        data.__setitem__(length, LData)
    # Finding for details of match Ends here

    return render(request, 'home/widgets.html', {'data': data, 'upcoming': datadic, 'past': datadi, "MBD": datedata, "Live": Livedata})

def Main(request):

    # Storing Eid from Index.html in session
    if (request.POST.get('match') != None):
        request.session['NEid'] = request.POST.get('match')
    # Storing Ends Here

    # Fetching Eid from Session
    Eid = request.session['NEid']
    url = "https://livescore6.p.rapidapi.com/matches/v2/detail"
    datas = []
    data = {}
    querystring = {"Eid": Eid, "Category": "cricket", "LiveTable": "true"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()
    Team = res['Stg']['Snm']
    players = res['Prns']
    length = len(res['SDInn'])
    for j in res['SDInn']:
        Inn = j['Ti']
        Batting_info = j['Bat']
        for k in Batting_info:
            if 'B' in k.keys():
                balls = k['B']
            if 'R' in k.keys():
                runs = k['R']
            if '$4' in k.keys():
                four = k['$4']
            if '$6' in k.keys():
                sixes = k['$6']
            if 'Sr' in k.keys():
                SR = k['Sr']
            if k['LpTx'] == "did not bat" or k['LpTx'] == 'yet to bat':
                runs = 0
                four = 0
                sixes = 0
                extra = k['LpTx']

            for l in players:
                if k['Pid'] == int(l['Pid']):
                    player_name = l['Fn'] + " " + l['Ln']
                if k['Bid'] == int(l['Pid']):
                    bowler_name = l['Fn'] + " " + l['Ln']

            datas.append({
                "Team": Team,
                "Runs": runs,
                "fours": four,
                "sixes": sixes,
                "player_name": player_name,
                "bowler_name": bowler_name,
                'balls': balls,
                'Innings': Inn,
                'StrikeRate': SR
            })
    data.__setitem__(length, datas)
    print(data)
    return render(request, 'home/main.html', {'data': data})

def GetCricketLiveMatches():
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"
    querystring = {"Category": "cricket"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()
    Eid = []
    print(res)
    for i in res['Stages']:
        Eid.append(i['Events'][0]['Eid'])
    return Eid

def GetCricketMatchesByDate(Date):
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
    querystring = {"Category": "cricket", "Date": Date}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()
    Eid = []
    for i in res['Stages']:
        Eid.append(i['Events'][0]['Eid'])
    return Eid

def GetLatestCricketNews():
    url = "https://livescore6.p.rapidapi.com/news/v2/list-by-sport"
    querystring = {"category": "2021020913321411486", "page": "1"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()['data']
    news = []
    newss = {}
    for i in data:
        news.append({
            'Title': i['title'],
            'Time': i['published_at'],
            'Body': i['body'][0]['data']['content'].replace("</p>", "").replace("<p>",""),
            'Image': i['image']['data']['urls']['uploaded']['gallery']
        })
    newss.__setitem__("news",news)
    return newss

def CricketGallery():
    url = "https://livescore6.p.rapidapi.com/news/v2/list-by-sport"
    querystring = {"category": "2021020913321411486", "page": "1"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()['data']
    Image = []
    Images = {}
    for i in data:
        Image.append({
            'Image': i['image']['data']['urls']['uploaded']['gallery']
        })
    Images.__setitem__("img", Image)
    print(Images)
    return Images

def UpcomingCricketMatches():
    presentday = datetime.now()
    tomorrow = presentday + timedelta(1)
    return tomorrow.strftime('%Y%m%d')

def PastCricketMatches():
    presentday = datetime.now()
    yesterday = presentday - timedelta(1)
    return yesterday.strftime('%Y%m%d')

def CricketMatchesToday():
    presentday = datetime.now()
    return presentday.strftime('%Y%m%d')