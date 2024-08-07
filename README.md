<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-wwgachalogs

_✨ 鸣潮抽卡记录插件 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/BraveCowardp/nonebot-plugin-wwgachalogs.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-wwgachalogs">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-wwgachalogs.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>

## 📖 介绍

在群聊中展示你的鸣潮抽卡记录，目前只做了最简单的显示每个金抽数的功能，后面会增加显示内容和优化显示效果

## 💿 安装

<details open>
<summary>使用 nb-cli 安装(推荐！)</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-wwgachalogs

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-wwgachalogs
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-wwgachalogs
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-wwgachalogs
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-wwgachalogs
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_wwgachalogs"]

</details>

## 🎉 使用
### 更新数据模型 <font color=#fc8403 >使用必看！！！！！</font>
本插件使用了官方推荐的`nonebot-plugin-orm`插件操作数据库，安装插件或更新插件版本后，在启动机器人前，都需要执行此命令。
```shell
nb orm upgrade
```
手动执行下列命令检查数据库模式是否与模型定义一致。机器人启动前也会自动运行此命令，并在检查失败时阻止启动。
```shell
nb orm check
```
看到`没有检测到新的升级操作`字样时，表明数据库模型已经成功创建或更新，可以启动机器人
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 抽卡记录帮助 | 群员 | 否 | 群聊 | 查看使用帮助 |
| 鸣潮抽卡信息绑定 | 群员 | 否 | 群聊 | 绑定获取抽卡记录需要的参数 |
| 抽卡记录 | 群员 | 否 | 群聊 | 显示抽卡记录信息，目前只会显示出金抽数，可以通过@群友查看其他已绑定抽卡信息群友的抽卡记录 |

## TODO
- [ ] 增加抽卡记录信息显示内容，加一些渲染，优化排版