# Puppet

Read the Puppet version, module constraints, Hiera configuration, and target operating systems from the project.

## Design

- `ensure_resource` and `if !defined()` hide that two classes claim one resource. Recommend one owner class.
- A hostname, an address, or a team name in a component module ties the module to one site. Recommend a profile that gets the data from Hiera and passes parameters.
- A role with resources in it does more than name profiles. Recommend a move of each resource to a profile.
- A profile that manages one resource is a shallow layer. Recommend that it composes two or more classes.
- `lookup()` inside a component class hides the interface. Recommend class parameters with defaults in module `data/`.
- More than about twenty parameters on one class shows more than one job. Recommend a division, or a `Struct` parameter.
- A defined type with one use is a shallow abstraction. Recommend inline resources until a second use exists.
- `case $facts['os']['family']` in many classes is branch growth. Recommend module data with the OS family as a hierarchy level.
- A chain of ten `->` and `~>` arrows breaks when one resource moves. Recommend `contain` at the class level and `require` where a resource needs it.
- A collector (`<| |>`) that changes resources from a different class is action at a distance. Recommend a parameter on the class that owns the resource.
- Conditions and loops in an ERB or EPP template make a program without tests. Recommend that the class computes the values and the template prints them.
