import random
from django.shortcuts import render
import requests
from datetime import datetime, timedelta
from json import dumps

Eids = []

headers = {
    'x-rapidapi-host': "livescore6.p.rapidapi.com",
    'x-rapidapi-key': "2f7d4e24b8msh1eca7845910287cp1caff8jsnc9bd026ddb82"
}


# headers = {
#     'x-rapidapi-host': "livescore6.p.rapidapi.com",
#     'x-rapidapi-key': "179f92de74msh12ff1e0eeed7f88p15465djsn09f3cb5c5863"
#     }

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

    return render(request, 'home/cricket/index.html', {'data': data, 'news': News, 'MatchInfo': Team, 'Images': Image})


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
    querystring = {"Category": "cricket", "Date": Upcomingdate}
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
    date_time_obj = Date.replace("-", "")
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
    if (request.POST.get('Eid') != None):
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

    return render(request, 'home/cricket/widgets.html',
                  {'data': data, 'upcoming': datadic, 'past': datadi, "MBD": datedata, "Live": Livedata})


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
    return render(request, 'home/cricket/main.html', {'data': data})


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
            'Body': i['body'][0]['data']['content'].replace("</p>", "").replace("<p>", ""),
            'Image': i['image']['data']['urls']['uploaded']['gallery']
        })
    newss.__setitem__("news", news)
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


