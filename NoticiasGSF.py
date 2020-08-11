import pickle
from selenium import webdriver
import requests
mugre = ["xmlns=http://www.w3.org/1999/>", "<\n", "\n>", "<<p>", "<p>", "</p", "xmlns=http://www.w3.org/1999/>",
         "xmlns=http://www.w3.org/1999/>", "<br />", "CDATA", "</div>>", "<div>", "</div>", "%>", "<iframe>",
         "</iframe>", "100%", "<div", "http://w3.org/", "xmlms", "xhtml", ";>", "<", ">", "'", '"', "\/", "]", "["]
j_link_enviado = {}
def limpiar(texto, mugre):
    for m in mugre:
        texto = texto.replace(m, "")
    return texto
def link_enviado(l):
    l = limpiar(l, mugre)
    if not l in j_link_enviado.keys():
        print(" Enviando a telegram :", l)
        j_link_enviado[l] = 1
        return False
    else:
        print(" !!!!!!!!!!!!!!! ENCONTRO DUPLICADO !!!!!!!!!!!!!!!!!! ")
        return True
def save_persist(elem):
    try:
        vpath = "C:/Users/eellena/PycharmProjects/EzequielScraper/persist/"
        varchivo = vpath + elem + ".bin"

        with open(varchivo, "bw") as archivo:
            pickle.dump(eval(elem), archivo)
    except Exception as e:
        print("Except de save_persist", e)
def load_persist(elem):
    try:
        vpath = "C:/Users/eellena/PycharmProjects/EzequielScraper/persist/"
        varchivo = vpath + elem + ".bin"
        with open(varchivo, "br") as archivo:
            # #print(pickle.load(archivo))
            return pickle.load(archivo)
    except Exception as e:
        print("269 - Except load_persit ", e)
def enviar_noticiasGSF(arr,titulo,copete):

    try:
        url_api = "bot1294708386:AAHCE0tRcq-hqT_b14UbHaArxs9q4XCj5fs" + "/sendMessage"
        men_mensaje = "✔ Se publicó la siguiente Noticia: " + "\n"
        men_titulo = "Título: %s" % (titulo) + "\n"
        men_copete = "Copete: %s " %(copete)
        ta = False
        men = []
        for a in arr:
            l = "- " + a + "\n\n"
            men.append(l)
            if a != "" and not (link_enviado(a)):
                ta = True
        if ta:
            requests.post('https://api.telegram.org/' + url_api, data={'chat_id': "-489973892", 'text': men_mensaje + men_titulo + men_copete})
            for m in men:
                requests.post('https://api.telegram.org/' + url_api,
                              data={'chat_id': "-489973892", 'text': m})
                print(requests.status_codes)
    except Exception as e:
        print(" 279 - enviar ", e)



options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(chrome_options=options)
vultimonro = 0
vultimonro = load_persist('vultimonro')
if vultimonro == None:
    vultimonro = 268204
UltimoLinkNoticiaSantafe = "https://www.santafe.gov.ar/noticias/noticia/" + str(vultimonro)
try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    if requests.get(UltimoLinkNoticiaSantafe, headers=headers).status_code != 404:
        driver.get(UltimoLinkNoticiaSantafe)
        titulo = driver.find_element_by_class_name('title-post').text
        copete = driver.find_element_by_class_name('headline-post').text
        vultimonro = vultimonro + 1
        save_persist('vultimonro')
        enviar_noticiasGSF([UltimoLinkNoticiaSantafe], titulo, copete)
    else:
        print("NO HAY NOTICIA NUEVA")
except Exception as e:
    print(e)

