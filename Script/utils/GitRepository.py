import os
from git.repo import Repo
from git.repo.fun import is_git_dir


class GitRepository(object):
    """
    git仓库管理
    """

    def __init__(self, local_path, repo_url, branch='master'):
        self.local_path = local_path
        self.repo_url = repo_url
        self.repo = None
        self.initial(repo_url, branch)

    def initial(self, repo_url, branch):
        """
        初始化git仓库
        :param repo_url:
        :param branch:
        :return:
        """
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

        git_local_path = os.path.join(self.local_path, '.git')
        if not is_git_dir(git_local_path):
            self.repo = Repo.clone_from(repo_url, to_path=self.local_path, branch=branch)
        else:
            self.repo = Repo(self.local_path)

    def pull(self):
        """
        从线上拉最新代码
        :return:
        """
        self.repo.git.pull()

    def branches(self):
        """
        获取所有分支
        :return:
        """
        branches = self.repo.remote().refs
        return [item.remote_head for item in branches if item.remote_head not in ['HEAD', ]]

    def commits(self):
        """
        获取所有提交记录
        :return:
        """
        commit_log = self.repo.git.log('--pretty={"commit":"%H","author":"%an","date":"%cd"}',
                                       date='format:%Y-%m-%d %H:%M')
        log_list = commit_log.split("\n")
        return [eval(item) for item in log_list]

    def tags(self):
        """
        获取所有tag
        :return:
        """
        return [tag.name for tag in self.repo.tags]

    def get_tag_commit_hash(self, tag_name):
        tag = self.repo.tags[tag_name]
        tag_commit = tag.commit
        return tag_commit

    def get_commit_hash_by_index(self, index):
        commit = list(self.repo.iter_commits())[index]
        return commit

    def get_commit_index(self, commit_sha):
        # 遍历commit历史并计数
        count = 0
        commit_list = list(self.repo.iter_commits())
        for c in reversed(commit_list):
            if c.hexsha == commit_sha:
                break
            count += 1

        return count

    def change_to_branch(self, branch):
        """
        切换分值
        :param branch:
        :return:
        """
        self.repo.git.checkout(branch)

    def change_to_commit(self, commit):
        """
        切换commit
        :param commit:
        :return:
        """
        self.repo.git.reset('--hard', commit)

    def change_to_tag(self, tag):
        """
        切换tag
        :param tag:
        :return:
        """
        self.repo.git.checkout(tag)


if __name__ == '__main__':
    pro_name = 'maven-dependency-plugin'
    local_path = 'C:\\Users\\lxyeah\\Desktop\\maven-dependency-plugin\\'
    remote_path = 'https://github.com/apache/maven-dependency-plugin.git'
    repo = GitRepository(local_path, remote_path)
    commits = repo.commits()
    for commit in commits:
        print('Now at ' + commit['commit'])