def findex(request):
    Eids = GetSoccerLiveMatches()
    News = GetLatestSoccerNews()
    Image = SoccerGallery()
    url = "https://livescore6.p.rapidapi.com/matches/v2/detail"

    # Leagues details Starts Here

    Live_Teams = []
    liveteams = {}
    for i in Eids:
        querystring = {"Eid": i, "Category": "soccer", "LiveTable": "true"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = response.json()
        # League Data
        Team1 = res['T1'][0]['Nm']
        Team2 = res['T2'][0]['Nm']
        Team1Img = res['T1'][0]['Img']
        Team2Img = res['T2'][0]['Img']
        Live_Teams.append({'T1': Team1, 'T2': Team2, 'T1Img': Team1Img, 'T2Img': Team2Img})
    liveteams.__setitem__("live", Live_Teams)
    leaguesdetails = GetSoccerMatchDetailsByLeague("europa-league", "group-a")

    # Leagues Details Ends Here

    # pointsTable starts here

    pointsTable = []
    ptable = {}
    count = 0
    for i in leaguesdetails:
        count += 1
        pointsTable.append({
            'Count': count,
            'Team': i['Tnm'],
            'Wins': i['win'],
            'Loose': i['lst'],
            'Points': i['pts'],
            'Played': i['pld'],
            'Draws': i['drw'],
            'GoalDiff': i['gd'],
            'GoalFor': i['gf'],
            'GoalsAgainst': i['ga']
        })
    ptable.__setitem__("pts", pointsTable)

    # # points table ends here

    # Stats Details Starts Here
    Eids = GetSoccerMatchesByLeague("europa-league", "group-a")
    url = "https://livescore6.p.rapidapi.com/matches/v2/detail"
    Stats = []
    statsdata = {}
    for i in Eids:
        querystring = {"Eid": i, "Category": "soccer", "LiveTable": "true"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = response.json()
        # Stats Data
        Stats.append({
            'Score': res['Tr1'],
            # 'Team': res['T1']['Nm'],
            'Possession': res['Stat'][0]['Pss'],
            'Offside': res['Stat'][0]['Ofs'],
            'Fouls': res['Stat'][0]['Fls'],
            'Corners': res['Stat'][0]['Cos'],
            'YellowCards': res['Stat'][0]['Ycs'],
            'Score2': res['Tr2'],
            # 'Team2': res['T2']['Nm'],
            'Possession2': res['Stat'][1]['Pss'],
            'Offside2': res['Stat'][1]['Ofs'],
            'Fouls2': res['Stat'][1]['Fls'],
            'Corners2': res['Stat'][1]['Cos'],
            'YellowCards2': res['Stat'][1]['Ycs']
        })
    statsdata.__setitem__("stats", Stats)

    # Stats Details Ends Here

    # Previous Matches
    PastDate = PastSoccerMatches()
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
    querystring = {"Category": "soccer", "Date": PastDate}
    responses = requests.request("GET", url, headers=headers, params=querystring)
    LData = []
    datadi = {}
    resu = responses.json()
    for i in resu['Stages']:
        if ('CompN' in i.keys()):
            Team = i['CompN']
            LData.append({
                "Team": Team
            })
        else:
            Team = i['Snm']
            LData.append({
                "Team": Team
            })
    length = len(resu)
    datadi.__setitem__(length, LData)
    # Previous Matches Ends Here

    return render(request, 'home/football/index.html',
                  {'stats': statsdata, 'pointstable': ptable, 'live': liveteams, 'news': News, 'Images': Image,
                   'past': datadi})


def GetSoccerLiveMatches():
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"
    querystring = {"Category": "soccer"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()
    Eid = []
    for i in res['Stages']:
        Eid.append(i['Events'][0]['Eid'])
    return Eid


def GetSoccerMatchesByDate(Date):
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
    querystring = {"Category": "soccer", "Date": Date}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()
    Eid = []
    for i in res['Stages']:
        Eid.append(i['Events'][0]['Eid'])
    return Eid


def GetSoccerMatchDetailsByLeague(league, grp):
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"

    querystring = {"Category": "soccer", "Ccd": league, "Scd": grp}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()
    return res['Stages'][0]['LeagueTable']['L'][0]['Tables'][0]['team']


def GetSoccerMatchesByLeague(league, grp):
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"

    querystring = {"Category": "soccer", "Ccd": league, "Scd": grp}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()
    Eid = []
    for i in res['Stages']:
        Eid.append(i['Events'][0]['Eid'])
    return Eid

    # for i in res['Stages']:
    #     for j in i['Events']:
    #         Eid.append(j['Eid'])


def GetLatestSoccerNews():
    url = "https://livescore6.p.rapidapi.com/news/v2/list-by-sport"
    querystring = {"category": "2021020913320920836", "page": "1"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()['data']
    news = []
    newss = {}
    for i in data:
        news.append({
            'Title': i['title'],
            'Time': i['published_at'],
            'Body': i['body'][2]['data']['content'].replace("</p>", "").replace("<p>", ""),
            'Image': i['image']['data']['urls']['uploaded']['gallery']
        })
    newss.__setitem__("news", news)
    return newss


def SoccerGallery():
    url = "https://livescore6.p.rapidapi.com/news/v2/list-by-sport"
    querystring = {"category": "2021020913320920836", "page": "1"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()['data']
    Image = []
    Images = {}
    for i in data:
        Image.append({
            'Image': i['image']['data']['urls']['uploaded']['gallery']
        })
    Images.__setitem__("img", Image)
    return Images


def UpcomingSoccerMatches():
    presentday = datetime.now()
    tomorrow = presentday + timedelta(1)
    return tomorrow.strftime('%Y%m%d')


def PastSoccerMatches():
    presentday = datetime.now()
    yesterday = presentday - timedelta(1)
    return yesterday.strftime('%Y%m%d')


def SoccerMatchesToday():
    presentday = datetime.now()
    return presentday.strftime('%Y%m%d')





def bindex(request):
    Eids = GetBasketballMatchesByLeague('nba')
    News = GetLatestBasketballNews()
    Image = BasketballGallery()
    url = "https://livescore6.p.rapidapi.com/matches/v2/detail"
    data1 = {}
    datas1 = []
    data2 = {}
    datas2 = []
    NBATeamsdic = {}
    NBATeamsList = []
    NBAStatsdic = {}
    NBAStatsList = []
    for i in Eids:
        querystring = {"Eid": i, "Category": "basketball", "LiveTable": "true"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        res = response.json()
        Tr1 = res['Tr1']
        Tr2 = res['Tr2']
        if ('Tr1Q1' in res.keys()):
            Tr1Q1 = res['Tr1Q1']
        else:
            Tr1Q1 = 0
        if ('Tr1Q2' in res.keys()):
            Tr1Q2 = res['Tr1Q2']
        else:
            Tr1Q2 = 0
        if ('Tr1Q3' in res.keys()):
            Tr1Q3 = res['Tr1Q3']
        else:
            Tr1Q3 = 0
        if ('Tr1Q4' in res.keys()):
            Tr1Q4 = res['Tr1Q4']
        else:
            Tr1Q4 = 0
        if ('Tr2Q1' in res.keys()):
            Tr2Q1 = res['Tr2Q1']
        else:
            Tr2Q1 = 0
        if ('Tr2Q2' in res.keys()):
            Tr2Q2 = res['Tr2Q2']
        else:
            Tr2Q2 = 0
        if ('Tr2Q3' in res.keys()):
            Tr2Q3 = res['Tr2Q3']
        else:
            Tr2Q3 = 0
        if ('Tr2Q4' in res.keys()):
            Tr2Q4 = res['Tr2Q4']
        else:
            Tr2Q4 = 0

        NBAStatsList.append({
            'T1Q1': Tr1Q1,
            'T1Q2': Tr1Q2,
            'T1Q3': Tr1Q3,
            'T1Q4': Tr1Q4,
            'T2Q1': Tr2Q1,
            'T2Q2': Tr2Q2,
            'T2Q3': Tr2Q3,
            'T2Q4': Tr2Q4,
        })
        NBAStatsdic.__setitem__('Stats', NBAStatsList)
        Team1 = res['T1'][0]['Nm']
        Team2 = res['T2'][0]['Nm']
        Dates = str(res['Esd'])
        Year = Dates[0:4]
        Month = Dates[4:6]
        Datet = Dates[6:8]
        Date = Datet + "-" + Month + "-" + Year
        League = res['Stg']['Snm']
        NBATeamsList.append({
            'Team1Score': Tr1,
            'Team2Score': Tr2,
            'Team1Name': Team1,
            'Team2Name': Team2,
            'Date': Date,
            'League': League
        })
        NBATeamsdic.__setitem__("Listing", NBATeamsList)
        if ('Lu' in res.keys()):
            Team1Details = res['Lu'][0]['Ps']
            Team2Details = res['Lu'][1]['Ps']
            for j in Team1Details:
                PlayerName = j['Snm']
                Status = j['Pon']
                if ('Snu' in j.keys()):
                    PlayerNo = j['Snu']
                else:
                    PlayerNo = "NA"
                datas1.append({
                    "PlayerName": PlayerName,
                    "Status": Status,
                    "PlayerNo": PlayerNo
                })
            for j in Team2Details:
                PlayerName = j['Snm']
                Status = j['Pon']
                if ('Snu' in j.keys()):
                    PlayerNo = j['Snu']
                else:
                    PlayerNo = "NA"
                datas2.append({
                    "PlayerName": PlayerName,
                    "Status": Status,
                    "PlayerNo": PlayerNo
                })

    data1.__setitem__("Team1", datas1)
    data2.__setitem__("Team2", datas2)

    return render(request, 'home/basketball/index.html',
                  {'Stats': NBAStatsdic, 'NBATeamDets': NBATeamsdic, 'team1details': data1, 'team2details': data2,
                   'news': News, 'Images': Image})


def GetBasketballLiveMatches():
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"
    querystring = {"Category": "basketball"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()
    Eid = []
    for i in res['Stages']:
        Eid.append(i['Events'][0]['Eid'])
    return Eid


def GetBasketbllMatchesByDate(Date):
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
    querystring = {"Category": "basketbll", "Date": Date}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()
    Eid = []
    for i in res['Stages']:
        Eid.append(i['Events'][0]['Eid'])
    return Eid


def GetBasketballMatchDetailsByLeague(league):
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"

    querystring = {"Category": "basketball", "Ccd": league}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()
    return res['Stages'][0]['LeagueTable']['L'][0]['Tables'][0]['team']


def GetBasketballMatchesByLeague(league):
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"

    querystring = {"Category": "basketball", "Ccd": league}
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = response.json()
    Eid = []
    for i in res['Stages']:
        Eid.append(i['Events'][0]['Eid'])
    return Eid

    # for i in res['Stages']:
    #     for j in i['Events']:
    #         Eid.append(j['Eid'])


def GetLatestBasketballNews():
    url = "https://livescore6.p.rapidapi.com/news/v2/list-by-sport"
    querystring = {"category": "2021020913321516170", "page": "1"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()['data']
    news = []
    newss = {}
    for i in data:
        news.append({
            'Title': i['title'],
            'Time': i['published_at'],
            'Body': i['body'][2]['data']['content'].replace("</p>", "").replace("<p>", ""),
            'Image': i['image']['data']['urls']['uploaded']['gallery']
        })
    newss.__setitem__("news", news)
    return newss


def BasketballGallery():
    url = "https://livescore6.p.rapidapi.com/news/v2/list-by-sport"
    querystring = {"category": "2021020913321516170", "page": "1"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()['data']
    Image = []
    Images = {}
    for i in data:
        Image.append({
            'Image': i['image']['data']['urls']['uploaded']['gallery']
        })
    Images.__setitem__("img", Image)
    return Images


def UpcomingBasketballMatches():
    presentday = datetime.now()
    tomorrow = presentday + timedelta(1)
    return tomorrow.strftime('%Y%m%d')


def PastBasketballMatches():
    presentday = datetime.now()
    yesterday = presentday - timedelta(1)
    return yesterday.strftime('%Y%m%d')


def triviaindex(request):
    url = "https://opentdb.com/api.php?amount=10&category=21&type=multiple"
    response = requests.request("GET", url)
    res = response.json()
    Set = {}
    QList = []

    CorrectSet = {}
    CQList = []

    count = 0
    percent = 0
    for i in res['results']:
        count+= 1
        percent+= 10
        OptionString = ['Option1', 'Option2', 'Option3', 'Option4']
        random.shuffle(OptionString)
        QList.append({
            'percent': percent,
            'index': count,
            'Question': i['question'].replace("&#039;","'").replace("&quot;",'"').replace("&eacute;","e").replace("&ouml;","o"),
            OptionString.pop(): i['correct_answer'].replace("&#039;","'").replace("&quot;",'"').replace("&eacute;","e").replace("&ouml;","o"),
            OptionString.pop(): i['incorrect_answers'][0].replace("&#039;","'").replace("&quot;",'"').replace("&eacute;","e").replace("&ouml;","o"),
            OptionString.pop(): i['incorrect_answers'][1].replace("&#039;","'").replace("&quot;",'"').replace("&eacute;","e").replace("&ouml;","o"),
            OptionString.pop(): i['incorrect_answers'][2].replace("&#039;","'").replace("&quot;",'"').replace("&eacute;","e").replace("&ouml;","o")
        })
        CQList.append({
            'Correct': i['correct_answer'],
        })
    Set.__setitem__("ques", QList)
    CorrectSet.__setitem__('question', CQList)
    dataJSON = dumps(CorrectSet)
    return render(request, 'home/games/trivia.html', {'questions': Set, 'Ans': dataJSON})

def bball(request):
    return render(request, 'home/games/index.html')

def chess(request):
    return render(request, 'home/games/chess.html')
