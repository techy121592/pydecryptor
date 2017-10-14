#####################################################################################
# Copyright (C) 2017  David Welch                                                   #
#                                                                                   #
# This program is free software; you can redistribute it and/or                     #
# modify it under the terms of the GNU General Public License                       #
# as published by the Free Software Foundation; either version 2                    #
# of the License, or (at your option) any later version.                            #
# this program is distributed in the hope that it will be useful,                   #
# but WITHOUT ANY WARRANTY; without even the implied warranty of                    #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                     #
# GNU General Public License for more details.                                      #
# You should have received a copy of the GNU General Public License                 #
# along with this program; if not, write to the Free Software                       #
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.   #
#####################################################################################

class Decrypter:
    cypher = {}
    def __init__(self, cypher):
        self.cypher = cypher

    def swap_letters(self, letter):
        try:
            if letter.isupper():
                return self.cypher[letter.lower()].upper()
            else:
                return self.cypher[letter]
        except:
            return letter

    def decrypt(self, line):
        return ''.join(list(map(self.swap_letters, list(line))))
