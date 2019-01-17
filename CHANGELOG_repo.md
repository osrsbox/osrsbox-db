## Repository Changelog:

#### 2019-01-18 06:22:23: 46a233a7a
- Weekly update: 01/18 - added new inventory icons (mystic recolor).

#### 2019-01-18 06:18:24: 6ae8216c7
- Slight update to quest_db_tools and a new bestiary extraction script (work in progress).

#### 2019-01-12 16:33:30: bd655cd7d
- Added new property into database called tradeable_on_ge
- And re-generated database
- This fixes #8, where some items were not shown as tradeable, but were
- tradeable_on_ge is items (none noted) that can be traded on the GE
- tradeable is items (not noted and noted) that can be traded between players.

#### 2019-01-12 16:29:34: d4f0a4fc5
- Added support for tradeable versus tradeable_on_ge
- Just need to re-gen item database.

#### 2019-01-12 15:11:48: 7f36246fa
- Added helper tools to join wikitext extraction output dirs.

#### 2019-01-11 18:14:14: 880676fe2
- Did a little mucking around on quests data processing tools.

#### 2019-01-11 18:10:27: 4e465e4ed
- Cleaned examine text on some items in items-json - not yet populated to other docs files.

#### 2019-01-11 15:38:21: 4d8c8716f
- Fished 01/10 update for all items, and generation of items_complete, items-json and item-json-slot files
- Also small update to item skill requirements script and json file.

#### 2019-01-11 15:17:30: 5a5531101
- Updated items skill requirements, but still needs update for 01/10 update
- Slight update to db_tools for new processing.

#### 2019-01-11 14:59:17: 5b5af0861
- Updated osrs wiki item JSON files
- Slight update to extraction tool readme.

#### 2019-01-11 12:23:36: c934b890b
- Decent update to wiki extractions tools for items
- Combines items and other into one script
- Updated wikitext extraction script to able to restart if failed previously (e.g., connection loss) - but raw wikitext is no longer hosted
- Updated template extraction scipt for items
- Also updated readme file with changes.

#### 2019-01-11 10:44:56: 5180e56d7
- Update base item db JSON files
- Couple small updates to wiki extraction scripts
- Updated changelog for new items in this weeks update
- Also updated determine new items script to order results.

#### 2019-01-11 07:57:32: be282b7b3
- Added new inventory item icons after Kebos update today
- JSON item update to follow.

#### 2019-01-04 12:13:17: c31164449
- Added all extra files for items API (slots, and complete)
- Also updated items_api_tools and item_db_tools for new linked_id property
- Finally, also updated normalized names for some OSRS wiki name changes.

#### 2019-01-04 12:10:31: 6ea0ea04c
- Updated some missing items that didn't have a newly added linked_id property.

#### 2019-01-04 10:54:51: b36213bc4
- Happy 100th commit! Added new property into item database: linked_id which holds the id number of an associated item, for example, noted and un-noted variants.

#### 2019-01-04 10:22:13: abaf50b55
- Updated items-json based on updates to the OSRS Wiki
- Primarily updates to weight and examine text for items.

#### 2019-01-04 09:59:20: 2d3e00328
- Remove custom agent from wiki extraction script.

#### 2019-01-04 09:57:12: 7ed0f7671
- Updated osrs wiki extraction tools and dumped data.

#### 2018-12-30 08:28:18: c658875c9
- Updates to some of the project README files.

#### 2018-12-30 08:13:30: 1c976759c
- Slight update to READMEs for project and item_api_tools
- Also removed old item_db_workflow folder as all tools were slowly migrated to the item_api_tools folder and code base.

#### 2018-12-30 07:54:32: c404bfb5f
- Updated items_complete, and items-json-slot files after the buylimit update yesterday.

#### 2018-12-29 15:49:42: 6f3399e03
- Added the script used to help automate item_skill_requirements data
- Also updated the list of skill requirements to allign with last few game updates
- And updated readme.

#### 2018-12-29 15:02:04: f3c6feb17
- Added updated buy limits for the entire item database
- This fixes #12
- Also updated ProcessItems program to use new extraction_tools directories.

#### 2018-12-29 14:43:48: bbd6fb3d3
- Created two folders for extraction tools - one for wiki, one for other
- This was becuase the folders were getting messy
- Added buy limits, name normalization and skill requirement material to extraction_tools_other folder.

