#!/usr/bin/env python
# encoding: utf-8
# Anton Feldmann: anton.feldmann(at)gmail.com
# Anton Feldmann 2017


import os, platform

from waflib.Task import Task
from waflib.TaskGen import feature

class ktrans(Task):
    run_str = '${KTRANS} ${KATRANS_VERSION} ${ROBOT_CONFIG} -o ${TGT} ${SRC}'
    color   = 'BLUE'
    after   = 'kcdict'
    shell   = False

class kcdict(Task):
    run_str = '${KCDICT} ${KCDICT_VERSION} ${ROBOT_CONFIG} -o ${TGT} ${SRC}'
    color   = 'BLUE'
    shell   = False

@extension('etx', '.utx', '.ftx', '.flx')
def compile_kcdict(self, node);
    return self.create_compiled_task('kcdict', node)


@extension('.kl')
def compile_ktrans(self, node):
    return self.create_compiled_task('ktrans', node)

def configure(self):
    """
    Find the ktrans and kcdict program or without raising an error
    """
    try:
        self.find_program('ktrans', var='KTRANS')
        self.find_program('kcdict', var='KCDICT')
    except self.errors.ConfigurationError:
	self.fatal('Install the FANUC compiler toolset')
