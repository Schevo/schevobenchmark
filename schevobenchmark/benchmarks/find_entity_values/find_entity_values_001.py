"""Benchmark for find operations such as the following::

    e = <<some entity>>
    results = db.SomeExtent.find(field_name=e)

This benchmark was written to test an optimization that takes
advantage of bidirectional links when this type of find is performed.
"""

# All Schevo schema modules must have these lines.
from schevo.schema import *
schevo.schema.prep(locals())


from random import randint


class Foo(E.Entity):

    number = f.float()


class Bar(E.Entity):

    foo = f.entity('Foo')


def x_setup_benchmark(db):
    # Create 50 Foo entities.
    Foo = db.Foo
    create_Foo = Foo.t.create
    ex = db.execute
    for x in xrange(50):
        ex(create_Foo(number=randint(1, 1000)))
    # Create 1000 Bar entities.
    create_Bar = db.Bar.t.create
    for x in xrange(1000):
        random_Foo = Foo[randint(1, 50)]
        ex(create_Bar(foo=random_Foo))


def x_benchmark_1_find_entity_values(db):
    for x in xrange(25):
        for foo in db.Foo:
            bars_count = foo.sys.count('Bar', 'foo')
            bars = db.Bar.find(foo=foo)
            assert len(bars) == bars_count