#### 2018-12-21 08:18:12: eee08fe10
- Updated database for in-game release date, but there was no update today
- Made modification to ItemScraper plugin for buy_limit to be None/null and not -1 by default
- This changed a collection of items in database
- Also authored DetermineNewItems script as slowly moving from workflow tools.

#### 2018-12-18 09:37:12: f5a724f31
- General clean-up of item_api_tools
- Removed some redundant code, simplified helper methods
- Also added a new script to process the items-json folder contents and produce items_complete.json
- Will slowly remove similar old code from workflow folder to apt_tools.

#### 2018-12-18 09:09:53: 5da53a0d6
- Added individual JSON files for equipable items for each inventory slot
- This closes #11.

#### 2018-12-18 08:56:56: 96d6a1e9d
- Updated some documentation to api_tools, db_tools and repo readme
- Updated api_tools with some example scripts and small fixes.

#### 2018-12-17 14:30:19: ae176e3e1
- Updated items-json for new items.

#### 2018-12-17 14:24:50: 227543af5
- Removed un-needed merge script
- Some small updated to ItemDefinition classes (for API and tools), and updated ProcessItems to use newly modified JSON files from wiki_extraction_tools.

#### 2018-12-17 13:45:08: ccb03b8a0
- Updated wiki extraction tools, and redumped some content
- Updated output method for some scripts, and also slightly updated readme.

#### 2018-12-17 09:41:22: 899669931
- Update database for new items added in last two weeks updates (base JSON files and icon images - still need to re-gen single JSON files)
- Lots of image changes due to modification of ring inventory model location tweaks.

#### 2018-12-11 15:29:52: 8b37174be
- Updated the items_complete.json file for the recent db changes
- Slight updates to API for calling single file or dir for processing.

#### 2018-12-11 12:38:48: c77af9a94
- Push one final item change, with slight change to normalized names
- Also, a couple small updates to ItemDefinition - including logging levels to make future debugging easier.

#### 2018-12-11 11:47:20: 987872175
- Changed attack speed property to store null instead of zero (0) for equipable items that are not weapons
- This makes much more sense.

#### 2018-12-11 11:41:37: 826f877a1
- Updated normalized names to allign with changes in OSRS Wiki
- Updated a collection of missed items with new data model for missed items.

#### 2018-12-10 16:40:21: e5bb3135c
- Small changes to some tools after final generation.

#### 2018-12-10 16:29:10: a90f0d778
- Fixed a large variety of items that did not validate in the first pass with the new structure.

#### 2018-12-10 13:09:47: 2e838ab4b
- Updated all items in docs/items-json/ folder with new equipment element
- Also updated lots of innacuracies in lots of items (with versioned Infoboxes).

#### 2018-12-10 11:14:52: 3125c746c
- Big update to data processing method and JSON format structure
- Added new entry named equipment for equipable items to store equipment related information (item slot, attack speed, and item skill requirements)
- Added new ItemEquipment class to handle this
- Reverted to storing examine text as a string, not a list
- Added master list of items and their skill requirements in JSON format
- Also updated normalized names database for new changes to wiki.

#### 2018-12-08 13:29:51: 70fcafdb8
- Edited api_tools to support new ItemEquipment class
- Edited db_tools to support infobox versioning from OSRS Wiki, but still need to modify for new ItemEquipment class.

#### 2018-12-06 08:26:20: da924eb85
- Slight updates to item DB tools to documentation and reading input.

#### 2018-12-02 11:34:42: 03ed3017d
- Updated wiki extraction scripts for new OSRS wiki.

#### 2018-11-23 13:25:48: 19b57482b
- Added new workflow tool to compare current DB contents to itemscraper contents (for when items are modified, such as high alch price).

#### 2018-11-23 06:19:10: af9326f3a
- Changes for this weeks update
- No items added, only a cost change on cowhides
- Updated CHANGELOG.txt.

#### 2018-11-16 10:38:27: 34bb8f8e4
- General updates after this weeks game update, including revised changelog
- No new items added, but a collection of icon images have changed since last updated.

#### 2018-11-13 09:22:54: 2af3f8c4d
- Fixed all blessings
- Set equipable to true, and added item bonuses with all values set to zero, apart from a +1 prayer bonus
- This change affected the following item IDs: 20220, 20223, 20226, 20229, 20232, 20235
- This closes #6.

#### 2018-11-13 09:13:36: 324bb8cd6
- Fixed some inaccuracies in the items-json database for Magma helm, Serpentine helm, and Toxic staff of the dead.

