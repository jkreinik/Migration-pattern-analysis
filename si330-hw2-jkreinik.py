import csv
from collections import defaultdict
from pprint import pprint

def filter_year(filename):
    with open(filename,'r') as input_file:
        country_data_reader = csv.DictReader(input_file, delimiter = "\t")
        with open('world-bank-output-hw2-jkreinik.csv','w') as output_file:
            country_data_writer = csv.DictWriter(output_file, fieldnames=country_data_reader.fieldnames,
                                                   extrasaction='ignore',delimiter=',',quotechar='"')
            country_data_writer.writeheader()
            for row in country_data_reader:
                try:
                    if row['Date'].split('/')[2] == '2000':
                        country_data_writer.writerow(row)
                except:
                     pass


def read_directed_graph_from_csv(filename, source_column, dest_column, weight_column):
    graph = defaultdict(list)  # returns an empty list if looking up key that doesn't exist
    with open(filename, 'r', newline='') as input_file:
        graph_file_reader = csv.DictReader(input_file, delimiter=',', quotechar='"')
        for row in graph_file_reader:
            if row[weight_column] == '' or row[weight_column] == '..':
                row[weight_column] = '0'

            connected_nodes = (row[dest_column], row[weight_column])
            graph[row[source_column]].append(connected_nodes)
            graph[row[source_column]].sort(key = lambda x: float(x[1]), reverse = True )


    return (graph)

def location_writer():
    nodes = {}
    edge_dict_list = []
    with open('locations.csv','r') as input_file:
        location_reader = csv.DictReader(input_file, delimiter = ',', quotechar = '"')
        with open('nodes.csv','w', newline = "") as output_file:
            location_writer = csv.DictWriter(output_file,
                                                   fieldnames=['country', 'latitude', 'longitude'],
                                                   extrasaction='ignore',delimiter=',',quotechar='"')
            location_writer.writeheader()
            for row in location_reader:
                row['country'] = row['Country Name']
                row['latitude'] = row['Latitude']
                row['longitude'] = row['Longitude']
                nodes[row['Country Name']] = (row['Latitude'], row['Longitude'])
                location_writer.writerow(row)

    with open('world_bank_migration.csv', 'r', newline="") as input_file2:
        edge_reader = csv.DictReader(input_file2, delimiter = ',', quotechar = '"')
        with open('si330-hw2-edges-jkreinik.csv','w') as output_file2:
            edge_writer = csv.DictWriter(output_file2,fieldnames=['start_country','end_country','start_lat','start_long', 'end_lat', 'end_long', 'count'],extrasaction='ignore',delimiter=',',quotechar='"')
            edge_writer.writeheader()
            edge_dict = {}
            for row in edge_reader:
                row['start_country'] = row['Country Origin Name']
                row['end_country'] = row['Country Dest Name']

                try:
                    row['count'] = float(row['2000 [2000]'])
                except:
                    row['count'] = 0

                try:
                    row['start_lat'] = nodes[row['Country Origin Name']][0]
                    row['start_long'] = nodes[row['Country Origin Name']][1]
                    row['end_lat'] = nodes[row['Country Dest Name']][0]
                    row['end_long'] = nodes[row['Country Dest Name']][1]
                except:
                    pass
                edge_dict_list.append(row)

            sorted_edge_dict = sorted(edge_dict_list, key = lambda x: -x['count'])[0:1000]
            for edge in sorted_edge_dict:
                edge_writer.writerow(edge)













def main():
    file = "world_bank_country_data.txt"
    filter_year(file)

    migration_outflow_graph = read_directed_graph_from_csv("world_bank_migration.csv",
                                                           "Country Origin Name", "Country Dest Name", "2000 [2000]")

    print(migration_outflow_graph["Canada"][0:5])

    destinations = read_directed_graph_from_csv("world_bank_migration.csv",
                                                           "Country Origin Name", "Country Dest Name", "2000 [2000]")
    origins = read_directed_graph_from_csv("world_bank_migration.csv",
                                                           "Country Dest Name", "Country Origin Name", "2000 [2000]")

    with open('world_bank_country_data.txt','r') as input_file:
        world_bank_reader = csv.DictReader(input_file, delimiter = '\t', quotechar = '"')
        with open('world-bank-output-hw2-jkreinik.csv','w', newline = "") as output_file:
            world_bank_writer = csv.DictWriter(output_file,
                                                   fieldnames=world_bank_reader.fieldnames + ['Migration: Top 3 destinations', 'Migration: Top 3 sources'],
                                                   extrasaction='ignore',delimiter=',',quotechar='"')
            world_bank_writer.writeheader()
            for row in world_bank_reader:
                try:
                    if row['Date'].split('/')[2] == '2000':
                        row['Migration: Top 3 destinations'] = destinations[row['Country Name']][0:3]
                        row['Migration: Top 3 sources'] = origins[row['Country Name']][0:3]
                        world_bank_writer.writerow(row)

                except:
                    pass

    location_writer()

if __name__ == '__main__':
    main()