#Course Schedule Automator

import csv
import pdb

#my first effort at using classes in a program
#we ended up pursuing a path through this project through different technology, so I stopped working on it
#but I've retained this for posterity

class Record:
    'base class for course schedule records'
    recordCount = 0

    def __init__(self, recordID):
        self.recordID = recordID
        Record.recordCount += 1

    def displayCount(self):
        print 'Total Records: %d' % Record.recordCount

    def copy(self):
        NewRecord = Record(str(self.recordID)+'_'+str(Record.recordCount))
        return NewRecord

def import_courseschedule(filename):
    """returns a dictionary of Records from an input file"""
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        headers = spamreader.next()
        i = len(headers)
        recs = {}
        for row in spamreader:
            recs[row[0]] = Record(row[0])
            for col in xrange(i-1):
                setattr(recs[row[0]], headers[col], row[col])
        return recs

def import_rules(filename):
    """returns a tuple for term, rotation, and period splitting rules from an input file"""
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        term_rules = {}
        rot_rules = {}
        per_rules = {}
        for row in spamreader:
            if row[0] == 'Term':
                term_rules[row[1]] = [i for i in row[2:] if i != '']
            if row[0] == 'Rotation':
                rot_rules[row[1]] = [i for i in row[2:] if i != '']
            if row[0] == 'Period':
                per_rules[row[1]] = [i for i in row[2:] if i != '']
        return term_rules, rot_rules, per_rules

def sort_by_stu(recs):
    """this takes a dict of records and returns a dict sorted by students"""
    stu_list = {}
    for rec in recs:
        stu_list[recs[rec].StudentID] = stu_list.get(recs[rec].StudentID,{})
        stu_list[recs[rec].StudentID][recs[rec].RecordID] = rec
    return stu_list


records = import_courseschedule('CourseSchedule.csv')
term_rules, rot_rules, per_rules = import_rules('splittingrules.csv')



j = 100
for rec in records.keys():
    if records[rec].Term in term_rules:
        for item in term_rules[records[rec].Term]:
            new_record = str(j)
            j += 1
            records[new_record] = copy.deepcopy(records[rec])
            records[new_record].Term_Wt /= len(term_rules[records[rec].Term])
            records[new_record].Term = item
            records[new_record].classID = records[rec].classID + '_' + item
            records[new_record].Term = item
        del records[rec]

