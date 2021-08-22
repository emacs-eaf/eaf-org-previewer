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

from PyQt5 import QtCore
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QColor
from core.webengine import BrowserBuffer
from core.utils import get_emacs_var
import os

class AppBuffer(BrowserBuffer):
    def __init__(self, buffer_id, url, arguments):
        BrowserBuffer.__init__(self, buffer_id, url, arguments, False)

        self.url = url

        self.dark_mode = False
        dark_mode = get_emacs_var("eaf-org-dark-mode")
        if (dark_mode == "force" or \
            dark_mode == True or \
            (dark_mode == "follow" and self.theme_mode == "dark")):
            self.dark_mode = True

        self.buffer_widget.dark_mode_js = open(os.path.join(os.path.dirname(__file__),
                                                            "node_modules",
                                                            "darkreader",
                                                            "darkreader.js")).read()

        self.buffer_widget.loadProgress.connect(self.update_progress)

        self.load_org_html_file()

    @QtCore.pyqtSlot(int)
    def update_progress(self, progress):
        # We need load dark mode js always, otherwise will white flash when loading page.
        if self.dark_mode:
            self.buffer_widget.load_dark_mode_js()
            self.buffer_widget.enable_dark_mode()

    def load_org_html_file(self):
        self.buffer_widget.setUrl(QUrl.fromLocalFile(os.path.splitext(self.url)[0]+".html"))

    def update_with_data(self, update_data):
        self.load_org_html_file()
        self.buffer_widget.reload()
