# RDF Knowledge Graph Generator (xlsx-to-rdf)
A Python tool that converts Excel spreadsheets into RDF knowledge graphs in Turtle format, using standard Semantic Web ontologies, applied to uses cases in the Built Environment.

## Setup
1. Clone this repository
2. Place your input files in the `input/` folder
3. Run the script: `python src/xlsx_to_ttl.py`
4. Results will be saved in `output/`
5. Add data/output folders to .gitignore

```
# .gitignore
input/*.xlsx
output/*.ttl
!input/.gitkeep
!output/.gitkeep
```

## Description
This tool reads structured data from Excel files and transforms it into semantic web triples (subject-predicate-object statements). It automatically handles data type detection, CURIE expansion, and namespace management to create valid RDF graphs.

- **Multi-sheet Excel support**: Processes all sheets in a single Excel file
- **Automatic type detection**: Intelligently converts values to appropriate XSD datatypes (integers, doubles, booleans, dates, strings)
- **CURIE handling**: Expands compact URIs (e.g., `rec:Building`) to full URIs
- **Standard ontologies**: Built-in support for REC, WMTO, BOT, BRICK, FOAF, ORG, and custom namespaces (through the insertion of namespaces of desired ontologies)
- **Turtle output**: Generates clean, readable RDF in Turtle format

## Requirements
```
rdflib
pandas
numpy
openpyxl
```

Install dependencies:
```bash
pip install rdflib pandas numpy openpyxl
```

## Project Structure
```
project/
├── input/
│   └── resources.xlsx    # Your input Excel file
├── output/
│   └── resources.ttl     # Generated RDF output
├── python scr/
│   └── xlsx_to_ttl.py    # Main script
└── README.md
```

## Usage

1. Place your Excel file in the `input/` folder as `resources.xlsx`
2. Run the script:
```bash
   python xlsx_to_ttl.py
```
3. Find the generated RDF graph in `output/resources.ttl`

## Excel Format

Your Excel file should be structured as follows:

- **First column**: Subject URIs (can use CURIEs like `utr:Room101`)
- **Remaining columns**: Predicate names (can use CURIEs like `rdf:type`, `rec:capacity`)
- **Cell values**: Objects (URIs, literals, numbers, dates, etc.)

### Example

| utr:Room101 | rdf:type        | rec:capacity | rec:hasFloor |
|-------------|-----------------|--------------|--------------|
| Room101     | rec:MeetingRoom | 20           | utr:Floor2   |

This generates:
```turtle
utr:Room101 rdf:type rec:MeetingRoom .
utr:Room101 rec:capacity "20"^^xsd:integer .
utr:Room101 rec:hasFloor utr:Floor2 .
```

## Output

The script generates a Turtle (.ttl) file containing all triples extracted from the Excel sheets, with proper namespace prefixes and datatype annotations.

## License

GNU Affero General Public License v3.0

## Contributing

This is a personal project related to an academic research project, created for specific use cases. While contributions are appreciated, please note that maintenance may be limited. Feel free to fork the project for your own needs.