import datetime
import json

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import requests
import re
from bs4 import BeautifulSoup


j = open("config1tag.json", "r")
confiTagPage = {}
confiTagPage = json.loads(j.read())["j"]
url = confiTagPage[0]["link"]
urlCortada = confiTagPage[0]["link"]
urlCortada = urlCortada.replace("http:", "").replace("//", "").replace(".","").replace("www", "").replace("https:", "").replace("/" , "").replace("\n", "")
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
response = requests.get(url, headers=headers).text


Noticias = eval(confiTagPage[0]["BuscarNoticia"])
if confiTagPage[0]["BuscarNoticia2"] != "":
    Noticias2 = eval(confiTagPage[0]["BuscarNoticia2"])
    Noticias.extend(Noticias2)

ficComparativo = open("C:/Users/eellena/Desktop/" + urlCortada + "LOG.txt", "w", encoding='utf-8')
ArchivoNoticiasCompletas = open("C:/Users/eellena/Desktop/" + urlCortada + ".txt", "w", encoding='utf-8')
items = []
for i in Noticias:
    try:
        item = eval(confiTagPage[0]["path"])
        if item[:1] == "/":
            item = item[1:]
        items.append(url + item.replace(url, ""))
        ficComparativo.write(str(url + item.replace(url, "")) + '\n')
    except Exception as e:
        print(e)
print(items)
ficComparativo.close()
for paginas in items:
    link_web = confiTagPage[0]["link"]

    response2 = requests.get(paginas, headers=headers).text

    try:
        eze = json.loads(BeautifulSoup(response2, "html.parser").find("script", {"type": 'application/ld+json'}).string)

    except Exception as e:

        print(e)

    FechaHoraScrapeo = str(datetime.datetime.now())
    try:
        titulo_noticia = eval(confiTagPage[0]["tituloNoticia"])
    except Exception as e:
        print(e)
        try:
            titulo_noticia = eval(confiTagPage[0]["tituloNoticia2"])
        except Exception as e:
            print(e)
            titulo_noticia = "No se pudo obtener el titulo de la noticia"
    try:
        DescripcionNoticia = eval(confiTagPage[0]["descripcionNoticia"])
    except Exception as e:
        print(e)
        try:
            DescripcionNoticia = eval(confiTagPage[0]["descripcionNoticia2"])
        except Exception as e:
            print(e)
            DescripcionNoticia = "No se pudo obtener la descripcion"


    try:
        Nota = eval(confiTagPage[0]["Nota"])
        NotComp = ""
        if type(Nota) != str:
            for no in Nota:
                NotComp += no.text
            Nota = NotComp
    except Exception as e:
        print(e)
        try:
            Nota = eval(confiTagPage[0]["Nota2"])
        except Exception as e:
            print(e)
            Nota = "No se pudo obtener la nota"


    try:
        fechaPublicacion = eval(confiTagPage[0]["fechaPublicacion"])
    except Exception as e:
        print(e)
        try:
            fechaPublicacion = eval(confiTagPage[0]["fechaPublicacion2"])
        except Exception as e:
            print(e)
            fechaPublicacion = "No se pudo obtener fecha de publicacion"
    try:
        fechaPublicacionModificacion = eval(confiTagPage[0]["fechaPublicacionModificada"])
    except Exception as e:
        print(e)
        try:
            fechaPublicacionModificacion = eval(confiTagPage[0]["fechaPublicacionModificada2"])
        except Exception as e:
            print(e)
            fechaPublicacionModificacion = "No se pudo obtener fecha de modificacion o no tiene"

    data = {"Pagina_Web": link_web,
            "Link_Noticia": paginas,
            "Fecha_Hora_Scrapeo": FechaHoraScrapeo,
            "Fecha_Hora_Noticia": fechaPublicacion,
            "Fecha_Modificacion": fechaPublicacionModificacion,
            "Titulo_Noticia": titulo_noticia,
            "Descripcion_Noticia:": DescripcionNoticia,
            "Texto_Noticia": Nota.replace("\n", "")}
    stringjsonordenado = json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False)
    print(stringjsonordenado)
    ArchivoNoticiasCompletas.write(stringjsonordenado + '\n')

ArchivoNoticiasCompletas.close()
#print("Titulo: " + titulo_noticia +"\n","Descripcion: "+ DescripcionNoticia+"\n", "Nota: " + Nota+"\n","Fecha Publicacion: "+fechaPublicacion+"\n","Fecha Publicacion Modificada: " +fechaPublicacionModificacion+"\n")