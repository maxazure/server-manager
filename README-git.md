# 🔧 Git 配置说明

本项目包含完整的 Git 配置文件，用于版本控制和协作开发。

## 📁 Git 配置文件

### `.gitignore`
忽略不需要版本控制的文件，包括：

#### 🐍 Python 相关
- `__pycache__/` - Python 字节码缓存
- `*.pyc` - 编译的 Python 文件
- `.env` - 环境变量文件
- `venv/` - 虚拟环境目录

#### 🗄️ 数据库文件
- `*.db` - SQLite 数据库文件
- `flask_app/data/deploy.db` - 应用数据库
- `backup/*.db` - 数据库备份

#### 📄 日志文件
- `deploy/logs/*.log` - 部署日志
- `*.log` - 所有日志文件
- `logs/` - 日志目录

#### 🔒 安全文件
- `*.key` - 私钥文件
- `*.pem` - 证书文件
- `*secret*` - 包含敏感信息的文件
- `.secrets` - 秘密配置文件

#### 🛠️ 开发工具
- `.vscode/` - VS Code 配置
- `.idea/` - PyCharm 配置
- `*.swp` - Vim 临时文件

### `.gitattributes`
定义文件属性和处理方式：

#### 📝 文本文件
```
*.py text eol=lf diff=python
*.html text eol=lf diff=html
*.md text eol=lf diff=markdown
*.sh text eol=lf
```

#### 🔄 二进制文件
```
*.db binary
*.png binary
*.jpg binary
*.zip binary
```

#### 🎯 特殊处理
- 脚本文件强制使用 Unix 换行符 (LF)
- Python 文件使用专门的差异显示
- 大文件使用 Git LFS

### `.gitkeep`
确保空目录被 Git 跟踪：
- `deploy/logs/.gitkeep` - 保留日志目录
- `flask_app/static/css/.gitkeep` - 保留CSS目录

## 🚀 Git 使用指南

### 初始化仓库
```bash
# 初始化 Git 仓库
git init

# 添加远程仓库
git remote add origin https://github.com/username/server-manager.git

# 首次提交
git add .
git commit -m "feat: 初始化自动化部署管理系统"
git push -u origin main
```

### 常用命令
```bash
# 查看状态
git status

# 添加文件
git add .                    # 添加所有文件
git add specific-file.py     # 添加特定文件

# 提交变更
git commit -m "feat: 添加新功能"
git commit -m "fix: 修复数据库连接问题"
git commit -m "docs: 更新README文档"

# 推送到远程
git push origin main

# 拉取最新代码
git pull origin main
```

### 分支管理
```bash
# 创建开发分支
git checkout -b develop

# 创建功能分支
git checkout -b feature/webhook-enhancement

# 合并分支
git checkout main
git merge feature/webhook-enhancement

# 删除分支
git branch -d feature/webhook-enhancement
```

## 📋 提交规范

### 提交消息格式
```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

### 类型说明
- **feat**: 新功能
- **fix**: 修复bug
- **docs**: 文档更新
- **style**: 代码格式化
- **refactor**: 代码重构
- **test**: 测试相关
- **chore**: 构建/工具变更

### 示例
```bash
git commit -m "feat(webhook): 添加GitHub签名验证功能"
git commit -m "fix(database): 修复SQLite连接超时问题"
git commit -m "docs(readme): 更新安装说明"
git commit -m "refactor(auth): 重构用户认证模块"
```

## 🔍 忽略文件说明

### 为什么忽略这些文件？

#### 数据库文件 (`*.db`)
- 包含用户数据和配置
- 大小可能很大
- 每个环境应该有独立的数据库

#### 日志文件 (`*.log`)
- 运行时生成
- 包含敏感信息
- 大小增长快

#### 配置文件 (`*.key`, `*.pem`)
- 包含敏感的密钥信息
- 每个环境应该有不同的配置

#### 临时文件 (`__pycache__`, `*.tmp`)
- 系统自动生成
- 不影响功能
- 增加仓库大小

## 🛠️ 开发工作流

### 1. 功能开发
```bash
# 1. 创建功能分支
git checkout -b feature/new-feature

# 2. 开发和测试
# ... 编写代码 ...

# 3. 提交变更
git add .
git commit -m "feat: 实现新功能"

# 4. 推送分支
git push origin feature/new-feature

# 5. 创建 Pull Request
```

### 2. 修复 Bug
```bash
# 1. 创建修复分支
git checkout -b hotfix/critical-bug

# 2. 修复问题
# ... 修复代码 ...

# 3. 提交修复
git add .
git commit -m "fix: 修复关键bug"

# 4. 合并到主分支
git checkout main
git merge hotfix/critical-bug
git push origin main
```

### 3. 更新文档
```bash
# 直接在 main 分支更新
git checkout main
git add README.md
git commit -m "docs: 更新使用说明"
git push origin main
```

## 📊 仓库统计

### 检查仓库大小
```bash
# 查看仓库大小
git count-objects -vH

# 查看最大的文件
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | sort -k3 -n | tail -10
```

### 清理仓库
```bash
# 清理未跟踪的文件
git clean -fd

# 清理 Git 缓存
git gc --prune=now --aggressive
```

## 🔄 协作开发

### Fork 工作流
1. Fork 主仓库到个人账户
2. Clone 个人仓库到本地
3. 创建功能分支开发
4. 推送到个人仓库
5. 创建 Pull Request 到主仓库

### 代码审查
- 所有代码变更需要经过审查
- Pull Request 必须通过测试
- 至少一人审核通过才能合并

## 🎯 最佳实践

### 1. 频繁提交
- 小步快跑，频繁提交
- 每个提交只解决一个问题
- 提交消息要清晰明确

### 2. 分支策略
- `main`: 稳定的生产代码
- `develop`: 开发分支
- `feature/*`: 功能分支
- `hotfix/*`: 紧急修复分支

### 3. 安全考虑
- 永远不要提交密钥和密码
- 使用环境变量存储敏感信息
- 定期检查是否有敏感信息泄露

---

**维护者**: Claude Code Assistant  
**最后更新**: 2025-06-20  
**版本**: v1.0