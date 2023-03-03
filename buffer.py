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

from PyQt6.QtCore import QUrl
from core.webengine import BrowserBuffer
from core.utils import get_app_dark_mode, get_emacs_theme_foreground, get_emacs_theme_background, interactive
import os

class AppBuffer(BrowserBuffer):
    def __init__(self, buffer_id, url, arguments):
        BrowserBuffer.__init__(self, buffer_id, url, arguments, False)

        self.url = url

        self.dark_mode = get_app_dark_mode("eaf-org-dark-mode")

        self.buffer_widget.init_dark_mode_js(__file__)

        self.load_org_html_file()

    @interactive
    def update_theme(self):
        self.dark_mode = get_app_dark_mode("eaf-org-dark-mode")
        self.theme_foreground_color = get_emacs_theme_foreground()
        self.theme_background_color = get_emacs_theme_background()
        self.buffer_widget.eval_js("document.body.style.background = '{}'; document.body.style.color = '{}'".format(
            self.theme_background_color, self.theme_foreground_color))

        self.load_org_html_file()
        self.buffer_widget.reload()

    def load_org_html_file(self):
        self.buffer_widget.setUrl(QUrl.fromLocalFile(os.path.splitext(self.url)[0]+".html"))

    def update_with_data(self, update_data):
        self.load_org_html_file()
        self.buffer_widget.reload()
