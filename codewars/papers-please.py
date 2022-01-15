class Entrant:
    def __init__(self, presented_documents, wanted, current_day):
        self.nationality = ""
        self.wanted = False
        self.documents = {}
        self.forgery = False
        self.expired_documents = None
        self.has_passport = False

        self.parse_presented_documents(presented_documents)
        if wanted != None:
            self.check_if_wanted(wanted)

        if self.wanted:
            return

        self.forgery_check()

        if self.forgery != False:
            return

        if "passport" in self.documents.keys():
            self.has_passport = True

        self.check_documents_expiration(current_day)

        self.get_nationality()

    def parse_presented_documents(self, presented_documents):
        for key in presented_documents.keys():
            temp = presented_documents[key].split("\n")
            self.documents[key] = {}
            for i in temp:
                i = i.split(": ")

                if i[0] == "NAME":
                    i[1] = i[1].split(", ")
                    i[1] = i[1][1] + " " + i[1][0]

                self.documents[key][i[0]] = i[1]

    def check_if_wanted(self, wanted):
        for document in self.documents.keys():
            if "NAME" in self.documents[document].keys():
                if self.documents[document]["NAME"] == wanted:
                    self.wanted = True

    def get_nationality(self):
        keys = [a for a in self.documents.keys()]
        for i in ["certificate_of_vaccination", "ID_card"]:
            if i in keys: keys.remove(i)
        if keys != []:
            self.nationality = self.documents[keys[0]]["NATION"]

    def forgery_check(self):
        checked = {}
        result = False

        for document in self.documents.keys():
            for key in self.documents[document].keys():
                if key in checked.keys() and key != "EXP":
                    if self.documents[document][key] != checked[key]:
                        result = "Detainment: "
                        if "ID" in key:
                            result += "ID number"
                        else:
                            result += key.lower().replace("nation", "nationality").replace("dob", "date of birth")

                        result += " mismatch."
                        break
                else:
                    checked[key] = self.documents[document][key]

            if result != False: break

        self.forgery = result

    def check_documents_expiration(self, current_day):
        for document in self.documents.keys():
            if "EXP" in self.documents[document].keys():
                exp = self.documents[document]["EXP"].split(".")

                if type(current_day) != list:
                    current_day = current_day.split(".")
                    current_day = [int(x) for x in current_day]
                exp = [int(x) for x in exp]

                if current_day[0] > exp[0] or current_day[1] > exp[1] and current_day[0] == exp[0] or current_day[2] > \
                        exp[2] and current_day[0] == exp[0] and current_day[1] == exp[1]:
                    self.expired_documents = document
                    break


