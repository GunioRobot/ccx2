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

import commands
import search
import signals

class TabContainer(urwid.Pile):
  context_name = 'tabs'

  def __init__(self, app, tabs, focus_tab=0):
    self.app = app

    self.tabs = tabs

    self.cur_tab = focus_tab
    self.tabbar = urwid.Text('', align='left', wrap=urwid.CLIP)
    self._update_tabbar_string()

    w = self.tabs[self.cur_tab][1]
    self.tab_w = urwid.WidgetWrap(w)

    self.__super.__init__([('flow', self.tabbar),
                           ('flow', urwid.Divider(u'\u2500')),
                           self.tab_w],
                          2)

  def _update_tabbar_string(self):
    texts = []
    for i, t in enumerate(self.tabs):
      text = '%d%s%s' % (i+1, i==self.cur_tab and '*' or ':', t[0])
      texts.append(text)

    self.tabbar.set_text(' '.join(texts))

  def get_current(self):
    return self.tabs[self.cur_tab][1]

  def load_tab(self, n, wrap=False):
    tlen = len(self.tabs)

    if n >= tlen or n < 0:
      if wrap:
        n = n % tlen
      else:
        return

    self.cur_tab = n

    self._update_tabbar_string()
    self.tab_w._w = self.tabs[n][1]

    signals.emit('need-redraw')

  def load_tab_by_name(self, name):
    for i, t in enumerate(self.tabs):
      if t[0] == name:
        self.load_tab(i)
        return

  def add_tab(self, name, body, switch=False):
    self.tabs.append((name, body))
    index = len(self.tabs) - 1

    if switch:
      self.load_tab(index)
    else:
      self._update_tabbar_string()

    return index

  def remove_tab(self, n):
    if n < 0:
      n = len(self.tabs) + n

    if self.cur_tab == n:
      self.load_tab(n-1)

    try:
      del self.tabs[n]
      self._update_tabbar_string()
    except IndexError:
      pass

  def get_contexts(self):
    w = self.tab_w._w
    while not hasattr(w, 'get_contexts') and hasattr(w, 'get_focus'):
      w = w.get_focus()

    c = []
    if hasattr(w, 'get_contexts'):
      c = w.get_contexts()

    return c + [self]

  def tab_is_closable(self, n):
    # XXX: move to classes?
    try:
      t = type(self.tabs[n][1])
      return t == search.SearchListBox
    except IndexError:
      return False

  def cmd_tab(self, args):
    if not args:
      raise commands.CommandError("need an argument")

    arg = args.strip()
    try:
      n = int(arg)
      self.load_tab(n-1)
      return
    except ValueError:
      pass

    if arg == 'next':
      self.load_tab(self.cur_tab+1, wrap=True)
    elif arg == 'prev':
      self.load_tab(self.cur_tab-1, wrap=True)
    elif arg == 'lastfocus':
      pass # TODO
    else:
      raise commands.CommandError("not a valid argument: %s" % arg)

