import csv

data = []

with open("archive_dataset.csv", "r") as f:
    csvreader = csv.reader(f)
    for row in csvreader: 
        data.append(row)

headers = data[0]
planet_data = data[1:]

#Converting all planet names to lower case
for data_point in planet_data:
    data_point[2] = data_point[2].lower()

#Sorting planet names in alphabetical order
planet_data.sort(key=lambda planet_data: planet_data[2])

#Python opens files almost in the same way as in C:
#r+ Open for reading and writing. The stream is positioned at the beginning of the file.
#a+ Open for reading and appending (writing at end of file). The file is created if it does not exist. The initial file position for reading is at the beginning of the file, but output is appended to the end of the file (but in some Unix systems regardless of the current seek position).
with open("Ilyaas_archive_dataset_sorted.csv", "a+") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(planet_data)

#remove blank lines
with open('Ilyaas_archive_dataset_sorted.csv') as input, open('Ilyaas_sorted_WOblanks.csv', 'w', newline='') as output:
     writer = csv.writer(output)
     for row in csv.reader(input):
         if any(field.strip() for field in row):
             writer.writerow(row)
