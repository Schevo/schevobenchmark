"""Benchmark for updating entities where there are several fields and
several indices, but little overlap in the index specs.

This benchmark was written to test optimizations to the handling of
indices in `schevo.database2:Database._update_entity`.  The
optimizations were rolled back because they didn't improve the
performance.  This benchmark is kept for completeness.
"""

# All Schevo schema modules must have these lines.
from schevo.schema import *
schevo.schema.prep(locals())


from random import random


class Foo(E.Entity):

    f1 = f.float(required=False)
    f2 = f.float(required=False)
    f3 = f.float(required=False)
    f4 = f.float(required=False)
    f5 = f.float(required=False)
    f6 = f.float(required=False)
    f7 = f.float(required=False)
    f8 = f.float(required=False)
    f9 = f.float(required=False)

    _index(f1)
    _index(f2)
    _index(f3)
    _index(f4)
    _index(f5)
    _index(f6)
    _index(f7)
    _index(f8)
    _index(f9)


def x_setup_benchmark(db):
    # Create 1000 Foo entities.
    create_Foo = db.Foo.t.create
    ex = db.execute
    for x in xrange(1000):
        ex(create_Foo())


def x_benchmark_1_update_f1_only(db):
    Foo = db.Foo
    ex = db.execute
    for x in xrange(1, 1001):
        foo = Foo[x]
        ex(foo.t.update(
            f1 = random(),
            ))


def x_benchmark_2_update_f1_f2(db):
    Foo = db.Foo
    ex = db.execute
    for x in xrange(1, 1001):
        foo = Foo[x]
        ex(foo.t.update(
            f1 = random(),
            f2 = random(),
            ))


def x_benchmark_3_update_all(db):
    Foo = db.Foo
    ex = db.execute
    for x in xrange(1, 1001):
        foo = Foo[x]
        ex(foo.t.update(
            f1 = random(),
            f2 = random(),
            f3 = random(),
            f4 = random(),
            f5 = random(),
            f6 = random(),
            f7 = random(),
            f8 = random(),
            f9 = random(),
            ))
