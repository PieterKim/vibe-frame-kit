"""Report executable availability only; do not read credentials or environment values."""
import platform
import shutil
import sys
print("OS:", platform.system(), platform.release())
print("Python:", platform.python_version(), "OK" if sys.version_info >= (3, 11) else "NEEDS 3.11+")
for name in ("git", "codex", "node", "npm"):
    print(name + ":", "available" if shutil.which(name) else "not available")
print("Model, course versions and MCP: instructor decision required")
