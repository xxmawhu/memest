MeST
==============
Multi-Repository Sync Tool


features
-----------------
* Automated synchronization between a local bare repository or multiple remote repositories directly, enabling seamless updates.
* The synchronization process runs entirely in the background, ensuring that branches across all repositories remain consistently up-to-date.
* Users only interact with the local bare repository, enjoying a smooth experience without noticeable network latency, making it seem as though they are working locally despite the syncing of multiple repositories.

Install
```
pip install memest
```

Usage
-----------------

1. setup config for `memest`

The unique config file is `~/.config/memest/config.ini`.
You can customize your own configurations, and here's an example,
```
[default]
; Repository synchronization check interval
loop_period=10
; Repository cache folder
cache=~/.local/gitcache

[example]
; the local bare repository
; If it does not exist, the system will automatically create it.
local=~/.local/rep/example.git
; List of all remote repositories
; The configuration format for each repository is as follows
;   [address]|[private key file] or [address]
remote=git@github.com:xxmawhu/example.git|~/.ssh/id_rsa,
       git@githuh.com:xxmawhu/another.git,
```
2. start memest

```bash
memest start
```

3. others
```bash
memest restart 
memest stop
memest status
````

