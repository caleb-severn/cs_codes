# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 23:04:31 2020

@author: caleb
"""
import base64
from github import Github
from github import InputGitTreeElement

def push():
    user = "caleb-severn.github.io"

    token = "4f68e4e0e6062d40d319b9ceb680106da3315a84"
    location = "https://github.com/caleb-severn/caleb-severn.github.io"
    #4f68e4e0e6062d40d319b9ceb680106da3315a84
    g = Github(token)
    repo = g.get_user().get_repo('caleb-severn.github.io')
    file_list = [
        "C://Users/user/Documents/GitHub/caleb-severn.github.io/world-news.html",
        "C://Users/user/Documents/GitHub/caleb-severn.github.io/projects.html",
    
    ]
    
    file_names = [
        'world-news.html',
        'projects.html',
    
    ]
    commit_message = 'python update 2'
    master_ref = repo.get_git_ref('heads/main')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)
    element_list = list()
    for i, entry in enumerate(file_list):
        with open(entry,encoding='utf-8') as input_file:
            data = input_file.read()
        if entry.endswith('.png'):
            data = base64.b64encode(data)
        element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
        element_list.append(element)
    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)