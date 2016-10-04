import csv

doc_in = []
doc_new = [['test','dat','to','go'],['at','the','end','another']]
# Open and read
with open('out.csv', 'rb') as inText:
    reader = csv.reader(inText)
    for row in reader:
        doc_in.append(row)
inText.close()

for doc in doc_new:
    #print doc
    doc_in.append(doc)

print doc_in

# Store all information in a csv file    
with open("out.csv", "w") as outText:
    writer = csv.writer(outText, delimiter=",")
    writer.writerow(doc_in[0])

    for i in range(1,len(doc_in)):
        out_doc = doc_in[i]
        #print(i, "out", out_doc)
        
        writer.writerow(out_doc)
outText.close()