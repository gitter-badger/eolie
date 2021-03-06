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

from gi.repository import Gtk, Gdk, GLib, Pango

from eolie.label_indicator import LabelIndicator
from eolie.define import El, ArtSize


class SitesManagerChild(Gtk.ListBoxRow):
    """
        Child showing snapshot, title and favicon
    """

    def __init__(self, netloc, window):
        """
            Init child
            @param netloc as str
            @param window as Window
        """
        Gtk.ListBoxRow.__init__(self)
        self.__window = window
        self.__netloc = netloc
        self.__views = []
        self.__connected_ids = []
        self.__scroll_timeout_id = None
        self.set_property("has-tooltip", True)
        self.connect("query-tooltip", self.__on_query_tooltip)
        builder = Gtk.Builder()
        builder.add_from_resource("/org/gnome/Eolie/SitesManagerChild.ui")
        builder.connect_signals(self)
        widget = builder.get_object("widget")
        self.__close_button = builder.get_object("close_button")
        self.__indicator_label = LabelIndicator()
        self.__indicator_label.set_property("halign", Gtk.Align.CENTER)
        self.__indicator_label.show()
        builder.get_object("grid").attach(self.__indicator_label, 1, 0, 1, 1)
        self.__netloc_label = builder.get_object("netloc")
        self.__netloc_label.set_text(self.__netloc)
        self.__image = builder.get_object("image")
        self.__image.set_property("pixel-size", ArtSize.FAVICON)
        self.add(widget)

    def add_view(self, view):
        """
            Add view
            @param view as View
            @param uri as str
        """
        if not self.__views:
            self.__set_initial_artwork(self.__netloc, view.webview.ephemeral)
        if view not in self.__views:
            self.__views.append(view)
        self.update_indicator(view)
        self.update_label()

    def remove_view(self, view):
        """
            Remove view and destroy self if no more view
            @param view as View
        """
        if view in self.__views:
            self.__views.remove(view)
        self.update_indicator(view)
        self.update_label()

    def set_favicon(self, surface):
        """
            Set favicon
            @param surface as cairo.Surface
        """
        self.__image.set_from_surface(surface)

    def set_minimal(self, minimal):
        """
            Make widget minimal
            @param minimal as bool
        """
        if minimal:
            self.__netloc_label.hide()
            self.__close_button.hide()
            self.__image.set_property("halign", Gtk.Align.CENTER)
            self.__image.set_hexpand(True)
        else:
            self.__netloc_label.show()
            self.__close_button.show()
            self.__image.set_hexpand(False)
            self.__image.set_property("halign", Gtk.Align.START)

    def reset(self, netloc):
        """
            Reset widget to new netloc
            @param netloc as str
        """
        if netloc != self.__netloc:
            self.__netloc = netloc
            self.__netloc_label.set_text(self.__netloc)
            self.__set_initial_artwork(self.__netloc)

    def update_label(self):
        """
            Update label: if one view, use title else use netloc
            @param view as View
        """
        if len(self.__views) == 1:
            title = self.__views[0].webview.get_title()
            if title is None:
                self.__netloc_label.set_text(self.__netloc)
            else:
                self.__netloc_label.set_text(title)
        else:
            self.__netloc_label.set_text(self.__netloc)

    def update_indicator(self, view):
        """
            Update indicator (count and color)
            @param view as View
        """
        i = 0
        unread = False
        for view in self.__views:
            if view.webview.access_time == 0:
                unread = True
            i += 1
        if unread:
            self.__indicator_label.show_indicator(True)
        else:
            self.__indicator_label.show_indicator(False)
        # We force value to 1, Eolie is going to add a new view
        if i == 0:
            i = 1
        self.__indicator_label.set_text(str(i))

    @property
    def empty(self):
        """
            True if no view associated
            @return bool
        """
        return len(self.__views) == 0

    @property
    def views(self):
        """
            Get views
            @return [view]
        """
        return self.__views

    @property
    def netloc(self):
        """
            Get netloc
            @return str
        """
        return self.__netloc

#######################
# PROTECTED           #
#######################
    def _on_close_button_clicked(self, button):
        """
            Close site
            @param button as Gtk.Button
        """
        for view in self.__views:
            self.__window.container.pages_manager.try_close_view(view)

    def _on_scroll_event(self, eventbox, event):
        """
            Switch between children
            @param eventbox as Gtk.EventBox
            @param event as Gdk.Event
        """
        if event.direction == Gdk.ScrollDirection.UP:
            self.__window.container.pages_manager.previous()
            self.__window.container.pages_manager.ctrl_released()
        elif event.direction == Gdk.ScrollDirection.DOWN:
            self.__window.container.pages_manager.next()
            self.__window.container.pages_manager.ctrl_released()

    def _on_button_press_event(self, eventbox, event):
        """
            Hide popover or close view
            @param eventbox as Gtk.EventBox
            @param event as Gdk.Event
        """
        if event.button == 2:
            for view in self.__views:
                self.__window.container.pages_manager.try_close_view(view)
            return True
        elif event.button == 3:
            from eolie.menu_sites import SitesMenu
            menu = SitesMenu(self.__views, self.__window)
            popover = Gtk.Popover.new_from_model(eventbox, menu)
            popover.set_position(Gtk.PositionType.RIGHT)
            popover.forall(self.__update_popover_internals)
            popover.show()
            return True

#######################
# PRIVATE             #
#######################
    def __update_popover_internals(self, widget):
        """
            Little hack to manage Gtk.ModelButton text
            @param widget as Gtk.Widget
        """
        if isinstance(widget, Gtk.Label):
            widget.set_ellipsize(Pango.EllipsizeMode.END)
            widget.set_max_width_chars(40)
            widget.set_tooltip_text(widget.get_text())
        elif hasattr(widget, "forall"):
            GLib.idle_add(widget.forall, self.__update_popover_internals)

    def __set_initial_artwork(self, uri, ephemeral=False):
        """
            Set initial artwork on widget
            @param uri as str
            @param ephemeral as bool
        """
        artwork = El().art.get_icon_theme_artwork(
                                                 uri,
                                                 ephemeral)
        if artwork is not None:
            self.__image.set_from_icon_name(artwork,
                                            Gtk.IconSize.INVALID)
        else:
            self.__image.set_from_icon_name("applications-internet",
                                            Gtk.IconSize.INVALID)

    def __on_query_tooltip(self, widget, x, y, keyboard, tooltip):
        """
            Show tooltip if needed
            @param widget as Gtk.Widget
            @param x as int
            @param y as int
            @param keyboard as bool
            @param tooltip as Gtk.Tooltip
        """
        tooltip = "<b>%s</b>" % GLib.markup_escape_text(self.__netloc)
        for view in self.__views:
            title = view.webview.get_title()
            if not title:
                title = view.webview.get_uri()
            tooltip += "\n%s" % GLib.markup_escape_text(title)
        widget.set_tooltip_markup(tooltip)
