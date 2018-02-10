# Return the repo revision information as a tuple of strings
# refer to https://stackoverflow.com/questions/14989858/get-the-current-git-hash-in-a-python-script

import os
import subprocess

def get_repo_version(git_location = None):
    '''
    Returns a tuple containing identification of the git repository containing the calling source code
    
    Input:
    git_location: string: contains the path to a git executable
    
    Returns:
    a tuple of strings, of the form:
    (GIT_BRANCH, GIT_REVISION, GIT_TAGS, GIT_REVSHORT, GIT_REPOSITORY, GIT_REMOTE), where 
    
    GIT_BRANCH contains the current branch name
    
    GIT_REVISION contains the long version of the git id (eg f83a90d8335eb9c5dce01781e66cbe7bd9ed8b92)
    
    GIT_TAGS contains the information about the most recent tag (release) if any,
    in the form "v1.0-11-gacf3e94"
    
    GIT_REVSHORT contains a short version of the version id, like f83a90d  (this may include tag information)
    
    GIT_REPOSITORY contains the path to the local git repository
    
    GIT_REMOTE contains the path to the remote git repository
    
    Outputs:
    If an OSError exception is seen, function outputs a diagnostic of form on standard output
    
    OS Error in getting GIT revision using: 
    followed by git executable as supplied
    
    Error Conditions:
    If the call to the supplied git executable fails with an OSError exception,
    the string "Unknown" is returned for the corresponding member of the tuple
    
    If the supplied git executable path is == None, an assertion error is thrown
    '''
    assert not( git_location == None), 'git executable location not supplied'
    
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for k in ['SYSTEMROOT', 'PATH']:
            v = os.environ.get(k)
            if v is not None:
                env[k] = v
            #end if
        #end for
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'

        out = subprocess.Popen(cmd, stdout = subprocess.PIPE, env=env).communicate()[0]
   
        return out
    #end _minimal_ext_cmd

   
    # get version id of form 
    # f83a90d8335eb9c5dce01781e66cbe7bd9ed8b92
    try:
        out = _minimal_ext_cmd([git_location, 'rev-parse', 'HEAD'])
        GIT_REVISION = out.strip().decode('ascii')
    except OSError as e:
        print(' OS Error in getting GIT revision using: '+git_location, e)
        GIT_REVISION = "Unknown"
    #end try
    
    # get current branch name
    try:
        out = _minimal_ext_cmd([git_location, 'symbolic-ref', 'HEAD'])
        GIT_BRANCH = out.strip().decode('ascii')
    except OSError as e:
        print(' OS Error in getting GIT branch using: '+git_location, e)
        GIT_BRANCH = "Unknown"
    #end try
    
    # get short form of version, like
    # f83a90d  (this may include tag information)
    try:
        out = _minimal_ext_cmd([git_location, 'describe', '--always'])
        GIT_REVSHORT = out.strip().decode('ascii')
    except OSError as e:
        print(' OS Error in getting GIT short revision using: '+git_location, e)
        GIT_REVSHORT = "Unknown"
    #end try
    
    # show top level of local GIT repository
    try:
        out = _minimal_ext_cmd([git_location, 'rev-parse', '--show-toplevel'])
        GIT_REPOSITORY = out.strip().decode('ascii')
    except OSError as e:
        print(' OS Error in getting GIT local repository name using: '+git_location, e)
        GIT_REPOSITORY = "Unknown"
    #end try
    
    # show remote GIT repository
    try:
        out = _minimal_ext_cmd([git_location, 'remote', '--verbose'])
       
        # decode binary array to ascii, split on newlines, split line 0 on blank, skip first 6 chars
        GIT_REMOTE = out.strip().decode('ascii').split('\n')[0].split(' ')[0][7:]
    except OSError as e:
        print(' OS Error in getting GIT remote repository name using: '+git_location, e)
        GIT_REMOTE = "Unknown"
    #end try
    
  # show tags info
    try:
        out = _minimal_ext_cmd([git_location, 'describe', '--tags', '--long'])
       
        # decode binary array to ascii,
        GIT_TAGS = out.strip().decode('ascii')
    except OSError as e:
        print(' OS Error in getting GIT tags information using: '+git_location, e)
        GIT_TAGS = "Unknown"
    #end try

    return (GIT_BRANCH, GIT_REVISION, GIT_TAGS, GIT_REVSHORT, GIT_REPOSITORY, GIT_REMOTE)
#end get_repo_version