# osrsbox-db: Model database population tools

## ProcessModels.py

- Purpose: Parse ItemDefinition, NpcDefinition and ObjectDefinition output from the RuneLite Cache tool and extract model id numbers
- The output is a single JSON file with all model ids that has the associated name, item/npc/object id and the type (item/npc/object)
- This script takes one command line argument
    - A directory that should contain 3 folders:
    - `items`: All ItemDefinitions in JSON
    - `npcs`: All NpcDefinitions in JSON
    - `objects`: All ObjectDefinitions in JSON
- Command to run:
- `python3.6 ProcessModels.py -d C:\Users\ph01l\Desktop\definitions\`
- `python.exe .\ProcessModels.py -d /home/users/ph01l/Desktop/definitions/`
