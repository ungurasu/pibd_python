# pibd_python
*Ungurasu Ioan-Andrei 435E UPB ETTI 2021*

- [pibd_python](#pibd-python)
  * [Clasa DatabaseHandler](#clasa-databasehandler)
  * [fail-window](#fail-window)
  * [success-window](#success-window)
  * [insert](#insert)
  * [insert-window](#insert-window)
  * [select-all](#select-all)
  * [filter-window](#filter-window)
  * [select-window](#select-window)
  * [update](#update)
  * [update-window](#update-window)
  * [delete](#delete)
  * [findbypk-window](#findbypk-window)
  * [get-tables](#get-tables)
  * [repeate-login](#repeate-login)
  * [attempt-login](#attempt-login)
  * [login-screen](#login-screen)
  * [logout](#logout)
  * [init](#init)

## Clasa DatabaseHandler
Contine logica pentru interfata grafica, dar si logica pentru operarea asupra bazei de date.

## fail-window
*text* - mesajul de eroare

Metoda care genereaza o fereastra cu un mesaj de eroare.

## success-window
*text* - mesaj de succes

Metoda care genereaza o fereastra cu un mesaj de succes.

## insert
*table* - numele tabelului in care inseram

*columns* - numele coloanelor tabelului

*nullable* - vector care memoreaza daca o coloana este nullable sau nu

*fields* - campurile ferestrei anterioare, care contin datele de inserat

Generam comanda de inserare si o executam

## insert-window

*table* - numele tabelului in care inseram

Generam o fereastra in care utilizatorul va scrie datele de inserat.

## select-all

*table* - tabelul pe care selectam

*column* - coloana dupa care filtram (facem where) daca e cazul

*equals* - valoarea pe care o vrem in coloana dupa care filtram (facem where)

Generam instructiunea de select, si punem rezultatele query-ului intr-o fereastra.

## filter-window

*table* - tabelul pe care selectam

Generam o fereastra cu cate un camp pentru fiecare coloana din tabel. Utilizatorul va putea filtra (where) doar dupa o singura coloana deodata.

## select-window

*table* - tabelul pe care selectam

Generam o fereastra in care intrebam utilizatorul daca vrea sa afiseze toate datele din tabel, sau daca vrea sa filtreze (where).

## update

*table* - tabelul in care updatam

*primary* - numele campului de PK

*primaryvalue* - valoarea PK-ului la care updatam

*columns* - numele coloanelor din tabel

*columnentries* - campuri cu date de updatat

Generam comanda de update si o executam.

## update-window

*table* - tabelul pe care facem update

*primary* - numele campului de PK

*primaryentry* - camp ce contine valoarea PK-ului la care vom updata

Generam o fereastra cu campuri pentru row-ul pe care utilizatorul doreste sa il updateze. Fiecare camp va contine datele actuale ale row-ului, asa cum se gaseste el deja in baza de date.

## delete

*table* - tabelul din care facem delete

*primary* - numele campului de PK

*primaryentry* - camp ce contine valoarea PK-ului la care vom delete

Construim instructiunea de delete si o executam.

## findbypk-window

*table* - tabelul pe care vom lucra

*task* - update sau delete

Generam o fereastra in care selectam dupa PK un row din tabel, pentru a face delete sau update.

## get-tables

*task* - insert/select/update/delete

Generam o fereastra cu o lista de tabele, din care selectam unul pentru a actiona asupra lui.

## repeate-login

Refacem conectorul la baza de date. Facem asta inainte de a opera asupra bazei de date, pentru a ne asigura ca nu lucram cu un conector expirat.

## attempt-login

*address* - camp cu adresa la care se afla baza de date

*user* - camp care contine username-ul contului cu care vom opera asupra bazei de date

*password* - camp care contine parola contului cu care vom opera asupra bazei de date

Incercam sa facem un conector la baza de date. Daca operatia are succes, salvam credentialele local.

## login-screen

Generam o fereastra in care utilizatorul va trece credentialele pentru operarea asupra bazei de date.

## logout

Stergem credentialele utilizatorului si distrugem conectorul.

## init

Generam o fereastra cu butoane catre functionalitatile principale ale interfetei.