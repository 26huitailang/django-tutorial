#!/usr/bin/env python
# coding=utf-8


from fabric.api import (
    env,
    roles,
    task,
    parallel,
    run,
    cd,
    prefix,
)
from contextlib import contextmanager as _contextmanager
from fabric.context_managers import shell_env

from django_vises.deploy import DeployLevel


class Constants(object):
    """默认参数以 develop-team 为范例"""

    def __init__(self):
        self.PYPI_MIRROR = 'https://pypi.tuna.tsinghua.edu.cn/simple'

        self.VENV_NAME = 'venv'

        self.DEPLOY_LEVEL = DeployLevel.develop
        self.DEPLOY_HOME_PATH = '/home/deploy/server'  # 部署的工程根目录

        self.PROJECT_NAME = 'tzdashboard'

        self.VCS_BRANCH = 'develop'

    @property
    def path_venv(self):
        """虚环境目录

        /home/deploy/server/venv
        """
        return '{}/{}'.format(self.DEPLOY_HOME_PATH, self.VENV_NAME)

    @property
    def path_django(self):
        """Django 目录

        /home/deploy/server/tzdashboard
        """
        return '{}/{}'.format(self.DEPLOY_HOME_PATH, self.PROJECT_NAME)

    @property
    def path_django_settings(self):
        """django 主应用的目录

        /home/deploy/server/tzdashboard/tzdashboard
        """
        return '{}/{}/settings'.format(self.path_django, self.PROJECT_NAME)

    @property
    def path_scripts(self):
        """其他脚本目录"""
        return '{}/scripts'.format(self.DEPLOY_HOME_PATH)

    @property
    def file_supervisor_conf(self):
        """supervisor配置目录

        通过-c指定该配置来启动和执行管理命令
        """
        return '{}/deploy/supervisor/supervisord.conf'.format(self.DEPLOY_HOME_PATH)

    @property
    def path_running(self):
        """运行配置的目录

        根据DevelopLevel的判断，不同环境放入相应配置，一般是开发环境
        """
        return '{}/running'.format(self.DEPLOY_HOME_PATH)


REMOTE = Constants()


def develop():
    """环境: develop-team"""
    REMOTE.DEPLOY_LEVEL = DeployLevel.develop
    env.roledefs['main-server'] = [
        'deploy@10.100.100.110',
    ]

    return


env.roledefs = {
    'main-server': [],
}
develop()  # 默认预设置为开发环境


def release():
    """环境: release"""
    REMOTE.DEPLOY_LEVEL = DeployLevel.release
    REMOTE.VCS_BRANCH = 'master'
    env.roledefs['main-server'] = [
        'deploy@example.com',
    ]

    return


@_contextmanager
def venv():
    with prefix('source %s/bin/activate' % REMOTE.path_venv):
        yield


@task
@roles('main-server', )
@parallel
def supervisor_start():
    # 更新并启动服务
    with cd(REMOTE.DEPLOY_HOME_PATH), shell_env(DJANGO_TUTORIAL_HOME=REMOTE.DEPLOY_HOME_PATH):
        run('supervisorctl -c {} update'.format(REMOTE.file_supervisor_conf))
        run('supervisorctl -c {} start all'.format(REMOTE.file_supervisor_conf))

    return


@task
@roles('main-server', )
@parallel
def supervisor_stop():
    with cd(REMOTE.DEPLOY_HOME_PATH), shell_env(DJANGO_TUTORIAL_HOME=REMOTE.DEPLOY_HOME_PATH):
        # 停止服务
        run('supervisorctl -c {} stop all'.format(REMOTE.file_supervisor_conf))

    return


@task
@roles('main-server')
def upgrade_venv():
    """更新 python 库环境"""
    with cd(REMOTE.DEPLOY_HOME_PATH), venv():
        run('pip install --upgrade pip')

        if REMOTE.DEPLOY_LEVEL == DeployLevel.develop:
            run('pip install --upgrade -r requirements/develop.txt -i {}'.format(REMOTE.PYPI_MIRROR))
        else:
            run('pip install --upgrade -r requirements.txt -i {}'.format(REMOTE.PYPI_MIRROR))

    return


def _update_code_base(django=False, celery=False):
    """"""
    with cd(REMOTE.DEPLOY_HOME_PATH), venv():
        # 更新代码库
        run('git checkout {}'.format(REMOTE.VCS_BRANCH))
        run('git reset --hard')
        run('git pull')

        # 更新 supervisor 配置文件
        run('rm -f {}/supervisor/*.conf'.format(REMOTE.path_running))

        supervisor_conf_file_source_path = '{}/deploy/supervisor/{}'.format(
            REMOTE.DEPLOY_HOME_PATH, REMOTE.DEPLOY_LEVEL.name
        )
        if django:
            run('cp -f {}/django-tutorial-server.conf {}/supervisor'.format(
                supervisor_conf_file_source_path,
                REMOTE.path_running
            ))

        if celery:
            run('cp -f {}/tz-data-dws-celery-worker.conf {}/supervisor'.format(
                supervisor_conf_file_source_path,
                REMOTE.path_running
            ))
            run('cp -f {}/tz-data-dws-celery-beat.conf {}/supervisor'.format(
                supervisor_conf_file_source_path,
                REMOTE.path_running
            ))

        if REMOTE.DEPLOY_LEVEL == DeployLevel.develop:
            run('cp -f {}/dt-supervisord-inet-http-server.conf {}/supervisor'.format(
                supervisor_conf_file_source_path,
                REMOTE.path_running
            ))

    with cd(REMOTE.path_django):
        if REMOTE.DEPLOY_LEVEL != DeployLevel.release:
            # 更新 django settings 文件
            # 将develop.py 文件设置为自定义的settings.py配置
            run('cp -f {}/{}.py {}/settings.py'.format(
                REMOTE.path_django_settings,
                REMOTE.DEPLOY_LEVEL.name,
                REMOTE.path_django_settings,
            ))

    return


@task
def set(level=DeployLevel.develop.name):
    """环境设置: 开发环境(默认,不需要调用): set:level=develop; 生产环境: set:level=release"""
    if level == DeployLevel.release.name:
        release()
    else:
        develop()

    return


@task
@roles('main-server', )
def deploy():
    """部署命令
    """
    supervisor_stop()
    _update_code_base(django=True)
    upgrade_venv()

    # 部署静态文件
    with cd(REMOTE.path_django), venv():
        run('./manage.py collectstatic -v0 --noinput')

    if REMOTE.DEPLOY_LEVEL == DeployLevel.develop:
        # 生成临时的 migration 文件并更新数据库
        with cd(REMOTE.path_django), venv():
            run('./manage.py migrate')
        # 启动服务
        supervisor_start()

    else:
        print("please update DB PASSWORD and restart Services by hand...")

    return
