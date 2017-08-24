"""
Your task in this exercise has two steps:

- audit the OSMFILE and change the variable 'mapping' to reflect the changes needed to fix
    the unexpected street types to the appropriate ones in the expected list.
    You have to add mappings only for the actual problems you find in this OSMFILE,
    not a generalized solution, since that may and will depend on the particular area you are auditing.
- write the update_name function, to actually fix the street name.
    The function takes a string with street name as an argument and should return the fixed name
    We have provided a simple test so that you see what exactly is expected
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "example.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ['Delhi', 'Road', 'Avenue', 'Vihar', 'Nagar', 'Lane', 'Colony', 'Society', 'Janakapuri', 'Vasundhara',
            'Park', 'Street']

# UPDATE THIS VARIABLE
mapping = {"St": "Street",
           "St.": "Street",
           "delhi": "Delhi",
           "Ave": "Avenue",
           "avenue": "Avenue",
           "vihar": "Vihar",
           "Rd.": "Road",
           "Rd": "Road",
           "Marg": "Road",
           "marg": "Road",
           "road": "Road",
           "Roads": "Road",
           "nagar": "Nagar",
           "lane": "Lane",
           "colony": "Colony",
           "society": "Society",
           "soc.": "Society",
           "Socity": "Society",
           "janakapuri": "Janakapuri",
           "vasundhar": "Vasundhara",
           "park": "Park"

           }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping=mapping):
    newnm = name.split(' ')
    l1 = []
    for nam in newnm:
        token = 0

        for mapp in mapping.items():
            if mapp[0] == nam:
                var = mapp[1]
                token = 1
                l1.append(var)
                break
        if token!= 1:
            l1.append(nam)
    string = ' '.join(l1)
    return string


def test():
    st_types = audit(OSMFILE)
    assert len(st_types) == 3
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.items():
        for name in ways:
            new_name = update_name(name, mapping)
            print(name, "=>", new_name)



if __name__ == '__main__':
    test()