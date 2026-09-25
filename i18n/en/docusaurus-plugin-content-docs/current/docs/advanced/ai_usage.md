---
sidebar_position: 6
---

# AI-Assisted Configuration
To perform structural optimization with EMSOptimizer, it is important to configure the configuration files according to the mesh information, analysis conditions, evaluation budget, and other requirements.  
Although configuration can be performed manually, EMSOptimizer configuration files are written in YAML, so **generative AI can be used to draft configurations and consider optimization methods suited to the objective**.  
This page presents examples of using AI to assist with EMSOptimizer configuration.  
:::info
AI may produce incorrect answers or answers that do not match the user's intent.  
Users must verify the content of AI responses and generated configurations themselves.
:::

## Configuring the MCP Server
EMSOptimizer provides product-specific knowledge to AI agents through resources supplied by a local MCP server.  
- To use the local MCP server, first install the whl file provided by SSIL in the Python environment.
    - Installing the whl registers `emsopt-docs-mcp` as the MCP server startup command. Normally, the command is placed in the Scripts directory (Windows) or bin directory (Linux) of the Python environment.  
- Register this command as a reference source in each AI agent service.
    - See the documentation for the service you use for specific registration instructions.  

## Example: Automatically Generating an Optimization Configuration for an 8P12S Permanent Magnet Synchronous Motor
One typical use is to **describe the desired optimization in natural language and have AI generate a draft configuration file**.  
For example, by entering requirements such as “perform multi-objective shape optimization to maximize average torque and reduce torque ripple,” “use CMA-ES for single-objective optimization,” or “run the analysis in parallel,” you can obtain candidate configuration options and a YAML draft.

The following image shows an example in which the mesh and analysis input files for an 8-pole, 12-slot permanent magnet synchronous motor were provided to an AI agent, which generated the corresponding configuration file. The AI agent configures the settings to the extent that they can be inferred from the input.

![Example of EMSOptimizer configuration generation by AI](/img/ai_usage_config_generation.png)

After reviewing the configuration, you can also proceed directly to submitting the optimization job.

![Example of EMSOptimizer job submission by AI](/img/ai_usage_job_running.png)

AI can also assist with tasks such as the following.
- Drafting core object settings in `optimization.yaml` (`optimizer`, `evaluator`, `level_set_function`, and so on)
- Organizing the objective functions, constraints, and analysis case names in `optimization_problem.yaml`
- Identifying configuration options for parallel processing, distributed processing, output settings, and so on
- Drafting configuration adjustments for similar projects based on existing showcases and the User Guide
- Checking for missing options and inconsistent values in configuration files
:::tip
When asking AI to generate a configuration, provide as much detail as possible about the purpose of the target project, whether it is single-objective or multi-objective, the Evaluator to use, analysis case names, the number and ranges of design variables, and required constraints. This makes it more likely that the generated configuration matches the user's intent.
:::
