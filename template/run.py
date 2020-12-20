#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
#from importlib import reload

#reload(sys)
#sys.setdefaultencoding('utf8')

from app import app
app.run(debug=True)