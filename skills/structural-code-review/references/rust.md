# Rust

Read the Rust edition, the minimum supported Rust version, the feature flags, and the async runtime from the project.

## Design

- `.clone()` at each call site to satisfy the borrow checker shows an unclear owner. Recommend one owner, a borrow, or `Cow`.
- `Arc<Mutex<T>>` or `Rc<RefCell<T>>` as the default data shape hides the data flow. Recommend one owner and data in, data out.
- A `match` on a `&str` for a fixed set of values is a missing enum. Recommend `FromStr` at the boundary and the enum inside.
- `Box<dyn Error>` or `anyhow` in a library interface stops the caller from matching on the error. Recommend a typed error at each public boundary. `anyhow` belongs at the top of a binary.
- A trait with one implementation is a shallow interface. Test doubles do not count as a second implementation.
- A `T: Trait` bound in five signatures for one call site is an abstraction in the incorrect place. Recommend `dyn Trait` at one boundary, or the concrete type.
- Two or more lifetime parameters on a public struct show that callers see the internal borrow structure. Recommend that the struct owns its data.
- `#[cfg(feature = ...)]` inside a function body is branch growth. Recommend one module for each feature with one interface.
- A `macro_rules!` that expands to a `return` or a loop hides control flow. Recommend a function.

