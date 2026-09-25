---
sidebar_position: 5
---

# Dmodel Mixed-Variable Optimization Example
This page introduces the `Dmodel_mixed_variables` project.  
Compared with the `Dmodel` project, `Dmodel_mixed_variables` uses the `ga` optimizer and eMotorSolution integration to optimize categorical and discrete variables that determine the motor configuration together with the continuous variables of the NGnet on/off method.

## machine.yaml (`Dmodel_mixed_variables` project)
The basic `machine.yaml` settings are the same as in the `Dmodel` project, but the `ems_project_filepath` configuration is added to enable optimization with eMotorSolution.  
The `Dmodel_mixed_variables` project already contains the eMotorSolution project JSON file, so specify its path.  
```yaml
# ems functionality link
ems_project_filepath: "Path/To/EMSOptimizer/projects/Dmodel_mixed_variables/Dmodel.json"
```
:::info
Set the file path above according to the location where EMSOptimizer is installed.
:::

## optimization.yaml (`Dmodel_mixed_variables` project)
The contents of `optimization.yaml` are shown below.  
ems_shape_builder is `Dmodel_mixed_builder`, an implementation example that receives one categorical variable (permanent-magnet material), one discrete variable (number of coil turns), and three continuous variables (permanent-magnet dimensions), and configures them through eMotorSolution integration.  
The NGnet on/off method is also configured as in the `Dmodel` project.
```yaml
ems_shape_builder:
  name: Dmodel_mixed_builder
level_set_function:
  name: ngnet
  kwargs:
    sigma: 0.0020
    design_region: [[0.008, 0.0275], [0, 45.0]]
    coordinate: Polar
```

Set `ga` as the optimizer and specify one categorical variable and one discrete variable. The categorical variable (permanent-magnet material) is 0 (NdFeB, $B_r=1.25\text{T}$) or 1 (FerriteMagnet, $B_r=0.40\text{T}$); the discrete variable (number of coil turns) ranges from 20 to 35.  
Specify the ranges of the continuous variables in `bounds`. Here, the lower and upper bounds of the permanent-magnet dimensions are specified.
```yaml
optimizer:
  name: ga
  kwargs:
    seed: 42
    population_size: 30
    variable_type_counts:
      categorical: 1
      discrete: 1
    categorical_choices: [[0, 1]]
    discrete_values: [[20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]]
    bounds: [[10.0, 20.0], [3.0, 13.0], [1.5, 3.5]]
```

## optimization_problem.yaml (`Dmodel_mixed_variables` project)
In `optimization_problem.yaml`, the configuration maximizes average torque and minimizes a virtual permanent-magnet material cost (permanent-magnet area × cost coefficient).  
When `FerriteMagnet` is selected, a coefficient of 0.2 is applied to the cost to reflect its lower cost than `NdFeB`.  
The constraint also limits the maximum voltage to 80.0 V. Optimizing the rotor structure and number of turns balances torque and cost while keeping the voltage below the target value.
```yaml
objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    normalization_const: 2.1
    coefficient: -0.8
  - function_name: magnet_cost
    kwargs:
      physical_tag: 50000
      ferrite_coef: 0.2
    normalization_const: 4.9975e-05
    coefficient: 0.2

ineq_constraints:
  - function_name: maximum_voltage
    normalization_const: 80.0
    baseline: 80.0
```

## Optimization Example
This example performs 50 generations of optimization. The result is shown below: average torque 2.12 Nm, permanent-magnet cost 33.4 ($\text{mm}^2$), and maximum voltage 76.9 V. NdFeB is selected as the permanent-magnet material, and the number of turns is the maximum value, 35.  
The same torque is achieved with less permanent-magnet material than in the original Dmodel. The permanent magnets are closer to the rotor surface than in Dmodel, suggesting a shape that makes greater use of magnet torque.  
![Dmodel mixed-variable optimization result](/img/Dmodel_mixed_usual_best.png)

Now change the objective-function settings as follows. Because `magnet_cost` has a larger weight under these settings, solutions with lower permanent-magnet cost are expected.
```yaml
objectives:
  - function_name: average_torque
    kwargs:
      torque_scale: 4.0
    normalization_const: 2.1
    coefficient: -0.5
  - function_name: magnet_cost
    kwargs:
      physical_tag: 50000
      ferrite_coef: 0.2
    normalization_const: 4.9975e-05
    coefficient: 0.5
```

The result after changing the settings is shown below: average torque 0.87 Nm, permanent-magnet cost 5.85 ($\text{mm}^2$), and maximum voltage 69.0 V. FerriteMagnet is selected as the permanent-magnet material, and the number of turns is the maximum value, 35.  
Compared with the previous result, the selection of FerriteMagnet is notable. The rotor structure also changes accordingly, suggesting a larger contribution from reluctance torque.  
![Dmodel mixed-variable lower-cost optimization result](/img/Dmodel_mixed_lowercost_best.png)
