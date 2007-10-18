"""Benchmark runner class.

For copyright, license, and warranty, see bottom of file.
"""

import sys
from schevo.lib import optimize

import datetime
import random
from time import time

import pkg_resources

from schevo.backend import backends
from schevo.schema import latest_version
from schevo.test import EvolvesSchemata
from schevo.transaction import CallableWrapper


class BenchmarkRunner(object):

    def __init__(self, package_name, backend_name, backend_args):
        self.package_name = package_name
        self.backend_name = backend_name
        self.backend_args = backend_args
        self.times = {
            # method_name: [elapsed_time, ...],
            }
        self.started_at = None

    def run(self):
        if self.started_at is None:
            self.started_at = datetime.datetime.now()
        # Create a class to run the benchmark.
        BackendClass = backends[self.backend_name]
        if self.backend_args is None:
            self.backend_args = {}
        elif isinstance(self.backend_args, basestring):
            self.backend_args = BackendClass.args_from_string(self.backend_args)
        class Benchmark(EvolvesSchemata):
            backend_name = self.backend_name
            backend_args = self.backend_args
            schemata = self.package_name
            schema_version = latest_version(self.package_name)
            skip_evolution = False
            _use_db_cache = False
            def setUp(self):
                super(Benchmark, self).setUp()
                # Ensure consistency with pseudo-random generator.
                random.seed(1)
                self.db.execute(CallableWrapper(db.x.setup_benchmark))
            def run(self):
                # Ensure consistency with pseudo-random generator.
                random.seed(2)
                results = {}
                for method_name in sorted(db.x):
                    if method_name.startswith('benchmark'):
                        start_time = time()
                        self.db.execute(CallableWrapper(db.x[method_name]))
                        end_time = time()
                        elapsed_time = end_time - start_time
                        results[method_name] = elapsed_time
                return results
        # Run each benchmark method and record elapsed times.
        benchmark = Benchmark()
        benchmark.setUp()
        results = benchmark.run()
        for method_name, elapsed_time in results.iteritems():
            L = self.times.setdefault(method_name, [])
            L.append(elapsed_time)
        benchmark.tearDown()

    def best_times(self):
        return dict(
            (method_name, min(elapsed_times))
            for method_name, elapsed_times
            in self.times.iteritems()
            )

    def store_in(self, db, machine):
        """Store best results for this benchmark."""
        benchmark_type = db.execute(db.BenchmarkType.t.create_if_necessary(
            package_name=self.package_name))
        benchmark = db.execute(db.Benchmark.t.create(
            type=benchmark_type,
            machine=machine,
            schevo_version=pkg_resources.require('Schevo')[0].version,
            started_at=self.started_at,
            ))
        for method_name, best_result in self.best_times().items():
            benchmark_section_type = db.execute(
                db.BenchmarkSectionType.t.create_if_necessary(
                benchmark_type=benchmark_type,
                method_name=method_name,
                ))
            benchmark_section = db.execute(db.BenchmarkSection.t.create(
                benchmark=benchmark,
                type=benchmark_section_type,
                repetitions=len(self.times[method_name]),
                best_result=best_result,
                ))


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
