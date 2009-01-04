# Copyright (c) 2008, Pablo Flouret <quuxbaz@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met: Redistributions of
# source code must retain the above copyright notice, this list of conditions and
# the following disclaimer. Redistributions in binary form must reproduce the
# above copyright notice, this list of conditions and the following disclaimer in
# the documentation and/or other materials provided with the distribution.
# Neither the name of the software nor the names of its contributors may be
# used to endorse or promote products derived from this software without specific
# prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import urwid

from ccx2 import collbrowser
from ccx2 import playlist
from ccx2 import signals

from ccx2.config import keybindings

class TabContainer(urwid.Pile):
  def __init__(self, app):
    self.app = app

    help = urwid.ListBox([urwid.Text('yeah right')])
    help.get_widget = lambda : help

    # TODO: make configurable
    self.tabs = [('help', help),
                 ('playlist', playlist.Playlist(self.app)),
                 ('switcher', playlist.PlaylistSwitcher(self.app)),
                 ('collbrowser', collbrowser.CollectionBrowserManager(self.app))]

    # XXX: does it make sense to have more than one playlist tab? what to do then?
    # XXX: the damn coll browser needs to know the current playlist in view, any other solutions?
    self.playlist = self.tabs[1][1]

    self.cur_tab = 1
    self.tabbar = urwid.Text('', align='center', wrap=urwid.CLIP)
    self._update_tabbar_string()

    w = self.tabs[self.cur_tab][1].get_widget()
    self.tab_w = urwid.WidgetWrap(w)

    self.__super.__init__([('flow', self.tabbar), self.tab_w], 1)

  def _update_tabbar_string(self):
    texts = []
    for i, t in enumerate(self.tabs):
      if i == self.cur_tab:
        text = '<%d:%s>' % (i+1, t[0])
      else:
        text = ' %d:%s ' % (i+1, t[0])
      texts.append(text)

    self.tabbar.set_text(' '.join(texts))

  def load_tab(self, n, wrap=False):
    tlen = len(self.tabs)

    if n >= tlen or n < 0:
      if wrap:
        n = n % tlen
      else:
        return

    self.cur_tab = n

    self._update_tabbar_string()
    self.tab_w._w = self.tabs[n][1].get_widget()

    signals.emit('need-redraw')

  def keypress(self, size, key):
    if key in keybindings['general']['goto-tab-n']:
      self.load_tab(keybindings['general']['goto-tab-n'].index(key))
    elif key in keybindings['general']['goto-prev-tab']:
      self.load_tab(self.cur_tab-1, wrap=True)
    elif key in keybindings['general']['goto-next-tab']:
      self.load_tab(self.cur_tab+1, wrap=True)
    else:
      return self.__super.keypress(size, key)


