// use libloading::Library;
// use pyo3;

pub mod base;
mod manifest;

// enum TypePlugin {
//     RustPlugin,
//     PythinPlugin
// }

// pub struct RustPlugin {
//     lib: Library,
//     id : String,
// }

// pub struct PythonPlugin {

// }


pub use manifest::PluginManifest;
