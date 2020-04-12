#!/usr/bin/env python3

import pweave
pweave.weave(
    file = 'analyse.pmd',
    doctype = 'markdown',
    informat = 'markdown',
    shell = 'python',
    plot = True,
    output = 'figure/corona_visualisation.md'
    )