class Inspector:
    allowed_countries = set()
    vax = {"Arstotzka": set(), "Antegria": set(), "Impor": set(), "Kolechia": set(), "Obristan": set(),
           "Republia": set(), "United Federation": set()}
    required_documents = dict(everyone=set(), foreigners=set(), workers=set(), citizens=set())
    wanted = None
    current_day = "1982.11.22"

    def receive_bulletin(self, bulletin):
        self.wanted = None
        self.update_date()
        updates = bulletin.split("\n")
        for update in updates:
            self.parse_bulletin_line(update)

    def inspect(self, presented_documents):
        entrant = Entrant(presented_documents, self.wanted, self.current_day)

        # Detainment cases
        if entrant.wanted:
            return "Detainment: Entrant is a wanted criminal."

        if entrant.forgery != False:
            return entrant.forgery

        # Deny cases
        document_expired = "Entry denied: replace_me expired."
        invalid_diplomatic_authorization = "Entry denied: invalid diplomatic authorization."
        banned_nation = "Entry denied: citizen of banned nation."
        missing_required_document = "Entry denied: missing required replace_me."

        if entrant.expired_documents != None:
            return document_expired.replace("replace_me", entrant.expired_documents).replace("_", " ")

        if not entrant.has_passport:
            return missing_required_document.replace("replace_me", "passport")

        if entrant.nationality not in self.allowed_countries:
            return banned_nation

        if "diplomatic_authorization" in entrant.documents.keys():
            if not self.diplomat_is_allowed(entrant):
                return invalid_diplomatic_authorization

        missing = self.get_missing_document(entrant)
        if missing != None:
            return missing_required_document.replace("replace_me", missing).replace("_", " ")

        # Everything is correct
        if entrant.nationality == "Arstotzka":
            return "Glory to Arstotzka."
        else:
            return "Cause no trouble."

    def update_date(self):
        day = int(self.current_day[-2:]) + 1
        month = int(self.current_day[-5:-3])

        if day == 31:
            day = 1
            month = str(month + 1)
        else:
            month = str(month)

        if day < 10:
            day = "0" + str(day)
        else:
            day = str(day)

        self.current_day = "1982." + month + "." + day

    def parse_bulletin_line(self, line):
        if "Wanted" in line:
            self.update_wanted(line)
        elif "Allow" in line:
            self.add_countries(line)
        elif "Deny" in line:
            self.pop_countries(line)
        elif "no longer" in line:
            self.pop_vax(line)
        elif "require" in line:
            if "vaccination" in line:
                self.add_vax(line)
            else:
                self.add_document(line)

    def update_wanted(self, wanted):
        self.wanted = wanted.replace("Wanted by the State: ", "")

    def add_countries(self, countries):
        countries = self.parse_countries_line(countries)

        for country in countries:
            self.allowed_countries.add(country)

    def pop_countries(self, countries):
        countries = self.parse_countries_line(countries)

        for country in countries:
            if country in self.allowed_countries:
                self.allowed_countries.remove(country)

    def parse_countries_line(self, countries):
        return countries.replace("Allow", "").replace("Deny", "").replace(" citizens of ", "").split(", ")

    def add_vax(self, line):
        countries, vax = self.parse_vax_line(line)

        for country in countries:
            self.vax[country].add(vax)

    def pop_vax(self, line):
        countries, vax = self.parse_vax_line(line)

        for country in countries:
            self.vax[country].remove(vax)

    def parse_vax_line(self, vax_line):
        vax_line = vax_line.replace("Citizens of ", "").replace(" vaccination", "").replace("no longer ", "").split(
            " require ")
        if vax_line[0] == "Foreigners":
            vax_line[0] = "Antegria, Impor, Kolechia, Obristan, Republia, United Federation"
        elif vax_line[0] == "Entrants":
            vax_line[0] = "Arstotzka, Antegria, Impor, Kolechia, Obristan, Republia, United Federation"
        return vax_line[0].split(", "), vax_line[1]

    def add_document(self, line):
        if "ID card" in line:
            self.required_documents["citizens"].add("ID_card")
        elif "Entrants" in line:
            self.required_documents["everyone"].add(line.split("require ")[1].lower().replace(" ", "_"))
        elif "Foreigners" in line:
            self.required_documents["foreigners"].add(line.split("require ")[1].lower().replace(" ", "_"))
        elif "Workers" in line:
            self.required_documents["workers"].add(line.split("require ")[1].lower().replace(" ", "_"))

    def get_missing_document(self, entrant):
        needed = self.required_documents["everyone"]
        if entrant.nationality == "Arstotzka":
            needed = needed.union(self.required_documents["citizens"])
        else:
            needed = needed.union(self.required_documents["foreigners"])
            if "access_permit" in entrant.documents.keys():
                if entrant.documents["access_permit"]["PURPOSE"] == "WORK":
                    needed = needed.union(self.required_documents["workers"])

        if "grant_of_asylum" not in entrant.documents.keys() and "diplomatic_authorization" not in entrant.documents.keys():
            for document in needed:
                if document not in entrant.documents.keys():
                    return document

        if len(self.vax[entrant.nationality]) > 0:
            if "certificate_of_vaccination" not in entrant.documents.keys():
                return "certificate of vaccination"
            if self.vaccines_missing(entrant):
                return "vaccination"

        return None

    def vaccines_missing(self, entrant):
        needed = self.vax[entrant.nationality]
        entrant_vax = entrant.documents["certificate_of_vaccination"]["VACCINES"].split(", ")

        for n in needed:
            if n not in entrant_vax:
                return True

        return False

    def diplomat_is_allowed(self, entrant):
        return "Arstotzka" in entrant.documents["diplomatic_authorization"]["ACCESS"].split(", ")
