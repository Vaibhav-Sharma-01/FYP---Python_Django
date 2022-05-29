import random

import requests
from django.shortcuts import render
from datetime import datetime, timedelta
from json import dumps
import asyncio
import aiohttp

# headers = {
#     'x-rapidapi-host': "livescore6.p.rapidapi.com",
#     'x-rapidapi-key': "2f7d4e24b8msh1eca7845910287cp1caff8jsnc9bd026ddb82"
# }

# headers = {
#     'x-rapidapi-host': "livescore6.p.rapidapi.com",
#     'x-rapidapi-key': "179f92de74msh12ff1e0eeed7f88p15465djsn09f3cb5c5863"
# }

headers = {
	"X-RapidAPI-Host": "livescore6.p.rapidapi.com",
	"X-RapidAPI-Key": "253e8389f6msh66b34d07e515957p1e944ejsn4d9f6216ded8"
}


def home(request):
    return render(request, 'home/HomePage.html')


async def getTasks(session, querystring):
    url = "https://livescore6.p.rapidapi.com/matches/v2/detail"
    async with session.get(url, headers=headers, params=querystring) as response:
        response = await response.json()
    return response


async def index(request):
    Today = MatchesToday()
    r = await asyncio.gather(GetCricketMatchesByDate(Today), GetLatestCricketNews(), CricketGallery())
    Eids = r[0]
    News = r[1]
    Image = r[2]
    datas = []
    Team = []
    data = {}
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in Eids:
            querystring = {"Eid": i, "Category": "cricket", "LiveTable": "true"}
            task = asyncio.ensure_future(getTasks(session, querystring))
            tasks.append(task)
        res = await asyncio.gather(*tasks)
    for k in range(len(Eids)):
        if ('Stg' in res[k].keys() and 'SDInn' in res[k].keys()):
            Team.append(res[k]['Stg']['Snm'])
            length = len(res[k]['SDInn'])
            for j in res[k]['SDInn']:
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
                    'Eid': Eids[k]
                })
    data.__setitem__(length, datas)

    return render(request, 'home/cricket/index.html', {'data': data, 'news': News, 'MatchInfo': Team, 'Images': Image})


async def matchesToday(querystring):
    # Find Live Cricket Matches but using list by Date
    # Today's Date
    url = 'https://livescore6.p.rapidapi.com/matches/v2/list-by-date'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=querystring) as response:
            resu = await response.json()
    LData = []
    datadi = {}
    for i in resu['Stages']:
        Team = i['Snm']
        LData.append({
            "Team": Team
        })
    length = len(resu)
    datadi.__setitem__(length, LData)
    # Previous Matches Ends Here
    return datadi


async def matchesPast(querystring):
    # Previous Matches
    url = 'https://livescore6.p.rapidapi.com/matches/v2/list-by-date'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=querystring) as response:
            resu = await response.json()
    LData = []
    datadi = {}
    for i in resu['Stages']:
        Team = i['Snm']
        LData.append({
            "Team": Team
        })
    length = len(resu)
    datadi.__setitem__(length, LData)
    # Previous Matches Ends Here
    return datadi


async def matchesFuture(querystring):
    # Upcoming Matches
    url = 'https://livescore6.p.rapidapi.com/matches/v2/list-by-date'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=querystring) as response:
            resu = await response.json()
    LData = []
    datadi = {}
    for i in resu['Stages']:
        Team = i['Snm']
        LData.append({
            "Team": Team
        })
    length = len(resu)
    datadi.__setitem__(length, LData)
    # Previous Matches Ends Here
    return datadi


async def matchesDateWise(date_time_obj):
    # Date Wise Matches
    LData = []
    datedata = {}
    url = 'https://livescore6.p.rapidapi.com/matches/v2/list-by-date'
    querystrings = {"Category": "cricket", "Date": date_time_obj}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=querystrings) as response:
            result = await response.json()
    for i in result['Stages']:
        Team = i['Snm']
        Leagues = i['Cnm']
        LData.append({
            "Team": Team,
            "Leagues": Leagues
        })
    length = len(result)
    datedata.__setitem__(length, LData)
    # Date Wise Matches Ends Here
    return datedata


