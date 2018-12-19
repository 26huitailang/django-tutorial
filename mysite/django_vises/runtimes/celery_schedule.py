#!/usr/bin/env python
# coding=utf-8


def rename_celery_tasks_with_app_name(app_name, tasks, tasks_folder='tasks'):
    """根据传入的任务配置，重新组合成celery beat的系统配置（因为shared_task无法通过celery_app.on_after_configure.connect工作）

    任务名中加入了app名和运行周期
    """
    new_tasks = dict()
    for period, task_list in tasks.items():
        for task in task_list:
            task_name = app_name + "." + period + "." + task[1].split('.')[-1]
            new_tasks[task_name] = {
                'task': app_name + "." + tasks_folder + "." + task[1],
                'schedule': task[0],
            }

    return new_tasks
