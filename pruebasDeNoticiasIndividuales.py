import datetime
import json

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import requests
import re
from bs4 import BeautifulSoup
def filtroReplace(object):
    object.replace("/", "").replace(":", "").replace("%", "").replace("-", "").replace("[", "").replace("]", "").replace("<","").replace(
        ">", "").replace("!", "").replace(",", "")
    return " ".join(object.split())

j = open("configParaIngresarAlLink.json", "r")
confiTagPage = {}
confiTagPage = json.loads(j.read())["j"]
try:

    for web in confiTagPage:
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

        LogErrores = open("C:/Users/eellena/Desktop/Errores" + urlCortada + "LOG_ERRORES.txt", "w", encoding='utf-8')
        ficComparativo = open("C:/Users/eellena/Desktop/Comparativo" + urlCortada + "LOG.txt", "w", encoding='utf-8')
        ArchivoNoticiasCompletas = open("C:/Users/eellena/Desktop/Noticias" + urlCortada + ".txt", "w", encoding='utf-8')
        items = []
        for i in Noticias:
            try:
                item = eval(confiTagPage[0]["path"])
                if item[:1] == "/":
                    item = item[1:]
                if url in item:
                    items.append(url + item.replace(url, ""))
                else:
                    items.append(item)
                ficComparativo.write(str(url + item.replace(url, "")) + '\n')
            except Exception as e:
                LogErrores.write("Error sobre link noticias:" + e)
        print(items)
        ficComparativo.close()
        for paginas in items:
            link_web = confiTagPage[0]["link"]
            response2 = requests.get(paginas, headers=headers).text
            FechaHoraScrapeo = str(datetime.datetime.now())

            try:
                titulo_noticia = filtroReplace(eval(confiTagPage[0]["tituloNoticia"]))
            except Exception as e:
                print(e)
                LogErrores.write("Error Titulo Noticia:" + e)
                try:
                    titulo_noticia = filtroReplace(eval(confiTagPage[0]["tituloNoticia2"]))
                except Exception as e:
                    print(e)
                    LogErrores.write("Error Titulo Noticia:" + e)
                    titulo_noticia = "No se pudo obtener el titulo de la noticia"
            try:
                DescripcionNoticia = filtroReplace(eval(confiTagPage[0]["descripcionNoticia"]))
            except Exception as e:
                print(e)
                LogErrores.write("Error Descripcion Noticia:" + e)
                try:
                    DescripcionNoticia = filtroReplace(eval(confiTagPage[0]["descripcionNoticia2"]))
                except Exception as e:
                    print(e)
                    LogErrores.write("Error Descripcion Noticia:" + e)
                    DescripcionNoticia = "No se pudo obtener la descripcion o no contiene"


            try:
                eze = BeautifulSoup(response2, "html.parser").find_all("p", {"class":"p1"})
                Nota = eval(confiTagPage[0]["Nota"])
                NotComp = ""
                if type(Nota) != str:
                    for no in Nota:
                        NotComp += no.text
                    Nota = NotComp
            except Exception as e:
                print(e)
                LogErrores.write("Error Nota Noticia:" + e)
                try:
                    Nota = eval(confiTagPage[0]["Nota2"])
                except Exception as e:
                    print(e)
                    LogErrores.write("Error Nota Noticia:" + e)
                    Nota = "No se pudo obtener la nota"


            try:
                fechaPublicacion = filtroReplace(eval(confiTagPage[0]["fechaPublicacion"]))
            except Exception as e:
                print(e)
                LogErrores.write("Error fecha publicacion Noticia:" + e)
                try:
                    fechaPublicacion = filtroReplace(eval(confiTagPage[0]["fechaPublicacion2"]))
                except Exception as e:
                    print(e)
                    LogErrores.write("Error fecha publicacion Noticia:" + e)
                    fechaPublicacion = "No se pudo obtener fecha de publicacion"
            try:
                fechaPublicacionModificacion = filtroReplace(eval(confiTagPage[0]["fechaPublicacionModificada"]))
            except Exception as e:
                print(e)
                LogErrores.write("Error fecha modificacion Noticia:" + e)
                try:
                    fechaPublicacionModificacion = filtroReplace(eval(confiTagPage[0]["fechaPublicacionModificada2"]))
                except Exception as e:
                    print(e)
                    LogErrores.write("Error fecha modificacion Noticia:" + e)
                    fechaPublicacionModificacion = "No se pudo obtener fecha de modificacion o no tiene"

            data = {"Pagina_Web": link_web,
                    "Link_Noticia": paginas,
                    "Fecha_Hora_Scrapeo": FechaHoraScrapeo,
                    "Fecha_Hora_Noticia": fechaPublicacion,
                    "Fecha_Modificacion": fechaPublicacionModificacion,
                    "Titulo_Noticia": titulo_noticia,
                    "Descripcion_Noticia:": DescripcionNoticia,
                    "Texto_Noticia": Nota.replace("\n", "")}
            try:
                stringjsonordenado = json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False)
                print(stringjsonordenado)
                ArchivoNoticiasCompletas.write(stringjsonordenado + '\n')
            except Exception as e:
                LogErrores.write("Error al crear json:" + e)

        ArchivoNoticiasCompletas.close()
except Exception as e:
    print("207 - problema en el for general ", e)
    #print("Titulo: " + titulo_noticia +"\n","Descripcion: "+ DescripcionNoticia+"\n", "Nota: " + Nota+"\n","Fecha Publicacion: "+fechaPublicacion+"\n","Fecha Publicacion Modificada: " +fechaPublicacionModificacion+"\n")