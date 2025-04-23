use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug)]
pub struct PluginManifest {
    pub name: String,
    pub description: String,
    pub version: String,
    pub author: Option<String>,
    pub plugin_type: String,
    pub entry: Option<String>,    // pour Python
    pub library: Option<String>,  // pour Rust
    pub os: Option<Vec<String>>,
    pub requires: Option<Vec<String>>,  // Dépendances supplémentaires, si nécessaire
}
