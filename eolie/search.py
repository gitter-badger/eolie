# Copyright (c) 2017 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gio

from gettext import gettext as _
import json

from eolie.helper_task import TaskHelper
from eolie.define import El, EOLIE_LOCAL_PATH


class Search:
    """
        Eolie search engines
    """

    def __init__(self):
        """
            Init search
        """
        # Gettext does not work outside init
        self.__ENGINES = {
            'Google': [
                # Translators: Google url for your country
                _("https://www.google.com"),
                'https://www.google.com/search?q=%s&ie=utf-8&oe=utf-8',
                'https://www.google.com/complete/search?client=firefox&q=%s',
                'unicode_escape',
                'g'
                ],
            'DuckDuckGo': [
                'https://duckduckgo.com',
                'https://duckduckgo.com/?q=%s',
                'https://ac.duckduckgo.com/ac/?q=%s&type=list',
                'utf-8',
                'd'
                ],
            'Yahoo': [
                # Translators: Yahoo url for your country
                _("https://www.yahoo.com"),
                # Translators: Yahoo url for your country
                _("https://us.search.yahoo.com") + "/search?p=%s&ei=UTF-8",
                'https://ca.search.yahoo.com/sugg/ff?'
                'command=%s&output=fxjson&appid=fd',
                'utf-8',
                'y'
                ],
            'Bing': [
                'https://www.bing.com',
                'https://www.bing.com/search?q=%s',
                'https://www.bing.com/osjson.aspx?query=%s&form=OSDJAS',
                'utf-8',
                'b'
                ]
            }

        self.__uri = ""
        self.__search = ""
        self.__keyword = ""
        self.__encoding = ""
        self.update_default_engine()

    def update_default_engine(self):
        """
            Update default engine based on user settings
        """
        wanted = El().settings.get_value('search-engine').get_string()
        for engine in self.engines:
            if engine == wanted:
                self.__uri = self.engines[engine][0]
                self.__search = self.engines[engine][1]
                self.__keyword = self.engines[engine][2]
                self.__encoding = self.engines[engine][3]
                break

    def get_search_uri(self, words):
        """
            Return search uri for words
            @param words as str
            @return str
        """
        if len(words) > 2 and words[1] == ":":
            for engine in self.engines:
                if words.startswith("%s:" % self.engines[engine][4]):
                    return self.engines[engine][1] % words[2:]
        try:
            return self.__search % words
        except:
            return self.engines["Google"][1] % words

    def search_suggestions(self, value, cancellable, callback):
        """
            Search suggestions for value
            @param value as str
            @param cancellable as Gio.Cancellable
            @param callback as str
        """
        try:
            if not value.strip(" "):
                return
            uri = self.__keyword % value
            task_helper = TaskHelper()
            task_helper.load_uri_content(uri, cancellable,
                                         callback, self.__encoding, value)
        except Exception as e:
            print("Search::search_suggestions():", e)

    def is_search(self, string):
        """
            Return True is string is a search string
            @param string as str
            @return bool
        """
        # String contains space, not an uri
        search = string.find(" ") != -1 or\
            (len(string) > 2 and string[1] == ":")
        if not search:
            # String contains dot, is an uri
            search = string.find(".") == -1 and\
                string.find(":") == -1
        return search

    @property
    def engines(self):
        """
            Get engines
            return {}
        """
        engines = {}
        # Load user engines
        try:
            f = Gio.File.new_for_path(EOLIE_LOCAL_PATH +
                                      "/search_engines.json")
            if f.query_exists():
                (status, contents, tag) = f.load_contents(None)
                engines.update(json.loads(contents.decode("utf-8")))
        except Exception as e:
            print("Search::engines():", e)
        if not engines:
            engines = self.__ENGINES
        return engines

    @property
    def uri(self):
        """
            Search engine uri
            @return str
        """
        return self.__uri

#######################
# PRIVATE             #
#######################
