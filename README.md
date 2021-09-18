# idur
a community package manager to debian systems (ubuntu-based too)

Like an AUR, but more simple.

## Easy to use
```
sudo idur install <package>
```
```
sudo idur remove <package>
```
```
sudo idur update
```
```
idur search <search here>
```

## Install
I've made a test installer, use it with precaution

## Create idurs
#### (simple bash knows needed)
so simple just use the create-idur. Install with
```
sudo idur install create-idur
```
And execute it on terminal
this will create a file with the start of your idur
and you have to modified the Description, Install and Remove sections.

# I'm an Expert User and I want to know more
## --help
```
idur <command> <package>
Use:
    install        <package>                Install package
    remove         <package>                Remove package
    show           <package>                Show details of package
    show-install   <package>                Show install instructions of package
    show-remove    <package>                Show remove instructions of package
    search         <name>                   Search packages
    list                                    list all installed packages
    list-all                                list all packages
    reinstall      <package>                Reinstall package
    update         <package>                Update package
    update                                  Update all package
    update-repos                            Update just repos
    add-repo       <repo-name> <repo-link>  Add a new repo
    remove-repo    <repo name>              Remove a repo
    list-repos                       
```
