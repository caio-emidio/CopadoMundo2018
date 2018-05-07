import json
from requests import Session, get
from bs4 import BeautifulSoup
import time

#Incluindo flask
from flask import Flask
from flask import render_template, redirect
app = Flask(__name__)


#Funcao para tratar mes :)
def tratames(mes):
    if mes == "Jun":
        return "06"
    elif mes == "Jul":
        return "07"

def criaJson():
    link = "http://www.fifa.com/worldcup/matches/"

    url =  get(link,proxies = proxyDict)

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
        TimeCasaId = ""
        TimeVisitanteId = ""
        for time in timesJson:
            if time['sigla'] == timeCasaSigla.text:
                TimeCasaId = time["id"]
            elif  time['sigla'] == timeVisitanteSigla.text :
                TimeVisitanteId = time["id"]

        partidaJson = {
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
                        "TimeCasa" : TimeCasaId,
                        "TimeVisitante" : TimeVisitanteId,
                    }
        listaPartida.append(partidaJson)
    return listaPartida


@app.route("/")
def index():
    saida = criaJson()
    saida = str(saida)
    return saida

@app.route("/hoje")
def hoje():
    listaPartida = criaJson()
    dia = time.strftime("%d")
    mes = time.strftime("%m")
    ano = time.strftime("%Y")
    listaSaida = []
    for partida in listaPartida:
        if ((partida["data"]["dia"] == dia) and (partida["data"]["mes"] == mes) and (partida["data"]["ano"] == ano)):
            listaSaida.append(partida)
    return str(listaSaida)


@app.route("/buscasigla/<sigla>")
def buscaSigla(sigla):
    sigla = sigla.upper()
    listaPartida = criaJson()
    listaSaida = []
    for partida in listaPartida:
        if ((partida["Time1"]["timeCasaSigla"] == sigla) or (partida["Time2"]["timeVisitanteSigla"] == sigla)):
            listaSaida.append(partida)
    return str(listaSaida)

@app.route("/buscanome/<nome>")
def buscaNome(nome):
    nome = nome.upper()
    listaPartida = criaJson()
    listaSaida = []
    for partida in listaPartida:
        if ((partida["Time1"]["timeCasa"] == nome) or (partida["Time2"]["timeVisitante"] == nome)):
            listaSaida.append(partida)
    return str(listaSaida)

@app.route("/buscagrupo/<grupo>")
def buscaGrupo(grupo):
    grupo = grupo.upper()
    if(len(grupo) == 1):
        grupo = "Group " + grupo

    listaPartida = criaJson()
    listaSaida = []
    for partida in listaPartida:
        if (partida["grupo"] == grupo):
            listaSaida.append(partida)
    return str(listaSaida)


if __name__ == '__main__':
    app.run(port=8000, debug=True)
