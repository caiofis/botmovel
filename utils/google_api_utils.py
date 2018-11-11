""" Basecode to send static mensages"""

import re
import requests


class GoogleApiUtils:
    api_key = 'AIzaSyA7eksstdIlK9-gJbYjaNXuOrAC37RfxNs'
    route_base_query = 'https://maps.googleapis.com/maps/api/directions/json?'
    url_sh_base_query = 'https://www.googleapis.com/urlshortener/v1/url?'
    maps_base_query = 'https://www.google.com/maps/dir/'

    def __init__(self):
        self.res_json = None
        self.route_options = []
        self.destAddress = ""
        self.origAddress = ""
        self.optionsCounter = 0
        self.currOptionsSize = 0

    @staticmethod
    def convertHTMLtoZapZap(html):
        bolder = re.compile('<(/)*b>')
        text = re.sub(bolder, '*', html)

        remove_html = re.compile('<div[^>]*>(.*)</div>')
        return re.sub(remove_html, "\n_\\1_", text)


    def getShortURL(self):
        if self.res_json is not None:
            first_route = self.res_json["routes"][0]
            first_leg = first_route["legs"][0]
            start_address = first_leg["start_address"]
            end_address = first_leg["end_address"]

            maps_query = (GoogleApiUtils.maps_base_query
                        + start_address + "/" + end_address)

            short_query_param = "longUrl=%s" % maps_query

            print(GoogleApiUtils.url_sh_base_query + short_query_param)

            try:
                res = requests.post(GoogleApiUtils.url_sh_base_query + short_query_param)
            except requests.exceptions.RequestException, e:
                print("Failed querying url shortener: %s", e.message)

            resJson = res.json()

            if "id" in resJson:
                return resJson["id"]
            else:
                return None
        else:
            return None

    def queryRoute(self, origin, destination, mode="transit"):
        query_param = (
            'origin=%s'
            '&destination=%s'
            '&key=%s'
            '&mode=%s'
            '&language=pt-BR')\
            %(origin, destination, GoogleApiUtils.api_key, mode)

        print(GoogleApiUtils.route_base_query + query_param)
        try:
            res = requests.get(GoogleApiUtils.route_base_query + query_param)
        except requests.exceptions.RequestException, e:
            print("Failed querying google maps API: %s", e.message)
            self.res_json = None
            return False

        if res.status_code != requests.codes.ok:
            self.res_json = None
            return False

        self.res_json = res.json()

        if ("status" in self.res_json) and (self.res_json["status"] == "OK"):
            for route in self.res_json["routes"]:
                self.route_options.append(route["legs"][0])
                self.currOptionsSize += 1
            print(self.route_options)
            return True
        else:
            return False

    def getInstructions(self):
        currRoute = self.route_options[self.optionsCounter]

        instructions = []
        GoogleApiUtils.recGetSteps(currRoute, instructions)

        return instructions

    def setNextOption(self):
        self.optionsCounter += 1
        return self.optionsCounter != self.currOptionsSize

    @staticmethod
    def recGetSteps(currRoute, instructions):
        if "steps" in currRoute:
            for step in currRoute["steps"]:
                print(step)
                instruction = GoogleApiUtils\
                    .convertHTMLtoZapZap(step["html_instructions"])
                instructions.append(instruction)

                if "steps" in step:
                    GoogleApiUtils.recGetSteps(step, instructions)


g = GoogleApiUtils()
if g.queryRoute("Nego Veio", "Shopping Bauru"):
    print(g.getInstructions())
    # print(g.getShortURL())
