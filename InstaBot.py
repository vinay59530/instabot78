import requests, urllib#for opening and reading URLs

from textblob import TextBlob# library for processing textual data,provides a simple API for diving into common NLP tasks

from textblob.sentiments import NaiveBayesAnalyzer

import matplotlib.pyplot as plt #used to plot pie chart

access_token = '3966572302.75b1a1a.e6d8a82e6b9448e2abc73e6ad69ca81e' #access token of user
base_url = 'https://api.instagram.com/v1/'

def fetch_id(username):#declearing a function to to get the ID of a user
    url = (base_url + 'users/search?q=%s&access_token=%s') % (username, access_token)
    information = requests.get(url).json()
    if information['meta']['code'] == 200:
        if len(information['data']):
            return information['data'][0]['id']
        else:
            return None
    else:
        print "Something Error!\nstatus code other than 200 found"
        exit()


def posts_id(username):#function declaration to get media ID
    id = fetch_id(username)
    if id == None:
        print 'User does not exist!'
        exit()
    url = (base_url + 'users/%s/media/recent/?access_token=%s') % (id, access_token)
    post = requests.get(url).json()

    if post['meta']['code'] == 200:
        if len(post['data']):
            return post['data'][0]['id']
        else:
            print "No recent post available of this user!"
            exit()
    else:
        print "Something Error!\nstatus code other than 200 found"
        exit()


def my_posts():#function declaration to get own posts
    url = (base_url + 'users/self/media/recent/?access_token=%s') % (access_token)
    posts = requests.get(url).json()

    if posts['meta']['code'] == 200:
        if len(posts['data']):
            img_name = posts['data'][0]['id'] + '.jpeg'
            imag_link = posts['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(imag_link, img_name)
            print "Congratulations! Image is downloaded successfully :)"
        else:
            print "Sorry! No post available :("
    else:
        print "Something Error!\nstatus code other than 200 found"


def own_info(): #to get own details
    url = (base_url + 'users/self/?access_token=%s') % (access_token)
    information = requests.get(url).json()
    if information['meta']['code'] == 200:
        if len(information['data']):
            print 'Hey! your username is %s' % (information['data']['username'])
            print "You're following %s people" % (information['data']['counts']['follows'])
            print  "You've %s followers"% (information['data']['counts']['followed_by'])
            print  "You've updated %s posts till now!" % (information['data']['counts']['media'])
        else:
            print "Sorry! user does not exist"
    else:
        print "Something Error!\nstatus code other than 200 found"


def others_info(username):#function declaration to get other user's details
    id = fetch_id(username)
    if id == None:
        print "Sorry! user does not exist"
        exit()
    url = (base_url + 'users/%s?access_token=%s') % (id, access_token)
    information = requests.get(url).json()

    if information['meta']['code'] == 200:
        if len(information['data']):
            print "Your friend's username is %s" % (information['data']['username'])
            print "He/She has %s followers" % (information['data']['counts']['followed_by'])
            print "He/She is following %s people" % (information['data']['counts']['follows'])
            print "And he/she has updated %s posts till now" % (information['data']['counts']['media'])
        else:
            print "It seems your friend is new to instagram\nNo details available"
    else:
        print "Something Error!\nstatus code other than 200 found"


def others_posts(username):##function declaration to get other user's posts
    id = fetch_id(username)
    if id == None:
        print "Sorry! user does not exist"
        exit()
    url = (base_url + 'users/%s/media/recent/?access_token=%s') % (id, access_token)
    post = requests.get(url).json()

    if post['meta']['code'] == 200:
        if len(post['data']):
            img_name = post['data'][0]['id'] + '.jpeg'
            img_link = post['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(img_link, img_name)
            print "Congratulations! Image is downloaded successfully :)"
        else:
            print "Sorry! No post available :("
    else:
        print "Something Error!\nstatus code other than 200 found"


def like(username):##function declaration to like other's recent post
    id = posts_id(username)
    request_url = (base_url + 'media/%s/likes') % (id)
    payload = {"access_token": access_token}
    like = requests.post(request_url, payload).json()
    if like['meta']['code'] == 200:
        print "Like Successful :)"
    else:
        print "Like unsuccessful!\nPlease try again"


def comment(username):#function declaration to comment on other user's recent post
    post = posts_id(username)
    type_comment = raw_input("Type your comment: ")
    payload = {"access_token": access_token, "text" : type_comment}
    url = (base_url + 'media/%s/comments') % (post)
    comment = requests.post(url, payload).json()
    if comment['meta']['code'] == 200:
        print "Comment added successfully! :)"
    else:
        print "Something went wrong! :( \nPlease try again!"


def comments_list(username):#function declaration to get list of comments on other's post
    post = posts_id(username)
    request_url = (base_url + 'media/%s/comments?access_token=%s')% (post,access_token)
    comment_info = requests.get(request_url).json()
    print comment_info['data'][0]['text']


def delete_negative_comment(username):#function declaration to delete negative comments on user's recent post
    media_id = posts_id(username)
    request_url = (base_url + 'media/%s/comments/?access_token=%s') % (media_id, access_token)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (base_url + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, access_token)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()
                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print"positive comment : %s" %(comment_text)
        else:
            print 'Comments not found on the post!'
    else:
        print 'Status code other than 200 received!'


def comparision_piechart(username):##function declaration to show number of positive and negative comments and plot a pie-chart
    media_id = posts_id(username)
    request_url = (base_url + 'media/%s/comments/?access_token=%s') % (media_id, access_token)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)



            for y in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][y]['id']
                comment_text = comment_info['data'][y]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg < blob.sentiment.p_pos):
                    print 'positive comment : %s' % (comment_text)
                    a = y + 1  # positive comments
                    b = x - y  # negative comments
                    print "No. of Positive comments: %s" % (a)
                    print "No. of negative comments: %s" % (b)#Displays correct value when loop ends
                    c = a + b
                    print "Total no. of comments: %s" %(c)

                    # Data to plot
                    labels = 'Positive ', 'Negative'
                    sizes = [a, b]
                    colors = ['gold', 'yellowgreen']
                    explode = (0.1, 0)  # explode 1st slice

                    # Plot
                    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                            autopct='%1.1f%%', shadow=True, startangle=140)

                    plt.axis('equal')
                    plt.show()#Displays correct piechart when loop ends



        else:
            print 'Comments not found on the post!'
    else:
        print 'Status code other than 200 received!'




