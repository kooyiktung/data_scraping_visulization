import csv
import pandas as pd
import datetime
from timeit import default_timer as timer
from instaloader import Instaloader, Profile
from pprint import pprint
'''
REF: 
https://instaloader.github.io/
https://www.geeksforgeeks.org/introduction-to-instaloader-module-in-python/
'''

start = timer()

def read_account():
    f = open('../data/account_input.txt', 'r')
    accounts = f.read()
    p = accounts.split('\n')
    return p

def last_account():
    with open('../data/last.txt', 'r') as f:
        last = f.read()
        last = last.strip()
    return last

def get_complete():
    f = open('../data/completed.txt', 'r')
    accounts_complete = f.read()
    p_complete = accounts_complete.split('\n')
    p_complete = list(set(p_complete))
    return p_complete

def remove(l1, l2):
    # return [first for first, second in zip(l1, l2) if first != second]
    return [x for x in l1 if not any([x in l2])]

# Attributes of Profile class
'''
followers: returns the number of accounts following the given account
followees: returns the number of accounts followed by give account
mediacount: returns the total number of posts
igtvcount: returns the total number of igtv posts
is_private: returns whether account is private or not
biography: returns the description/bio of the account
profile_pic_url: returns the link to the profile picture of the account
external_url: returns the external url (if any)
is_business_account: returns whether the account is a business account or not
business_category_name: returns the type of business account is associated with
'''
def get_profile_info():
    ## Get instance
    L = Instaloader()
    ## Login using the credentials
    '''
    username: personal IG account username
    passwors: personal IG account password
    '''
    username = '***********'
    password = '***********'
    L.login(username, password)
    ## Read account need to get data from txt
    p = read_account()
    last = last_account()
    p_complete = get_complete()
    print('Last account scraped was:', last)
    p = remove(p, p_complete)
    if len(p):
        for profile in p:
            if last in profile and len(last) > 2:
                print(last, profile)
                p.remove(profile)
        print('Resuming from:', p[0])
        PROFILE = p[:]
        print(PROFILE)
        print('Total accounts:', len(PROFILE))
        path = '../data/'
        filename_1 = 'main_account_info_V1.csv'
        csv_1_columns = ['user_id', 'username', 'fullname', 'followers', 'following',
                         'is_verified', 'is_private', 'media_count', 'igtv_count', 'bio',
                         'website', 'is_business', 'business_category_name']
        with open(path + filename_1, 'a', newline='', encoding='utf_8_sig') as csvf:
            csv_writer = csv.writer(csvf)
            csv_writer.writerow(csv_1_columns)
        for i in range(len(PROFILE)):
            pro = PROFILE[i]
            try:
                ## Use Profile class to access metadata of account
                '''
                pro: USERNAME of IG account needed to get data from
                '''
                profile = Profile.from_username(L.context, pro)
                main_followers = profile.followers
                main_dict = dict(
                    main_user_id=profile.userid,
                    main_username=pro,
                    main_fullname=profile.full_name,
                    main_followers=main_followers,
                    main_following_count=profile.followees,
                    main_is_verified=profile.is_verified,
                    main_is_private=profile.is_private,
                    main_media_count=profile.mediacount,
                    main_igtv_count=profile.igtvcount,
                    main_bio=profile.biography,
                    main_website=profile.external_url,
                    main_is_business=profile.is_business_account,
                    main_business_category_name=profile.business_category_name)
                with open(path + filename_1, 'a+', newline='', encoding='utf_8_sig') as csvf:
                    csv_writer = csv.writer(csvf)
                    csv_writer.writerow(main_dict.values())
                ## get followers of each profile
                print('Getting followers from', pro)
                # profile_list = []
                total = 0
                filename_2 = 'account_' + pro + 'follower_info.csv'
                csv_2_columns = ['user_id', 'username', 'fullname', 'is_verified', 'is_private',
                                 'media_count', 'igtv_count', 'follower_count', 'following_count',
                                 'bio', 'website', 'is_business', 'business_category_name']
                with open(path + filename_2, 'a', newline='', encoding='utf_8_sig') as csvf:
                    csv_writer = csv.writer(csvf)
                    csv_writer.writerow(csv_2_columns)
                for account in profile.get_followers():
                    try:
                        total += 1
                        account_dict = dict(
                            user_id=account.userid,
                            username=account.username,
                            fullname=account.full_name,
                            is_verified=account.is_verified,
                            is_private=account.is_private,
                            media_count=account.mediacount,
                            igtv_count=account.igtvcount,
                            follower_count=account.followers,
                            following_count=account.followees,
                            bio=account.biography,
                            website=account.external_url,
                            is_business=account.is_business_account,
                            business_category_name=account.business_category_name)
                        # profile_list.append(account_dict)
                        with open(path + filename_2, 'a+', newline='', encoding='utf_8_sig') as csvf:
                            csv_writer = csv.writer(csvf)
                            csv_writer.writerow(account_dict.values())
                        print('********************Total followers scraped:', total, 'out of', main_followers)
                        print('Time:', str(datetime.timedelta(seconds=(timer() - start))))
                    except Exception as e:
                        print(e)
                # df = pd.DataFrame(profile_list)
                # filename_2 = 'account_' + pro + 'follower_info.csv'
                # df.to_csv(path + filename_2, index=False, encoding='utf_8_sig')
                ## saving the last account for resume
                f = open('../data/last.txt', 'w+')
                f.write(pro)
                f.close()
                ## log of completed account
                f = open('../data/completed.txt', 'a+')
                f.write(pro + '\n')
                f.close()

            except Exception as e:
                print(e)

if __name__ == '__main__':
    # help(Profile)
    # get = dir(Profile)
    # pprint(get)
    # read_account()
    # last_account()
    # get_complete()
    get_profile_info()