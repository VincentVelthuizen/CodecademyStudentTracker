import requests
from lxml import html

DEBUG = False

login_url = 'https://www.codecademy.com/login'
url = 'https://www.codecademy.com'
auth_token_xpath = '//*[@id="new-user"]/input[1]/@value'
achievement_xpath = '/html/body/main/article/div/div[2]/div/div[2]/h5/text()'
achievement_xpath = '//h5/text()'
user = '<user to check>'

user_details = {
    'user[login]'           :'<Username>',
    'user[password]'        :'<Password',
 
}

try:
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
    achievements = tree.xpath(achievement_xpath)
    print( achievements )
    
except Exception as e:
    print( e )
    print('something went wrong getting the user')
