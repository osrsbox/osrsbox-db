"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Script to update all Items data.

Copyright (c) 2020, PH01L

###############################################################################
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
"""
from scripts.items import items_buylimits
from scripts.items import items_properties
from scripts.items import items_unalchable
from scripts.icons import convert_item_icons


def main():
    items_buylimits.fetch()

    items_properties.fetch()
    items_properties.process()

    items_unalchable.fetch()

    convert_item_icons.main()


if __name__ == '__main__':
    main()
