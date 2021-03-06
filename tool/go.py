#!/usr/bin/env python
# encoding: utf-8
# Anton Feldmann: anton.feldmann(at)gmail.com
# Anton Feldmann 2017


import os, platform

from waflib import Utils, Task
from waflib.TaskGen import feature, extension, after, before
from waflib.Tools.ccroot import link_task, stlink_task

def configure(cfg):
    ''' Set the definition for the environment '''

    def set_env_var(key, value):
        if not cfg.env[key]:
            cfg.env[key] = value

    if "GOPATH" in os.environ:
        set_env_var('GOPATH',os.getenv('GOPATH'))

    def set_go_arch(argument):
        return {
            '386': 'i386',
            'amd64': 'x86_64',
            'arm': 'arm',
        }.get(argument, platform.machine())

    set_def('GO_ARCH',set_go_arch(os.getenv('GOARCH')))

    if conf.env.GO_ARCH == 'x86_64':
	set_def('GO_COMPILER', '6g')
	set_def('GO_LINKER', '6l')
    elif conf.env.GO_ARCH in ['i386', 'i486', 'i586', 'i686']:
	set_def('GO_COMPILER', '8g')
	set_def('GO_LINKER', '8l')
    elif conf.env.GO_ARCH == 'arm':
	set_def('GO_COMPILER', '5g')
	set_def('GO_LINKER', '5l')
	set_def('GO_EXTENSION', '.5')

    if not (conf.env.GO_COMPILER or conf.env.GO_LINKER):
	raise conf.fatal('Unsupported platform ' + platform.machine())

    set_def('GO_PACK', 'gopack')# go ar tool
    set_def('gopackage_PATTERN', '%s.a')
    set_def('CPPPATH_ST', '-I%s')

    conf.find_program(conf.env.GO_COMPILER, var='GOC')
    conf.find_program(conf.env.GO_LINKER,   var='GOL')
    conf.find_program(conf.env.GO_PACK,     var='GOP')
    conf.find_program('cgo',                var='CGO')

class go(Task.Task):
    run_str = '${GOC} ${GOCFLAGS} ${CPPPATH_ST:INCPATHS} -o ${TGT} ${SRC}'

class gopackage(stlink_task):
    run_str = '${GOP} grc ${TGT} ${SRC}'

class goprogram(link_task):
    run_str = '${GOL} ${GOLFLAGS} -o ${TGT} ${SRC}'
    run_str = '${BINDIR}'

@extension('.go')
def compile_go(self, node):
    return self.create_compiled_task('go', node)

#from https://github.com/akaspin/sandbox/blob/master/tools/go.py
@feature('gopackage', 'goprogram')
@before('process_source')
def gopackage_is_foobar(self):
    self.source = self.to_nodes(self.source)
    src = []
    go = []
    for node in self.source:
	if node.name.endswith('.go'):
	    go.append(node)
        else:
	    src.append(node)

    self.source = src
    tsk = self.create_compiled_task('go', go[0])
    tsk.inputs.extend(go[1:])

@feature('gopackage', 'goprogram')
@after('process_source', 'apply_incpaths')
def go_local_libs(self):
    names = self.to_list(getattr(self, 'use', []))
    for name in names:
	tg = self.bld.get_tgen_by_name(name)
	if not tg:
	    raise Utils.WafError('no target of name %r necessary for %r in go uselib local' % (name, self))
	tg.post()
	for tsk in self.tasks:
	    if isinstance(tsk, go):
		tsk.set_run_after(tg.link_task)
		tsk.dep_nodes.extend(tg.link_task.outputs)
	path = tg.link_task.outputs[0].parent.abspath()
	self.env.append_unique('GOCFLAGS', ['-I%s' % path])
	self.env.append_unique('GOLFLAGS', ['-L%s' % path])
