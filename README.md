# eBird Analyses
The purpose of this project is to perform additional analyses on a set of eBirding data that is not already available at [ebird.org](https://ebird.org). 

## What is eBird?
eBird is an online database of bird observations providing scientists, researchers and amateur naturalists with real-time data about bird distribution and abundance. Birders submit sightings as "checklists", which list what birds were seen, how many, where, when, various metadata about the birding effort, and more. See [ebird.org](https://ebird.org) for more.

## Questions to be answered

1) How many total birds did I report in 2021?
2) Which species showed up most frequently on my checklists?

## Technologies
- Python
- Pandas, Jupyter

## Data sources
**[MyEBirdData.csv](MyEBirdData.csv)**
  - Personal eBird data available via "Download My Data" link: https://ebird.org/downloadMyData. Requires being logged in to eBird to download data. This data was downloaded on 1/3/22 and includes all of my personal checklists submitted up to that point. 
#### Column definitions
- **Submission ID**: unique identifier of a checklist
- **Common Name**: the common name of the bird seen
- **Scientific Name**: the scientific name of the bird seen
- **Taxonomic Order**: the taxonomic group that this bird belongs to
- **Count**: how many birds were seen. Best estimates for large quantities are acceptable and common.
  - * *Note: some entries will list count as "X", which denotes "Present". This  means that the bird was seen, but a count was not estimated. Usually this is done for common, abundant birds* *
- **State/Province**: the state that the bird was seen in
- **Count**: the county that the bird was seen in
- **Location ID**: unique identifier of the specific location that the bird was seen in.
- **Location**: the name of the location that the bird was seen in. See more [here](https://support.ebird.org/en/support/solutions/articles/48001009443-ebird-hotspot-faqs#anchorWhatIsHotspot)
- **Latitude**: latitude of location
- **Longitude**: longitude of location
- **Date**: date of sighting
- **Time**: start time of checklist
- **Protocol**: describes the method of birding. Most common protocols are listed below, see [here](https://support.ebird.org/en/support/solutions/articles/48000950859-guide-to-ebird-protocols#anchorQuickProtocols) for more.
  - "eBird - Traveling Count": moved more than 100 feet away from the starting point of your checklist at any point in the duration of the checklist. 
  - "eBird - Stationary Count": did not move more than 100 feet away. 
  - "eBird - Casual Observation": the birder was not birding when the bird was seen. E.g. out working in the garden when a hawk flew overhead.
- **Duration (min)**: how long the checklist lasted, i.e. how long the birder went birding.
- **All Obs Reported**: "Obs" means observations. This field denotes whether a checklist is "complete" (evaluates to 1) or "incomplete" (evaluates to 0), i.e. whether the list includes every species seen during the checklist, without omitting any, even a common one. See [here](https://support.ebird.org/en/support/solutions/articles/48000795623-ebird-rules-and-best-practices#Keep-complete-checklists) for more.
- **Distance Traveled (km)**: only applies to "Traveling protocol" checklists. How many kilometers were covered during the checklist. This does **not** mean how far the birder walked. A 1km out and back trail should be recorded as 0.5km. However, eBird automatically generates this value using GPS data in the app, so it is incumbent upon the birder to remember to adjust this number before submitting the checklist.
- **Area Covered (ha)**: uncommon. Hectares covered during a targeted, specialized survey of birds in a specific area. Not applicable for a trail that meanders around a forest.
- **Number of Observers**: number of birders
- **Breeding Code**: see [here](https://support.ebird.org/en/support/solutions/articles/48000837520-ebird-breeding-and-behavior-codes)
- **Observation Details**: birder's comment about the observation
- **Checklist Comment**: birder's comment about the entire checklist
- **ML Catalog Numbers**: ML = Media Library. Unique identifier of any media (photo or audio) that was attached as a part of this observation