#### 2018-11-10 09:32:14: 74f1913cd
- Added new item files and item icons for this weeks update
- Updated item workflow README
- Update project CHANGELOG
- Updated main README with model ID project information.

#### 2018-11-04 09:17:29: 62f6cda9a
- Another update to model ID script and JSON file
- Added exclusion of nulls and removed model_2 parsing.

#### 2018-11-04 08:11:12: 680f92de5
- Fixed python script and JSON file for model ID list.

#### 2018-11-04 07:33:23: 0eb342dd2
- Some small updates to model metadata extraction script - added model_id and type_id
- Also updated models_summary file to work with osrsbox model id search app.

#### 2018-11-03 14:26:55: df20031b7
- Added new script to parse Cache definitions and extract model id number/name information
- New naming scheme for public api files to help determine purpose of different complete JSON files
- Slight updates to item workflow scripts.

#### 2018-10-26 07:45:16: 9e674b5e6
- Updated item db (allitems.json, summary.json, icon images) for this weeks update
- Changelog updated to reflect: 26 items added in game, no other item or metadata changes.

#### 2018-10-19 08:03:39: c367188ab
- Checked this weeks update - no new items
- Slight update to project README.md file and updated CHANGELOG.txt to reflect new update.

#### 2018-10-13 14:07:36: 8c7632307
- Couple small updates to the items API scripts.

#### 2018-10-13 13:51:23: d1a026427
- Updated every items-json file to reflect new OSRS Wiki URL
- Also fixed a couple of broken URLs
- Also added new icons for the last two updates.

#### 2018-10-13 12:06:38: c901bca96
- Updated OSRS item database
- Also some minor changes to work-in-progress quest API.

#### 2018-09-30 10:34:16: 8606ea097
- Added base structure for new quest data abstraction and (future) API to automate processing and analysis of OSRS quests.

#### 2018-09-30 10:18:35: 82c3a4aea
- Changed project license to GPL3

#### 2018-09-30 09:54:40: aff944344
- Added base API tools written in Python to easily process, query and edit the osrsbox-db of items.

#### 2018-09-29 20:41:24: 9fa356d76
- Added new, completed item-json files.

#### 2018-09-29 15:18:34: 0bb31f98c
- Finished the clean up of scripts and workflow
- All items extracted, just need a manual clean then adding the new, updated database.

#### 2018-09-29 10:41:34: a5597d4de
- Major changes to repository structure and tools
- Added detailed README for each directory, including logical update process
- Almost completed re-implemented database - still missing approximately 600 items.

#### 2018-09-25 20:02:50: b8bb1b54f
- Continued development of database population tools
- Added various wikia extraction helper scripts
- Implemented normalization name method for problematic items.

#### 2018-09-19 15:19:29: 9f74b5c8a
- Added new script for buy limit fetching from OSRS Wiki
- Updated readme file for wikia extraction tools
- Still need to add buy_limit file into tools processing.

#### 2018-09-19 11:43:54: b4eda6265
- Finished bulk of initial development and testing
- Only need to add in buy_limits that are not available in API queries
- Also need to address items with missing Wiki pages.

#### 2018-09-17 18:55:27: 347bef871
- Slight tidy to itemdefinition handling
- Only examine left to go, then integration of buy_limits from other source (as not in infobox)

#### 2018-09-16 15:55:53: f0d3e6dc5
- Adding extensive cleaning for infobox parsing
- Done release date, weight, quest
- Still have examine, seller and store to go.

#### 2018-09-16 06:42:54: ee2a7526a
- Slight code tidy and removal of all cleaning definitions
- Ready to process data, and reimplement cleaning definitions with thorough testing.

#### 2018-09-15 16:28:37: 2822f1712
- New approach to parsing OSRS Wiki by extracting all data at once
- Added a bunch of code and files in a mess.

#### 2018-09-11 13:41:41: 401941b3d
- More tools/files added to workflow.

#### 2018-09-11 13:34:11: 5d5069351
- Tidy of workflow tools
- Added new script to join osrsbox-db JSON files into one
- Added README.md for workflow tools.

#### 2018-09-11 13:09:04: fea398efb
- Removed one erroneous item from items-json
- Added new script to check missing db items (json).

#### 2018-09-08 15:22:16: f94963a8d
- Updated allitems.json, summary.json, and item-icons for 2018-09-06 update
- Added changelog for any new items in game
- Small updates to tools.

#### 2018-09-08 07:45:33: e0506df18
- Continued development on DB workflow tools.

#### 2018-09-06 18:43:34: 272b4ff6d
- Slight changes to ItemDefinition after preliminary testing.

