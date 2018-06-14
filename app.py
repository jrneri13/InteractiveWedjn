import numpy as numpy

import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

engine = create_engine('sqlite:///belly_button_biodiversity.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)

Metadata = Base.classes.samples_metadata
Otu = Base.classes.otu 
Samples = Base.classes.samples 
session = Session(engine)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/names")
def names_list():
    inspector = inspect(engine)
    columns = inspector.get_columns('samples')
    names = []
    for column in columns[1:]:
        names.append(column['name'])
    return jsonify(names)

@app.route("/otu")
def description():
    results = session.query(Otu.lowest_taxonomic_unit_found).all()
    otus = []
    for result in results:
        otus.append(result[0])

@app.route("/metadata/<sample>")
def meta_sample(sample):
    sample_id = sample[3:]
    result = session.query(Metadata.AGE, Metadata.BBTYPE, Metadata.ETHNICITY, Metadata.GENDER, Metadata.LOCATION, Metadata.SAMPLEID).filter(Metadata.SAMPELEDID == sample_id).first()

    metadic = {
        'AGE': result[0], 'BBTYPE': result[1], 'ETHNICITY': result[2], 'GENDER': result[3], 'LOCATION': result[4], 'SAMPLEID': result[5]
    }
    return jsonify(metadic)

@app.route("/wfreq/<samples>")
def washing(sample):
    sample_id = sample[3:]
    result = session.query(Metadata.WFREQ,Metadata.SAMPLEID).filter(Metadata.SAMPLEID == sample_id).first()
    return jsonify(result[0])

@app.route("/samples/<samples>")
def samp(sample):
    sample_id_query = f'Samples.{sample}'
    results = session.query(Samples.otu_id, sample_id_query).order_by(desc(sample_id_query))
    sampdic = {'otu_ids': [result[0] for result in results],
                'sample_values': [result[1] for result in results]}
    return jsonify(sampdic)

if __name__ == "__main__":
    app.run()