"""
  Copyright (c) 2018 Dane Henson (http://brainofdane.com)

  This file is part of Bible.

  Bible is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  Bible is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with Bible.  If not, see <http://www.gnu.org/licenses/>.

  Authored by: Dane Henson <thegreatdane@gmail.com>
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, WebKit2
from gettext import gettext as _

class PassageView(Gtk.Grid):

    def __init__(self, library):
        Gtk.Grid.__init__(self,
                          expand=True)

        library

        stylesheet = """
            :root {
                font-family: 'Open Sans', 'sans-serif';
                color: #333;
                font-size: 100%;
            }
            .main {
                min-width: 32rem;
                max-width: 100rem;
                word-wrap: break-word;
                line-height: 1.5rem;
                margin: 0 auto 4rem auto;
                padding: 0 1rem 0 1rem;
                columns: 3 28rem;
            }
            span.verse-num {
                color: #999;
                font-size: .75rem;
                font-weight: bold;
                padding-right: .15rem;
                padding-left: .25rem;
                vertical-align: text-top;
            }
            h1 { font-size: 2rem }
            h2 {
                font-size: 1.5rem;
                column-span: all;
            }
            h3 {
                font-size: 1.125rem;
                font-weight: lighter;
            }
            h4 { font-size: 1rem }
            h5 { font-size: .875rem }
            h6 { font-size: .75rem }
            .mx-auto { margin-left: auto; margin-right: auto; }
            .divineName { font-variant: small-caps; }
            .wordsOfJesus { color: #7a0000 }
            .indent1 { margin-left: .5rem }
            .indent2 { margin-left: 1rem }
            .indent3 { margin-left: 2rem }
            .indent4 { margin-left: 4rem }
        """
        user_style = WebKit2.UserStyleSheet(stylesheet,
            WebKit2.UserContentInjectedFrames.ALL_FRAMES,
            WebKit2.UserStyleLevel.USER,
            None,
            None)

        content_manager = WebKit2.UserContentManager()
        content_manager.add_style_sheet(user_style)
        self.webview = WebKit2.WebView.new_with_user_content_manager(content_manager)
        self.webview.props.expand = True

        self.webview.connect('context-menu', self._on_context_menu)

        self.add(self.webview)
        library.connect('reference-changed', self._on_library_changed)
        library.connect('module-changed', self._on_library_changed)
        self.show_all()

    def load_html(self, html):
        self.webview.load_html(html)

    def _on_library_changed(self, library):
        self.webview.load_html(library.render_chapter())

    def _on_context_menu(self, web_view, context_menu, event, hit_test_result):
        items = context_menu.get_items()
        for item in items:
            action = item.get_stock_action()
            if (action == WebKit2.ContextMenuAction.RELOAD)\
            or (action == WebKit2.ContextMenuAction.GO_BACK)\
            or (action == WebKit2.ContextMenuAction.GO_FORWARD)\
            or (action == WebKit2.ContextMenuAction.STOP):
                context_menu.remove(item)