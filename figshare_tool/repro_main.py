from pathlib import Path
import argparse
import pandas as pd
import scanner
import main
import constants

def run(directory):
    directory = Path(directory).resolve()
    content_as_ls = scanner.runScanner(str(directory))
    df = pd.DataFrame(main.getCountFromAnalysis(content_as_ls))
    outfile = directory / "slikube_figshare_results.csv"
    df.to_csv(
        outfile,
        header=constants.CSV_HEADER,
        index=False,
        encoding=constants.CSV_ENCODING,
    )
    print(f"Wrote {outfile}")
    print(f"Rows analysed: {len(df)}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(
        description="Run the unmodified paper-era Figshare SLI-KUBE detector via a path wrapper."
    )
    ap.add_argument("directory")
    args = ap.parse_args()
    run(args.directory)
