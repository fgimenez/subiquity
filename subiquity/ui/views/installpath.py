# Copyright 2015 Canonical, Ltd.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Install Path

Provides high level options for Ubuntu install

"""
import logging
from urwid import (ListBox, Pile, BoxAdapter)

from subiquitycore.ui.lists import SimpleList
from subiquitycore.ui.buttons import menu_btn, cancel_btn
from subiquitycore.ui.utils import Padding, Color
from subiquitycore.view import BaseView

log = logging.getLogger('subiquity.installpath')


class InstallpathView(BaseView):
    def __init__(self, model, signal):
        self.model = model
        self.signal = signal
        self.items = []
        self.body = [
            Padding.center_79(self._build_model_inputs()),
            Padding.line_break(""),
            Padding.fixed_10(self._build_buttons()),
        ]
        super().__init__(ListBox(self.body))

    def _build_buttons(self):
        self.buttons = [
            Color.button(cancel_btn(on_press=self.cancel),
                         focus_map='button focus'),
        ]
        return Pile(self.buttons)

    def _build_model_inputs(self):
        sl = []
        for ipath, sig in self.model.get_menu():
            log.debug("Building inputs: {}".format(ipath))
            sl.append(Color.menu_button(
                menu_btn(label=ipath,
                         on_press=self.confirm,
                         user_data=sig),
                focus_map='menu_button focus'))

        return BoxAdapter(SimpleList(sl),
                          height=len(sl))

    def confirm(self, result, sig):
        self.signal.emit_signal(sig)

    def cancel(self, button):
        self.signal.emit_signal('prev-screen')
