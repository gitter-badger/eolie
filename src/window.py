# Copyright (c) 2014-2016 Cedric Bellegarde <cedric.bellegarde@adishatz.org>
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

from gi.repository import Gtk

from eolie.define import El
from eolie.toolbar import Toolbar


class Window(Gtk.ApplicationWindow):
    """
        Main window
    """

    def __init__(self):
        """
            Init window
        """
        self.__signal1 = None
        self.__signal2 = None
        self.__timeout = None
        self.__was_maximized = False
        Gtk.ApplicationWindow.__init__(self,
                                       application=El(),
                                       title="Eolie")

        self.__setup_content()

############
# Private  #
############
    def __setup_content(self):
        """
            Setup window content
        """
        self.set_default_icon_name('web-browser')
        vgrid = Gtk.Grid()
        vgrid.set_orientation(Gtk.Orientation.VERTICAL)
        vgrid.show()
        self.__toolbar = Toolbar()
        self.__toolbar.show()
        if El().prefers_app_menu():
            self.set_titlebar(self.__toolbar)
            self.__toolbar.set_show_close_button(True)
        else:
            vgrid.add(self.__toolbar)
        self.add(vgrid)
