# 📋 更新日志

本文档记录了自动化部署管理系统的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循 [语义化版本](https://semver.org/lang/zh-CN/) 规范。

## [未发布]

### 新增
- ✨ 完整的项目文档体系升级
- 📝 详细的贡献指南 (CONTRIBUTING.md)
- 📋 规范的变更日志 (CHANGELOG.md)
- 📄 MIT 开源许可证 (LICENSE)
- 🔧 开发环境依赖配置 (requirements-dev.txt)
- 🤖 GitHub Actions CI/CD 流水线
- 📝 GitHub Issue 和 PR 模板
- 📊 项目状态徽章和在线演示说明
- 🖼️ 界面截图展示区域
- ❓ 常见问题解答 (FAQ)

### 改进
- 🌟 更新 README.md 包含正确的 GitHub 仓库地址
- 📈 增强项目可见性和专业度
- 🤝 改进开源协作流程和规范
- 📚 完善文档结构和导航

### 计划中
- [ ] 支持 Docker 容器化部署
- [ ] 集成 Slack/钉钉通知
- [ ] 多环境部署管理 (开发/测试/生产)
- [ ] API 接口和 CLI 工具
- [ ] 部署回滚功能
- [ ] 实时部署状态推送
- [ ] 界面截图和在线演示环境
- [ ] 单元测试和集成测试覆盖

## [1.0.2] - 2025-06-20

### 新增
- ✨ 完整的 Git 配置体系
- 📝 详细的 Git 使用文档 (README-git.md)
- 🔧 项目专用的 .gitignore 配置
- 📋 文件属性配置 (.gitattributes)
- 🗂️ 目录结构保护 (.gitkeep)

### 改进
- 🛡️ 增强安全文件过滤
- 📁 优化目录结构保留机制
- 📖 更新项目文档和最佳实践

### 修复
- 🔧 修复部分配置文件路径问题

## [1.0.1] - 2025-06-20

### 改进
- 📁 将数据库迁移到应用程序目录 (`flask_app/data/`)
- 🔧 统一所有数据库路径引用
- 📝 更新相关配置文件和脚本

### 修复
- 🛠️ 修复数据库初始化路径问题
- 📂 确保数据目录的正确创建

## [1.0.0] - 2025-06-20

### 新增 - 初始版本
- 🚀 **核心功能**
  - GitHub Webhook 集成，支持 Push/Tag/Release 事件
  - 多项目自动化部署管理
  - HMAC-SHA256 签名验证安全机制
  - 完整的部署日志记录和管理

- 🌐 **Web 管理界面**
  - 基于 Flask + Tailwind CSS 的现代化界面
  - 用户认证和会话管理
  - 直观的仪表盘显示部署统计
  - 项目 CRUD 管理功能
  - 实时日志查看和筛选
  - 部署统计报表和趋势分析

- 🗄️ **数据存储**
  - SQLite 数据库支持
  - 用户、项目、部署日志三大核心表
  - 完整的数据库初始化脚本

- ⚙️ **系统集成**
  - Ubuntu Webhook 服务集成
  - Systemd 服务配置 (webhook.service, flask-deploy.service)
  - Nginx 反向代理配置
  - Gunicorn WSGI 服务器配置
  - Let's Encrypt SSL 证书支持

- 📦 **部署工具**
  - 灵活的部署脚本模板系统
  - 支持前置/后置脚本自定义
  - Python 日志写入工具
  - 一键安装脚本 (install.sh)
  - Makefile 管理命令集

- 📚 **文档系统**
  - 完整的项目说明文档 (README.md)
  - 详细的界面布局设计 (LAYOUT.md)
  - 系统架构图和部署流程说明
  - 故障排除和安全建议

- 🛡️ **安全特性**
  - 专用用户隔离 (webhook, deploy 用户)
  - 权限最小化原则
  - 敏感文件保护
  - 安全的 systemd 服务配置

### 支持的平台
- Ubuntu 20.04 LTS
- Ubuntu 22.04 LTS
- Python 3.8+
- 现代浏览器 (Chrome 70+, Firefox 70+, Safari 12+)

### 依赖项目
- [adnanh/webhook](https://github.com/adnanh/webhook) - Webhook 服务器
- [Flask](https://flask.palletsprojects.com/) - Web 框架
- [Tailwind CSS](https://tailwindcss.com/) - CSS 框架
- [Gunicorn](https://gunicorn.org/) - WSGI 服务器
- [Nginx](https://nginx.org/) - 反向代理服务器

---

## 版本说明

### 版本号格式
我们采用 [语义化版本控制](https://semver.org/lang/zh-CN/) 格式：`MAJOR.MINOR.PATCH`

- **MAJOR**: 不兼容的 API 修改
- **MINOR**: 向下兼容的功能性新增
- **PATCH**: 向下兼容的问题修正

### 变更类型
- **新增**: 新功能
- **改进**: 对现有功能的改进
- **修复**: 问题修复
- **安全**: 安全相关修复
- **废弃**: 将在未来版本中移除的功能
- **移除**: 已移除的功能
- **变更**: 其他变更

### 发布计划
- **主版本**: 每年 1-2 次，包含重大功能更新
- **次版本**: 每月 1-2 次，包含新功能和改进
- **补丁版本**: 按需发布，主要用于 bug 修复和安全更新

---

## 贡献者

感谢所有为这个项目做出贡献的开发者！

- **maxazure** - 项目创建者和主要维护者
- **Claude Code Assistant** - 开发协助和文档编写

---

## 相关链接

- [项目主页](https://github.com/maxazure/server-manager)
- [问题反馈](https://github.com/maxazure/server-manager/issues)
- [功能请求](https://github.com/maxazure/server-manager/issues/new?template=feature_request.md)
- [安全漏洞报告](https://github.com/maxazure/server-manager/security/advisories/new)

---

*最后更新: 2025-06-20*