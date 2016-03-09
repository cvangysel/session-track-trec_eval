TREC Session Track - trec_eval
==============================

A utility for converting the relevance judgments of the [TREC Session Track](http://trec.nist.gov/data/session.html) to a format understandable by [trec_eval](https://github.com/usnistgov/trec_eval).

The `fetch_and_convert_qrels.sh` (requires Bash 4 and up) script downloads all necessary files from TREC and creates converted judgments automatically for the 2011 to 2014 TREC Session Track editions.