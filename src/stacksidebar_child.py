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

from gi.repository import Gtk, GObject, Pango

import cairo

from eolie.define import El, ArtSize
from eolie.stack_child import StackChild


class StackSidebarChild(Gtk.ListBoxRow, StackChild):
    """
        A Sidebar Child
    """

    __gsignals__ = {
        'moved': (GObject.SignalFlags.RUN_FIRST, None, (str, bool))
    }

    def __init__(self, view, window):
        """
            Init child
            @param view as View
            @param window as Window
        """
        Gtk.ListBoxRow.__init__(self)
        StackChild.__init__(self, view, window)

    def show_title(self, b):
        """
            Show page title
            @param b as bool
        """
        if b:
            self._title.show()
            self._image_close.set_hexpand(False)
        else:
            self._title.hide()
            self._image_close.set_hexpand(True)

    def set_preview_height(self, height):
        """
            Set child preview height
            @param height as int
        """
        if height is None:
            ctx = self._title.get_pango_context()
            layout = Pango.Layout.new(ctx)
            height = int(layout.get_pixel_size()[1]) + 10
            self._grid.set_property("valign", Gtk.Align.CENTER)
        else:
            self._grid.set_property("valign", Gtk.Align.END)
        self._overlay.set_size_request(-1, height)

#######################
# PROTECTED           #
#######################
    def _on_snapshot(self, view, result, uri, save):
        """
            Set snapshot on main image
            @param view as WebView
            @param result as Gio.AsyncResult
            @param uri as str
            @param save as bool
            @warning view here is WebKit2.WebView, not WebView
        """
        current_uri = view.get_uri()
        if current_uri is None or current_uri != uri:
            return
        # Do not cache snapshot on error
        if self._view.webview.error is not None:
            save = False
        try:
            snapshot = view.get_snapshot_finish(result)

            if self._window.container.pages_manager.panel_mode == 0:
                # Set sidebar child image
                factor = self.get_allocated_width() /\
                    snapshot.get_width()
                surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                             self.get_allocated_width() -
                                             ArtSize.PREVIEW_WIDTH_MARGIN,
                                             ArtSize.PREVIEW_HEIGHT)
                context = cairo.Context(surface)
                context.scale(factor, factor)
                context.set_source_surface(snapshot, 0, 0)
                context.paint()
                self._image.set_from_surface(surface)
                del surface

            # Save start image to cache
            # We also cache original URI
            uris = [current_uri]
            if view.related_uri is not None and\
                    view.related_uri not in uris:
                uris.append(view.related_uri)
            view.reset_related_uri()
            # Set start image scale factor
            factor = ArtSize.START_WIDTH / snapshot.get_width()
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                         ArtSize.START_WIDTH,
                                         ArtSize.START_HEIGHT)
            context = cairo.Context(surface)
            context.scale(factor, factor)
            context.set_source_surface(snapshot, 0, 0)
            context.paint()
            for uri in uris:
                if not El().art.exists(uri, "start") and save:
                    El().art.save_artwork(uri, surface, "start")
            del surface
            del snapshot
        except Exception as e:
            print("StackSidebarChild::__on_snapshot():", e)
