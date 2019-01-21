#
# dbtool for MongoDB
#
# author: João 'Jam' Moraes
# license: MIT
#
# This tool is designed for identifying inconsistencies in MongoDB databases
# based on pre-defined models. It supports automated analysis over multiple
# databases located on multiple servers as a single batch operation. It is
# structured with memory efficiency as a priority, requiring the minimum amount
# of memory possible for each operation.
#

import src as DBTool
import json
from sys import argv

DBTool.app(argv)