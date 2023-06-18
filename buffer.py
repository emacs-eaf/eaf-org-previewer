#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (C) 2018 Andy Stewart
#
# Author:     Andy Stewart <lazycat.manatee@gmail.com>
# Maintainer: Andy Stewart <lazycat.manatee@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

from core.utils import *
from core.webengine import BrowserBuffer
from PyQt6.QtCore import QUrl


class AppBuffer(BrowserBuffer):
    def __init__(self, buffer_id, url, arguments):
        BrowserBuffer.__init__(self, buffer_id, url, arguments, False)

        self.url = url
        self.load_org_html_file()

    @interactive
    def update_theme(self):
        self.load_org_html_file()
        self.refresh_page()

    def load_org_html_file(self):
        (self.text_selection_color,
         self.dark_mode_theme
         ) = get_emacs_vars(["eaf-org-text-selection-color",
                             "eaf-org-dark-mode"])

        background_color = get_emacs_theme_background()
        foreground_color = get_emacs_theme_foreground()

        self.buffer_widget.init_dark_mode_js(__file__,
                                             self.text_selection_color,
                                             self.dark_mode_theme,
                                             {
                                                 "brightness": 100,
                                                 "constrast": 90,
                                                 "sepia": 10,
                                                 "mode": 0,
                                                 "darkSchemeBackgroundColor": background_color,
                                                 "darkSchemeForegroundColor": foreground_color})

        with open(os.path.splitext(self.url)[0]+".html", "r") as f:
            html = f.read().replace("</style>", "\n  a, p, h1, h2, h3, h4, h5, h6, li { color: " + f'''{foreground_color};''' + "}\n\n" + "  body { background: " + f'''{background_color};''' + "}\n</style>")

            self.buffer_widget.setHtml(html, QUrl("file://"))

    def update_with_data(self, update_data):
        self.load_org_html_file()
        self.refresh_page()
