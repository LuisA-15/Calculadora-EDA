# core/microkernel.py
from typing import Dict, List, Sequence
from types import ModuleType
import importlib.util, inspect, os, sys
from core.interfaces import Operation


class Microkernel:
    def __init__(self, bus, plugins_dir: str = "plugins") -> None:
        self._registry: Dict[str, Operation] = {}
        self._plugins_dir = plugins_dir
        self._loaded_modules: List[ModuleType] = []
        self.bus = bus
        self.bus.subscribe("calculate", self.on_calculate)

    def discover_and_load(self) -> None:
        if not os.path.isdir(self._plugins_dir):
            return
        for fname in os.listdir(self._plugins_dir):
            if not fname.endswith(".py") or fname.startswith("__"):
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
                print(f"Error loading {fname}: {e}")

    def _register_from_module(self, module: ModuleType) -> None:
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Operation) and obj is not Operation:
                instance = obj()
                self.register(instance)

    def register(self, op: Operation) -> None:
        name = op.name().lower().strip()
        if name not in self._registry:
            self._registry[name] = op

    def available(self):
        return sorted(self._registry.keys())

    # Event handler
    def on_calculate(self, data):
        try:
            opname = data["operator"].lower().strip()
            args = [float(x) for x in data["args"]]
            if opname not in self._registry:
                raise KeyError(f"Unknown operation '{opname}'.")
            op = self._registry[opname]
            result = op.execute(args)
            self.bus.publish("result", {"result": result})
        except Exception as e:
            self.bus.publish("error", {"message": str(e)})
