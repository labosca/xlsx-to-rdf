from rdflib import Graph, Literal, Namespace, RDF, OWL, URIRef, XSD, RDFS
from rdflib.namespace import FOAF, ORG, BRICK, SDO, SKOS
import pandas as pd
import numpy as np
import os
import datetime

# Initialize graph and namespaces
g = Graph()
REC = Namespace("https://w3id.org/rec#")
WMTO = Namespace("https://w3id.org/wmto#")
UTR = Namespace("https://example.org/UniToResources#")
BOT = Namespace("https://w3id.org/bot#")

# Bind namespaces
namespaces = [
    ("rdf", RDF),
    ("rdfs", RDFS),
    ("owl", OWL),
    ("foaf", FOAF),
    ("org", ORG),
    ("sdo", SDO),
    ("brick", BRICK),
    ("skos", SKOS),
    ("rec", REC),
    ("bot", BOT),
    ("wmto", WMTO),
    ("utr", UTR),
    ("", UTR)  # Default namespace
]
for prefix, ns in namespaces:
    g.bind(prefix, ns)

# Process Excel sheets directly
excel_file = r"input\resources.xlsx"
all_sheets = pd.read_excel(excel_file, sheet_name=None)

for sheet_name, df in all_sheets.items():
    # Clean column headers but keep CURIEs intact
    df.columns = [col.split(' (')[0].strip() for col in df.columns]
    
    for _, row in df.iterrows():
        # Handle subject: Check if it contains a prefix, otherwise use UTR namespace
        subject_value = row.iloc[0]
        try:
            # Expand CURIE using namespace manager if prefix exists
            subject = URIRef(g.namespace_manager.expand_curie(subject_value))
        except:
            # Fallback to UTR namespace if no registered prefix is found
            subject = URIRef(str(UTR) + subject_value.split(':')[-1])
        
        for predicate_col in df.columns[1:]:  # Remaining columns as predicates
            obj_value = row[predicate_col]
            if pd.isna(obj_value):
                continue

            # Use CURIE directly from column header
            try:
                # Expand CURIE using namespace manager
                predicate = URIRef(g.namespace_manager.expand_curie(predicate_col))
            except:
                # Fallback to REC namespace if not a registered prefix
                predicate = URIRef(str(WMTO) + predicate_col.split(':')[-1])

            # Handle object value typing
            if isinstance(obj_value, str) and ':' in obj_value:
                try:
                    # Expand CURIE using namespace manager
                    obj = URIRef(g.namespace_manager.expand_curie(obj_value))
                except:
                    # Fallback to UTR namespace if unknown prefix
                    obj = URIRef(UTR[obj_value.split(':')[-1]])
            else:
                # Convert numpy types to Python primitives
                if isinstance(obj_value, np.generic):
                    obj_value = obj_value.item()

                # Detect datatype and create appropriate literal
                if isinstance(obj_value, bool):
                    obj = Literal(obj_value, datatype=XSD.boolean)
                elif isinstance(obj_value, int):
                    obj = Literal(obj_value, datatype=XSD.integer)
                elif isinstance(obj_value, float):
                    obj = Literal(obj_value, datatype=XSD.double)
                elif isinstance(obj_value, datetime.datetime):
                    obj = Literal(obj_value, datatype=XSD.dateTime)
                elif isinstance(obj_value, str):
                    try:
                        # Try to parse datetime strings
                        dt = datetime.datetime.fromisoformat(obj_value)
                        obj = Literal(dt, datatype=XSD.dateTime)
                    except ValueError:
                        # Fallback to typed string detection
                        if obj_value.isdigit():
                            obj = Literal(int(obj_value), datatype=XSD.integer)
                        elif obj_value.replace('.', '', 1).isdigit():
                            obj = Literal(float(obj_value), datatype=XSD.double)
                        else:
                            obj = Literal(obj_value, datatype=XSD.string)
                else:
                    obj = Literal(str(obj_value), datatype=XSD.string)
            
            g.add((subject, predicate, obj))


# Serialize and save
output_path = r"output\resources.ttl"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
g.serialize(destination=output_path, format="turtle")
print(f"Generated {len(g)} triples in {output_path}")
