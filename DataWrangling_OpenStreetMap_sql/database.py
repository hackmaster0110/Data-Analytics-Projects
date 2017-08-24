import csv
import sqlite3

conn=sqlite3.connect('NewDelhi.db')

c=conn.cursor()
c.execute("CREATE TABLE nodes(id,lat,lon,user,uid,version,changeset,timestamp);")
with open('nodes.csv','r') as f:
    rdr=csv.DictReader(f)
    var=[(i['id'],i['lat'],i['lon'],i['user'],i['uid'],i['version'],i['changeset'],i['timestamp']) for i in rdr]
    c.executemany('INSERT INTO nodes (id,lat,lon,user,uid,version,changeset,timestamp) VALUES (?,?,?,?,?,?,?,?);',var)
    conn.commit()


c.execute("CREATE TABLE nodes_tags(id,key,value,type);")
with open('nodes_tags.csv', 'r') as f:
    rdr = csv.DictReader(f)
    var=[(i['id'],i['key'],i['value'],i['type']) for i in rdr]
    c.executemany('INSERT INTO nodes_tags (id,key,value,type) VALUES (?,?,?,?);', var)
    conn.commit()


c.execute("CREATE TABLE ways(id,user,uid,version,changeset,timestamp);")
with open('ways.csv', 'r') as f:
    rdr = csv.DictReader(f)
    var=[(i['id'],i['user'],i['uid'],i['version'],i['changeset'],i['timestamp']) for i in rdr]
    c.executemany('INSERT INTO ways (id,user,uid,version,changeset,timestamp) VALUES (?,?,?,?,?,?);', var)
    conn.commit()


c.execute("CREATE TABLE ways_nodes(id,node_id,position);")
with open('ways_nodes.csv', 'r') as f:
    rdr = csv.DictReader(f)
    var=[(i['id'],i['node_id'],i['position']) for i in rdr]
    c.executemany('INSERT INTO ways_nodes (id,node_id,position)  VALUES (?,?,?);', var)
    conn.commit()


c.execute("CREATE TABLE ways_tags(id,key,value,type);")
with open('ways_tags.csv', 'r') as f:
    rdr = csv.DictReader(f)
    var=[(i['id'],i['key'],i['value'],i['type']) for i in rdr]
    c.executemany('INSERT INTO ways_tags (id,key,value,type) VALUES (?,?,?,?);',var)
    conn.commit()

conn.close()