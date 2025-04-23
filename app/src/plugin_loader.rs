use std::path::Path;
use std::fs;

pub fn load_manifest<P: AsRef<Path>>(path: P) -> Result<PluginManifest, toml::de::Error> {
    let content = fs::read_to_string(path).unwrap();
    let manifest: PluginManifest = toml::de::from_str(&content)?;
    Ok(manifest)
}