async def selectedMatchData(Eid):
    LData = []
    data = {}
    urls = "https://livescore6.p.rapidapi.com/matches/v2/detail"
    querystring = {"Eid": Eid, "Category": "cricket", "LiveTable": "true"}
    async with aiohttp.ClientSession() as session:
        async with session.get(urls, headers=headers, params=querystring) as response:
            res = await response.json()
    Team = res['Stg']['Snm']
    Status = res['ECo']
    players = res['Prns']
    length = len(res['SDInn'])
    for j in res['SDInn']:
        bowler_name = []
        player_name = []
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
    return data


async def widgets(request):
    Date = request.POST.get('dates', datetime.now().strftime('%Y%m%d'))
    date_time_obj = Date.replace("-", "")
    if (request.POST.get('Eid') != None):
        request.session['Eid'] = request.POST.get('Eid')
    Eid = request.session['Eid']
    PastDate = PastMatches()
    querystring = {"Category": "cricket", "Date": PastDate}
    r = await asyncio.gather(matchesToday(querystring), matchesPast(querystring), matchesFuture(querystring),
                             matchesDateWise(date_time_obj),
                             selectedMatchData(Eid))
    Livedata = r[0]
    datadi = r[1]
    datadic = r[2]
    datedata = r[3]
    data = r[4]

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
    return render(request, 'home/cricket/main.html', {'data': data})


async def GetCricketLiveMatches():
    async with aiohttp.ClientSession() as session:
        url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"
        querystring = {"Category": "cricket"}
        async with session.get(url, headers=headers, params=querystring) as response:
            response = await response.json()
    data = response['Stages']
    Eid = []
    for i in data:
        Eid.append(i['Events'][0]['Eid'])
    return Eid


async def GetCricketMatchesByDate(Date):
    async with aiohttp.ClientSession() as session:
        url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
        querystring = {"Category": "cricket", "Date": Date}
        async with session.get(url, headers=headers, params=querystring) as response:
            response = await response.json()
    Eid = []
    for i in response['Stages']:
        Eid.append(i['Events'][0]['Eid'])
    return Eid


def getNewsTasks(session):
    tasks = []
    querystring = {"category": "2021020913321411486", "page": "1"}
    url = "https://livescore6.p.rapidapi.com/news/v2/list-by-sport"
    tasks.append(session.get(url, headers=headers, params=querystring))
    return tasks


