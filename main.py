import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from datetime import datetime

from db import (
    inizializza_db,
    salva_spesa_db,
    visualizza_spese_db,
    elimina_spesa_db,
    visualizza_importo_db,
    visualizza_grafico_spese_db
)


class GestioneSpeseApp:

    def __init__(self): #costruttore
        inizializza_db()

        self.root = tk.Tk() #finestra principale
        self.root.title("Gestione spese")
        self.root.geometry("385x500")
        self.root.configure(bg="lightblue")
        self.root.resizable(False, False)

        self._crea_widgets() #popola la finestra principale


    # CREAZIONE WIDGET PRINCIPALI

    def _crea_widgets(self):

        # Nome articolo
        tk.Label(self.root, text="Nome articolo:", bg="red", fg="white").grid(row=0, column=0, sticky="nw")
        self.input_nome = tk.Entry(self.root, width=32, fg="gray")
        self.input_nome.grid(row=0, column=1, padx=5)
        self.input_nome.insert(0, "Nome del tuo articolo")

        # Importo
        tk.Label(self.root, text="Importo in Euro:", bg="red", fg="white").grid(row=1, column=0, sticky="nw")
        self.input_importo = tk.Entry(self.root, width=32, fg="gray")
        self.input_importo.grid(row=1, column=1, padx=5)
        self.input_importo.insert(0, "00.00")

        # Data
        tk.Label(self.root, text="Data:", bg="red", fg="white").grid(row=2, column=0, sticky="nw")
        self.input_data = tk.Entry(self.root, width=32, fg="gray")
        self.input_data.grid(row=2, column=1, padx=5)
        self.input_data.insert(0, datetime.now().strftime("%d/%m/%Y"))

        # Categoria
        tk.Label(self.root, text="Categoria:", bg="red", fg="white").grid(row=3, column=0, sticky="nw")
        self.listbox_categoria = tk.Listbox(self.root, width=32, height=4, selectmode=tk.SINGLE)
        categorie = [
            "Abbigliamento e accessori",
            "Elettronica e tecnologia",
            "Tempo libero e intrattenimento",
            "Spese varie"
        ]
        for cat in categorie:
            self.listbox_categoria.insert(tk.END, cat)
        self.listbox_categoria.grid(row=3, column=1, padx=5)

        # Bottone salva
        tk.Button(
            self.root,
            text="CONFERMA SPESA",
            bg="green",
            fg="white",
            command=self.salva
        ).grid(row=10, column=0, columnspan=4, pady=50, sticky="ew")

        # Altre funzionalità
        tk.Label(self.root, text="Altre funzionalità:", bg="red", fg="white").grid(row=15, column=0)

        tk.Button(
            self.root,
            text="Visualizza/Elimina spese",
            bg="blue",
            fg="white",
            command=self.visualizza_spese
        ).grid(row=20, column=0, columnspan=4, pady=10, sticky="ew")

        tk.Button(
            self.root,
            text="Visualizza importo spese totale",
            bg="blue",
            fg="white",
            command=self.visualizza_importo
        ).grid(row=25, column=0, columnspan=4, pady=10, sticky="ew")

        tk.Button(
            self.root,
            text="Visualizza andamento delle spese mensili",
            bg="blue",
            fg="white",
            command=self.visualizza_grafico_spese
        ).grid(row=30, column=0, columnspan=4, pady=10, sticky="ew")

    # SALVATAGGIO SPESA

    def salva(self):
        nome = self.input_nome.get().strip()
        importo_str = self.input_importo.get().strip()
        data_str = self.input_data.get().strip()

        # Categoria
        try:
            categoria = self.listbox_categoria.get(self.listbox_categoria.curselection())
        except tk.TclError:
            messagebox.showerror("Errore", "Seleziona una categoria.")
            return

        # Campi vuoti
        if not nome:
            messagebox.showerror("Errore", "Il campo 'Nome articolo' non può essere vuoto.")
            return
        if not importo_str:
            messagebox.showerror("Errore", "Il campo 'Importo' non può essere vuoto.")
            return
        if not data_str:
            messagebox.showerror("Errore", "Il campo 'Data' non può essere vuoto.")
            return

        # Validazione importo
        try:
            importo = float(importo_str.replace(",", "."))
        except ValueError:
            messagebox.showerror("Errore", "L'importo deve essere un numero valido.")
            return

        # Validazione data
        try:
            data = datetime.strptime(data_str, "%d/%m/%Y").strftime("%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Errore", "La data deve essere nel formato GG/MM/AAAA.")
            return

        salva_spesa_db(nome, importo, data, categoria)
        messagebox.showinfo("Conferma", "Dati salvati correttamente!")

    # ---------------------------------------------------------
    # VISUALIZZA SPESE
    # ---------------------------------------------------------
    def visualizza_spese(self):
        finestra = tk.Toplevel(self.root)
        finestra.title("Spese memorizzate")
        finestra.geometry("780x400")
        finestra.configure(bg="lightblue")

        dati = visualizza_spese_db()

        colonne = ("ID", "Nome", "Importo", "Data", "Categoria")
        tabella = ttk.Treeview(finestra, columns=colonne, show="headings")

        for col in colonne:
            tabella.heading(col, text=col)
            tabella.column(col, width=100)

        for riga in dati:
            tabella.insert("", "end", values=riga)

        tabella.pack(expand=True, fill="both", pady=10)

        def elimina():
            selezione = tabella.selection()
            if not selezione:
                messagebox.showwarning("Attenzione", "Seleziona una riga da eliminare.")
                return

            item_id = selezione[0]
            item = tabella.item(item_id)
            articolo_id = item["values"][0]

            elimina_spesa_db(articolo_id)
            tabella.delete(item_id)

        tk.Button(
            finestra,
            text="Elimina spesa",
            bg="red",
            fg="white",
            command=elimina
        ).pack(pady=10)

    # ---------------------------------------------------------
    # VISUALIZZA IMPORTO TOTALE
    # ---------------------------------------------------------
    def visualizza_importo(self):
        totale = visualizza_importo_db()
        if totale is None:
            totale = 0

        finestra = tk.Toplevel(self.root)
        finestra.title("Totale delle tue spese")
        finestra.geometry("273x160")
        finestra.configure(bg="lightblue")
        finestra.resizable(False, False)

        tk.Label(
            finestra,
            text=f"In totale hai speso: {totale:.2f} Euro",
            font=("Arial", 14, "bold")
        ).grid(row=3, column=0)

        tk.Button(
            finestra,
            text="Chiudi",
            bg="red",
            fg="white",
            command=finestra.destroy
        ).grid(row=4, column=0, pady=80, padx=90, sticky="nsew")

    # ---------------------------------------------------------
    # GRAFICO SPESE
    # ---------------------------------------------------------
    def visualizza_grafico_spese(self):
        dati = visualizza_grafico_spese_db()

        if dati:
            mesi, importi = zip(*dati)
        else:
            mesi, importi = [], []

        plt.figure(figsize=(8, 8), facecolor="lightblue")
        plt.bar(mesi, importi, color="red", alpha=0.7)
        plt.xlabel("Mese/Anno")
        plt.ylabel("Totale spese (€)")
        plt.title("Andamento delle spese mensili")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.show()

    # ---------------------------------------------------------
    # AVVIO APP
    # ---------------------------------------------------------
    def run(self):
        self.root.mainloop()


# Avvio
if __name__ == "__main__":
    app = GestioneSpeseApp()
    app.run()