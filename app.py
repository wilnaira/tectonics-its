from flask import Flask, render_template, jsonify
from rdflib import Graph

app = Flask(__name__)

# Load the ontology
g = Graph()
g.parse("ontology.owl")

# Route for Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Route for Tutorial Page (dynamically generated from ontology)
@app.route("/tutorial.html")
def tutorial():
    # Query to get classes with their labels and comments from the ontology
    query = """
    SELECT ?class ?label ?comment
    WHERE {
        ?class a owl:Class .
        OPTIONAL { ?class rdfs:label ?label }
        OPTIONAL { ?class rdfs:comment ?comment }
    }
    """
    results = g.query(query)
    
    # Extract the results into a list of dictionaries
    tutorial_data = [{
        "uri": str(row['class']),
        "label": str(row['label']) if row['label'] else "No label",
        "comment": str(row['comment']) if row['comment'] else "No comment"
    } for row in results]
    
    # Render the template with tutorial data
    return render_template("tutorial.html", tutorial_data=tutorial_data)


# Route for Quiz Page (dynamically generated from ontology)
@app.route("/quiz.html")
def quiz():
    # Query to get classes with labels for the quiz
    query = """
    SELECT ?class ?label
    WHERE {
        ?class a owl:Class .
        OPTIONAL { ?class rdfs:label ?label }
    }
    """
    results = g.query(query)
    
    # Create a list of quiz questions from the RDF data
    quiz_data = [{
        "uri": str(row['class']),
        "label": str(row['label']) if row['label'] else "No label"
    } for row in results]
    
    # Render the quiz page with the extracted data
    return render_template("quiz.html", quiz_data=quiz_data)


# API endpoint to get the classes in JSON format (can be used in quiz, tutorial, etc.)
@app.route("/api/classes", methods=["GET"])
def get_classes():
    query = """
    SELECT ?class ?label ?comment
    WHERE {
        ?class a owl:Class .
        OPTIONAL { ?class rdfs:label ?label }
        OPTIONAL { ?class rdfs:comment ?comment }
    }
    """
    results = g.query(query)
    return jsonify([{
        "uri": str(row.class_),
        "label": str(row.label) if row.label else "No label",
        "comment": str(row.comment) if row.comment else "No comment"
    } for row in results])

if __name__ == "__main__":
    app.run(debug=True)
