# 🚀 自动化部署管理系统

基于 Ubuntu 的完整自动化部署解决方案，集成 GitHub Webhook、Flask 管理界面和实时日志监控。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Ubuntu](https://img.shields.io/badge/ubuntu-20.04%20%7C%2022.04-orange.svg)](https://ubuntu.com/)
[![Flask](https://img.shields.io/badge/flask-2.x-green.svg)](https://flask.palletsprojects.com/)

> 🎯 **一键部署，自动化管理** - 让部署变得简单高效！

## ✨ 功能特性

### 🔧 核心功能
- **GitHub Webhook 集成**: 自动响应 Push/Tag/Release 事件
- **多项目管理**: 支持多个项目的独立部署配置
- **实时日志监控**: 完整的部署过程日志记录和查看
- **Web 管理界面**: 直观的项目管理和状态监控
- **安全验证**: X-Hub-Signature-256 签名验证
- **灵活部署脚本**: 支持前置/后置脚本自定义

### 📊 管理界面
- **仪表盘**: 部署统计、成功率分析、最近活动
- **项目管理**: 项目的增删改查、配置管理
- **日志查看**: 实时日志展示、筛选、下载
- **统计报表**: 部署趋势分析、项目对比

### 🛡️ 安全特性
- **用户认证**: 基于用户名/密码的登录系统
- **权限控制**: 登录验证和会话管理
- **HTTPS 支持**: Let's Encrypt SSL 证书
- **安全配置**: systemd 服务隔离和权限限制

## 📸 系统预览

### 🎥 在线演示
- **演示地址**: [https://demo.server-manager.com](https://demo.server-manager.com) (即将上线)
- **演示账户**: `demo` / `demo123`

### 🖼️ 界面截图

<table>
  <tr>
    <td width="50%">
      <h4>📊 仪表盘</h4>
      <img src="docs/images/dashboard.png" alt="仪表盘界面" width="100%">
      <p>实时监控部署状态和统计信息</p>
    </td>
    <td width="50%">
      <h4>📁 项目管理</h4>
      <img src="docs/images/projects.png" alt="项目管理界面" width="100%">
      <p>可视化项目配置和管理</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h4>📄 日志查看</h4>
      <img src="docs/images/logs.png" alt="日志查看界面" width="100%">
      <p>详细的部署过程日志</p>
    </td>
    <td width="50%">
      <h4>📈 统计报表</h4>
      <img src="docs/images/stats.png" alt="统计报表界面" width="100%">
      <p>部署成功率和趋势分析</p>
    </td>
  </tr>
</table>

## 🏗️ 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub        │───▶│   Nginx         │───▶│   Webhook       │
│   Repository    │    │   Reverse Proxy │    │   Server        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                         │
                              ▼                         ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Flask         │    │   Deploy        │
                       │   Application   │    │   Scripts       │
                       └─────────────────┘    └─────────────────┘
                              │                         │
                              ▼                         ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   SQLite        │    │   Log Files     │
                       │   Database      │    │   Storage       │
                       └─────────────────┘    └─────────────────┘
```

## 📁 项目结构

```
server-manager/
├── 📁 flask_app/                    # Flask Web 应用
│   ├── app.py                       # 主应用入口
│   ├── auth.py                      # 用户认证模块
│   ├── project.py                   # 项目管理模块
│   ├── logview.py                   # 日志查看模块
│   └── 📁 templates/                # HTML 模板
│       ├── base.html                # 基础模板
│       ├── login.html               # 登录页面
│       ├── dashboard.html           # 仪表盘
│       ├── projects.html            # 项目列表
│       ├── project_form.html        # 项目表单
│       ├── logs.html                # 日志列表
│       ├── log_detail.html          # 日志详情
│       └── deployment_stats.html    # 统计报表
├── 📁 webhook/                      # Webhook 配置
│   └── hooks.json                   # Webhook 路由配置
├── 📁 deploy/                       # 部署相关脚本
│   ├── 📁 scripts/                  # 部署脚本目录
│   │   ├── deploy_project1.sh       # 项目1部署脚本
│   │   ├── deploy_project2.sh       # 项目2部署脚本
│   │   ├── pre_deploy.sh            # 前置脚本
│   │   └── post_deploy.sh           # 后置脚本
│   ├── init_db.py                   # 数据库初始化
│   └── log_writer.py                # 日志记录工具
├── 📁 config/                       # 系统配置文件
│   ├── webhook.service              # Webhook systemd 服务
│   ├── flask-deploy.service         # Flask systemd 服务
│   ├── nginx-deploy.conf            # Nginx 配置
│   └── gunicorn.conf.py             # Gunicorn 配置
├── requirements.txt                 # Python 依赖
├── install.sh                       # 一键安装脚本
├── Makefile                         # 管理命令
├── LAYOUT.md                        # 界面布局设计
└── README.md                        # 项目说明
```

## 🚀 快速开始

### 系统要求

- **操作系统**: Ubuntu 20.04/22.04 LTS
- **权限**: 具有 sudo 权限的普通用户
- **网络**: 能够访问 GitHub 和包管理器

### 一键安装

```bash
# 克隆项目
git clone https://github.com/maxazure/server-manager.git
cd server-manager

# 运行安装脚本
chmod +x install.sh
./install.sh
```

### 手动安装

<details>
<summary>展开查看详细步骤</summary>

#### 1. 安装系统依赖

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx git curl wget sqlite3 systemd certbot python3-certbot-nginx webhook
```

#### 2. 创建用户和目录

```bash
sudo useradd -r -s /bin/bash -d /opt/deploy -m webhook
sudo useradd -r -s /bin/bash -d /home/deploy -m deploy
sudo mkdir -p /opt/deploy/{scripts,logs,data}
sudo mkdir -p /etc/webhook
sudo mkdir -p /var/log/flask-deploy
```

#### 3. 复制配置文件

```bash
sudo cp webhook/hooks.json /etc/webhook/
sudo cp deploy/scripts/* /opt/deploy/scripts/
sudo cp deploy/*.py /opt/deploy/
sudo cp -r flask_app/* /home/deploy/server-manager/
sudo cp requirements.txt /home/deploy/server-manager/
```

#### 4. 设置权限

```bash
sudo chown -R webhook:webhook /opt/deploy
sudo chown -R deploy:deploy /home/deploy
sudo chmod +x /opt/deploy/scripts/*.sh
sudo chmod +x /opt/deploy/*.py
```

#### 5. 安装 Python 依赖

```bash
sudo -u deploy bash -c "cd /home/deploy/server-manager && python3 -m pip install --user -r requirements.txt"
```

#### 6. 初始化数据库

```bash
sudo -u webhook python3 /opt/deploy/init_db.py
```

#### 7. 配置系统服务

```bash
sudo cp config/*.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable webhook.service flask-deploy.service
sudo systemctl start webhook.service flask-deploy.service
```

#### 8. 配置 Nginx

```bash
sudo cp config/nginx-deploy.conf /etc/nginx/sites-available/deploy
sudo ln -s /etc/nginx/sites-available/deploy /etc/nginx/sites-enabled/deploy
sudo systemctl restart nginx
```

</details>

## ⚙️ 配置说明

### 📡 Webhook 配置

编辑 `/etc/webhook/hooks.json`：

```json
{
  "id": "deploy-project1",
  "execute-command": "/opt/deploy/scripts/deploy_project1.sh",
  "trigger-rule": {
    "and": [
      {
        "match": {
          "type": "payload-hmac-sha256",
          "secret": "your-webhook-secret",
          "parameter": {
            "source": "header",
            "name": "X-Hub-Signature-256"
          }
        }
      },
      {
        "match": {
          "type": "value",
          "value": "refs/heads/main",
          "parameter": {
            "source": "payload",
            "name": "ref"
          }
        }
      }
    ]
  }
}
```

### 🌐 GitHub 配置

1. 进入 GitHub 仓库 Settings → Webhooks
2. 添加新的 Webhook：
   - **Payload URL**: `https://your-domain.com/webhook/deploy-project1`
   - **Content type**: `application/json`
   - **Secret**: 与 hooks.json 中的 secret 匹配
   - **Events**: Push, Tag push, Releases

### 🔐 SSL 证书配置

```bash
# 自动获取 Let's Encrypt 证书
sudo certbot --nginx -d your-domain.com

# 设置自动续期
sudo crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

## 💻 使用方法

### 🎯 管理命令

```bash
# 使用 Makefile 管理
make help           # 查看所有可用命令
make start          # 启动所有服务
make stop           # 停止所有服务
make restart        # 重启所有服务
make status         # 查看服务状态
make logs           # 查看实时日志
make backup         # 备份数据库和日志
make ssl            # 配置SSL证书
```

### 📊 Web 界面

访问 `https://your-domain.com` 并使用默认账户登录：
- **用户名**: `admin`
- **密码**: `admin123`

### 🔧 项目管理

1. **添加项目**：
   - 项目名称：唯一标识符
   - 仓库地址：Git HTTPS URL
   - 分支：要部署的分支
   - 部署目录：服务器路径
   - Webhook Secret：安全密钥

2. **配置部署脚本**：
   - 系统自动生成基础部署脚本
   - 可自定义 `pre_deploy.sh` 和 `post_deploy.sh`

3. **监控部署**：
   - 实时查看部署日志
   - 部署状态统计
   - 成功率分析

## 📝 日志管理

### 📍 重要路径

- **数据库**: `/home/deploy/server-manager/data/deploy.db`
- **部署日志**: `/opt/deploy/logs/`
- **系统日志**: `journalctl -u webhook.service -u flask-deploy.service`
- **Nginx 日志**: `/var/log/nginx/deploy_*.log`

### 🔍 日志查看

```bash
# 实时查看 Webhook 日志
sudo journalctl -u webhook.service -f

# 实时查看 Flask 日志
sudo journalctl -u flask-deploy.service -f

# 查看部署脚本日志
tail -f /opt/deploy/logs/project_name_*.log
```

## 🔧 故障排除

### 常见问题

<details>
<summary>🔴 Webhook 服务无法启动</summary>

**检查步骤**:
1. 验证配置文件语法：`webhook -validate-hooks /etc/webhook/hooks.json`
2. 检查端口占用：`sudo netstat -tlnp | grep 9000`
3. 查看详细错误：`sudo journalctl -u webhook.service -l`

**解决方案**:
```bash
# 修复配置文件权限
sudo chown webhook:webhook /etc/webhook/hooks.json
sudo systemctl restart webhook.service
```
</details>

<details>
<summary>🔴 部署脚本执行失败</summary>

**检查步骤**:
1. 验证脚本权限：`ls -la /opt/deploy/scripts/`
2. 检查目标目录权限：`ls -la /var/www/`
3. 测试手动执行：`sudo -u webhook bash /opt/deploy/scripts/deploy_project.sh`

**解决方案**:
```bash
# 修复脚本权限
sudo chmod +x /opt/deploy/scripts/*.sh
sudo chown webhook:webhook /opt/deploy/scripts/*
```
</details>

<details>
<summary>🔴 Flask 应用无法访问</summary>

**检查步骤**:
1. 服务状态：`sudo systemctl status flask-deploy.service`
2. 端口监听：`sudo netstat -tlnp | grep 5000`
3. Nginx 配置：`sudo nginx -t`

**解决方案**:
```bash
# 重启相关服务
sudo systemctl restart flask-deploy.service nginx
```
</details>

### 🛠️ 调试模式

```bash
# 开发模式启动 Flask
cd flask_app
python3 app.py

# 调试 Webhook
webhook -hooks /etc/webhook/hooks.json -verbose -hotreload
```

## 🔒 安全建议

### 🛡️ 系统安全

- **定期更新**: `sudo apt update && sudo apt upgrade`
- **防火墙配置**: 只开放必要端口 (22, 80, 443)
- **SSH 安全**: 禁用密码登录，使用密钥认证
- **用户权限**: 使用专用用户运行服务

### 🔐 应用安全

- **修改默认密码**: 首次登录后立即修改 admin 密码
- **定期轮换**: 定期更新 Webhook Secret
- **监控日志**: 定期检查异常访问记录
- **备份数据**: 定期备份数据库和配置文件

## 📚 扩展功能

### 🔌 插件扩展

- **通知集成**: Slack、钉钉、企业微信通知
- **监控集成**: Prometheus、Grafana 指标收集
- **多环境**: 开发、测试、生产环境隔离

### 🎨 界面定制

- **主题切换**: 支持深色模式
- **多语言**: 国际化支持
- **自定义面板**: 可配置的监控面板

## ❓ 常见问题

<details>
<summary><strong>Q: 支持哪些 Git 仓库提供商？</strong></summary>

A: 目前主要支持 GitHub，理论上支持所有使用 Git 协议的仓库，包括：
- GitHub (完全支持)
- GitLab (部分支持)
- Gitee (部分支持)
- 自建 Git 服务器 (需要手动配置)
</details>

<details>
<summary><strong>Q: 可以同时部署多个项目吗？</strong></summary>

A: 可以！系统支持多项目管理，每个项目可以有独立的：
- 部署脚本
- Webhook 配置
- 日志记录
- 部署目录
</details>

<details>
<summary><strong>Q: 支持哪些部署类型？</strong></summary>

A: 支持多种部署场景：
- 静态网站 (HTML/CSS/JS)
- Node.js 应用
- Python 应用
- PHP 应用
- Docker 容器
- 自定义脚本部署
</details>

<details>
<summary><strong>Q: 如何备份数据？</strong></summary>

A: 可以使用以下方式备份：
```bash
# 使用 Makefile 一键备份
make backup

# 手动备份数据库
cp flask_app/data/deploy.db backup/deploy_$(date +%Y%m%d).db

# 备份日志文件
tar -czf backup/logs_$(date +%Y%m%d).tar.gz deploy/logs/
```
</details>

<details>
<summary><strong>Q: 系统资源占用如何？</strong></summary>

A: 系统资源占用很低：
- **内存**: ~100MB (Flask + Webhook 服务)
- **CPU**: 空闲时 <1%，部署时根据项目大小
- **磁盘**: 基础安装 ~50MB，日志和数据库随使用增长
- **网络**: 仅在 Git 拉取时占用
</details>

## 🤝 贡献指南

我们欢迎所有形式的贡献！🎉

### 🔧 开发流程

1. **Fork 本项目** 到你的 GitHub 账户
2. **克隆项目** 到本地：
   ```bash
   git clone https://github.com/your-username/server-manager.git
   cd server-manager
   ```
3. **创建功能分支**：
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **开发和测试** 你的功能
5. **提交更改**：
   ```bash
   git commit -m "feat: add amazing feature"
   ```
6. **推送到你的分支**：
   ```bash
   git push origin feature/amazing-feature
   ```
7. **创建 Pull Request**

### 📝 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式化
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建或工具变更

### 🧪 开发环境

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
python -m pytest

# 代码格式化
black .
flake8 .

# 启动开发服务器
cd flask_app
python app.py
```

### 🐛 报告问题

发现 bug？请 [创建 Issue](https://github.com/maxazure/server-manager/issues/new) 并提供：

1. **环境信息** (操作系统、Python 版本等)
2. **复现步骤** 
3. **期望行为** vs **实际行为**
4. **错误日志** (如果有)
5. **截图** (如果适用)

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [adnanh/webhook](https://github.com/adnanh/webhook) - Webhook 服务器
- [Flask](https://flask.palletsprojects.com/) - Web 框架
- [Tailwind CSS](https://tailwindcss.com/) - CSS 框架
- [Ubuntu](https://ubuntu.com/) - 操作系统支持

## 📞 支持

- **文档**: [查看完整文档](https://github.com/maxazure/server-manager/wiki)
- **问题反馈**: [提交 Issue](https://github.com/maxazure/server-manager/issues)
- **讨论交流**: [Discussions](https://github.com/maxazure/server-manager/discussions)

---

⭐ **如果这个项目对你有帮助，请给个 Star！**