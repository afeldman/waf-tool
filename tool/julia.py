#!/usr/bin/env python
# encoding: utf-8
# Anton Feldmann: anton.feldmann(at)gmail.com
# Anton Feldmann 2018

import os, platform, re

from waflib import Utils, Task
from waflib.TaskGen import feature, extension, after, before
from waflib.Tools.ccroot import link_task, stlink_task
from waflib.Configure import conf

@conf
def fing_julia(cfg):
    julia = conf.find_program(['julia'], var='JL')
    conf.get_julia_version()
    conf.env.JL_NAME = 'julia'

@conf
def get_julia_version(cfg):
    reg = re.compile(r'julia version ([0-9].[0-9]).*',re.M)

    out = cfg.cmd_and_log(cfg.env['JL']+['--version'])
    ver_s = reg.findall(out)[0].split('.')
    ver_i = tuple([int(s) for s in ver_s[0:2]])

    cfg.msg('Checking for JULIA version', '.'.join(map(str,ver_i)), color='BLUE')

    return ver_i

@conf
def assert_julia_version(cfg, min_version):

    ver_i = cfg.get_julia_version()
    res = '.'.join(map(str,ver_i))

    if (ver_i < min_version):
        cfg.msg(msg, res, color='RED')
        cfg.fatal('update julia')
    else:
        cfg.msg(msg, res, color='GREEN')
