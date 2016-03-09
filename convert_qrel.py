#!/usr/bin/env python

from __future__ import unicode_literals

import sys

import argparse
import collections
import os
import logging

SESSION2011, SESSION2012, SESSION2013, SESSION2014 = range(2011, 2014 + 1)
TRACKS = (SESSION2011, SESSION2012, SESSION2013, SESSION2014)

__RELEVANCE_MAPPING_2012 = {
    -2: 0,
    0: 0,
    1: 1,
    4: 2,
    2: 3,
    3: 4,
}


def existing_file_path(value):
    value = str(value)

    if os.path.exists(value):
        return value
    else:
        raise argparse.ArgumentTypeError(
            'File "{0}" does not exists.'.format(value))


def nonexisting_file_path(value):
    value = str(value)

    if not os.path.exists(value):
        return value
    else:
        raise argparse.ArgumentTypeError(
            'File "{0}" already exists.'.format(value))


def parse_qrel(f_qrel, track_edition):
    assert track_edition in TRACKS

    qrel = collections.defaultdict(lambda: collections.defaultdict(None))

    for line in f_qrel:
        topic_id, subtopic_id, document_id, relevance = \
            line.strip().split()

        relevance = int(relevance)

        if track_edition == SESSION2012:
            relevance = __RELEVANCE_MAPPING_2012[relevance]

        qrel[topic_id][document_id] = max(
            qrel[topic_id].get(document_id, None), relevance)

    return qrel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--loglevel', type=str, default='INFO')

    parser.add_argument('--judgments',
                        type=existing_file_path,
                        required=True)
    parser.add_argument('--session_topic_map',
                        type=existing_file_path,
                        required=True)

    parser.add_argument('--track_year',
                        type=int,
                        choices=TRACKS, required=True)

    parser.add_argument('--qrel_out',
                        type=nonexisting_file_path,
                        required=True)

    args = parser.parse_args()

    # Set logging level.
    numeric_log_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_log_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel.upper())

    logging.basicConfig(level=numeric_log_level)

    logging.info('Arguments: %s', args)

    topic_id_to_subtopics = collections.defaultdict(lambda: set([0]))
    topic_id_to_session_ids = collections.defaultdict(set)

    with open(args.session_topic_map, 'r') as f_mapping:
        for line in f_mapping:
            line = line.strip()

            if not line:
                continue

            try:
                data = line.strip().split()[:3]
            except:
                logging.warning('Unable to parse %s', line)

                continue

            if len(data) == 3:
                session_id, topic_id, subtopic_id = data
            else:
                session_id, topic_id, subtopic_id = data + [0]

            topic_id_to_subtopics[topic_id].add(subtopic_id)
            topic_id_to_session_ids[topic_id].add(session_id)

    with open(args.judgments, 'r') as f_judgments:
        qrel = parse_qrel(f_judgments, args.track_year)

    with open(args.qrel_out, 'w') as f_out:
        for topic_id, session_ids in topic_id_to_session_ids.iteritems():
            relevant_items = qrel[topic_id]

            for session_id in session_ids:
                for document_id, relevance in relevant_items.iteritems():
                    f_out.write(
                        '{session_id} 0 {document_id} {relevance}\n'.format(
                            session_id=session_id,
                            document_id=document_id,
                            relevance=relevance))

if __name__ == "__main__":
    sys.exit(main())