def begin():#choice menu
    while True:#loop begin
        print"Welcome to instaBot :) \nLet's explore!"
        print "1.Get your details"
        print "2.Get other's details"
        print "3.Get your recent post"
        print "4.Get the recent post of other's"
        print "5.Like the recent post of other's"
        print "6.Get a list of comments done on other's recent post"
        print "7.Make a comment on the recent post of other's"
        print "8.Delete negative comments"
        print "9.Make a pie chart compairing positive and negative comments"
        print "0.Exit Application"
        option = raw_input("Please Choose: ")
        if option == "1":
            own_info()
        elif option == "2":
            username = raw_input("Enter the username of the user: ")
            others_info(username)
        elif option == "3":
            my_posts()
        elif option == "4":
            username = raw_input("Enter the username of the user: ")
            others_posts(username)
        elif option=="5":
           username = raw_input("Enter the username of the user: ")
           like(username)
        elif option=="6":
           username = raw_input("Enter the username of the user: ")
           comments_list(username)
        elif option=="7":
           username = raw_input("Enter the username of the user: ")
           comment(username)
        elif option == "8":
            username =raw_input("Enter the username of the user: ")
            delete_negative_comment(username)
        elif option == "9":
            username =raw_input("Enter the username of the user: ")
            comparision_piechart(username)
        elif option == "0":
            exit()
        else:
            print"Wrong input!\nPlease Try Again"
begin()
