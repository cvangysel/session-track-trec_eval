#!/usr/bin/env bash

declare -A SESSION_TRACKS
SESSION_TRACKS[2011]="http://trec.nist.gov/data/session/11/judgments.txt"
SESSION_TRACKS[2012]="http://trec.nist.gov/data/session/12/qrels.txt"
SESSION_TRACKS[2013]="http://trec.nist.gov/data/session/2013/qrels.txt"
SESSION_TRACKS[2014]="http://trec.nist.gov/data/session/2014/judgments.txt"

declare -A TOPIC_MAPS
TOPIC_MAPS[2011]="http://trec.nist.gov/data/session/11/sessionlastquery_subtopic_map.txt"
TOPIC_MAPS[2012]="http://trec.nist.gov/data/session/12/sessiontopicmap.txt"
TOPIC_MAPS[2013]="http://trec.nist.gov/data/session/2013/sessiontopicmap.txt"
TOPIC_MAPS[2014]="http://trec.nist.gov/data/session/2014/session-topic-mapping.txt"

if [[ -d "build" ]]; then
	echo "Output directory 'build' already exists."

	exit -1
fi

mkdir -p "build"

for SESSION_TRACK in "${!SESSION_TRACKS[@]}"; do
	echo "Fetching ${SESSION_TRACK} judgments: ${SESSION_TRACKS[${SESSION_TRACK}]}"
	curl -s "${SESSION_TRACKS[${SESSION_TRACK}]}" > "build/${SESSION_TRACK}.original_qrel"

	echo "Fetching ${SESSION_TRACK} session-topic map: ${TOPIC_MAPS[${SESSION_TRACK}]}"
	curl -s "${TOPIC_MAPS[${SESSION_TRACK}]}" > "build/${SESSION_TRACK}.session_topic_map"

	echo "Creating ${SESSION_TRACK} trec_eval-compatible qrel."
	python convert_qrel.py \
		--judgments "build/${SESSION_TRACK}.original_qrel" \
		--session_topic_map "build/${SESSION_TRACK}.session_topic_map" \
		--track_year "${SESSION_TRACK}" \
		--qrel_out "build/${SESSION_TRACK}.qrel"
done