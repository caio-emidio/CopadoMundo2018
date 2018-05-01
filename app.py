import json
from requests import Session, get
from bs4 import BeautifulSoup
import time


#OK - Ideia eh trazer e por em json as partidas da copa.
#Criar via flask :)
#mandar via Facebook todos os dias as partidas do dia :)
#Criar Bolao (possivelmente outro codigo)

#27/04/2018
#print (time.strftime("%d/%m/%Y"))

#Funcao para tratar mes :)
def tratames(mes):
    if mes == "Jun":
        return "06"
    elif mes == "Jul":
        return "07"

link = "http://www.fifa.com/worldcup/matches/"

url =  get(link)

bsObj = BeautifulSoup(url.text, "html.parser")
blocoGeral = bsObj.find("div", {"class":"fi-matchlist"})
blocoPartidas = blocoGeral.findAll("div", {"class":"fi-mu fixture"})

listaPartida = []
for partida in blocoPartidas:
    dadosHorario = partida.find("div", {"class":"fi-mu__info__datetime"})
    horario = dadosHorario.text.strip()[:-18][-5:]
    hora = horario[:2]
    minuto = horario [-2:]
    horarioCompleto = "{}:{}".format(hora,minuto)

    #horarioLocal
    horaLocal = str(int(hora) - 6)
    horarioLocalCompleto = "{}:{}".format(horaLocal,minuto)

    dia = dadosHorario.text.strip()[:2]
    mes = dadosHorario.text.strip()[3:6]
    mes = tratames(mes)
    ano = dadosHorario.text.strip()[7:11]
    grupo = partida.find("div", {"class":"fi__info__group"})
    estadio = partida.find("div", {"class":"fi__info__stadium"})
    cidade = partida.find("div", {"class":"fi__info__venue"})
    dadosCasa = partida.find("div", {"class":"fi-t fi-i--4 home"})
    timeCasa = dadosCasa.find("span",{"class":"fi-t__nText "})
    timeCasaSigla = dadosCasa.find("span",{"class":"fi-t__nTri"})
    dadosVisitante = partida.find("div", {"class":"fi-t fi-i--4 away"})
    timeVisitante = dadosVisitante.find("span",{"class":"fi-t__nText "})
    timeVisitanteSigla = dadosVisitante.find("span",{"class":"fi-t__nTri"})
    nome = "{} X {}".format(timeCasaSigla.text, timeVisitanteSigla.text)
    partidaJson = {
        "nome": nome,
        "data" : {
                "dia": dia,
                "mes": mes,
                "ano": ano
                },
        "horario": {
                "horarioCompleto" : horarioCompleto,
                "hora": hora,
                "minuto": minuto
                },
        "horarioLocal" : {
                "horarioCompleto" : horarioLocalCompleto,
                "hora": horaLocal,
                "minuto": minuto
        },
        "grupo" : grupo.text,
        "estadio" : estadio.text,
        "cidade" : cidade.text.lower().capitalize(),
        "Time1" : {
                "timeCasa" : timeCasa.text.upper(),
                "timeCasaSigla" : timeCasaSigla.text.upper()
                },
        "Time2" : {
                "timeVisitante" : timeVisitante.text.upper(),
                "timeVisitanteSigla" : timeVisitanteSigla.text.upper()
                }
            }
    listaPartida.append(partidaJson)
listaResp = []
for i in listaPartida:
    listaResp.append(i)
print(listaResp)
