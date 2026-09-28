---
sidebar_position: 4
---

# Distributed Processing Across Compute Nodes
## Overview
For shape optimization, EMSOptimizer supports distributed processing across multiple compute nodes in addition to parallel shape evaluation.  
Distributed processing uses the client/scheduler/worker coordination provided by the Dask Distributed package\[18\]. To enable it, set `optimization.yaml` > `enable_dask_distribution` to `True`.
:::info
The following two requirements must be met.
- The EMSOptimizer runtime environment is installed on every node.
- Licensing with CodeMeter Runtime is configured on every node.
:::

## Compute-node configuration
![Dask distributed compute-node configuration](/img/dask_distributed.png)
- In EMSOptimizer, the compute node that runs shape optimization with the `run` command becomes the client node.
- Scheduler and worker nodes are configured separately. The worker nodes connect to the scheduler node.
- When distributed processing is enabled:
    - When the client node runs shape optimization, shape-evaluation tasks are passed to the scheduler node.
    - The scheduler divides the tasks and distributes them to the worker nodes.
    - Each worker further divides the tasks with multiprocessing and processes them in parallel.
        - Therefore, the total parallelism is `（workerノードの数）×（各workerノード内での並列処理数）`.
:::info
The nodes may also be separate processes on the same computer. For example, the client and scheduler can be started as separate processes on one computer.
:::

## Running distributed processing
### Environment setup
- Set the following environment variable on the scheduler node.  
    - Variable name: `PYTHONPATH`
    - Value: `{ノードに配置したEMSOptimizerフォルダへのパス}`
        - Required for Python to find the `EMSOptimizer` scripts.
- Set the following environment variables on each worker node.
    - Variable name: `PYTHONPATH`
    - Value: `{ノードに配置したEMSOptimizerフォルダへのパス}`
        - Required for Python to find the `EMSOptimizer` scripts.
    - Variable name: `DASK_DISTRIBUTED__WORKER__DAEMON`
    - Value: `False`
        - Makes worker processes started by Dask Distributed non-daemonic. This is required for parallel processing within a worker node.

### Execution flow
1. Start the scheduler by running the following command on the scheduler node.
```sh
dask scheduler
```
- When the scheduler starts, record the information inside {} in the following log; it is used in the subsequent steps.
```sh
Scheduler at: tcp://{schedulerノードのIPアドレス}:{ポート番号}
```
2. Start a worker by running the following command on a worker node.
```sh
dask worker tcp://{schedulerノードのIPアドレス}:{ポート番号} --nworkers 1 --nthreads 1
```
3. In the project to run on the client node, configure the following options in `optimization.yaml`.  
- `enable_dask_distribution: True`
- `dask_scheduler_url: tcp://{schedulerノードのIPアドレス}:{ポート番号}`
- `num_chunks: {タスク分割数}` or `null`
    - Shape-evaluation tasks are divided into `num_chunks` and distributed among active worker nodes.
    - When `null`, `タスク分割数＝アクティブなworkerノード数` is set automatically.
- `enable_parallelization: True` or `False`
    - Set to `True` to process the shape-evaluation tasks divided into `num_chunks` in parallel within worker nodes.
- `num_processes: {並列処理数}` or `null`
    - Each worker processes shape-evaluation tasks with the number of processes specified by `num_processes`.
    - Therefore, total parallelism is `num_chunks` × `num_processes`.
- `resource_dir: {共有フォルダへのパス}`
    - Intermediate optimization files are collected in `resource_dir`, so specify for `resource_dir` a shared folder accessible from all client, scheduler, and worker nodes.
4. Run the optimization from the client node with the `run` command.
    - During shape optimization, shape-evaluation tasks are automatically distributed among the worker nodes.
