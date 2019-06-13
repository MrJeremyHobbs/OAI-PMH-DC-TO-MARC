#!/usr/bin/python3
from sickle import Sickle
from pymarc import Record, Field, MARCWriter
import os
import re

# configurations
save_file = 'c:\\users\\user\\desktop\\books.dat'

# delete old file (if exists)
os.system(f'del {save_file}')

# load OAI-PMH client
# documentation: https://sickle.readthedocs.io/en/latest/
sickle = Sickle('http://content.cdlib.org/oai')
records = sickle.ListRecords(metadataPrefix='oai_dc', set='YOUR_SET_ID_HERE')

# parse harvested records and generate MARC21
for record in records:
    # parse dc record
    dc  = record.metadata
    contributors = dc.get("contributor", [])
    coverages = dc.get("coverage", [])
    creators = dc.get("creator", [])
    dates = dc.get("date", [])
    descriptions = dc.get("description", [])
    formats = dc.get("format", [])
    identifiers = dc.get("identifier", [])
    languages = dc.get("language", [])
    publishers = dc.get("publisher", [])
    relations = dc.get("relation", [])
    rights = dc.get("rights", [])
    sources = dc.get("source", [])
    subjects = dc.get("subject", [])
    titles = dc.get("title", [])
    
    # other fields
    leader = ""
    #collections = ['The collection is open for research use.']
    
    # generate MARC record
    marc_record = Record(force_utf8=True)
    
    # MARC field 100
    if creators:
        for creator in creators:
            marc_record.add_field(
                Field(
                    tag = '100',
                    indicators = ['1', ''],
                    subfields = [
                        'a', f'{creator}',
                    ]))
                
    # MARC field 245
    if titles:
        for title in titles:
            marc_record.add_field(
                Field(
                    tag = '245',
                    indicators = ['1', '0'],
                    subfields = [
                        'a', f'{title}',
                    ]))
                
    # MARC field 264
    if dates:
        for date in dates:
            marc_record.add_field(
                Field(
                    tag = '264',
                    indicators = ['', '0'],
                    subfields = [
                        'c', f'{date}',
                    ]))
            
    # MARC field 300
    if formats:
        for format in formats:
            format.rstrip('\n')
            format = re.sub(r'\s{2}', '', format)
            marc_record.add_field(
                Field(
                    tag = '300',
                    indicators = ['', ''],
                    subfields = [
                        'a', f'{format}',
                        'f', '',
                    ]))
                
    # MARC field 506
    if rights:
        for right in rights:
            marc_record.add_field(
                Field(
                    tag = '506',
                    indicators = ['', ''],
                    subfields = [
                        'a', f'{right}',
                    ]))
                
    # MARC field 520
    if descriptions:
        for description in descriptions:
            marc_record.add_field(
                Field(
                    tag = '520',
                    indicators = ['3', ''],
                    subfields = [
                        'a', f'{description}',
                    ]))
                
    # MARC field 610
    if subjects:
        for subject in subjects:
            marc_record.add_field(
                Field(
                    tag = '610',
                    indicators = ['1', '0'],
                    subfields = [
                        'a', f'{subject}',
                    ]))
                
    # MARC field 651
    if coverages:
        for coverage in coverages:
            marc_record.add_field(
                Field(
                    tag = '651',
                    indicators = ['', '0'],
                    subfields = [
                        'a', f'{coverage}',
                    ]))
            
    # MARC field 700
    if creators:
        for creator in creators:
            marc_record.add_field(
                Field(
                    tag = '700',
                    indicators = ['1', ''],
                    subfields = [
                        'a', f'{creator}',
                        't', '',
                    ]))
            
    # MARC field 856
    if identifiers:
        for identifier in identifiers:
            marc_record.add_field(
                Field(
                    tag = '856',
                    indicators = ['4', '2'],
                    subfields = [
                        '3', 'Finding aid',
                        'u', f'{identifier}',
                    ]))
    
    # write to MARC output file
    writer = MARCWriter(open(save_file,'ab'))
    writer.write(marc_record)
    writer.close()

# open up MARC record in default viewer (NOTEPAD most likely)    
os.system(save_file)