#### 2018-09-06 17:01:41: c4f1ceccc
- Updated JSON output methods
- Added more logging.

#### 2018-09-05 11:51:57: d771f2676
- Added initial support for item bonuses from OSRS Wikia
- Still needs lots of testing and additional logic for more difficult items
- Plus, need to re-review logs to determine errors in items.

#### 2018-09-05 10:45:35: a00dd6d95
- Bought project back to functioning after adding buy_items.

#### 2018-09-05 10:39:07: 54858f40d
- Added gitignore for Python projects
- Updated WikiaExtractor to also parse the buy_limits page.

#### 2018-09-05 09:39:28: 1da8967bb
- First iteration of updated workflow for osrsbox-db contents
- Using API instead of scraping
- Most functionality included, apart from setting item bonuses
- Old workflow tools moved to tools-old folder.

#### 2018-08-26 18:18:37: 03d4b566a
- Updated items-icons and summary.json as of 2018/26/08

#### 2017-12-26 14:14:39: 30c1f90b9
- Added new png icons for some missing items
- Also uploaded Python OSRS GE scraper to download GIF icons from the official website.

#### 2017-12-25 12:41:16: 1de5c0638
- Uploaded original tools to create database of items using RuneLite cache information combined with OSRS Wikia site.

#### 2017-12-24 16:54:51: 5883795a7
- Update README.md

#### 2017-12-24 16:53:45: 095e5b750
- Added items.csv file with a complete item list for OSRS cache 160

#### 2017-12-24 11:51:52: d2384533f
- Removed website from docs folder to main pages repo.

#### 2017-12-24 10:07:03: 8079b105d
- Update README.md

#### 2017-12-24 08:57:50: 3bead0709
- re-added all icons.

#### 2017-12-24 08:54:59: f097aa74d
- Removed old file structure for icon images.

#### 2017-12-23 14:41:08: 65a7b03bb
- Upload of revised JSON files - more metadata, better accuracy, covers every item in OSRS.

#### 2017-12-23 14:20:01: 4a469088f
- Removed old JSON files.

#### 2017-12-23 14:18:28: 63d1d3f1f
- Couple small updates to documentation.

#### 2017-12-22 16:22:20: 666d90c09
- Updated docs for new website design.

#### 2017-05-30 18:53:53: ea34c4e29
- Quick fix to script call.

#### 2017-05-30 18:52:02: 13bf2c750
- Updated small fixes to documentation and added tooltips library

#### 2017-05-30 18:47:57: a67fccf73
- Fixed some documentation
- Rounded off the end of the document until there is more time to finish.

#### 2017-05-30 18:08:45: ad200ce69
- Added master list of OSRS item IDs sourced from OSBuddy GE and OSRS GE APIs.

#### 2017-05-29 08:01:40: f295ded6b
- Added classes for table formatting and style.

#### 2017-05-29 06:52:23: 9fb61b9ad
- Fixed incorrect characters beign displayed in index page.

#### 2017-05-29 06:43:37: 9867dea5e
- Updated index page - added classes to all code boxes.

#### 2017-05-29 06:39:28: aa3d4e952
- Migrated repository to docs folder
- Moved all json and pngs to docs folder, created site layout, include and index pages
- Also, updated readme with pointer to new web page.

#### 2017-03-25 16:57:17: c69cf71f8
- Updated readme with more examples, again again.

#### 2017-03-25 16:56:02: 6fdb7475c
- Updated readme with more examples, again.

#### 2017-03-25 16:47:05: f68688742
- Updated readme with more examples.

#### 2017-03-25 15:59:18: 276196c08
- Re-ordered JSON for better viewing pleasure and converted equipable stats to integers
- This closes #3.

#### 2017-03-24 15:45:42: 6f563eb38
- Updated ReadMe again.

#### 2017-03-24 15:25:52: 8a48ce475
- Updated ReadMe.

#### 2017-03-24 07:47:00: 1b2eb79fe
- Divided JSON and PNG to subdirectories based on first digtial of id number
- This closes #1 and makes it much quicker to browse the JSON and PNG items directories on GitHub.

#### 2017-03-19 17:43:20: 710df67bd
- Initial JSON upload.

#### 2017-03-19 17:40:02: 81a0d8909
- Initial item image upload.

#### 2017-03-17 17:32:10: 1cf19dc9f
- Uploaded item id 12205 for testing.

#### 2017-03-17 15:46:34: ea59b140e
- Initial commit

