def GeraNomes():
    link = "http://www.fifa.com/worldcup/groups/"
    url =  get(link,proxies = proxyDict)
    bsObj = BeautifulSoup(url.text, "html.parser")
    blkTable = bsObj.findAll("table", {"class":"fi-table fi-standings"})
    id = 1
    listaTimes = []
    for tables in blkTable:
        tbodys = tables.find("tbody")
        nometimes = tbodys.findAll("span", {"class":"fi-t__nText "})
        siglatimes = tbodys.findAll("span", {"class":"fi-t__nTri"})
        linkImgs = tbodys.findAll("div", {"class":"fi-t__i"})

        for i in range(4):
            imgs = linkImgs[i].find("img")
            nome = {
                    "id":id,
                    "nome": nometimes[i].text,
                    "sigla": siglatimes[i].text,
                    "img": imgs['src']
                    }
            id = id + 1
            listaTimes.append(nome)
    return listaTimes
