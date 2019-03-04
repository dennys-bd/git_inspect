import datetime
import http
import json
import requests

from git_inspect.celery import app
from .models import Repository, Commit

@app.task
def recover_commits(repository_id):
    repo = Repository.objects.select_related().get(id=repository_id)
    if repo.commit_set.count() > 0:
        pass
    else:
        since = datetime.date.today()  - datetime.timedelta(days=30)
        sincestr = since.strftime('%Y-%m-%D')
        req = requests.get(
            f'https://api.github.com/repos/{repo.full_name}/commits?since={sincestr}',
            headers={
                'Authorization': f'token {repo.user.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
        )

        if req.status_code == http.HTTPStatus.OK:
            json_data = json.loads(req.text)
            for c_data in json_data:
                try:
                    commit = Commit(
                        url=c_data['html_url'],
                        author=c_data['commit']['author'],
                        commiter=c_data['commit']['committer'],
                        message=c_data['commit']['message'],
                        repository=repo,
                    )
                    commit.save()
                except Exception:
                    print('exception')
                    pass
