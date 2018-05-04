def GeraGrupo():
    link = "http://www.fifa.com/worldcup/groups/"
    url =  get(link,proxies = proxyDict)
    bsObj = BeautifulSoup(url.text, "html.parser")
    blkTable = bsObj.findAll("table", {"class":"fi-table fi-standings"})
    listaResposta = []
    for tables in blkTable:
        nomeGrupo = tables.find("p", {"class":"fi-table__caption__title"}).text
        tbodys = tables.find("tbody")
        nometimes = tbodys.findAll("span", {"class":"fi-t__nText "})
        siglatimes = tbodys.findAll("span", {"class":"fi-t__nTri"})
        matchplayeds = tbodys.findAll("td", {"class":"fi-table__matchplayed"})
        wins = tbodys.findAll("td", {"class":"fi-table__win"})
        draws = tbodys.findAll("td", {"class":"fi-table__draw"})
        losts = tbodys.findAll("td", {"class":"fi-table__lost"})
        goalfors = tbodys.findAll("td", {"class":"fi-table__goalfor"})
        goalagainsts = tbodys.findAll("td", {"class":"fi-table__goalagainst"})
        diffgoals = tbodys.findAll("td", {"class":"fi-table__diffgoal"})
        ptss = tbodys.findAll("td", {"class":"fi-table__pts"})
        listGroup = []
        for i in range(4):
            print(i, nometimes[i])
            nome = {
                    "timenome" : nometimes[i].text,
                    "timesigla" : siglatimes[i].text,
                    "matchplayed" : matchplayeds[i].text,
                    "win" : wins[i].text,
                    "draw" : draws[i].text,
                    "lost" :losts[i].text,
                    "goalfor": goalfors[i].text,
                    "goalagainst": goalagainsts[i].text,
                    "diffgoal" :diffgoals[i].text,
                    "points": ptss[i].text
                    }
            listGroup.append(nome)
        listaResposta.append({nomeGrupo:listGroup})
    return(listaResposta)
