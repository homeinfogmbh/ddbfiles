# ddbfiles
Stand: 2026-07-29, geprüft gegen Commit f49d7a7

## Zweck
Autorisierte Download-API für Dokumentations- und Bilddateien rund um das
DDB-Projekt. Stellt Dateien kontrolliert (nach Auth) zum Download bereit.

## Stack & Einstiegspunkte
Python 3, Flask/`wsgilib`. Package `ddbfiles`. ⚠️ ANNAHME: WSGI-Download-
Endpunkte; Dateien unter `files/`. Console-Script vorhanden (aus `setup.py`).

## Schnittstellen
### Konsumiert
- **Dependencies:** `his` (Auth/Autorisierung), `emaillib`, `configlib`,
  `flask`, `wsgilib`. Dateiablage im Repo/Dateisystem (`files/`).

### Bietet an
- **Autorisierte Download-Endpunkte** für DDB-Doku/-Bilder (nur für berechtigte
  Nutzer).

## Deployment / Laufzeit
WSGI-Anwendung hinter dem HIS-Stack. ⚠️ ANNAHME: Auslieferung per mod_wsgi/uwsgi.

## Ersetzbarkeit
Kopplungsgrad: **mittel**. Kleiner, abgegrenzter Download-Service; an `his`-Auth
gebunden.

## Weitere Doku
- `README.md` (Zweck: autorisierte Download-API).
- Verwandt: `his`, `filedb`, `ddb-setup-manual`.
- ⚠️ ANNAHME: Zentrales Repo `homeinfo-architektur` (Ordner `komponenten/`) noch
  nicht geprüft.
