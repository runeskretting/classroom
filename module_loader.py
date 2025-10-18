"""
Module Loader
Handles loading module data from JSON files in the modules/ directory.
"""

import json
import os
from glob import glob


class ModuleLoader:
    """Loads and manages module data from JSON files."""

    def __init__(self, modules_dir='modules'):
        self.modules_dir = modules_dir
        self._modules_cache = None

    def load_all_modules(self):
        """Load all module JSON files from the modules directory."""
        if self._modules_cache is not None:
            return self._modules_cache

        modules = {}
        module_files = sorted(glob(os.path.join(self.modules_dir, 'module_*.json')))

        for module_file in module_files:
            try:
                with open(module_file, 'r', encoding='utf-8') as f:
                    module_data = json.load(f)
                    module_id = module_data.get('id')
                    if module_id:
                        modules[module_id] = module_data
            except Exception as e:
                print(f"Error loading {module_file}: {str(e)}")

        self._modules_cache = modules
        return modules

    def get_module(self, module_id):
        """Get a specific module by ID."""
        modules = self.load_all_modules()
        return modules.get(module_id)

    def get_module_count(self):
        """Get the total number of modules."""
        return len(self.load_all_modules())

    def reload_modules(self):
        """Clear cache and reload all modules."""
        self._modules_cache = None
        return self.load_all_modules()


# Global module loader instance
_loader = ModuleLoader()


def get_all_modules():
    """Get all modules."""
    return _loader.load_all_modules()


def get_module(module_id):
    """Get a specific module by ID."""
    return _loader.get_module(module_id)


def get_module_count():
    """Get the total number of modules."""
    return _loader.get_module_count()


def reload_modules():
    """Reload all modules from disk."""
    return _loader.reload_modules()
