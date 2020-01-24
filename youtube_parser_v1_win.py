#! python3
#youtube_parser.py
import requests, bs4, re, openpyxl, calendar, os
from os.path import expanduser
from statistics import mean
from datetime import datetime
from template_maker import template_maker
#this function will expand sub counts to full numbers.
def number_expander(x):
    num = 0
# K to a thousand
    if '千' in x:
        if len(x) > 1:
            num = int(float(x.replace('千', ''))* 1000)  
# M to a million
    elif '萬' in x:
        if len(x) > 1:
            num = int(float(x.replace('萬', ''))* 1000000) 
# less than a thousand
    else:
        num = int(x)
    return int(num)

#These scrape webpages with beautiful soup.
#arg1 get request, arg2 objtag we're scraping for, arg3 class
#of obj we're scraping for.
#The first one returns a single text value
def parser(res, htmltag, htmlclass):
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    target = soup.find(htmltag, {'class': htmlclass})
    return(target.get_text())
#this one returns several values in a list.
def parser_find_all(res, htmltag, htmlclass):
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    target = soup.find_all(htmltag, {'class': htmlclass})
    return(target)

#this regex gets video views from an unordered list
views_regex = re.compile(r'\d{2,}')
#this regex matches 'days' and 'weeks' to see how many videos were
#uploaded this month.
last_month_regex = re.compile(r'(週|天)前')

#load excel workbook, create a template for future workbooks if
#it's not in the directory already
try:
    wb = openpyxl.load_workbook('template.xlsx')
except FileNotFoundError:
    template_maker()
    wb = openpyxl.load_workbook('template.xlsx')
sheet = wb.active

upl_list = [0, 0, 0, 0, 0, 0, 0]

#Get our channel ids from the txt file where they're stored.
with open('channel_ids.txt') as f:
    channel_list = f.read().splitlines()
print('Working...')
#this for loop finds each data point we want and adds them to our
#spreadsheet for each channel id
for i, name in enumerate(channel_list, start = 2):
    
    col = str(i)
    mainpage_res = requests.get('https://www.youtube.com/channel/' + name)
    videos_res = requests.get('https://www.youtube.com/channel/' + name + '/videos')
    about_res = requests.get('http://www.youtube.com/channel/' + name + '/about')
    
    #get user's channel name ---------mainpage
    channel_name = parser(mainpage_res, 'span', "qualified-channel-title-text")
    sheet['A' + col] = channel_name
    
    print('Collecting data on ' + channel_name + '\'s channel...')
    
    #------SUBSCRIBERS-----
    #get subcount, main function to convert to integer---------mainpage
    subs = parser(mainpage_res, 'span', 'yt-subscription-button-subscriber-count-branded-horizontal subscribed yt-uix-tooltip')
    sub_count = number_expander(subs)
    sheet['B' + col] = sub_count
    
    #------TOTAL VIEWS----- ---------about
    about_stats = parser(about_res, 'span', 'about-stat')
    #pull views from about stats
    total_views_text = about_stats.replace(',','')
    total_views = views_regex.search(total_views_text)
    sheet['C' + col] = total_views.group()
    
    #-----AVERAGE UPLOAD RATE-------  ---------videos
    six_month_lib = parser_find_all(videos_res, 'ul', 'yt-lockup-meta-info')
    #search uploads for uploads in the last month
    last_month = [i for i in six_month_lib if last_month_regex.search(str(i))]
    upl_list[0] += len(last_month)
    for n in range(1,7):
        upl_list[n] = sum(1 for i in six_month_lib if re.search(str(n) + ' 個月前', str(i)))
    avg_upl_rate = round(mean(upl_list))
    sheet['E' + col] = avg_upl_rate
    
    #-------AVERAGE VIEWS AND ENGAGEMENT------- ---------mainpage
    #find 10 most recent uploads (or fewer if they're new) and pull
    #views and the engagement
    
    #pull view number out of the unordered list using regex, add ---------mainpage
    #view number to views_list
    recent_upl = parser_find_all(mainpage_res, 'ul', 'yt-lockup-meta-info')
    recent_videos = parser_find_all(mainpage_res, 'a', 'yt-uix-sessionlink yt-uix-tile-link spf-link yt-ui-ellipsis yt-ui-ellipsis-2')
    num_open = min(10, len(recent_upl))
    upl_text = [recent_upl[i].get_text().replace(',','')for i in range(num_open)]
    views_list = [int(views_regex.search(upl_text[i]).group()) for i in range(len(upl_text))]
    for j in range(num_open):
        recent_res = requests.get('https://www.youtube.com/' + recent_videos[i].get('href'))
        #pull likes, dislikes, comments, and views from each video
        #page to get engagement as a percentage (L + D + C/ V)
        #-------still need comments-----------
        likes = parser(recent_res, 'button', 'yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-like-button like-button-renderer-like-button-clicked yt-uix-button-toggled hid yt-uix-tooltip')
        dislikes = parser(recent_res, 'button', 'yt-uix-button yt-uix-button-size-default yt-uix-button-opacity yt-uix-button-has-icon no-icon-markup like-button-renderer-dislike-button like-button-renderer-dislike-button-unclicked yt-uix-clickcard-target yt-uix-tooltip')     
    #average views_list
    avg_views = round(mean(views_list))
    sheet['D' + col] = avg_views
        
current_day = str(datetime.now().day)
current_month = calendar.month_abbr[datetime.now().month]
current_year = str(datetime.now().year)
#file named after date script is run
file_name = current_month + ' ' + current_day +', ' + current_year
#if needed, create a directory to save the file in named after
#current month and year.
home = expanduser('~')
file_path = home +'/' + current_month + ' ' + current_year
if not os.path.exists(file_path):
    print('Making new directory for ' + current_month + '...')
    os.makedirs(file_path)
    
wb.save('%s/%s.xlsx' % (file_path, file_name))
print('Done!')