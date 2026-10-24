import flet as ft
from flet import TextAlign

from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO
    def prezzo_meno(e):
        txt_prezzo.value = int(txt_prezzo.value)-1
        page.update()
    def prezzo_piu(e):
        txt_prezzo.value = int(txt_prezzo.value) + 1
        page.update()
    txt_tipo = ft.TextField(label="Tipo", width=200)
    txt_marca = ft.TextField(label="Marca", width=200)
    txt_anno = ft.TextField(label="Anno di acquisto", width=150)
    txt_prezzo = ft.TextField(value="0", width=50, text_align = TextAlign.CENTER)
    pulsante_meno = ft.IconButton(icon=ft.Icons.REMOVE, icon_color = ft.Colors.RED, on_click=prezzo_meno)
    pulsante_piu = ft.IconButton(icon=ft.Icons.ADD, icon_color = ft.Colors.GREEN, on_click=prezzo_piu)
    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO
    def inserisci_strumento(e):
        tipo = txt_tipo.value
        marca = txt_marca.value
        anno = txt_anno.value
        prezzo = txt_prezzo.value
        if tipo == "" or marca =="" or anno == "":
            alert.show_alert("Tutti i campi devono essere compilati")
            return
        try:
            anno = int(anno)
            prezzo = int(prezzo)
        except ValueError:
            alert.show_alert("Inserire dei valori validi per prezzo e anno")
            return
        deposito.aggiungi_strumento(tipo, marca, anno, prezzo)
        txt_tipo.value = ""
        txt_marca.value = ""
        txt_anno.value = ""
        txt_prezzo.value = "0"
        aggiorna_lista_strumenti()
        page.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO
    pulsante_aggiungi_strumento = ft.Button("Aggiungi Strumento", on_click = inserisci_strumento)

    # --- LAYOUT ---
    page.add(
        ft.Row(controls =toggle_cambia_tema, alignment=ft.MainAxisAlignment.START),

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Divider(),
        ft.Text("Aggiungi Nuovo Strumento", size=20),
        ft.Row(controls=[txt_tipo, txt_marca, txt_anno, pulsante_meno, txt_prezzo, pulsante_piu],
               alignment=ft.MainAxisAlignment.CENTER),
        pulsante_aggiungi_strumento,
        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
