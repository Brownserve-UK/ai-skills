# TypeScript

Read the compiler configuration, runtime, module format, framework, and dependency versions from the project.

## Behavior

- Check external data at each runtime boundary. A type assertion does not validate data. Recommend a parse function that returns the type or an error.
- Follow `any`, `as`, and `!` to a real contract failure before you report them. Accept `unknown` at an untrusted boundary when the code narrows it before use.
- Check optional fields, missing properties, and null values against the real input contract.
- Check promises for lost errors, a missing `await`, unbounded concurrency, and cancellation gaps. `catch (e) {}` hides an incorrect state.
- Check shared mutable state and stale closures when a callback runs after the function returns.
- Check numeric precision, truthiness defaults, and serialization on the changed data path.
- Check framework effects and subscriptions for cleanup, repeat behavior, and ownership.

## Design

- A boolean parameter that changes what a function does is a hidden second function. Recommend two functions or a discriminated union.
- An interface where most fields are optional is two or more types with one name. Recommend a discriminated union with one type for each state.
- A conditional or mapped type that a reader cannot follow in one minute hides an easy shape. Recommend the plain type, even with some duplication.
- A `utils.ts` or `helpers.ts` that becomes larger with each change has no owner. Recommend a module for each concept with a small export list.
- An `index.ts` that re-exports everything flattens the module structure and causes import cycles. Recommend public types only, or no barrel.
- An import of the internal files of a second feature has no boundary. Recommend one entry module for each feature.
- An import cycle shows two modules that are one module, or a shared type with no home. Recommend a third module for the shared type.
- `throw "string"` for a condition the caller must handle stops the caller from matching. Recommend an error class or a result type.
- A React component that owns fetch, cache, and layout has three jobs. Recommend a hook for data and a component for layout.
- A `useEffect` that sets state a second `useEffect` reads is a hidden state machine. Recommend a reducer, or logic outside the component.
- Keep a small adapter or schema type when it protects a real boundary.

## Checks

Use the project's type check, tests, and lint rules.
Do not infer runtime safety from a successful type check.
