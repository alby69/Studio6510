import os
import importlib.util

class PluginManager:
    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = []

    def load_plugins(self, main_window):
        if not os.path.exists(self.plugin_dir):
            return

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                file_path = os.path.join(self.plugin_dir, filename)
                plugin_name = filename[:-3]

                spec = importlib.util.spec_from_file_location(plugin_name, file_path)
                module = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(module)
                    if hasattr(module, "register"):
                        module.register(main_window)
                        self.plugins.append(module)
                        print(f"Loaded plugin: {plugin_name}")
                except Exception as e:
                    print(f"Failed to load plugin {plugin_name}: {e}")
