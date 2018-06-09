import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
app = Flask(__name__)


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///sbc_2015_ytd2018.sqlite')

# reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(engine, reflect=True)

# Table1 = Base.classes._____table1
# BankName = Base.classes.BankName
# Table3 = Base.classes.table3

# Create our session (link) from Python to the DB
# session = Session(engine)
app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/banks')
def banks():
    """Return a list of banks from the database"""
    conn = engine.connect()
    banks_df = pd.read_sql("select distinct BankName from bank_data2", conn)
    all_banks = banks_df.to_json(orient='records')
    # all_banks = [bank for bank in all_banks]
    return all_banks   

# 
@app.route('/fundings/<bank>')
def fundings(bank):
    """Return a list of funding from the database per funding year"""
    conn = engine.connect()
    loanPie_df = pd.read_sql("select ApprovalYear as FundingYear, sum(grossApproval) as TotalApproval from bank_data2 group by 1,2", conn)
    all_fundings = loanPie_df.to_json(orient='records')

    return all_fundings

@app.route('/sic')
def sic():
    """Return a list of top 10 SIC from the database per bank"""
    conn = engine.connect()
    sicPie_df = pd.read_sql("select SICDescription, SICode, count(SICode) SICode_count from bank_data2 group by 1,2 order by SICode_count desc limit 10", conn)
    all_sic = sicPie_df.to_json(orient='records')

    return all_sic

@app.route('/loans100')
def loans100():
    """Return a list of loans approvals >$100M and C/O>$25M from the database per bank"""
    conn = engine.connect()
    loans100_df = pd.read_sql("select BorrName, BankName, sum(GrossApproval) as TotalLoansApproval, ApprovalYear, sum(COAmount) as ChargeOff, CODate from bank_data2 where BankName <> 'NONE' and GrossApproval >100000 AND COAmount >25000 group by 1", conn)
    all_loans100 = loans100_df.to_json(orient='records')

    return all_loans100

if __name__ == '__main__':
    app.run(debug=True)   