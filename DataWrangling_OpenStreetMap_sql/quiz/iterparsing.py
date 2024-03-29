#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Your task is to use the iterative parsing to process the map file and
find out not only what tags are there, but also how many, to get the
feeling on how much of which data you can expect to have in the map.
Fill out the count_tags function. It should return a dictionary with the 
tag name as the key and number of times this tag can be encountered in 
the map as value.

Note that your code will be tested with a different data file than the 'example.osm'
"""
import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict


def count_tags(filename):
    tags=defaultdict(int)
    context=ET.parse(filename)
    root=context.getroot()
    k=0
    for elem in root.iter():
        tags[elem.tag]+=1
    #print(tags)

    return tags

def test():

    tags = count_tags('example.osm')
    pprint.pprint(tags)
    



if __name__ == "__main__":
    test()
