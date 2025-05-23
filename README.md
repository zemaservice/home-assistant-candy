# Candy Home Assistant component Zema

[![Run tests](https://github.com/ofalvai/home-assistant-candy/actions/workflows/test.yml/badge.svg)](https://github.com/ofalvai/home-assistant-candy/actions/workflows/test.yml)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![codecov](https://codecov.io/gh/ofalvai/home-assistant-candy/branch/main/graph/badge.svg?token=HE0AIQOGAD)](https://codecov.io/gh/ofalvai/home-assistant-candy)

Custom component for [Home Assistant](https://homeassistant.io) that integrates Candy/Haier/Simply-Fi home appliances.


## Funzionalità
- Elettrodomestici supportati:
- lavatrice
- asciugatrice
- forno
- lavastoviglie
- Utilizza l'API locale e il suo endpoint di stato
- Crea diversi sensori, come lo stato del dispositivo e il tempo rimanente. Tutto il resto viene visualizzato come attributi del sensore

## Installazione

1. Installa [HACS](https://hacs.xyz/)
2. Vai all'elenco delle integrazioni in HACS e cerca `Candy Simply-Fi`
4. Riavvia Home Assistant
5. Vai alla pagina Integrazioni, fai clic su Aggiungi integrazioni e seleziona `Candy`
6. Completa il flusso di configurazione

## Configurazione

Sono necessari l'indirizzo IP del dispositivo e la chiave di crittografia. Questi possono essere ricavati con [CandySimplyFi-tool](https://github.com/MelvinGr/CandySimplyFi-tool).

## Il mio dispositivo non è supportato. Potete aiutarmi?

Sì. Se disponi di un dispositivo non ancora supportato o visualizzi un errore, accedi alla [sezione Discussioni](https://github.com/ofalvai/home-assistant-candy/discussions/categories/device-support-improvements). Apri una nuova discussione o commenta una discussione esistente con le seguenti informazioni:

- La risposta API sullo stato del tuo dispositivo (utilizza [CandySimplyFi-tool](https://github.com/MelvinGr/CandySimplyFi-tool) per ottenere il file JSON)
- Una breve spiegazione del significato di ciascun campo nella risposta e di come cambia in base allo stato del dispositivo, ad esempio: _Il campo `SpinSp` è probabilmente la velocità di centrifuga divisa per 100; ho visto i valori 6, 8, 10 e 12 nella risposta_
