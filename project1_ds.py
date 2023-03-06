"""
Collaboration with Zachary Currie
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 15:41:54 2023
#67
@author: zach martin & zach currie
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import csv



idlist = []
data=dict()
data2=dict()
l = 1
while(len (data) < 25):
    with urlopen("https://stats.stackexchange.com/questions?tab=newest&page=" + str(l)) as doc:
        soup = BeautifulSoup(doc,"html.parser")
        divs=soup.findAll('div', {'class':"s-post-summary"})
        doc.close()
    l = l + 1
    classlist2 = ["data-user-id"]
    classlist = ["s-avatar"]
    d = 1

    while(d < 16):
        try:
            weep = divs[d].findAll('a', {'class':'s-link'})[0]["href"]
            deep = "https://stats.stackexchange.com" + weep
            response = requests.get(deep)
            soup2 = BeautifulSoup(response.content, 'html.parser')
            comment_elements = soup2.find_all('div', {'class': 'comment-body'})
            comment_count = len(comment_elements)
            edited_indicator = soup2.find('span', {'class': 'fw-bold mr4'})
            a_user_name=(divs[1].find('div', class_="user-details").text.strip())
            a_user_score=(divs[1].find('span', class_="reputation-score").text.strip())
            if edited_indicator is not None:
                edit = True
            else:
                edit = False

            user_id=divs[d].findAll('a', {'class':'s-avatar'})[0]["data-user-id"]
            title=(divs[d].find("h3", class_="s-post-summary--content-title")).text.strip()
            if('[closed]' in title):
                closed = bool(1)
            if('[closed]' not in title):
                closed = bool(0)
            temp=(divs[d].find('div', class_="s-user-card").text.strip())
            y = temp.splitlines()
            name = y[0]
            postid=divs[d].findAll('a', {'class':'s-avatar'})[0]["data-user-id"]
            rep=y[3]
            time=y[6]
            temp=(divs[d].find('div', class_="s-post-summary--stats").text.strip())
            z = temp.splitlines()
            score=int(z[0])
            views=int(z[8])
            answer=int(z[4])
            tags=(divs[d].find('li', class_="d-inline mr4 js-post-tag-list-item").text.strip())
            f = divs[d].find('div', class_="s-post-summary--stats-item has-answers has-accepted-answer")
            if f is None:
                accept = bool(0)
            else:
                accept = bool(1)
          
          
            
    
            z = globals() ["Post_ID:"+postid] = [title,postid,name,user_id,rep,time,score,views,answer,comment_count,edit,accept,tags,closed]
            z2 = globals() ["Post_ID:"+postid] = [postid,a_user_score,a_user_name,user_id,rep,comment_count,accept]
            idlist.append(user_id)
            data["Post_ID:"+postid]= z
            data2["Post_ID"+postid] = z2
            d  = d + 1
        except:
           # print(data)
            d = d + 1
test=1
#data.update([1, "123456"])

questions_file_name = 'stats.stackexchange-questions.csv'
questions_headers = ['Question_Title', 'Question_ID', 'Author_Name', 'Author_ID', 'Author_Rep', 'Question_Post_Time','Question_Score', 'Number_Of_Views', 'Number_Of_Answers', 'Number_Of_Comments', 'Edited', 'Answer_Accepted', 'tags', 'Question_Closed']
with open(questions_file_name, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(questions_headers)
    for post_id, z in data.items():
        title,postid,name,user_id,rep,time,score,views,answer,comment_count,edit,accept,tags,closed = z
        writer.writerow([title,postid,name,user_id,rep,time,score,views,answer,comment_count,edit,accept,tags,closed])

questions_file_name = 'stats.stackexchange-answers.csv'
questions_headers = ['Question_ID', 'Answer_score', 'Author_Name', 'Author_ID', 'Author_Rep','Number_of_Comments', 'Answer_accepted']
with open(questions_file_name, 'w', newline='', encoding='utf-8') as q:
    writer = csv.writer(q)
    writer.writerow(questions_headers)
    for post_id, z2 in data2.items():
        postid,score,name,user_id,rep,comment_count,accept= z2
        writer.writerow([postid,score,name,user_id,rep,comment_count,accept])
print("data added")