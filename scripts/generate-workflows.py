import yaml
import os
from pathlib import Path

# 加载配置
with open('repos.yaml') as f:
    config = yaml.safe_load(f)

# 创建目标目录
Path('generated-workflows').mkdir(exist_ok=True)

# 处理每个仓库
for repo in config['repositories']:
    # 生成上游同步工作流
    with open('templates/sync-upstream.yml') as t:
        upstream_workflow = t.read().format(
            repo=repo['source'],
            fork=repo['fork'],
            branch=repo['branch'],
            schedule=repo['schedule']
        )
    
    # 生成Gitee同步工作流
    with open('templates/sync-to-gitee.yml') as t:
        gitee_workflow = t.read().format(
            gitee_repo=repo['gitee'],
            branch=repo['branch']
        )
    
    # 保存到目标仓库目录
    repo_dir = f"generated-workflows/{repo['fork'].replace('/', '-')}"
    Path(repo_dir).mkdir(exist_ok=True)
    
    with open(f"{repo_dir}/sync-upstream.yml", 'w') as f:
        f.write(upstream_workflow)
    
    with open(f"{repo_dir}/sync-to-gitee.yml", 'w') as f:
        f.write(gitee_workflow)

print(f"Generated {len(config['repositories']*2} workflow files")
