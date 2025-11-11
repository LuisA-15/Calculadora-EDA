import importlib.util
import inspect
import os
import sys
from types import ModuleType
from typing import Dict, List, Sequence

from core.interfaces import Operation

class Microkernel:
    def __init__(self, plugins_dir: str = "plugins") -> None:
        self._registry: Dict[str, Operation] = {}
        self._plugins_dir = plugins_dir
        self._loaded_modules: List[ModuleType] = []


    # --- Plugins---
    def discover_and_load(self) -> None:
        """Dynamically import all .py files in plugins_dir and register Operation subclasses."""
        if not os.path.isdir(self._plugins_dir):
            return
        for fname in os.listdir(self._plugins_dir):
            if not fname.endswith(".py") or fname.startswith("__"): # skip dunders
                continue
            fpath = os.path.join(self._plugins_dir, fname)
            modname = f"plugin_{os.path.splitext(fname)[0]}"
            try:
                spec = importlib.util.spec_from_file_location(modname, fpath)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[modname] = module
                    spec.loader.exec_module(module)
                    self._loaded_modules.append(module)
                    self._register_from_module(module)

            except Exception as e:
                print(f"Errorr raise {e}")


    def _register_from_module(self, module: ModuleType) -> None:
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Operation) and obj is not Operation:
                instance = obj()
                self.register(instance)


    # --- Registry ---
    def register(self, op: Operation) -> None:
        name = op.name().lower().strip()
        if not name in self._registry:
            self._registry[name] = op


    def available(self) -> List[str]:
        return sorted(self._registry.keys())


    def execute(self, opname: str, args: Sequence[float]) -> float:
        opname = opname.lower().strip()
        if opname not in self._registry:
            raise KeyError(f"Unknown operation '{opname}'. Available: {', '.join(self.available())}")
        op = self._registry[opname]
        return op.execute([float(x) for x in args])