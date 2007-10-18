"""Benchmark command.

For copyright, license, and warranty, see bottom of file.
"""

from operator import attrgetter
from pprint import pprint

from schevo import database
from schevo.script.command import Command
from schevo.script import opt

from schevobenchmark.mapping import benchmark_map, benchmark_package_names
from schevobenchmark.runner import BenchmarkRunner


usage = """
schevo benchmark [options] NAME [NAME [...]]
schevo benchmark list
schevo benchmark -d DBNAME report

NAME: The name of a benchmark to run. More than one name may be
specified; multiple benchmarks are run sequentially.

Use 'schevo benchmark list' to get a list of all available benchmarks.
"""


def _parser():
    p = opt.parser(usage)
    p.add_option('-d', '--database',
                 dest = 'database',
                 help = 'Store benchmark results in the named database.',
                 metavar = 'NAME',
                 type = str,
                 default = None,
                 )
    p.add_option('-r', '--repeat',
                 dest = 'repeat',
                 help = 'Repeat each benchmark COUNT times.',
                 metavar = 'COUNT',
                 type = int,
                 default = 3,
                 )
    return p


class Benchmark(Command):

    name = 'Benchmark'
    description = 'Run one or more performance benchmarks.'

    def main(self, arg0, args):
        print
        print
        parser = _parser()
        options, args = parser.parse_args(list(args))
        if len(args) == 0:
            print 'At least one NAME, or "list"/"report", must be specified.'
            return 1
        if len(args) == 1 and args[0].lower() == 'list':
            print 'Available benchmarks:'
            print
            for name, value in sorted(benchmark_map.items()):
                if isinstance(value, basestring):
                    print name
                else:
                    print '%s %r' % (name, value)
        else:
            if options.repeat < 1:
                print 'COUNT must be >= 1, not %i.' % options.repeat
                return 1
            if options.backend_name is None:
                print 'NOTE: Using schevo.store backend.'
                print
                options.backend_name = 'schevo.store'
            db = None
            if options.database is not None:
                print 'Opening database %r.' % options.database
                db = database.open(options.database)
                machine = db.Machine.x.this()
                print 'Machine is %s (OID %r)' % (machine, machine.sys.oid)
            names = [arg.lower() for arg in args]
            package_names = benchmark_package_names(names)
            print 'Preparing to run these benchmarks:'
            for package_name in package_names:
                print '  %s' % package_name
            print
            print 'Backend name:', options.backend_name
            print 'Backend args:', options.backend_args
            print
            for package_name in package_names:
                print package_name
                print '=' * len(package_name)
                runner = BenchmarkRunner(
                    package_name, options.backend_name, options.backend_args)
                for count in xrange(options.repeat):
                    print 'Starting repetition %i.' % (count + 1)
                    runner.run()
                print 'Finished.'
                if db:
                    runner.store_in(db, machine)
                    print 'Stored results.'
                print 'Best times:'
                pprint(runner.best_times())
                print


start = Benchmark


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
