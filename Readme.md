MeST
==============
Multi-Repository Sync Tool

features
-----------------
do sync between different repository


Usage
-----------------

1. setup config for `memest`

The unique config file is `~/.config/memest/config.ini`
You can setup, such as
```
[default]
; check period for sync
loop_period=10
cache=~/.local/gitcache

[example]
loop_period=10
; the local bare repository
local=~/.local/rep/example.git
; 远程的一系列仓库的配置，每个用`,`隔开。
; 单个配置格式为[git address] | [key]
; git address 须是git协议
; [key] 可省略
remote=git@github.com:xxmawhu/example.git|~/.ssh/id_rsa,
```
2. start

```bash
memest start
```
