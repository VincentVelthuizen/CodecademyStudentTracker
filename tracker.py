import requests
import configparser, json
from lxml import html
from pprint import pprint

DEBUG = False

# Codecademy details
login_url = 'https://www.codecademy.com/login'
url = 'https://www.codecademy.com'
auth_token_xpath = '//*[@id="new-user"]/input[1]/@value'
achievement_xpath = '/html/body/main/article/div/div[2]/div/div[2]/h5/text()'
achievement_xpath = '//h5/text()'

# Load settings
settings_path = 'settings.json'
config = configparser.ConfigParser()
config.read( settings_path )

# Read settings
try:
    user_details = {}
    user_details['user[login]'] = config.get('codecademy','user[login]')
    user_details['user[password]'] = config.get('codecademy','user[password]')

    users = []
    users = json.loads(config.get('participants','usernames'))
    lessons = json.loads(config.get('course_elements','lessons'))
    achievements = set()
    for lesson in lessons:
        achievements.add('Lesson Completed: '+lesson)
except Exception as e:
    print( e )
    print('no credentials given')

# Read Codecademy site
try:
    # Setup session
    session = requests.session()

    login_page = session.get(login_url)
    tree = html.fromstring(login_page.text)
    user_details['authenticity_token'] = list(set(tree.xpath(auth_token_xpath)))[0]
    result = session.post(
	login_url, 
	data = user_details, 
	headers = dict(referer=login_url)
    )
    if DEBUG:
        f = open('login_result.html', 'w+')
        f.write( result.text )
        f.close()

    # Get user achievements
    users_achievements = []
    for user in users:
        achievement_page = session.get(
            url + '/users/' + user + '/achievements',
            headers = dict(referer = url)
        )

        if DEBUG:
            f = open('achievement_result.html', 'w+')
            text = [letter for letter in achievement_page.text if ord(letter) < 128]
            text = ''.join(text)
            f.write( text )
            f.close()
        tree = html.fromstring( achievement_page.text )
        user_achievements = achievements.intersection(set(tree.xpath(achievement_xpath)))
        users_achievements.append((user, len(user_achievements)/len(achievements)))
    pprint( users_achievements )
except Exception as e:
    print( e )
    print('something went wrong getting the user')


