import sqlite3
import csv


#Number of nodes#
def num_nodes(cur):
    var=cur.execute("SELECT COUNT(*) FROM nodes")
    return var.fetchone()




#Number of nodes_tags#
def num_nodes_tags(cur):
    var=cur.execute("SELECT COUNT(*) FROM nodes_tags")
    return var.fetchone()





#Number of ways#
def num_ways(cur):
    var=cur.execute("SELECT COUNT(*) FROM ways")
    return var.fetchone()




#Number of ways_nodes#
def num_ways_nodes(cur):
    var=cur.execute("SELECT COUNT(*) FROM ways_nodes")
    return var.fetchone()






#Number of ways_tags#
def num_ways_tags(cur):
    var=cur.execute("SELECT COUNT(*) FROM ways_tags")
    return var.fetchone()

#=======================#


#Popular cuisines
def top_cuisines(cur):
    for var in cur.execute("SELECT nodes_tags.VALUE,COUNT(*) AS num \
        FROM nodes_tags \
            JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE VALUE='restaurant') i \
            ON nodes_tags.id=i.id \
        WHERE nodes_tags.key='cuisine' \
        GROUP BY nodes_tags.Value \
        ORDER BY num DESC"):
            return var

#Biggest Religion
def biggest_religion(cur):
	for var in cur.execute('SELECT nodes_tags.value, COUNT(*) as num \
            FROM nodes_tags \
                JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value="place_of_worship") i \
                ON nodes_tags.id=i.id \
            WHERE nodes_tags.key="religion" \
            GROUP BY nodes_tags.value \
            ORDER BY num DESC \
            LIMIT 1;'):
		return var

#Popular ammenities
def popular_ammenities(cur):
	for var in cur.execute('SELECT value, COUNT(*) as num \
            FROM nodes_tags \
            WHERE key="amenity" \
            GROUP BY value \
            ORDER BY num DESC \
            LIMIT 10'):
		return var


def top_users(cur):
    for var in cur.execute("SELECT e.user,COUNT(*) AS num \
        FROM(SELECT user FROM nodes UNION ALL SELECT user FROM ways) e \
        GROUP BY e.user \
        ORDER BY num DESC \
        LIMIT 10;"):
            return var



if __name__=='__main__':
    conn=sqlite3.connect("NewDelhi.db")
    c=conn.cursor()
    print("Number of nodes:")
    print(num_nodes(c))

    print("Number of ways: ")
    print(num_ways(c))
    print("Number of nodes_tags : ")
    print(num_nodes_tags(c))
    print("Number of ways : ")
    print(num_ways(c))
    print("Number of way_nodes:")
    print(num_ways_nodes(c))
    print("Number of way_tags ")
    print(num_ways_tags(c))
    print("Biggest Religion:")
    print(biggest_religion(c))
    print("Top cuisines:")
    print(top_cuisines(c))
    print("Top users : ")
    print(top_users(c))
    print("Popular ammenities : ")
    print(popular_ammenities(c))
    conn.close()
