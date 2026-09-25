# Terraform

Read the Terraform version, provider versions, module sources, backend, and workspace conventions from the project.

## Behavior

- Check resource addresses and instance keys after a refactor. A changed address destroys and replaces the resource unless a `moved` block exists.
- Check `count` for named resources. `count` gives identity by index, and one removed item moves the rest. Recommend `for_each`.
- Check unknown values in `count`, `for_each`, and provider configuration. A value that is unknown at plan time stops the plan.
- Check secrets in state, plans, logs, and outputs. `sensitive = true` hides a value in output but not in state.
- Check provisioners, `null_resource`, and `local-exec` for repeat behavior, failure recovery, and hidden side effects. Shell in Terraform has no plan and no state.
- Check `lifecycle` rules. A stateful resource without `prevent_destroy` can disappear in one plan. An `ignore_changes` list can hide drift.
- Check `depends_on` against the real dependencies. Recommend an attribute reference when one can exist.

## Design

- A module that wraps one resource and repeats its arguments as variables is shallow. Recommend the resource directly, or a module that owns a full unit.
- More than about fifteen variables, or a variable of type `any`, shows a module that hides nothing. Recommend a typed object variable, or two modules.
- A `provider` block inside a module lets the module select where it runs. Recommend providers in the root, with `configuration_aliases` when necessary.
- An output for each attribute is interface width. Recommend outputs for the values a caller needs.
- `envs/dev` and `envs/prod` with the same resources and different literals is duplication that hides a module. Recommend one module with an environment object.
- `count = var.enabled ? 1 : 0` in many places is branch growth. Recommend a module for the optional unit.
- Providers and modules without a version constraint drift. Recommend a pin in `required_providers` and in each `module` block.
- Keep a small module when it gives a real infrastructure contract. Do not demand one module for each resource.

## Checks

Use `terraform validate`, `fmt -check`, and the project tests.
Read an available plan for the intended environment. Plan generation can connect to providers, remote state, and external programs. Use isolated fixtures when live access is not permitted.
Do not run `apply` or `destroy` for a review.
Do not claim that a successful validation proves a safe deployment.
