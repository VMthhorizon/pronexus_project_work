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


def dipendenti_reparto():
    try:
        connessione = connect_database()
        cursore = connessione.cursor()
        input_reparto = input("Inserisci un reparto ").strip()
        query = (
            "SELECT d.reparto, d2.nome, d2.cognome FROM dipartimento AS d LEFT JOIN dipendente AS d2 "
            "ON d.id_dipartimento = d2.id_dipartimento "
            "WHERE d.reparto = %s;"
        )

        cursore.execute(query, (input_reparto,))
        risultati = cursore.fetchall()

        if risultati:
            for riga in risultati:
                print(riga)
        else:
            print("Nessun risultato trovato!")

        cursore.close()

    except Error as errore:
        print(f"Errore nella connessione al DB: {errore}")

    finally:
        if "connessione" in locals() and connessione:
            connessione.close()
            print("Connessione al DB chiusa!")


def aggiungi_dipendente():

    nome = input("Scrivi il nome del dipendente da aggiungere ").strip().upper()
    cognome = input("Scrivi il cognome del dipendente da aggiungere ").strip().upper()
    email = input("Scrivi l'email del dipendente da aggiungere ").strip().upper()
    data_assunzione = (
        input(
            "Inserisci la data in cui il dipendente è stato assunto (es. DD-MM-AAAA) "
        )
        .strip()
        .upper()
    )

    try:
        stipendio = float(input("Scrivi lo stipendio del dipendente da aggiungere "))
    except ValueError as e:
        print(f"Non hai inserito un valore valido! {e}")
        return

    id_dipartimento = int(input("Scrivi l'id del dipartimento da aggiungere "))

    try:
        connessione = connect_database()

        cursore = connessione.cursor()

        query = (
            "INSERT INTO dipendente (nome, cognome, email, data_di_assunzione, stipendio, id_dipartimento) "
            "values (%s, %s, %s, %s, %s, %s);"
        )

        cursore.execute(
            query, (nome, cognome, email, data_assunzione, stipendio, id_dipartimento)
        )

        connessione.commit()
        print("Dipendente aggiunto correttamente")

    except Error as error:
        if connessione:
            connessione.rollback()
            print(f"ERRORE: {error} | Rollback effettuato")

    finally:
        if connessione:
            connessione.close()
            print("Connessione chiusa")


def cerca_dipendente():
    cognome_dipendente = input(
        "Inserisci il cognome del dipendente che vuoi cercare: "
    ).strip()

    try:
        connessione = connect_database()
        cursore = connessione.cursor()

        query = (
            "SELECT d.id_dipendente, d.nome, d.cognome, d.stipendio, d2.reparto "
            "FROM dipendente as d "
            "LEFT JOIN dipartimento as d2 "
            "  ON d.id_dipartimento = d2.id_dipartimento "
            "WHERE d.cognome ILIKE %s "
            "ORDER BY d.id_dipendente;"
        )

        cursore.execute(query, (cognome_dipendente,))
        risultati = cursore.fetchall()

        for id_dip, nome, cognome, stipendio, reparto in risultati:
            print(
                f"ID: {id_dip} | Nome: {nome} | Cognome: {cognome} | "
                f"Reparto: {reparto} | Stipendio: {stipendio}"
            )

    except Error as errore:
        print(f"ERRORE: {errore}")

    finally:
        if connessione:
            connessione.close()
            print("Connessione al DB chiusa!")


def ordina_dipendenti():

    try:
        connessione = connect_database()

        cursore = connessione.cursor()

        query = (
            "SELECT d.id_dipendente, d.nome, d.cognome, d2.reparto "
            "FROM dipendente AS d "
            "LEFT JOIN dipartimento AS d2 on d.id_dipartimento = d2.id_dipartimento "
            "ORDER BY d2.reparto;"
        )

        cursore.execute(query)

        risultati = cursore.fetchall()

        for riga in risultati:
            print(
                f"id: {riga[0]} | Nome: {riga[1]} | "
                f"Cognome: {riga[2]} | Reparto: {riga[3]}"
            )

    except Error as errore:
        print(f"ERRORE: {errore}")

    finally:
        if "connessione" in locals() and connessione:
            connessione.close()
            print("Connessione al DB chiusa!")


def media_stipendi():

    try:

        connessione = connect_database()

        cursore = connessione.cursor()

        query = (
            "select d.reparto, coalesce(round(avg(d2.stipendio) , 2), 0) AS media_stipendio "
            "FROM dipartimento AS d "
            "LEFT JOIN dipendente AS d2 ON d.id_dipartimento = d2.id_dipartimento "
            "GROUP BY d.reparto;"
        )

        cursore.execute(query)

        risultati = cursore.fetchall()

        for riga in risultati:
            print(f"Reparto: {riga[0]} | Media Stipendi: {riga[1]}")

    except Error as errore:
        print(f"ERRORE: {errore}")

    finally:
        if "connessione" in locals() and connessione:
            connessione.close()
            print("Connessione chiusa!")


def update_stipendi():

    try:
        connessione = connect_database()

        cursore = connessione.cursor()

        query = (
            "UPDATE dipendente SET stipendio = stipendio * %s "
            "WHERE dipendente.data_di_assunzione >= %s AND dipendente.data_di_assunzione <= %s;"
        )

        cursore.execute(query, (1.05, "01-01-2020", "31-12-2020"))

        connessione.commit()

        print("Stipendio per i dipendenti assunti nel 2020 aggiornato")

    except Error as errore:
        if connessione:
            connessione.rollback()
            print(f"ERRORE: {errore}, AZIONE ANNULLATA")

    finally:
        connessione.close()

        print("CONNESSIONE CHIUSA")


while True:

    try:
        opzioni = int(
            input(
                "Inserisci:\n"
                "1 - Per aggiungere un nuovo dipendente\n"
                "2 - Per cercare un dipendente tramite il cognome corrispondente\n"
                "3 - Per visualizzare l'elenco dei dipendenti e del relativo reparto\n"
                "4 - Per cercare i dipendenti di un dipartimento\n"
                "5 - Per avere la lista degli stipendi medi in base al reparto\n"
                "6 - Per aggiornare gli stipendi dei dipendenti assunti nel 2020\n"
                "0 - Per uscire dal programma\n"
            ).strip()
        )
    except ValueError as e:
        print(f"Valore inserito non valido {e}")
        continue

    match opzioni:
        case 1:
            aggiungi_dipendente()

        case 2:
            cerca_dipendente()

        case 3:
            ordina_dipendenti()

        case 4:
            dipendenti_reparto()

        case 5:
            media_stipendi()

        case 6:
            update_stipendi()

        case 0:
            break
        case _:
            print("Scelta non valida")
