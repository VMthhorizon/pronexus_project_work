import csv
import psycopg2
import os

from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()


def connect_database():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


lista_dipendenti = []
try:
    with open("dipendenti.csv", "r", newline="", encoding="utf-8") as file_csv:

        reader = csv.DictReader(file_csv)

        for riga in reader:
            try:
                stipendio = float(riga["stipendio"])
            except ValueError as e:
                print(f"Non è stato inserito un numero corretto! {e}")
                continue

            lista_dipendenti.append(
                {
                    "Nome": riga["nome"].strip().upper(),
                    "Cognome": riga["cognome"].strip().upper(),
                    "Reparto": riga["reparto"].strip().upper(),
                    "Stipendio": stipendio,
                }
            )

except FileNotFoundError as e:

    print(f"ATTENZIONE: Il FILE non esiste! {e}")


def aggiungi_dipendente():
    nome = input("Scrivi il nome del dipendente da aggiungere ").strip().upper()
    cognome = input("Scrivi il cognome del dipendente da aggiungere ").strip().upper()
    reparto = input("Scrivi il reparto del dipendente da aggiungere ").strip().upper()

    try:
        stipendio = float(input("Scrivi lo stipendio del dipendente da aggiungere "))
    except ValueError as e:
        print(f"Non hai inserito un valore valido! {e}")

    nuovo_dipendente = {
        "Nome": nome,
        "Cognome": cognome,
        "Reparto": reparto,
        "Stipendio": stipendio,
    }

    lista_dipendenti.append(nuovo_dipendente)

    try:
        with open("dipendenti.csv", "a", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    nuovo_dipendente["Nome"],
                    nuovo_dipendente["Cognome"],
                    nuovo_dipendente["Reparto"],
                    nuovo_dipendente["Stipendio"],
                ]
            )

    except OSError as e:
        print(f"File non trovato o corrotto! {e}")


def cerca_dipendente():
    cognome_dipendente = input(
        "Inserisci il cognome del dipendente che vuoi cercare "
    ).upper()
    dipendenti_trovati = [
        dipendente
        for dipendente in lista_dipendenti
        if dipendente["Cognome"] == cognome_dipendente
    ]

    if not dipendenti_trovati:
        print("Nessun dipendente trovato!")
        return

    for trovato in dipendenti_trovati:
        print(
            f"Nome: {trovato['Nome']} | Cognome: {trovato['Cognome']} | "
            f"Reparto: {trovato['Reparto']} | Stipendio: {trovato['Stipendio']}"
        )


def chiave_reparto(dipendente):
    return dipendente["Reparto"]


def ordina_dipendenti():
    if not lista_dipendenti:
        print("Nessun dipendente presente.")
        return

    ordinati = sorted(lista_dipendenti, key=chiave_reparto)

    for dipendente in ordinati:
        print(
            f"Nome: {dipendente['Nome']} | Cognome: {dipendente['Cognome']} | "
            f"Reparto: {dipendente['Reparto']} | Stipendio: {dipendente['Stipendio']}"
        )


while True:

    try:
        opzioni = int(
            input(
                "Inserisci:\n"
                "1 - Per aggiungere un nuovo dipendente\n"
                "2 - Per cercare un dipendente tramite il cognome corrispondente\n"
                "3 - Per visualizzare l'elenco dei dipendenti per reparto, in ordine alfabetico\n"
                "0 - Per uscire dal programma\n"
            ).strip()
        )
    except ValueError as e:
        print(f"Valore inserito non valido {e}")

    match opzioni:
        case 1:
            aggiungi_dipendente()

        case 2:
            cerca_dipendente()

        case 3:
            ordina_dipendenti()
        case 0:
            break
        case _:
            print("Scelta non valida")
