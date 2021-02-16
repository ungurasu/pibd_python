# pibd_python
*Ungurasu Ioan-Andrei 435E UPB ETTI 2021*

- [pibd_python](#pibd-python)
  * [Clasa DatabaseHandler](#clasa-databasehandler)
  * [fail-window(self, text)](#fail-window-self--text-)
  * [success-window(self, text)](#success-window-self--text-)
  * [insert(self, table, columns, nullable, fields)](#insert-self--table--columns--nullable--fields-)

## Clasa DatabaseHandler
Contine logica pentru interfata grafica, dar si logica pentru operarea asupra bazei de date.

## fail-window(self, text)
*text* - mesajul de eroare

Metoda care genereaza o fereastra cu un mesaj de eroare.

## success-window(self, text)
*text* - mesaj de succes

Metoda care genereaza o fereastra cu un mesaj de succes.

## insert(self, table, columns, nullable, fields)
*table* - numele tabelului in care inseram

*columns* - numele coloanelor tabelului

*nullable* - vector care memoreaza daca o coloana este nullable sau nu

*fields* - campurile ferestrei anterioare, care contin datele de inserat

