import csv, json, os
from pairs import Pairs

DIR_CSV = 'csv/'
DIR_JSON = 'JSON/'

users_exp_one ='expone-curr-results'
users_exp_two ='curr-results'

emails_exp ='users'

pairs_exp_one = 'expone-pairs'
pairs_exp_two ='pairs'

"""
csv updates
- save_to_csv
- save_emails
- save_user_pairs_to_csv
- get_results_json
- get_user_all_pairs
- get_user_json
- open_json

"""

# Setters for results to CSV
def save_to_csv(doc_new, name, new):
    # Saves all results on exisiting file
    doc_in = []
    file_csv = DIR_CSV + name + '.csv'
    
    # Check file exists
    if os.path.exists(file_csv) == True:
        if new == False:
            with open(file_csv, 'rb') as inText:
                reader = csv.reader(inText)
                for row in reader:
                    doc_in.append(row)
                inText.close()
        else:
            os.remove(file_csv)
            
    for doc in doc_new:
        doc_in.append(doc)
   
    
    # Store all information in a csv file
    with open(file_csv, 'w') as outText:
        writer = csv.writer(outText, delimiter=",")
        writer.writerow(doc_in[0])
    
        for i in range(1,len(doc_in)):
            writer.writerow(doc_in[i])
    outText.close()

def save_emails_csv(username, email):
    # save emails
    e_doc=[]
    for i in range(0,len(email)):
        row=[username[i],email[i]]
        e_doc.append(row)
    save_to_csv(e_doc, 'email', False)

def save_user_to_csv(json, name):

    doc_new=[]
    for i in range(0,len(json['username'])):
        row=[json['username'][i],json['dob'][i],json['gender'][i],json['allergies'][i],json['diet'][i],json['occupation'][i],json['nationality'][i],json['permission'][i],json['completed'][i]]
        # save all info to a csv file
        doc_new.append(row)
    
    save_to_csv(doc_new, name, True)

def save_user_pairs_to_csv(json, exp):
    # formats and then saves a users pair preferances to a csv file
    doc_pairs = []
    doc_ui = []
    doc_exp =[]
    row =[]
    pairs = Pairs()
    for p in json:
        user = str(p[0])
        for i in range(0, len(p[1]['index'])):
            # pairwise details
            left_p, right_p = pairs.get_pairs(p[1]['index'][i])
            row=[ user, exp, p[1]['index'][i], left_p, right_p, p[1]['value'][i]]
            doc_pairs.append(row)
            # ui details
            row=[user,exp,p[1]['index'][i],p[1]['pic'][i],p[1]['time'][i],p[1]['t_at'][i],p[1]['scrn_h'][i],p[1]['scrn_w'][i],p[1]['scroll_x'][i], p[1]['scroll_y'][i]]
            doc_ui.append(row)
        
        # details of experiment   
        doc_exp.append([user,exp,str(p[1]['date']),str(p[1]['browser'])])
    #print doc_ui
    # save seperate documents
    save_to_csv(doc_pairs, 'pairwise', True)
    save_to_csv(doc_ui, 'ui-details', True)
    save_to_csv(doc_exp, 'users-exp-details', True)
    
    

# Getters for results to JSON
def get_results_json(name, exp):
    username=[]
    dob=[]
    gender=[]
    allergies=[]
    diet=[]
    occupation=[]
    nationality=[]
    permission=[]
    completed=[]
    data = open_json(name)
    return {
            'username': data['username'],
            'dob' : data['dob'],
            'gender' : data['gender'],
            'allergies': data['allergies'],
            'diet': data['diet'],
            'occupation': data['occupation'],
            'nationality': data['nationality'],
            'permission' : data['permission'],
            'completed' : data['completed time'],
            }

def get_user_all_pairs_json(name, exp):
    
    data = open_json(name)[exp]
    
    # loop through pairs
    all_pairs = []
    #print  'this is a admin: ', data[0]['admin'], '----------'
    #print  'this is a test1: ', data[1]['test1'], '----------'
    for user in range(0, len(data)):
        #print user, 'this is a u: ', data[user], '!!----------'
        users = data[user]
        for u in data[user]:
            user_pair={
            'value': users[u][0]['value'],
            'index': users[u][0]['index'],
            'pic': users[u][0]['pic'],
            'time':  users[u][0]['time'],
            't_at': users[u][0]['t_at'],
            'date': users[u][0]['date'],
            'browser' : users[u][0]['browser'],
            'scrn_h' :  users[u][0]['scrn_h'],
            'scrn_w':  users[u][0]['scrn_w'],
            'scroll_x' :  users[u][0]['scroll_x'],
            'scroll_y' :  users[u][0]['scroll_y'],
            }
            user_pairs = [u, user_pair]
            all_pairs.append(user_pairs)
    return all_pairs
    
def get_user_json(name):
    username=[]
    mail=[]
    
    data = open_json(name)
    return {'username': data['username'], 'mail' :  data['mail'],}
    
def open_json(name):
    # file location
    file = DIR_JSON + name + '.json'
    # open 
    with open(file) as open_json:
        data = json.load(open_json)
    return data

# Experiment one
#all_pairs = get_user_all_pairs_json(pairs_exp_one, 'exp_1')
#save_user_pairs_to_csv(all_pairs, 2)

#all_users = get_results_json(users_exp_one,'exp_1')
#save_user_to_csv(all_users, 'expone-user-details')

# Experiment two
all_pairs = get_user_all_pairs_json(pairs_exp_two, 'exp_2')
save_user_pairs_to_csv(all_pairs, 2)

all_users = get_results_json(users_exp_two,'exp_2')
save_user_to_csv(all_users, 'user-details')

all_users = get_user_json(emails_exp)
save_emails_csv(all_users['username'], all_users['mail'])