async def GetLatestCricketNews():
    news = []
    newss = {}
    res = []
    async with aiohttp.ClientSession() as session:
        tasks = getNewsTasks(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            res.append(await response.json())
    data = res[0]['data']
    for i in data:
        try:
            news.append({
                'Title': i['title'],
                'Time': i['published_at'],
                'Body': i['body'][0]['data']['content'].replace("</p>", "").replace("<p>", ""),
                'Image': i['image']['data']['urls']['uploaded']['gallery']
            })
        except Exception:
            news.append({
                'Title': i['title'],
                'Time': i['published_at'],
                'Body': i['body'][0]['data']['content'].replace("</p>", "").replace("<p>", ""),
            })
    newss.__setitem__("news", news)
    return newss


async def CricketGallery():
    Image = []
    Images = {}
    res = []
    async with aiohttp.ClientSession() as session:
        tasks = getNewsTasks(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            res.append(await response.json())
    data = res[0]['data']
    for i in data:
        try:
            Image.append({
                'Image': i['image']['data']['urls']['uploaded']['gallery']
            })
        except Exception:
            pass
    Images.__setitem__("img", Image)
    return Images


async def findex(request):
    PastDate = PastMatches()
    Today = MatchesToday()
    querystring = {"Category": "soccer", "Date": PastDate}
    r = await asyncio.gather(GetSoccerMatchesByDate(PastDate), GetLatestSoccerNews(), SoccerGallery(),
                             matchesPast(querystring))
    # r1 = await asyncio.gather(GetLatestSoccerNews())
    # r2 = await asyncio.gather(SoccerGallery())
    # r3 = await asyncio.gather(matchesPast(querystring))
    Eids = r[0]
    News = r[1]
    Image = r[2]
    datadi = r[3]

    rs = await asyncio.gather(GetSoccerMatchDetailsByLeague("europa-league", "group-a"),
                              GetSoccerMatchesByLeague("europa-league", "group-a"))
    rs1 = await asyncio.gather(GetSoccerMatchDetailsByLeague("europa-league", "group-b"),
                               GetSoccerMatchesByLeague("europa-league", "group-b"))
    leaguesdetails1 = rs[0]
    Eids2 = rs[1]
    leaguesdetails2 = rs1[0]
    Eids3 = rs1[1]
    # Leagues details Starts Here
    Live_Teams = []
    liveteams = {}
    # , soccerStats(Eids4)
    rl = await asyncio.gather(liveTeams(Eids), soccerStats(Eids2), soccerStats(Eids3))
    # rl1 = await asyncio.gather()
    # rl2 = await asyncio.gather()
    liveRes = rl[0]
    statsRes1 = rl[1]
    statsRes2 = rl[2]
    # statsRes3 = rl[3]
    for i in range(len(liveRes)):
        # League Data
        if ('T1' in liveRes[i]):
            Team1 = liveRes[i]['T1'][0]['Nm']
            Team2 = liveRes[i]['T2'][0]['Nm']
            Team1Img = liveRes[i]['T1'][0]['Img']
            Team2Img = liveRes[i]['T2'][0]['Img']
            Live_Teams.append({'T1': Team1, 'T2': Team2, 'T1Img': Team1Img, 'T2Img': Team2Img})
        else:
            pass
    liveteams.__setitem__("live", Live_Teams)
    # Leagues Details Ends Here

    # pointsTable starts here
    pointsTable1 = []
    ptable1 = {}
    count1 = 0
    for i in leaguesdetails1:
        count1 += 1
        pointsTable1.append({
            'Count': count1,
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
    ptable1.__setitem__("pts", pointsTable1)
    # # points table ends here

    # Stats Details Starts Here

    # pointsTable starts here
    pointsTable2 = []
    ptable2 = {}
    for i in leaguesdetails2:
        count1 += 1
        pointsTable2.append({
            'Count': count1,
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
    ptable2.__setitem__("pts", pointsTable2)
    # # points table ends here

    # # pointsTable starts here
    # pointsTable3 = []
    # ptable3 = {}
    # count3 = 0
    # for i in leaguesdetails3:
    #     count3 += 1
    #     pointsTable3.append({
    #         'Count': count3,
    #         'Team': i['Tnm'],
    #         'Wins': i['win'],
    #         'Loose': i['lst'],
    #         'Points': i['pts'],
    #         'Played': i['pld'],
    #         'Draws': i['drw'],
    #         'GoalDiff': i['gd'],
    #         'GoalFor': i['gf'],
    #         'GoalsAgainst': i['ga']
    #     })
    # ptable3.__setitem__("pts", pointsTable3)
    # # # points table ends here

    # Stats Details Starts Here

    Stats1 = []
    statsdata1 = {}

    for k in statsRes1:
        # Stats Data
        if ('Tr1' in k.keys()):
            Stats1.append({
                'Score': k['Tr1'],
                'Team': k['T1'][0]['Nm'],
                'Possession': k['Stat'][0]['Pss'],
                'Offside': k['Stat'][0]['Ofs'],
                'Fouls': k['Stat'][0]['Fls'],
                'Corners': k['Stat'][0]['Cos'],
                'YellowCards': k['Stat'][0]['Ycs'],
                'Score2': k['Tr2'],
                'Team2': k['T2'][0]['Nm'],
                'Possession2': k['Stat'][1]['Pss'],
                'Offside2': k['Stat'][1]['Ofs'],
                'Fouls2': k['Stat'][1]['Fls'],
                'Corners2': k['Stat'][1]['Cos'],
                'YellowCards2': k['Stat'][1]['Ycs']
            })
    statsdata1.__setitem__("stats1", Stats1)

    Stats2 = []
    statsdata2 = {}

    for l in statsRes2:
        # Stats Data
        if ('Tr1' in l.keys()):
            Stats2.append({
                'Score': l['Tr1'],
                'Team': l['T1'][0]['Nm'],
                'Possession': l['Stat'][0]['Pss'],
                'Offside': l['Stat'][0]['Ofs'],
                'Fouls': l['Stat'][0]['Fls'],
                'Corners': l['Stat'][0]['Cos'],
                'YellowCards': l['Stat'][0]['Ycs'],
                'Score2': l['Tr2'],
                'Team2': l['T2'][0]['Nm'],
                'Possession2': l['Stat'][1]['Pss'],
                'Offside2': l['Stat'][1]['Ofs'],
                'Fouls2': l['Stat'][1]['Fls'],
                'Corners2': l['Stat'][1]['Cos'],
                'YellowCards2': l['Stat'][1]['Ycs']
            })
        else:
            pass
    statsdata2.__setitem__("stats2", Stats2)

    # Stats3 = []
    # statsdata3 = {}
    #
    # for k in statsRes3:
    #     # Stats Data
    #     if ('Tr1' in k.keys()):
    #         Stats3.append({
    #             'Score': k['Tr1'],
    #             'Team': k['T1'][0]['Nm'],
    #             'Possession': k['Stat'][0]['Pss'],
    #             'Offside': k['Stat'][0]['Ofs'],
    #             'Fouls': k['Stat'][0]['Fls'],
    #             'Corners': k['Stat'][0]['Cos'],
    #             'YellowCards': k['Stat'][0]['Ycs'],
    #             'Score2': k['Tr2'],
    #             'Team2': k['T2'][0]['Nm'],
    #             'Possession2': k['Stat'][1]['Pss'],
    #             'Offside2': k['Stat'][1]['Ofs'],
    #             'Fouls2': k['Stat'][1]['Fls'],
    #             'Corners2': k['Stat'][1]['Cos'],
    #             'YellowCards2': k['Stat'][1]['Ycs']
    #         })
    # statsdata3.__setitem__("stats", Stats3)
    # # Stats Details Ends Here
    #
    # # Previous Matches
    # # Previous Matches Ends Here

    return render(request, 'home/football/index.html',
                  {'live': liveteams, 'stats1': statsdata1, 'stats2': statsdata2,
                   'pointstable1': ptable1, 'pointstable2': ptable2, 'news': News,
                   'Images': Image,
                   'past': datadi})


# 'pointstable3': ptable3,
#  'stats3': statsdata3,

async def soccerStats(Eids2):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in Eids2:
            querystring = {"Eid": i, "Category": "soccer", "LiveTable": "true"}
            task = asyncio.ensure_future(getTasks(session, querystring))
            tasks.append(task)
        res = await asyncio.gather(*tasks)
    return res


async def liveTeams(Eids):
    res = []
    url = "https://livescore6.p.rapidapi.com/matches/v2/detail"
    async with aiohttp.ClientSession() as session:
        for i in Eids:
            querystring = {"Eid": i, "Category": "soccer", "LiveTable": "true"}
            async with session.get(url, headers=headers, params=querystring) as response:
                res.append(await response.json())
    return res


async def GetSoccerLiveMatches():
    async with aiohttp.ClientSession() as session:
        url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"
        querystring = {"Category": "soccer"}
        async with session.get(url, headers=headers, params=querystring) as response:
            response = await response.json()
    data = response['Stages']
    Eid = []
    for i in data:
        Eid.append(i['Events'][0]['Eid'])
    return Eid


async def GetSoccerMatchesByDate(Date):
    async with aiohttp.ClientSession() as session:
        url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
        querystring = {"Category": "soccer", "Date": Date}
        async with session.get(url, headers=headers, params=querystring) as response:
            response = await response.json()
    Eid = []
    for i in range(len(response['Stages'])):
        if (i < 5):
            Eid.append(response['Stages'][i]['Events'][0]['Eid'])
    return Eid


async def GetSoccerMatchDetailsByLeague(league, grp):
    async with aiohttp.ClientSession() as session:
        url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"
        querystring = {"Category": "soccer", "Ccd": league, "Scd": grp}
        async with session.get(url, headers=headers, params=querystring) as response:
            res = await response.json()
    return res['Stages'][0]['LeagueTable']['L'][0]['Tables'][0]['team']


async def GetSoccerMatchesByLeague(league, grp):
    async with aiohttp.ClientSession() as session:
        url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"
        querystring = {"Category": "soccer", "Ccd": league, "Scd": grp}
        async with session.get(url, headers=headers, params=querystring) as response:
            res = await response.json()
    Eid = []
    for i in res['Stages'][0]['Events']:
        Eid.append(i['Eid'])
    return Eid

    # for i in res['Stages']:
    #     for j in i['Events']:
    #         Eid.append(j['Eid'])


def getNewsTasksoccer(session):
    tasks = []
    querystring = {"category": "2021020913320920836", "page": "1"}
    url = "https://livescore6.p.rapidapi.com/news/v2/list-by-sport"
    tasks.append(session.get(url, headers=headers, params=querystring))
    return tasks


async def GetLatestSoccerNews():
    news = []
    newss = {}
    res = []
    async with aiohttp.ClientSession() as session:
        tasks = getNewsTasksoccer(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            res.append(await response.json())
    data = res[0]['data']
    for i in data:
        try:
            news.append({
                'Title': i['title'],
                'Time': i['published_at'],
                'Body': i['body'][0]['data']['content'].replace("</p>", "").replace("<p>", ""),
                'Image': i['image']['data']['urls']['uploaded']['gallery']
            })
        except Exception:
            news.append({
                'Title': i['title'],
                'Time': i['published_at'],
                'Body': i['body'][0]['data']['content'].replace("</p>", "").replace("<p>", ""),
            })
    newss.__setitem__("news", news)
    return newss


async def SoccerGallery():
    Image = []
    Images = {}
    res = []
    async with aiohttp.ClientSession() as session:
        tasks = getNewsTasksoccer(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            res.append(await response.json())
    data = res[0]['data']
    for i in data:
        try:
            Image.append({
                'Image': i['image']['data']['urls']['uploaded']['gallery']
            })
        except Exception:
            pass
    Images.__setitem__("img", Image)
    return Images


async def basketBallData(Eids):
    res = []
    url = "https://livescore6.p.rapidapi.com/matches/v2/detail"
    async with aiohttp.ClientSession() as session:
        for i in Eids:
            querystring = {"Eid": i, "Category": "basketball", "LiveTable": "true"}
            async with session.get(url, headers=headers, params=querystring) as response:
                res.append(await response.json())
    return res


async def bindex(request):
    PastDate = PastMatches()
    querystring = {"Category": "basketball", "Date": PastDate}
    r = await asyncio.gather(GetBasketballMatchesByLeague('nba'), GetLatestBasketballNews(), BasketballGallery(),
                             matchesPast(querystring))
    Eids = r[0]
    News = r[1]
    Image = r[2]
    datadi = r[3]
    data1 = {}
    datas1 = []
    data2 = {}
    datas2 = []
    NBATeamsdic = {}
    NBATeamsList = []
    NBAStatsdic = {}
    NBAStatsList = []
    count = 0
    res = await basketBallData(Eids)

    for k in range(len(res)):
        Team1 = res[k]['T1'][0]['Nm']
        Team2 = res[k]['T2'][0]['Nm']
        Dates = str(res[k]['Esd'])
        Year = Dates[0:4]
        Month = Dates[4:6]
        Datet = Dates[6:8]
        Date = Datet + "-" + Month + "-" + Year
        League = res[k]['Stg']['Snm']
        count += 1
        Tr1 = res[k]['Tr1']
        Tr2 = res[k]['Tr2']
        if ('Tr1Q1' in res[k].keys()):
            Tr1Q1 = res[k]['Tr1Q1']
        else:
            Tr1Q1 = 0
        if ('Tr1Q2' in res[k].keys()):
            Tr1Q2 = res[k]['Tr1Q2']
        else:
            Tr1Q2 = 0
        if ('Tr1Q3' in res[k].keys()):
            Tr1Q3 = res[k]['Tr1Q3']
        else:
            Tr1Q3 = 0
        if ('Tr1Q4' in res[k].keys()):
            Tr1Q4 = res[k]['Tr1Q4']
        else:
            Tr1Q4 = 0
        if ('Tr2Q1' in res[k].keys()):
            Tr2Q1 = res[k]['Tr2Q1']
        else:
            Tr2Q1 = 0
        if ('Tr2Q2' in res[k].keys()):
            Tr2Q2 = res[k]['Tr2Q2']
        else:
            Tr2Q2 = 0
        if ('Tr2Q3' in res[k].keys()):
            Tr2Q3 = res[k]['Tr2Q3']
        else:
            Tr2Q3 = 0
        if ('Tr2Q4' in res[k].keys()):
            Tr2Q4 = res[k]['Tr2Q4']
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
            'Team1Score': Tr1,
            'Team2Score': Tr2,
            'Team1Name': Team1,
            'Team2Name': Team2,
            'Date': Date,
            'League': League
        })
        NBAStatsdic.__setitem__('Stats', NBAStatsList)

        if ('Lu' in res[k].keys()):
            Team1Details = res[k]['Lu'][0]['Ps']
            Team2Details = res[k]['Lu'][1]['Ps']
            for j in Team1Details:
                PlayerName = j['Snm']
                Status = j['Pon']
                if ('Snu' in j.keys()):
                    PlayerNo = j['Snu']
                else:
                    PlayerNo = "NA"
                datas1.append({
                    "TeamName": Team1,
                    "count": count,
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
                    "TeamName": Team2,
                    "count": count,
                    "PlayerName": PlayerName,
                    "Status": Status,
                    "PlayerNo": PlayerNo
                })
    data1.__setitem__("Team1", datas1)
    data2.__setitem__("Team2", datas2)
    return render(request, 'home/basketball/index.html',
                  {'Stats': NBAStatsdic, 'team1details': data1, 'team2details': data2,
                   'news': News, 'Images': Image, 'past': datadi})


# 'NBATeamDets': NBATeamsdic,

async def GetBasketballLiveMatches():
    async with aiohttp.ClientSession() as session:
        url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"
        querystring = {"Category": "basketball"}
        async with session.get(url, headers=headers, params=querystring) as response:
            response = await response.json()
    data = response['Stages']
    Eid = []
    for i in data:
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


async def GetBasketballMatchDetailsByLeague(league):
    async with aiohttp.ClientSession() as session:
        url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"
        querystring = {"Category": "basketball", "Ccd": league}
        async with session.get(url, headers=headers, params=querystring) as response:
            res = await response.json()
    return res['Stages'][0]['LeagueTable']['L'][0]['Tables'][0]['team']


async def GetBasketballMatchesByLeague(league):
    async with aiohttp.ClientSession() as session:
        url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-league"
        querystring = {"Category": "basketball", "Ccd": league}
        async with session.get(url, headers=headers, params=querystring) as response:
            res = await response.json()
    Eid = []
    for i in res['Stages']:
        Eid.append(i['Events'][0]['Eid'])
    return Eid


def getNewsTaskbasket(session):
    tasks = []
    querystring = {"category": "2021020913321516170", "page": "1"}
    url = "https://livescore6.p.rapidapi.com/news/v2/list-by-sport"
    tasks.append(session.get(url, headers=headers, params=querystring))
    return tasks


async def GetLatestBasketballNews():
    news = []
    newss = {}
    res = []
    async with aiohttp.ClientSession() as session:
        tasks = getNewsTaskbasket(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            res.append(await response.json())
    data = res[0]['data']
    for i in data:
        try:
            news.append({
                'Title': i['title'],
                'Time': i['published_at'],
                'Body': i['body'][0]['data']['content'].replace("</p>", "").replace("<p>", ""),
                'Image': i['image']['data']['urls']['uploaded']['gallery']
            })
        except Exception:
            news.append({
                'Title': i['title'],
                'Time': i['published_at'],
                'Body': i['body'][0]['data']['content'].replace("</p>", "").replace("<p>", ""),
            })
    newss.__setitem__("news", news)
    return newss


async def BasketballGallery():
    Image = []
    Images = {}
    res = []
    async with aiohttp.ClientSession() as session:
        tasks = getNewsTaskbasket(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            res.append(await response.json())
    data = res[0]['data']
    for i in data:
        try:
            Image.append({
                'Image': i['image']['data']['urls']['uploaded']['gallery']
            })
        except Exception:
            pass
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


async def tindex(request):
    PastDate = PastMatches()
    Today = MatchesToday()
    querystring = {"Category": "tennis", "Date": PastDate}
    r = await asyncio.gather(GetTennisMatchesByDate(Today), GetLatestTennisNews(), tennisGallery(),
                             matchesPast(querystring))
    Eids = r[0]
    News = r[1]
    Image = r[2]
    datadi = r[3]

    # Leagues details Starts Here
    Live_Teams = []
    liveteams = {}
    # , soccerStats(Eids4)
    rl = await asyncio.gather(liveTeams1(Eids))
    liveRes = rl[0]
    for i in range(len(liveRes)):
        # League Data

        Team1 = liveRes[i]['T1'][0]['Nm']
        Team2 = liveRes[i]['T2'][0]['Nm']
        CoNm1 = liveRes[i]['T1'][0]['CoNm']
        CoNm2 = liveRes[i]['T2'][0]['CoNm']

        Live_Teams.append({'T1': Team1, 'T2': Team2, 'C1': CoNm1, 'C2': CoNm2})
    liveteams.__setitem__("live", Live_Teams)
    # Leagues Details Ends Here
    Live_Teams1 = []
    liveteams1 = {}
    for i in range(len(liveRes)):
        # League Data
        Com = []
        if ('Com' in liveRes[i]):
            Team1 = liveRes[i]['T1'][0]['Nm']
            Team2 = liveRes[i]['T2'][0]['Nm']
            for k in liveRes[i]['Com']:
                Com.append(k['Txt'])
            Live_Teams1.append({'T1': Team1, 'T2': Team2, 'Com': Com})
    liveteams1.__setitem__("live", Live_Teams1)

    Stats = []
    stats = {}
    for i in range(len(liveRes)):
        # League Data
        if ('Tr1' in liveRes[i]):
            Team1 = liveRes[i]['T1'][0]['Nm']
            Team2 = liveRes[i]['T2'][0]['Nm']
            Score1 = liveRes[i]['Tr1']
            Score2 = liveRes[i]['Tr2']
            set11 = liveRes[i]['Tr1S1']
            set12 = liveRes[i]['Tr2S1']
            set21 = liveRes[i]['Tr1S2']
            set22 = liveRes[i]['Tr2S2']
            if('Tr1S3' in liveRes[i].keys()):
                set31 = liveRes[i]['Tr1S3']
                set32 = liveRes[i]['Tr2S3']
            Stats.append({'T1': Team1, 'T2': Team2, 'Score1': Score1, 'Score2': Score2, 'set11': set11, 'set12': set12,
                          'set21': set21, 'set22': set22, 'set31': set31, 'set32': set32})
    stats.__setitem__("stats", Stats)

    # pointsTable starts here

    # Stats3 = []
    # statsdata3 = {}
    #
    # for k in statsRes3:
    #     # Stats Data
    #     if ('Tr1' in k.keys()):
    #         Stats3.append({
    #             'Score': k['Tr1'],
    #             'Team': k['T1'][0]['Nm'],
    #             'Possession': k['Stat'][0]['Pss'],
    #             'Offside': k['Stat'][0]['Ofs'],
    #             'Fouls': k['Stat'][0]['Fls'],
    #             'Corners': k['Stat'][0]['Cos'],
    #             'YellowCards': k['Stat'][0]['Ycs'],
    #             'Score2': k['Tr2'],
    #             'Team2': k['T2'][0]['Nm'],
    #             'Possession2': k['Stat'][1]['Pss'],
    #             'Offside2': k['Stat'][1]['Ofs'],
    #             'Fouls2': k['Stat'][1]['Fls'],
    #             'Corners2': k['Stat'][1]['Cos'],
    #             'YellowCards2': k['Stat'][1]['Ycs']
    #         })
    # statsdata3.__setitem__("stats", Stats3)
    # # Stats Details Ends Here
    #
    # # Previous Matches
    # # Previous Matches Ends Here

    return render(request, 'home/tennis/index.html',
                  {'live': liveteams, 'news': News, 'Images': Image, 'past': datadi, 'live1': liveteams1, 'stats': stats})


# 'pointstable3': ptable3,
#  'stats3': statsdata3,

async def liveTeams1(Eids):
    res = []
    url = "https://livescore6.p.rapidapi.com/matches/v2/detail"
    async with aiohttp.ClientSession() as session:
        for i in Eids:
            querystring = {"Eid": i, "Category": "tennis", "LiveTable": "true"}
            async with session.get(url, headers=headers, params=querystring) as response:
                res.append(await response.json())
    return res


async def GetTennisLiveMatches():
    async with aiohttp.ClientSession() as session:
        url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"
        querystring = {"Category": "tennis"}
        async with session.get(url, headers=headers, params=querystring) as response:
            response = await response.json()
    data = response['Stages']
    Eid = []
    for i in data:
        Eid.append(i['Events'][0]['Eid'])
    return Eid


async def GetTennisMatchesByDate(Date):
    async with aiohttp.ClientSession() as session:
        url = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
        querystring = {"Category": "tennis", "Date": Date}
        async with session.get(url, headers=headers, params=querystring) as response:
            response = await response.json()
    Eid = []
    for i in response['Stages']:
        Eid.append(i['Events'][0]['Eid'])
    return Eid


def getNewsTaskTennis(session):
    tasks = []
    querystring = {"category": "2021020913321150030", "page": "1"}
    url = "https://livescore6.p.rapidapi.com/news/v2/list-by-sport"
    tasks.append(session.get(url, headers=headers, params=querystring))
    return tasks


async def GetLatestTennisNews():
    news = []
    newss = {}
    res = []
    async with aiohttp.ClientSession() as session:
        tasks = getNewsTaskTennis(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            res.append(await response.json())
    data = res[0]['data']
    for i in data:
        try:
            news.append({
                'Title': i['title'],
                'Time': i['published_at'],
                'Body': i['body'][0]['data']['content'].replace("</p>", "").replace("<p>", ""),
                'Image': i['image']['data']['urls']['uploaded']['gallery']
            })
        except Exception:
            news.append({
                'Title': i['title'],
                'Time': i['published_at'],
                'Body': i['body'][0]['data']['content'].replace("</p>", "").replace("<p>", ""),
            })
    newss.__setitem__("news", news)
    return newss


async def tennisGallery():
    Image = []
    Images = {}
    res = []
    async with aiohttp.ClientSession() as session:
        tasks = getNewsTaskTennis(session)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            res.append(await response.json())
    data = res[0]['data']
    for i in data:
        try:
            Image.append({
                'Image': i['image']['data']['urls']['uploaded']['gallery']
            })
        except Exception:
            pass
    Images.__setitem__("img", Image)
    return Images


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
        count += 1
        percent += 10
        OptionString = ['Option1', 'Option2', 'Option3', 'Option4']
        random.shuffle(OptionString)
        QList.append({
            'percent': percent,
            'index': count,
            'Question': i['question'].replace("&#039;", "'").replace("&quot;", '"').replace("&eacute;", "e").replace(
                "&ouml;", "o"),
            OptionString.pop(): i['correct_answer'].replace("&#039;", "'").replace("&quot;", '"').replace("&eacute;",
                                                                                                          "e").replace(
                "&ouml;", "o"),
            OptionString.pop(): i['incorrect_answers'][0].replace("&#039;", "'").replace("&quot;", '"').replace(
                "&eacute;", "e").replace("&ouml;", "o"),
            OptionString.pop(): i['incorrect_answers'][1].replace("&#039;", "'").replace("&quot;", '"').replace(
                "&eacute;", "e").replace("&ouml;", "o"),
            OptionString.pop(): i['incorrect_answers'][2].replace("&#039;", "'").replace("&quot;", '"').replace(
                "&eacute;", "e").replace("&ouml;", "o")
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


def UpcomingMatches():
    presentday = datetime.now()
    tomorrow = presentday + timedelta(1)
    return tomorrow.strftime('%Y%m%d')


def PastMatches():
    presentday = datetime.now()
    yesterday = presentday - timedelta(1)
    return yesterday.strftime('%Y%m%d')


def MatchesToday():
    presentday = datetime.now()
    return presentday.strftime('%Y%m%d')
