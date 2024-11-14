import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

type_mapping = {
    # Map Mintos types to Portfolio Performance types
    "Tilgungszahlungen": None,
    "Zinszahlungen": "Zinsen",
    "Erhaltene Zinsen aus Kreditrückkauf": "Zinsen",
    "Zinseinnahmen aus Kreditrückkauf": "Zinsen",
    "Erhaltene Zinsen": "Zinsen",
    "Erhaltene Tilgung aus Kreditrückkauf": None,
    "Übertragungsabgleich der Verzugszinseinnahmen": "Zinsen",
    "Investitionen in Darlehen": None,
    "Investition": None,
    "Zinseinnahmen aus ausstehenden Zahlungen": "Zinsen",
    "Steuereinbehalt": "Steuern",
    "Erhaltene Tilgung aus Rückkauf kleiner Kreditteile": None,
    "Erhaltene Tilgung": None,
    "Zweitmarkt-Transaktion – Ab- oder Aufschlag": "Zinsen",  # noqa: RUF001
    "Zweitmarkt-Transaktion": None,
    "Zweitmarktgebühr": "Gebühren",
    "Einzahlungen": "Einlage",
    "Abhebung": "Entnahme",
    "Antrag auf Beitrag/Spende": "Gebühren",
}

columns_of_interest = ["Datum", "Typ", "Wert", "Buchungswährung"]
how_many_types_expected = len(set(type_mapping.values()).difference({None}))


def _ask_if_ok(msg: str) -> None:
    print(msg)  # noqa: T201
    asdf = input("OK (Y/N)? ")
    print()  # noqa: T201

    if asdf not in ["Y", "y"]:
        sys.exit(1)


def start() -> None:
    """Entrypoint for CLI.

    Raises:
        Exception: _description_
    """
    statement_files = list(Path().glob("*.csv"))

    _ask_if_ok(f"Using the following files: {[x.name for x in statement_files]}")

    data = (
        pd.concat([pd.read_csv(x) for x in statement_files])
        .convert_dtypes()
        .assign(
            Datum=lambda df: pd.to_datetime(df["Datum"]).dt.date,
            Typ=lambda df: df["Zahlungsart"].replace(type_mapping),
            Wert=lambda df: df.groupby([df["Datum"], "Typ"])["Umsatz"].transform("sum").round(5),
        )
        .rename(columns={"Währung": "Buchungswährung"})
        .dropna(subset="Typ")
        .drop_duplicates(columns_of_interest)
    )

    if len(data["Typ"].unique().tolist()) != how_many_types_expected:
        msg = (
            f"Expecting {how_many_types_expected} distinct values here, got: '{data['Typ'].unique().tolist()}'. "
            + "Please check if Mintos export changed."
        )
        raise Exception(msg)  # noqa: TRY002

    output_file_name = Path("output") / f"{datetime.now().strftime('%Y-%m-%d')}.csv"  # noqa: DTZ005
    _ask_if_ok(f"Using the following output file: {output_file_name}")

    if not output_file_name.parent.exists():
        output_file_name.parent.mkdir()

    data[columns_of_interest].to_csv(
        output_file_name,
        index=False,
        sep=";",
        decimal=",",
    )
