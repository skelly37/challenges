class Document:
    type = ""
    nation = ""
    name = ""
    expiriation_date = "2004.10.20"

    def has_expired(self, current_date):
        current_day_split = [int(x) for x in current_date.split(".")]
        expiriation_date_split = [int(x) for x in self.expiriation_date.split(".")]

        if current_day_split[0] > expiriation_date_split[0]: return True
        elif current_day_split[1] > expiriation_date_split[1]: return True
        elif current_day_split[2] > expiriation_date_split[2]: return True

        return False

class Entrant:
    nationality = ""
    name = ""
    wanted = False
    documents = {}
    diplomat = False
    worker = False

    def __init__(self, presented_documents):
        for key in presented_documents.keys():
            self.documents[key] = presented_documents[key]

        print(self.documents)

    def get_status(self):
        if wanted: return "wanted"
        elif diplomat: return "diplomat"
        elif worker: return "worker"
        elif nationality == "Arstotzka": return "citizen"
        else: return "foreigner"


class Inspector:
    allowed_countries = set()
    vax = {}
    required_documents = dict(everyone=[], foreigners=[], workers=[], citizens=[])
    wanted = None
    current_day = "1982.11.22"

    whitelist = False

    def receive_bulletin(self, bulletin):
        self.update_date()
        updates = bulletin.split("\n")
        for update in updates:
            self.parse_bulletin_line(update)

        print(self.wanted)
        print(self.allowed_countries)

    def inspect(self, presented_documents):
        entrant = Entrant(presented_documents)

    def update_date(self):
        day = int(self.current_day[-2:]) + 1
        month = int(self.current_day[-5:-3])

        if day == 31:
            day = 1
            month = str(month+1)
        else:
            month = str(month)

        if day < 10:
            day = "0" + str(day)
        else:
            day = str(day)

        self.current_day = "1982." + month + "." + day


    def parse_bulletin_line(self, line):
        if "Wanted" in line:
            self.update_wanted(wanted)
        elif "Allow" in line:
            self.add_countries(line)
        elif "Deny" in line:
            self.pop_countries(line)
        elif "no longer" in line:
            if "vaccination" in line:
                self.pop_vax(line)
            else:
                self.pop_document(line)
        elif "require" in line:
            if "vaccination" in line:
                self.add_vax(line)
            else:
                self.add_document(line)
        else:
            print("Unhandled line: " + line)

    def update_wanted(self, wanted):
        self.wanted = wanted.replace("Wanted by the State: ", "")

    def add_countries(self, countries):
        countries = self.parse_countries_line(countries)

        for country in countries:
            self.allowed_countries.add(country)

    def pop_countries(self, countries):
        countries = self.parse_countries_line(countries)

        for country in countries:
            self.allowed_countries.pop(country)

    def parse_countries_line(self, countries):
        return countries.replace("Allow", "").replace("Deny", "").replace(" citizens of ", "").split(", ")

    def pop_vax(self, line):


inspector = Inspector()

bulletin = """Entrants require passport
Allow citizens of Arstotzka, Obristan"""




inspector.receive_bulletin(bulletin)

josef = {
        "passport": 'ID#: GC07D-FU8AR\nNATION: Arstotzka\nNAME: Costanza, Josef\nDOB: 1933.11.28\nSEX: M\nISS: East Grestin\nEXP: 1983.03.15'
}
guyovich = {
        "access_permit": 'NAME: Guyovich, Russian\nNATION: Obristan\nID#: TE8M1-V3N7R\nPURPOSE: TRANSIT\nDURATION: 14 DAYS\nHEIGHT: 159cm\nWEIGHT: 60kg\nEXP: 1983.07.13'
}
roman = {
        "passport": 'ID#: WK9XA-LKM0Q\nNATION: United Federation\nNAME: Dolanski, Roman\nDOB: 1933.01.01\nSEX: M\nISS: Shingleton\nEXP: 1983.05.12',
        "grant_of_asylum": 'NAME: Dolanski, Roman\nNATION: United Federation\nID#: Y3MNC-TPWQ2\nDOB: 1933.01.01\nHEIGHT: 176cm\nWEIGHT: 71kg\nEXP: 1983.09.20'
}


doc = Document()

inspector.inspect(josef)
inspector.inspect(guyovich)
inspector.inspect(roman)
