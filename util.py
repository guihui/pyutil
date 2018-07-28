#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

#######################
#
# NLP相关处理
#
#######################
def create_ngram_set(input_list, ngram_value=2):
    """
    Extract a set of n-grams from a list of integers.
    从一个整数列表中提取  n-gram 集合。
    >>> create_ngram_set([1, 4, 9, 4, 1, 4], ngram_value=2)
    {(4, 9), (4, 1), (1, 4), (9, 4)}
    >>> create_ngram_set([1, 4, 9, 4, 1, 4], ngram_value=3)
    [(1, 4, 9), (4, 9, 4), (9, 4, 1), (4, 1, 4)]
    """
    return set(zip(*[input_list[i:] for i in range(ngram_value)]))

def str2dict(s, l1_sep = ';', l2_sep = ':'):
    dct = {}
    if not isinstance(s, str):
        return dct
    for kv in s.split(l1_sep):
        kv = kv.split(l2_sep)
        if len(kv) == 2:
            k, v = kv
            dct[k] = v
    return dct

#######################
#
# IO相关
#
#######################

def read_input(f_in = sys.stdin, dim = '\t', check_col = 0):
    line_cnt = 0
    check_fail = 0
    empty_cnt = 0
    for line in f_in:
        line_cnt += 1
        line = line.strip('\n')
        if not line:
            empty_cnt += 1
            continue
        cols = line.split(dim)
        if check_col != 0 and len(cols) != check_col:
            check_fail += 1
            continue
        yield cols
    print >> sys.stderr, 'line_cnt:{} empty_cnt:{} check_col[{}]:{}'.format(line_cnt, empty_cnt, check_col, check_fail)

#######################
#
# App
#
#######################

import argparse

class App:
    def __init__(self):
        pass
    def _args(self):
        parser = argparse.ArgumentParser(description='cols sum')
        parser.add_argument('--op', action="store", dest="ops", required=True, nargs="+", help="ops")
        return parser.parse_args()
    def run(self):
        args = self._args()
        for op in args.ops:
            try:
                func = getattr(self, op)
            except:
                print >> sys.stderr, '%s.%s not found, continue' %(self.__class__.__name__, op)
                continue
            print >> sys.stderr, '%s.%s start' %(self.__class__.__name__, op)
            func()

class DemoApp(App):
    def __init__(self):
        App.__init__(self)
    def mapper(self):
        print "DemoApp.mapper() succ"

    def reducer(self):
        print "DemoApp.reducer() succ"

def __test_demo_app():
    demo = DemoApp()
    demo.run()

#######################
#
# NLP相关处理
#
#######################

def CMD_show(argv):
    """show all availabel command"""
    print "all availabel command"
    for key in sys.modules['__main__'].__dict__.keys():
        if key.startswith('CMD_'):
            print '- {}'.format(key.replace('CMD_', ''))
            func = eval(key)
            if func.__doc__:
                doc = func.__doc__.replace('\n', '\n')
                print '\t{}'.format(doc)
            else:
                print '\t[NO DOC]'
def CMD_aggregate_inline(argv):
    """聚合相同key的value到同一行"""
    return 0

def CMD_daterange(argv):
    """生成时间列表
        daterange --start 20180101 --days 7 --sep ,
        daterange --start 20180101 --end 20180115 --sep ,
        daterange --start 20180101 --end 20180115 --step 3 --sep ,
    """

    import datetime

    def _args(argv):
        parser = argparse.ArgumentParser(description='date days')
        parser.add_argument('--start', required=False, help='start')
        parser.add_argument('--end',   required=False, help='end')
        parser.add_argument('--days', type=int, required=False, help='days')
        parser.add_argument('--step', type=int, required=False, help='step', default=1)
        parser.add_argument('--sep', required=False, help='days', default='\t')
        return parser.parse_args(argv)

    args = _args(argv)
    start = args.start
    if start:
        start = datetime.datetime.strptime(start, "%Y%m%d")

    end = args.end
    if end:
        end = datetime.datetime.strptime(end, "%Y%m%d")

    days = args.days

    if start and end:
        dates = [start + datetime.timedelta(days = x) for x in range(0, (end - start).days + 1, args.step)]
    elif start and days:
        dates = [start + datetime.timedelta(days = x) for x in range(0, days, args.step)]
    elif end and days:
        dates = [end - datetime.timedelta(days = x) for x in range(0, days, args.step)]
    else:
        sys.stderr.write('start + end, start + days, end + days')
        return
    print args.sep.join([date.strftime("%Y%m%d") for date in dates])


def run_cmd():
    if len(sys.argv) <= 1:
        print """Usage:
    {} <command>
    run `{} show` to get all availabel command.
""".format(sys.argv[0], sys.argv[0])
        sys.exit(-1)

    func = eval('CMD_' + sys.argv[1])
    sys.exit(func(sys.argv[2:]))


if __name__ == "__main__":
    run_cmd()

