import csv

"""
Clean Data
 will clean any non permission users,
 will clean any null results.

- open_csv
- save_csv
- check_permisions
- bad_value 
- clean_values

"""


DIR_CSV = 'csv/raw/'
DIR_CSV_CEAN = 'csv/clean/'
DIR_CSV_BAD = 'csv/bad/'

c_permissions_username = 'controlled-7.10.2016/email'
c_pairs_data_expone = 'controlled-7.10.2016/exp-one/expone-pairwise'
c_pairs_data_exptwo = 'controlled-7.10.2016/exp-two/pairwise'
c_pairs_details_expone = 'controlled-7.10.2016/exp-one/expone-ui-details'
c_pairs_details_exptwo = 'controlled-7.10.2016/exp-two/ui-details'
permissions_username = 'heroku-7.10.2016/email'
pairs_data = 'heroku-7.10.2016/pairwise'
pairs_details = 'heroku-7.10.2016/ui-details'
user_details = 'heroku-7.10.2016/user-details'

out_c_pairs_data_expone = 'controlled/clean_expone-pairwise'
out_c_pairs_data_exptwo = 'controlled/clean_pairwise'
out_c_pair_expone_details = 'controlled/clean_expone-pairwise_details'
out_c_pair_exptwo_details = 'controlled/clean_pairwise_details'
out_c_user_details = 'controlled/clean_details'
out_c_users = 'controlled/clean_email'
out_pairs_data = 'uncontrolled/clean_pairwise'
out_pair_details = 'uncontrolled/clean_pairwise_details'
out_user_details = 'uncontrolled/clean_details'
out_users = 'uncontrolled/clean_email'

out_c_bad_pairs_expone ='controlled/bad_pairs_expone'
out_c_bad_pairs_exptwo ='controlled/bad_pairs_exptwo'
out_bad_pairs ='uncontrolled/bad_pairs'

# Get file
def open_csv(name):
    # file location
    file = name + '.csv'
    # open
    data = []
    with open(file) as open_csv:
        reader = csv.reader(open_csv)
        for row in reader:
            data.append(row)
    return data
    
# Save csv
def save_csv(doc_out, name):
    
    if len(doc_out) > 0:
        
        # file location
        file = name + '.csv'
        
        # Store all information in a csv file
        with open( file, 'w') as outText:
            writer = csv.writer(outText, delimiter=",")
            for i in range(0,len(doc_out)):
                writer.writerow(doc_out[i])
        outText.close()

# Remove Non permision Users
def check_permisions(pairs_list, user_list, save_name):
    pairs = open_csv(pairs_list)
    users = open_csv(user_list)
    pairs_clean = []
    pairs_bad = []
    
    # check for permitted users
    user_in = {}
    for row in pairs:
        if row[0] in user_in: pass
        else: user_in [ row[0] ]= False
    
    for row in users:
        if row[0] in user_in: user_in [ row[0] ]= True
        
    print save_name, user_in
    
    for row in pairs:
        if user_in[ row[0] ] == False: pairs_bad.append(row)
        else: pairs_clean.append(row)
        
    print 'pairs_bad: ', len(pairs_bad)
    print 'pairs_clean: ', len(pairs_clean)
    
    save_csv( pairs_clean, DIR_CSV_CEAN + save_name)
    save_csv( pairs_bad, DIR_CSV_BAD + save_name +'_no_permission')
    
# Check for bad data
def bad_value(row):
    if int(row[-1]) == 2: return True, row[0], row[2]
    else: return False, row[0], row[2]

def is_clean(user, user_doc):
    # checks for bad users
    users = open_csv(user_doc)
    for row in users:
        if user == row[0]: return True
        else: pass
    return False

# Clean bad values
def clean_values( doc_raw, doc_clean, doc_bad):
    raw = open_csv(doc_raw)
    clean = []
    bad = []
    dirty = []
    users_bad = {}
    
    for row in raw:
        a, b, c = bad_value(row)
        if a == True:
            bad.append(row)
            if b in users_bad:    users_bad[b] = users_bad[b] + 1
            else:  users_bad[b] = 1
            print b,c
        else: pass
        
    for row in raw:
        if row[0] in users_bad:
            if users_bad[ row[0] ] > 8: pass
            elif users_bad[row[0]]: dirty.append(row)
        else: clean.append(row)
    
    print 'doc_clean: ', doc_clean, 'doc_bad: ', doc_bad, 'users_bad: ', users_bad
    save_csv( clean, DIR_CSV_CEAN + doc_clean)
    save_csv( bad, DIR_CSV_BAD + doc_bad)
    save_csv(dirty, DIR_CSV_BAD + doc_bad+'_dirty')
    
    bad_users =[]
    for user in users_bad:
        row =[user, users_bad[user]]
        bad_users.append(row)
        
    save_csv(bad_users, DIR_CSV_BAD + doc_bad +'_usernames')
    
    clean_user = []
    users_clean ={}
    for row in clean:
        if row[0] not in clean_user: clean_user.append(row[0])
            
    save_csv(clean_user, DIR_CSV_CEAN + doc_clean +'_usernames')

# Clean bad details
def clean_details(doc_raw, doc_clean_users, out_doc):        
    
    # Take in raw pair details doc and get rid of bad details
    data = open_csv(doc_raw)
    clean_doc =[]
    for row in data:
        if is_clean(row[0], doc_clean_users) == True: clean_doc.append(row)
        else:pass
    
    save_csv(clean_doc, out_doc)

# Contolled exp one
#check_permisions( DIR_CSV + c_pairs_data_expone, DIR_CSV + c_permissions_username, out_c_pairs_data_expone)
#clean_values( DIR_CSV_CEAN + out_c_pairs_data_expone, out_c_pairs_data_expone, out_c_bad_pairs_expone)
clean_details( DIR_CSV + c_pairs_details_expone, DIR_CSV_CEAN +'controlled/clean_expone-pairwise_usernames', DIR_CSV_CEAN + out_c_pair_expone_details)

# Contolled exp two
#check_permisions( DIR_CSV + c_pairs_data_exptwo, DIR_CSV + c_permissions_username, out_c_pairs_data_exptwo)
#clean_values( DIR_CSV_CEAN + out_c_pairs_data_exptwo, out_c_pairs_data_exptwo, out_c_bad_pairs_exptwo)
clean_details( DIR_CSV + c_pairs_details_exptwo, DIR_CSV_CEAN +'controlled/clean_pairwise_usernames', DIR_CSV_CEAN + out_c_pair_exptwo_details)

# Uncontolled exp two
#check_permisions( DIR_CSV + pairs_data, DIR_CSV + permissions_username, out_pairs_data)
#clean_values( DIR_CSV_CEAN + out_pairs_data, out_pairs_data, out_bad_pairs)
clean_details( DIR_CSV + pairs_details, DIR_CSV_CEAN +'uncontrolled/clean_pairwise_usernames', DIR_CSV_CEAN + out_pair_details)
