pub trait PluginInfo {
    fn name(&self) -> &'static str;
    fn description(&self) -> &'static str;
}
