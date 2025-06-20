# 🤝 贡献指南

感谢您对自动化部署管理系统的关注！我们欢迎所有形式的贡献，包括但不限于：

- 🐛 报告 bug
- 🚀 提出新功能建议
- 📝 改进文档
- 💻 提交代码
- 🧪 编写测试
- 🎨 设计改进

## 📋 目录

- [开发环境设置](#开发环境设置)
- [提交流程](#提交流程)
- [代码规范](#代码规范)
- [提交规范](#提交规范)
- [测试要求](#测试要求)
- [文档贡献](#文档贡献)
- [问题报告](#问题报告)
- [功能请求](#功能请求)

## 🛠️ 开发环境设置

### 系统要求
- Ubuntu 20.04+ / macOS 10.15+ / Windows 10+ (WSL2)
- Python 3.8+
- Git 2.0+
- Node.js 14+ (用于前端工具)

### 1. Fork 和克隆项目

```bash
# Fork 项目到你的 GitHub 账户
# 然后克隆你的 fork

git clone https://github.com/your-username/server-manager.git
cd server-manager

# 添加上游仓库
git remote add upstream https://github.com/maxazure/server-manager.git
```

### 2. 设置开发环境

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或者 venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 如果存在

# 初始化开发数据库
cd deploy
python init_db.py
cd ..
```

### 3. 配置开发工具

```bash
# 安装 pre-commit hooks
pre-commit install

# 配置编辑器 (以 VS Code 为例)
# 安装推荐的扩展：Python, Pylance, Black Formatter
```

## 🔄 提交流程

### 1. 创建功能分支

```bash
# 确保主分支是最新的
git checkout main
git pull upstream main

# 创建新的功能分支
git checkout -b feature/amazing-feature
# 或者 fix/bug-description
# 或者 docs/update-readme
```

### 2. 开发和测试

```bash
# 进行你的修改
# ...

# 运行测试
python -m pytest

# 运行代码检查
flake8 .
black --check .
mypy .

# 手动测试 (启动开发服务器)
cd flask_app
python app.py
```

### 3. 提交更改

```bash
# 添加文件
git add .

# 提交 (使用规范的提交消息)
git commit -m "feat(api): add webhook signature validation"

# 推送到你的 fork
git push origin feature/amazing-feature
```

### 4. 创建 Pull Request

1. 访问 GitHub 上的项目页面
2. 点击 "New Pull Request"
3. 选择你的分支
4. 填写 PR 模板
5. 等待代码审查

## 📝 代码规范

### Python 代码规范

我们遵循 [PEP 8](https://pep8.org/) 和一些额外的规范：

```python
# 使用 Black 格式化代码
black .

# 使用 flake8 检查代码风格
flake8 . --max-line-length=88 --extend-ignore=E203,W503

# 使用 mypy 进行类型检查
mypy . --ignore-missing-imports
```

### 代码结构

```python
"""模块文档字符串。

详细描述模块的功能和用途。
"""

import os
import sys
from typing import Dict, List, Optional

from flask import Flask, request, jsonify

# 常量
DEFAULT_PORT = 5000
MAX_RETRIES = 3

# 类定义
class DeploymentManager:
    """部署管理器类。
    
    负责处理项目的部署逻辑。
    """
    
    def __init__(self, config: Dict[str, str]) -> None:
        """初始化部署管理器。
        
        Args:
            config: 配置字典
        """
        self.config = config
    
    def deploy_project(self, project_name: str) -> bool:
        """部署指定项目。
        
        Args:
            project_name: 项目名称
            
        Returns:
            部署是否成功
            
        Raises:
            ValueError: 项目名称无效时
        """
        if not project_name:
            raise ValueError("项目名称不能为空")
        
        # 部署逻辑
        return True

# 函数定义
def validate_webhook_signature(payload: str, signature: str, secret: str) -> bool:
    """验证 webhook 签名。
    
    Args:
        payload: 请求载荷
        signature: 签名
        secret: 密钥
        
    Returns:
        签名是否有效
    """
    # 验证逻辑
    return True
```

### HTML/CSS 规范

```html
<!-- 使用语义化 HTML -->
<article class="deployment-log">
    <header class="log-header">
        <h2 class="log-title">部署日志</h2>
        <time class="log-timestamp" datetime="2025-06-20T14:30:00">
            2025-06-20 14:30
        </time>
    </header>
    
    <section class="log-content">
        <!-- 日志内容 -->
    </section>
</article>
```

```css
/* 使用 Tailwind CSS 类名 */
.deployment-log {
    @apply bg-white rounded-lg shadow-md p-6 mb-4;
}

.log-header {
    @apply flex justify-between items-center mb-4 pb-2 border-b;
}

.log-title {
    @apply text-lg font-semibold text-gray-800;
}
```

## 📤 提交规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

### 类型说明

- **feat**: 新功能
- **fix**: 修复 bug
- **docs**: 仅文档更改
- **style**: 不影响代码含义的更改 (空格、格式化等)
- **refactor**: 既不修复 bug 也不添加功能的代码更改
- **perf**: 提高性能的代码更改
- **test**: 添加或修改测试
- **chore**: 对构建过程或辅助工具和库的更改

### 范围说明

- **api**: API 相关
- **ui**: 用户界面
- **db**: 数据库相关
- **auth**: 身份验证
- **webhook**: Webhook 处理
- **deploy**: 部署相关
- **docs**: 文档

### 提交示例

```bash
# 好的提交消息
git commit -m "feat(webhook): add signature validation for GitHub webhooks"
git commit -m "fix(db): resolve connection timeout issue"
git commit -m "docs(readme): update installation instructions"
git commit -m "refactor(auth): simplify user session management"

# 避免的提交消息
git commit -m "fix bug"
git commit -m "update stuff"
git commit -m "WIP"
```

## 🧪 测试要求

### 单元测试

```python
# tests/test_webhook.py
import pytest
from unittest.mock import patch, MagicMock

from webhook.validator import validate_signature

class TestWebhookValidator:
    """Webhook 验证器测试类。"""
    
    def test_valid_signature(self):
        """测试有效签名验证。"""
        payload = '{"test": "data"}'
        secret = "secret123"
        signature = "sha256=expected_hash"
        
        result = validate_signature(payload, signature, secret)
        
        assert result is True
    
    def test_invalid_signature(self):
        """测试无效签名验证。"""
        payload = '{"test": "data"}'
        secret = "secret123"
        signature = "sha256=invalid_hash"
        
        result = validate_signature(payload, signature, secret)
        
        assert result is False
    
    @patch('webhook.validator.hmac')
    def test_signature_generation(self, mock_hmac):
        """测试签名生成过程。"""
        # 测试实现
        pass
```

### 集成测试

```python
# tests/test_integration.py
import pytest
import tempfile
from flask import Flask

from flask_app.app import create_app

class TestDeploymentIntegration:
    """部署集成测试类。"""
    
    @pytest.fixture
    def app(self):
        """创建测试应用。"""
        app = create_app(testing=True)
        with app.app_context():
            yield app
    
    @pytest.fixture
    def client(self, app):
        """创建测试客户端。"""
        return app.test_client()
    
    def test_webhook_endpoint(self, client):
        """测试 webhook 端点。"""
        response = client.post('/webhook/deploy', 
                             json={'test': 'data'},
                             headers={'X-Hub-Signature-256': 'sha256=test'})
        
        assert response.status_code == 200
```

### 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行特定测试文件
python -m pytest tests/test_webhook.py

# 运行测试并生成覆盖率报告
python -m pytest --cov=./ --cov-report=html

# 运行测试但跳过集成测试
python -m pytest -m "not integration"
```

## 📚 文档贡献

### 文档类型

1. **代码文档**: 函数和类的 docstring
2. **API 文档**: API 接口说明
3. **用户文档**: README、安装指南等
4. **开发文档**: 架构说明、开发指南

### 文档格式

```python
def deploy_project(project_id: int, branch: str = "main") -> Dict[str, Any]:
    """部署指定项目到服务器。
    
    这个函数会执行以下步骤：
    1. 验证项目配置
    2. 拉取最新代码
    3. 执行部署脚本
    4. 记录部署日志
    
    Args:
        project_id: 项目 ID，必须是有效的项目标识符
        branch: Git 分支名，默认为 "main"
        
    Returns:
        包含部署结果的字典，格式如下：
        {
            "success": bool,
            "message": str,
            "deployment_id": int,
            "duration": float
        }
        
    Raises:
        ValueError: 当 project_id 无效时
        DeploymentError: 当部署过程失败时
        
    Example:
        >>> result = deploy_project(123, "develop")
        >>> print(result["success"])
        True
        
    Note:
        这个函数是异步执行的，可能需要几分钟才能完成。
        
    Warning:
        确保项目配置正确，否则部署可能失败。
    """
    pass
```

## 🐛 问题报告

### 报告 Bug

请使用 [Issue 模板](https://github.com/maxazure/server-manager/issues/new?template=bug_report.md) 报告 bug，包含：

1. **环境信息**
   - 操作系统和版本
   - Python 版本
   - 项目版本

2. **问题描述**
   - 清晰的问题描述
   - 期望的行为
   - 实际发生的行为

3. **复现步骤**
   - 详细的步骤说明
   - 相关的代码或配置

4. **附加信息**
   - 错误日志
   - 屏幕截图
   - 相关文件

### Bug 报告示例

```markdown
## 🐛 Bug 描述
部署时数据库连接超时

## 🔄 复现步骤
1. 启动 Flask 应用
2. 触发项目部署
3. 在部署日志中观察到数据库连接错误

## 💻 环境信息
- OS: Ubuntu 22.04
- Python: 3.10.12
- 项目版本: 1.0.1

## 📋 错误日志
```
[2025-06-20 14:30:01] ERROR: Database connection timeout
sqlalchemy.exc.TimeoutError: QueuePool limit of size 5 overflow 10 reached
```

## 🎯 期望行为
部署应该成功完成，不应该出现数据库连接超时

## 📷 截图
[附上相关截图]
```

## 🚀 功能请求

### 提出新功能

请使用 [功能请求模板](https://github.com/maxazure/server-manager/issues/new?template=feature_request.md)：

1. **功能描述**: 清晰描述建议的功能
2. **使用场景**: 说明功能的使用场景和价值
3. **详细设计**: 如果有具体的设计想法
4. **替代方案**: 考虑过的其他方案

## ❓ 获取帮助

如果你在贡献过程中遇到问题：

1. **查看文档**: 首先查看项目文档和 FAQ
2. **搜索 Issues**: 看看是否有类似的问题已经被讨论
3. **创建 Discussion**: 在 [Discussions](https://github.com/maxazure/server-manager/discussions) 中提问
4. **联系维护者**: 通过 Issue 或 Email 联系

## 🎉 贡献者认可

我们会在以下地方认可贡献者：

- **CHANGELOG.md**: 记录重要贡献
- **README.md**: 感谢部分列出贡献者
- **Release Notes**: 在发布说明中提及贡献者

## 📄 许可证

通过贡献，您同意您的贡献将在 [MIT License](LICENSE) 下许可。

---

感谢您的贡献！🙏

如有任何问题，请随时通过 [Issues](https://github.com/maxazure/server-manager/issues) 联系我们。