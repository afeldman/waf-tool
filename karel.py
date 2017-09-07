#!/usr/bin/env python
# encoding: utf-8
# Anton Feldmann: anton.feldmann(at)gmail.com
# Anton Feldmann 2017


import os, platform

from waflib import Utils, Task
from waflib.TaskGen import feature, extension, after, before
from waflib.Tools.ccroot import link_task, stlink_task

def options(opt):
    opt.add_option('--ktrans',
                   type='string',
                   default='',
                   dest='ktrans',
                   help='''path to ktrans''')

class karel(Task.task):
    run_str = '${KTRANS} -o ${TGT} ${SRC}'
    color = 'BLUE'
    
def options(opt):
    pass

def configure(conf):
    conf.find_program(conf.env.KAREL_COMPILER, var='KTRANS')
    conf.env.KAREL_FLAGS = []
    
@extension('.kl')
def compile_karel(self, node):
    return self.create_compiled_task('karel', node)
