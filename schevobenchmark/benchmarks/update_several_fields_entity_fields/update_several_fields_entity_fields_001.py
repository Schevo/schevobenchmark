"""Benchmark for updating entities where several of the fields are
entity fields.

This benchmark was written to test optimizations to the handling of
bidirectional links in `schevo.database2:Database._update_entity`.
"""

# All Schevo schema modules must have these lines.
from schevo.schema import *
schevo.schema.prep(locals())


from random import randint


class Foo(E.Entity):

    bar = f.entity('Bar')
    baz = f.entity('Baz')
    bar2 = f.entity('Bar')
    baz2 = f.entity('Baz')
    bar3 = f.entity('Bar')
    baz3 = f.entity('Baz')
    aa = f.integer(required=False)
    bb = f.integer(required=False)
    cc = f.integer(required=False)
    dd = f.integer(required=False)
    ee = f.integer(required=False)


class Bar(E.Entity):

    pass


class Baz(E.Entity):

    pass


def x_setup_benchmark(db):
    # Create 1000 Bar and Baz entities.
    create_Bar = db.Bar.t.create
    create_Baz = db.Baz.t.create
    ex = db.execute
    for x in xrange(1000):
        ex(create_Bar())
        ex(create_Baz())
    # Create 1000 Foo entities pointing to random Bar and Baz
    # entities.
    Bar = db.Bar
    Baz = db.Baz
    create_Foo = db.Foo.t.create
    for x in xrange(1000):
        ex(create_Foo(
            bar = Bar[randint(1, 1000)],
            baz = Baz[randint(1, 1000)],
            bar2 = Bar[randint(1, 1000)],
            baz2 = Baz[randint(1, 1000)],
            bar3 = Bar[randint(1, 1000)],
            baz3 = Baz[randint(1, 1000)],
            ))


def x_benchmark_1_update_two_entity_fields(db):
    # Update 1000 Foo entities to point to two different random
    # entities.
    Foo = db.Foo
    Bar = db.Bar
    Baz = db.Baz
    ex = db.execute
    for x in xrange(1, 1001):
        foo = Foo[x]
        ex(foo.t.update(
            bar = Bar[randint(1, 1000)],
            baz = Baz[randint(1, 1000)],
            ))


def x_benchmark_2_update_all_entity_fields(db):
    # Update 1000 Foo entities to point to several different random
    # entities.
    Foo = db.Foo
    Bar = db.Bar
    Baz = db.Baz
    ex = db.execute
    for x in xrange(1, 1001):
        foo = Foo[x]
        ex(foo.t.update(
            bar = Bar[randint(1, 1000)],
            baz = Baz[randint(1, 1000)],
            bar2 = Bar[randint(1, 1000)],
            baz2 = Baz[randint(1, 1000)],
            bar3 = Bar[randint(1, 1000)],
            baz3 = Baz[randint(1, 1000)],
            ))


def x_benchmark_3_update_integer_fields(db):
    # Update 1000 Foo entities' integer fields, ignoring entity
    # fields.
    Foo = db.Foo
    ex = db.execute
    for x in xrange(1, 1001):
        foo = Foo[x]
        ex(foo.t.update(
            aa = randint(1, 1000),
            bb = randint(1, 1000),
            cc = randint(1, 1000),
            dd = randint(1, 1000),
            ee = randint(1, 1000),
            ))
