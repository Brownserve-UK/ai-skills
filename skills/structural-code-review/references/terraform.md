# Terraform

Read the Terraform version, provider versions, module sources, backend, and workspace conventions from the project.

## Design

- A recommended restructure changes resource addresses. Include the `moved` blocks in the recommendation.
- `count` for named resources gives identity by index, and one removed item moves the rest. Recommend `for_each`.
- A module that wraps one resource and repeats its arguments as variables is shallow. Recommend the resource directly, or a module that owns a full unit.
- More than about fifteen variables, or a variable of type `any`, shows a module that hides nothing. Recommend a typed object variable, or two modules.
- A `provider` block inside a module lets the module select where it runs. Recommend providers in the root, with `configuration_aliases` when necessary.
- An output for each attribute is interface width. Recommend outputs for the values a caller needs.
- `envs/dev` and `envs/prod` with the same resources and different literals is duplication that hides a module. Recommend one module with an environment object.
- `count = var.enabled ? 1 : 0` in many places is branch growth. Recommend a module for the optional unit.
- Providers and modules without a version constraint drift. Recommend a pin in `required_providers` and in each `module` block.
