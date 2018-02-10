from githubid import githubid
import pytest

def test_empty():
    
    # expect to get an assertion error
    with pytest.raises(AssertionError):
        githubid.get_repo_version()
    #end with
#end test-empty

def test_wrong_gitexe():
    
    (v1, v2, v3, v4, v5, v6) = githubid.get_repo_version('a')
    # expect tuple with "Unknown" values
    assert v1 == "Unknown"
    assert v2 == "Unknown"
    assert v3 == "Unknown"
    assert v4 == "Unknown"
    assert v5 == "Unknown"
    assert v6 == "Unknown"
#end test_wrong_gitexe

def test_consistent():
    
    # expect the returned tuple to look like
    

    #('refs/heads/master',
    # '9cc94ef3aa6454104a0c7fbfeb359651df50f5db',
    # 'v1.0-13-g9cc94ef',
    # '9cc94ef',
    # 'C:/Users/donrc/Documents/JupyterNotebooks/GithubNotebookProject',
    # 'https://github.com/coolum001/GithubNotebookProject.git')
    
    # or every tuple member to look like "Unknown")
    
    #  GIT_LOCATION is the path of a valid git executable
    GIT_LOCATION = \
    'C:\\Users\\donrc\\AppData\\Local\\GitHub\\PortableGit_f02737a78695063deace08e96d5042710d3e32db\\cmd\\git.exe'
    
    (v1, v2, v3, v4, v5, v6) = githubid.get_repo_version(GIT_LOCATION)
    
    UNKNOWN = "Unknown"
    
    assert ((v2==UNKNOWN) and (v3==UNKNOWN) and (v4==UNKNOWN) ) or \
           ((v2[0:7]==v4) and (v4==v3[-7:])                   )
    
#end test_consistent
   
    
    