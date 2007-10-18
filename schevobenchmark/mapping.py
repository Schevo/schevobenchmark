"""Mapping of all benchmarks available in SchevoBenchmark.

For copyright, license, and warranty, see bottom of file.
"""

import sys
from schevo.lib import optimize


benchmark_map = {
    # ## Mapping of benchmark name to schema package name:
    # benchmark-name: package-name,

    # ## Mapping of an alias to a list of benchmark names:
    # benchmark-alias: [benchmark-name, ...],

    'all': ['updates'],

    'updates': ['update-few-fields-entity-fields',
                'update-several-fields-entity-fields',
                'update-indexed-entities',
                ],

    'update-few-fields-entity-fields':
    'schevobenchmark.benchmarks.update_few_fields_entity_fields',
    
    'update-several-fields-entity-fields':
    'schevobenchmark.benchmarks.update_several_fields_entity_fields',

    'update-indexed-entities':
    'schevobenchmark.benchmarks.update_indexed_entities',
    }


def benchmark_package_names(names):
    """Return a list of benchmark package names to load based on the
    given list of benchmark names."""
    L = []
    for name in names:
        value = benchmark_map[name]
        if isinstance(value, list):
            L.extend(benchmark_package_names(value))
        else:
            L.append(value)
    return sorted(L)


optimize.bind_all(sys.modules[__name__])  # Last line of module.


# Copyright (C) 2001-2007 Orbtech, L.L.C.
#
# Schevo
# http://schevo.org/
#
# Orbtech
# Saint Louis, MO
# http://orbtech.com/
#
# This toolkit is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This toolkit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
