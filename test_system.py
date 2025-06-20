#!/usr/bin/env python3

"""
测试自动化部署系统的各个组件
"""

import sys
import os
import sqlite3
from datetime import datetime

def test_database_connection():
    """测试数据库连接"""
    print("🔍 测试数据库连接...")
    
    try:
        # 使用与Flask应用相同的路径计算方式
        flask_app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'flask_app')
        db_path = os.path.join(flask_app_dir, 'data', 'deploy.db')
        
        print(f"   数据库路径: {db_path}")
        print(f"   文件存在: {os.path.exists(db_path)}")
        
        if not os.path.exists(db_path):
            print("   ❌ 数据库文件不存在")
            return False
            
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        # 测试查询用户
        users = conn.execute('SELECT * FROM user').fetchall()
        print(f"   👤 用户数量: {len(users)}")
        for user in users:
            print(f"      - {user['username']}")
            
        # 测试查询项目
        projects = conn.execute('SELECT * FROM project').fetchall()
        print(f"   📁 项目数量: {len(projects)}")
        for project in projects:
            print(f"      - {project['name']} ({project['branch']})")
            
        # 测试查询日志
        logs = conn.execute('SELECT COUNT(*) as count FROM deploy_log').fetchone()
        print(f"   📄 部署日志数量: {logs['count']}")
        
        conn.close()
        print("   ✅ 数据库连接测试通过")
        return True
        
    except Exception as e:
        print(f"   ❌ 数据库连接失败: {e}")
        return False

def test_log_writer():
    """测试日志写入工具"""
    print("🔍 测试日志写入工具...")
    
    try:
        # 导入log_writer
        sys.path.append(os.path.join(os.path.dirname(__file__), 'deploy'))
        from log_writer import write_log_entry, get_db_path
        
        # 测试写入日志
        test_log_path = "/tmp/test_deployment.log"
        success = write_log_entry("project1", "success", test_log_path, "abc123", "main")
        
        if success:
            print("   ✅ 日志写入测试通过")
            
            # 验证日志是否写入数据库
            db_path = get_db_path()
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            
            recent_log = conn.execute(
                'SELECT * FROM deploy_log ORDER BY timestamp DESC LIMIT 1'
            ).fetchone()
            
            if recent_log:
                print(f"   📝 最新日志: {recent_log['status']} - {recent_log['log_path']}")
            
            conn.close()
            return True
        else:
            print("   ❌ 日志写入失败")
            return False
            
    except Exception as e:
        print(f"   ❌ 日志写入工具测试失败: {e}")
        return False

def test_flask_app_import():
    """测试Flask应用导入"""
    print("🔍 测试Flask应用导入...")
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'flask_app'))
        
        # 测试导入主要模块
        import app
        import auth
        import project
        import logview
        
        print("   ✅ Flask应用模块导入成功")
        
        # 测试数据库连接函数
        conn = app.get_db_connection()
        conn.close()
        print("   ✅ Flask数据库连接测试通过")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Flask应用测试失败: {e}")
        return False

def test_file_structure():
    """测试文件结构"""
    print("🔍 测试文件结构...")
    
    required_files = [
        'flask_app/app.py',
        'flask_app/auth.py', 
        'flask_app/project.py',
        'flask_app/logview.py',
        'flask_app/data/deploy.db',
        'deploy/init_db.py',
        'deploy/log_writer.py',
        'deploy/scripts/deploy_project1.sh',
        'deploy/scripts/deploy_project2.sh',
        'webhook/hooks.json',
        'config/webhook.service',
        'config/flask-deploy.service',
        'config/nginx-deploy.conf',
        'install.sh',
        'Makefile',
        'requirements.txt'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
        else:
            print(f"   ✅ {file_path}")
    
    if missing_files:
        print("   ❌ 缺少以下文件:")
        for file_path in missing_files:
            print(f"      - {file_path}")
        return False
    else:
        print("   ✅ 所有必需文件都存在")
        return True

def main():
    """运行所有测试"""
    print("🚀 自动化部署系统测试")
    print("=" * 50)
    
    tests = [
        ("文件结构", test_file_structure),
        ("数据库连接", test_database_connection),
        ("日志写入工具", test_log_writer),
        ("Flask应用", test_flask_app_import),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"🎯 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统已准备就绪。")
        print("\n📌 下一步:")
        print("   1. 运行 ./install.sh 安装系统")
        print("   2. 配置域名和SSL证书")
        print("   3. 在GitHub仓库中配置Webhook")
        return True
    else:
        print("⚠️  部分测试失败，请检查问题后重试。")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)