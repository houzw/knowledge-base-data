#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/1/23 9:33

from subprocess import call
# call('python ./arcgis/demo.py')
call('python ./taudem/taudem2owl_new.py')
call('python ./saga/saga2owl.py')
call('python ./grass/grass2owl.py')
call('python ./arcgis/arc2owl.py')
call('python ./otb2owl/otb2owl.py')

