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

default_keybindings = {
    'general': {
        'move-up': ['k', 'up'],
        'move-down': ['j', 'down'],
        'page-up': ['ctrl u', 'page up'],
        'page-down': ['ctrl d', 'page down'],
        'move-top': ['home', 'meta <'],
        'move-bottom': ['end', 'meta >'],
        'goto-tab-n': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
        'goto-prev-tab': ['['],
        'goto-next-tab': [']'],
        'select-and-move-down': [' '], # space
        'select-and-move-up': ['<0>'], # ctrl space
        'delete': ['d', 'delete'],
        'cancel': ['esc', 'ctrl g'],
        'quit': ['q', 'ctrl q'],
    },
    'playback': {
        'play': ['x'],
        'play-pause-toggle': ['p', 'c'],
        'stop': ['s', 'backspace', 'v'],
        'next-track': ['>', 'b'],
        'previous-track': ['<', 'z'],
    },
    'playlist': {
        'play-highlighted': ['enter'],
    },
    'playlist-switcher': {
        'load': ['enter'],
        'new': ['n'],
        'rename': ['r'],
        'add-playlist-to-current': ['a'],
    },
    'collection-browser': {
        'navigate-in': ['l', 'right'],
        'navigate-out': ['h', 'left', 'backspace'],
        'add-to-playlist': ['a'],
    },
}

default_formatting = {
    'collbrowser': {
        'by_albumartist':
            """(or :performer :artist)
               > :album
               > (if :partofset (cat "CD" :partofset))
               > (pad :tracknr "2" "0"). 
                 (if (not (= :artist :performer)) (cat :artist " - ")):title'}
            """
    },
    'playlist': {
        'simple':
            """(or :performer :artist) - 
               (if :partofset (cat :partofset "."))(pad :tracknr "2" "0") - 
               :title (if :compilation (cat "| " :artist))"""
    },
}

keybindings = default_keybindings
formatting = default_formatting

