# Android

Read the minimum SDK, target SDK, language, UI framework, and library versions from the project.
Do not assume Kotlin or Compose. Check the project.

## Behavior

- Check blocking work on the main thread. A `suspend` function does not move work to a different thread by itself.
- Check coroutine and callback ownership against the component lifecycle. `GlobalScope` and a scope without an owner make work that no one can cancel.
- Check cancellation, exception handling, and tasks that outlive the screen or the process.
- Check state recovery after a configuration change and after process death. Use the persistence level that each value needs.
- Check references that keep a destroyed `Activity`, `Fragment`, or `View` alive: a `Context` in a singleton or a static field.
- For Compose, check side effects in a composable body, effect keys, and state ownership across recomposition.
- Check permissions, exported components, `Intent` inputs, and sensitive data against the supported SDK versions.
- Check user-visible changes for broken navigation, controls that a user cannot get to, and loss of user input.

## Design

- Business logic in an `Activity`, `Fragment`, or composable ties the domain to the UI lifecycle. Recommend a `ViewModel` or a use case class.
- A `ViewModel` with more than one screen state, or with network and database code inside, is shallow with a wide interface. Recommend one `ViewModel` for each screen and a repository for data.
- A repository that only sends each call to a DAO or an API client adds no contract. Recommend real work in it, or its removal.
- `isLoading` next to domain fields in one class mixes two lifecycles. Recommend a sealed `UiState` and a separate domain model.
- `!!` outside tests is a boundary where the type is not correct. Recommend a type change, or a check with a typed result.
- `Intent` extras and navigation arguments keyed by string constants spread across files. Recommend a typed route or an argument class.
- A data model with all fields nullable did not parse its input. Recommend a DTO at the network boundary and a non-null domain model inside.
- `LiveData`, `Flow`, and RxJava in one flow put a shallow adapter between each pair. Recommend one reactive type for each module.
- A feature flag test in a composable or a `ViewModel` is branch growth in shared UI. Recommend a flag that selects the implementation at the injection point.
- A Gradle module that imports the internals of a second module has no boundary. Recommend an `api` module and an `impl` module.

## Checks

Use the project's local tests and device tests for the failure path.
Do not claim lifecycle or device behavior from a compilation check alone.
