"""Schevo benchmark results."""

# All Schevo schema modules must have these lines.
from schevo.schema import *
schevo.schema.prep(locals())


import datetime
from operator import attrgetter
from socket import gethostname

NOW = datetime.datetime.now


class Machine(E.Entity):

    host_name = f.unicode()

    _key(host_name)

    @extentmethod
    def x_this(extent):
        machine = db.execute(
            extent.t.create_if_necessary(host_name=gethostname()))
        return machine


class Benchmark(E.Entity):

    type = f.entity('BenchmarkType')
    machine = f.entity('Machine')
    schevo_version = f.string()
    started_at = f.datetime()
    expired = f.boolean(default=False)

    _index(machine, type)


class BenchmarkSection(E.Entity):

    benchmark = f.entity('Benchmark')
    type = f.entity('BenchmarkSectionType')
    repetitions = f.integer()
    best_result = f.float()

    _key(benchmark, type)


class BenchmarkSectionType(E.Entity):

    benchmark_type = f.entity('BenchmarkType')
    method_name = f.unicode()

    _key(benchmark_type, method_name)


class BenchmarkType(E.Entity):

    package_name = f.unicode()

    _key(package_name)


def x_expire(keep=1):
    txlist = []
    for benchmark_type in db.BenchmarkType:
        for machine in db.Machine:
            # Find all of the benchmarks we'll expire for this machine
            # and benchmark type, taking into account the number of
            # benchmarks to keep.
            benchmarks_to_expire = sorted(
                db.Benchmark.find(machine=machine, type=benchmark_type),
                key=attrgetter('started_at')
                )[:-keep]
            txlist.extend(
                benchmark.t.update(expired=True)
                for benchmark in benchmarks_to_expire
                if not benchmark.expired
                )
    db.execute(schevo.transaction.Combination(txlist))


def x_print_report():
    for benchmark_type in db.BenchmarkType.by('package_name'):
        for benchmark_section_type in sorted(
            benchmark_type.m.benchmark_section_types(),
            key=attrgetter('method_name')
            ):
            print benchmark_type.package_name
            print benchmark_section_type.method_name
            # For each machine,
            for machine in db.Machine.by('host_name'):
                # Find the fastest benchmark section that matches.
                sections = []
                for benchmark in db.Benchmark.find(
                    type=benchmark_type,
                    machine=machine,
                    ):
                    if not benchmark.expired:
                        benchmark_section = db.BenchmarkSection.findone(
                            benchmark=benchmark,
                            type=benchmark_section_type,
                            )
                        sections.append(
                            (benchmark_section.best_result,
                             benchmark_section))
                if sections:
                    fastest_section = min(sections)[1]
                    # Show the version of Schevo used for that result.
                    print '  ** BEST ** %s' % machine
                    print '%s :: %0.3fs @ %s' % (
                        fastest_section.benchmark.schevo_version,
                        fastest_section.best_result,
                        fastest_section.benchmark.started_at,
                        )
                    print '  ** LAST 5 ** %s' % machine
                    for _, section in sections[-5:]:
                        print '%s :: %0.3fs @ %s' % (
                            section.benchmark.schevo_version,
                            section.best_result,
                            section.benchmark.started_at,
                            )
            # Done.
            print

