class holderClass:

    article = ''
    price = ''
    name = ''

    def __init__(self):
        self.article = ''
        self.price = ''
        self.name = ''

    def __init__(self, content):
        try:
            text = content.find('div', {"class": "skywalker_scheda_codice_produttore"}).text
            text = ''.join(line.strip() for line in text.split("\n"))
            self.article = text.replace(
                "Codice articolo:", "")
            text = content.find('span', {"class": "text-right"}).text
            text = ''.join(line.strip() for line in text.split("\n"))
            self.price = text.replace(",", ".")
            text = content.find('div', {"class": "skywalker_scheda_nome"}).text
            text = ''.join(line.strip() for line in text.split("\n"))
            self.name = text.replace(",", "")

        except:
            pass

