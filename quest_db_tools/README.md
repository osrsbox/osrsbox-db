# osrsbox-db: Item database population tools

## ProcessQuests.py

- Purpose: Handle construction of raw item data + OSRS Wiki data to JSON files for each item
- This script takes no command line arguments
- This script does not download any information from the OSRS Wiki. Instead it processes a collection of previously downloaded files from the `wikia_extraction` folder. All of these values are hardcoded that map to the files produced by the OSRS Wiki extraction tools.
- Command to run:
- `python3.6 ProcessQuests.py`
- `python.exe .\ProcessQuests.py`

## Quest Classes

- Purpose: Handle construction of a single OSRS quest using data from the OSRS Wiki
- Each quest is build using the following classes:
    - `QuestDefinition`: Main handling of a single quest
    - `QuestMetadata`: Data from the `Infobox Quest` wiki template
    - `QuestDetails`: Data from the `Infobox Details` wiki template
    - `QuestDefinition`: Data from the `Infobox Rewards` wiki template
