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

""" View policy

Contains some default key navigations
"""

from urwid import WidgetWrap


class BaseView(WidgetWrap):
    def keypress(self, size, key):
        if key == 'esc':
            self.signal.prev_signal()
            return None
        if key in ['ctrl x']:
            self.signal.emit_signal('control-x-quit')

        return super().keypress(size, key)
