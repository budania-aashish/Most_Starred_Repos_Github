import requests
import json
import hashlib
from bs4 import BeautifulSoup
from operator import itemgetter
import locale

from flask import Flask,request,make_response

app = Flask(__name__)

@app.route('/repos', methods=['GET','POST'])
def post_repos():
	if request.method == 'POST':
		org_id = request.json['org']
		page_url = 'https://github.com/' + org_id
		page = requests.get(page_url)

		soup = BeautifulSoup(page.text, 'html.parser')
		pages=1

		if soup.find("div",{"class":"paginate-container"}):
			pages=int(soup.find("div",{"class":"paginate-container"}).find("div",{"class":"pagination"}).find("em",{"class":"current"}).get('data-total-pages'))

		response=[]

		for i in range(1,pages+1):
			page = requests.get(page_url + '?page='+str(i))
			soup = BeautifulSoup(page.text, 'html.parser')

			org_repos = soup.find(id="org-repositories")
			repo_list = org_repos.find("div",{"class":"org-repos repo-list"})

			repos=repo_list.find("ul").find_all("li", {"class":"public source d-block py-4 border-bottom"})

			for j in range(len(repos)):
				name=repos[j].find("div",{"class":"flex-justify-between"} or {"class":"flex-justify-between d-flex"}).find("div",{"class":"flex-auto"}).find("h3",{"class":"wb-break-all"}).get_text().replace("\n","").strip()
				stars=int((repos[j].find("div",{"class":"text-gray f6 mt-2"}).find_all("a",{"class":"muted-link mr-3"})[1].get_text().replace("\n","").strip()).replace(",",""))
				response.append([name,stars])

		response.sort(key=lambda x: x[1],reverse=True)
		print(response[:3])
		
		result_json = {
			"results":[
				{"name":response[0][0], "stars":response[0][1]},
				{"name":response[1][0], "stars":response[1][1]},
				{"name":response[2][0], "stars":response[2][1]},
			]
		}
		print(result_json)
		
		return json.dumps(result_json)

	else:
		return "Please do the post request repo"
	

if __name__ == '__main__':
	app.run(debug = True)