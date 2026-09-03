import importlib
import sys

REQUIRED_MODULES = ["gradio", "transformers", "torch"]


def main() -> int:
    failed = []
    for module_name in REQUIRED_MODULES:
        try:
            importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001
            failed.append((module_name, str(exc)))

    if failed:
        print("Import verification failed:")
        for module_name, error in failed:
            print(f"- {module_name}: {error}")
        return 1

    print("All required imports succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
