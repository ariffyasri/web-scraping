# tested using Python 2

import mechanize
import cookielib
from bs4 import BeautifulSoup
import html2text
import re

# Browser
br = mechanize.Browser()



# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(False)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize.HTTPRefreshProcessor(), max_time=1)

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.addheaders = [
					('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh_CN) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0 baidubrowser/1.x Safari/534.7'),
                    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                    ('Accept-Language', 'en-US,en;q=0.5'),
                    ('Accept-Encoding', 'gzip,deflate'),
                    ('Referer', 'http://www.jobstreet.com.my/en/job-search/job-vacancy.php?ojs=2&key=data+analyst')]

# The site we will navigate into, handling it's session
br.open('https://myjobstreet.jobstreet.com.my/home/login.php?site=MY&language_code=en&nrfr=1&go=JOB-ADS')


# Select the second (index one) form (the first form is a search query box)
br.select_form(nr=2)

# User credentials
br.form['login_id'] = 'email'
br.form['password'] = 'password'


# Login
br.submit()

# for csv file to be opened using excel
print 'sep=;'


# edit the keyword, if have space, use '+'
keyword = 'data+analyst'

# set different user agent
ua = ['Mozilla/5.0 (Windows; U; Windows NT 6.1; zh_CN) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0 baidubrowser/1.x Safari/534.7',
	'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; baidubrowser 1.x)',
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh_CN) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0 baidubrowser/1.x Safari/534.7',
	'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3) Gecko/20090305 Firefox/3.1b3 GTB5',
	'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; ko; rv:1.9.1b2) Gecko/20081201 Firefox/3.1b2',
	'Mozilla/5.0 (X11; U; SunOS sun4u; en-US; rv:1.9b5) Gecko/2008032620 Firefox/3.0b5',
	'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.8.1.12) Gecko/20080214 Firefox/2.0.0.12']



total =1
total_salary = 1
link_jobs = br.open('http://www.jobstreet.com.my/en/job-search/job-vacancy.php?key='+keyword+'&area=2&experience-min=-1&experience-max=-1&classified=1&salary-option=on&job-posted=0&src=1&ojs=4').read()

for page in range(40):
	ua_index = page%6
	br.addheaders = [
					('User-Agent', ua[ua_index]),
                    ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                    ('Accept-Language', 'en-US,en;q=0.5'),
                    ('Accept-Encoding', 'gzip,deflate'),
                    ('Referer', 'http://www.jobstreet.com.my/en/job-search/job-vacancy.php?key='+keyword+'&area=1&option=1&job-source=1%2C64&classified=1&job-posted=0&sort=2&order=0&pg='+str(page+1)+'&src=16&ojs=21')]
	link_jobs = br.open('http://www.jobstreet.com.my/en/job-search/job-vacancy.php?key='+keyword+'&area=2&option=1&job-source=1%2C64&classified=1&job-posted=0&sort=2&order=0&pg='+str(page+1)+'&src=16&ojs=21').read()

	soup = BeautifulSoup(link_jobs, 'html.parser')
	

	for i in range(20):

		job = 'job_desc_summary_' + str(i+1)
		string = 'position_title_' + str(i+1)

		link_href = ''
		for link in soup.find_all("a", id=string, href=True):
			link_href = link['href']
			

		salary = soup.find_all("ul", id=job)
		string = salary[0]
		salary_search = re.search('<font class="">(.*)</font>', str(string), re.IGNORECASE)

		salary = ''
		if salary_search:
			salary = salary_search.group(1)
		else:
			salary = 'Undisclosed'

		

		link_desc = br.open(link_href).read()

		soup_desc =  BeautifulSoup(link_desc, 'html.parser')

		title = soup_desc.find_all("h1", id='position_title')
		striphtmltag = re.compile(r'<.*?>')
		title_search = striphtmltag.sub('',str(title))


		exp = soup_desc.find_all("p", id='years_of_experience')
		experience_search = re.search('<span id="years_of_experience" itemprop="experienceRequirements">(.*)</span>', str(exp), re.IGNORECASE)
		
		experience = ''
		if experience_search:
			experience = experience_search.group(1)
		else:
			experience = 'Undisclosed'


		loc = soup_desc.find_all("p", attrs={'class': 'main_desc_detail'})
		location_search = re.search('<span class="single_work_location" id="single_work_location">(.*)</span>', str(loc), re.IGNORECASE)

		location = ''
		if location_search:
			location = location_search.group(1)
		else:
			location = 'Undisclosed'

		job_desc = soup_desc.find_all("div", id='job_description')
		job_desc_search = re.search('<div class="unselectable wrap-text" id="job_description" itemprop="description">(.*)</div>', str(job_desc), re.IGNORECASE)

		job_desc = ''
		if job_desc_search:
			job_desc = job_desc_search.group(1)
			job_desc = job_desc.replace(';',',')
		else:
			job_desc = 'Undisclosed'


		print(str(total)+';'+title_search+';'+salary+';'+experience+';'+location+';'+job_desc)
		total =total + 1
		