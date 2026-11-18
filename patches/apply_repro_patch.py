from pathlib import Path
import sys

repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
main = repo / "main.py"
if not main.exists():
    raise SystemExit(f"main.py not found in {repo}")

text = main.read_text(encoding="utf-8-sig")

marker = "import constants\n"
imports = "import constants\nimport typer\nfrom pathlib import Path\n"
if "import typer" not in text or "from pathlib import Path" not in text:
    if marker not in text:
        raise SystemExit("Could not locate imports in main.py")
    text = text.replace(marker, imports, 1)

text = text.replace(
    'with open("SLIKUBE.sarif", "w") as f:',
    'with open(Path(directory, "SLIKUBE.sarif"), "w") as f:'
)

# The released file defines a Typer argument but calls main() directly.
# Replace only the final indented call under __main__.
needle = "    main()"
idx = text.rfind(needle)
if idx != -1:
    text = text[:idx] + "    typer.run(main)" + text[idx + len(needle):]
elif "typer.run(main)" not in text:
    raise SystemExit("Could not locate final main() call")

main.write_text(text, encoding="utf-8")

docker_src = Path(__file__).with_name("Dockerfile.repro")
docker_dst = repo / "Dockerfile.repro"
docker_dst.write_text(docker_src.read_text(encoding="utf-8"), encoding="utf-8")

print("Applied reproduction patch:")
print("- imported typer and pathlib.Path")
print("- changed direct main() call to typer.run(main)")
print("- writes SLIKUBE.sarif into the mounted analysis directory")
print("- installed Dockerfile.repro with pinned runtime dependencies and yq")
