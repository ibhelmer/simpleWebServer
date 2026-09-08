# simpleWebServer

En simpel webserver skrevet i Python 3 med standardbibliotekerne `socket` og `logging`. Serveren er et undervisningseksempel, der leverer lokale filer via HTTP og håndterer én klient og én forespørgsel ad gangen.

## Start serveren

Åbn en terminal i mappen med `main.py`, `index.html` og `favicon.ico`, og kør:

```sh
python main.py
```

Åbn derefter <http://127.0.0.1:7913/> i en browser. Stop serveren med `Ctrl+C`. Der skal ikke installeres ekstra Python-pakker.

## Sådan virker koden

1. Serveren opretter en IPv4 TCP-socket, binder den til en port og venter på forbindelser.
2. Når en klient forbinder, læser serveren op til 1024 bytes og tager filstien fra HTTP-forespørgslen.
3. Stien `/` bliver til `/index.html`. Andre stier bruges til at finde filer relativt til den mappe, serveren er startet fra.
4. Filen læses som binære data og returneres med status `200 OK`. `favicon.ico` får desuden en særlig `Content-Type`-header.
5. Ved en `IOError`, eksempelvis en manglende fil, forsøger serveren at sende et 404-svar. Forbindelsen lukkes efter svaret, og serveren venter på næste klient.

Serveren er tænkt til GET-forespørgsler via HTTP/1.0, men validerer ikke HTTP-metoden. Favicon-svaret bruger HTTP/1.1. Forbindelser og driftsbeskeder logges i `websrv.log`.

## Indstillinger

Indstillingerne ændres direkte i `main.py`. Genstart serveren efter en ændring.

| Indstilling | Nuværende værdi | Betydning |
| --- | --- | --- |
| `PORT` | `7913` | Porten serveren lytter på. Skift fx til `8080`, og brug samme port i browserens adresse. |
| `HOST` | `"127.0.0.1"` | Den tilsigtede IP-adresse. Variablen bruges aktuelt ikke i `bind()`; se nedenfor. |
| Standardfil | `b'/index.html'` | Filen der vises, når klienten anmoder om `/`. |
| Logfil | `websrv.log` | Angives i `DEBUG.basicConfig(filename=...)`. `filemode='a'` tilføjer til den eksisterende log. |
| Logniveau | `DEBUG.INFO` | Bestemmer hvilke logbeskeder der gemmes. `DEBUG` er her et alias for modulet `logging`. |
| Modtagestørrelse | `recv(1024)` | Maksimalt antal bytes i én læsning. En større værdi garanterer ikke, at hele forespørgslen modtages. |

### IP-adresse og port

Den nuværende linje `serverSocket.bind(('', PORT))` lytter på alle lokale IPv4-netværksinterfaces, selv om `HOST` er sat til localhost. For at bruge `HOST` skal bindingen ændres til:

```python
HOST = "127.0.0.1"
PORT = 7913
serverSocket.bind((HOST, PORT))
```

- `127.0.0.1`: Kun adgang fra samme computer.
- `0.0.0.0`: Lyt på alle lokale IPv4-interfaces. Andre computere bruger servercomputerens faktiske IP-adresse, fx `http://192.168.1.10:7913/`, hvis netværk og firewall tillader det.
- En bestemt lokal IP-adresse: Lyt kun på den adresse. Adressen skal være tildelt servercomputeren.

## Begrænsninger

Koden har ingen beskyttelse mod filstier som `../`, så filer uden for webmappen kan læses. Tomme eller delvise forespørgsler kan stoppe serveren, og en klient uden data kan blokere den, fordi der mangler timeout. Brug derfor eksemplet lokalt til læring; det er ikke egnet til offentlig drift i sin nuværende form.
