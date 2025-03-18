# Spoofer project
This pacakge is written to interact with the Spoofer API presented by CAIDA (https://www.caida.org/projects/spoofer/).
It makes the connection easy for end users by constructing the API url and parsing the response to a dictionary. It also provides functions to write the results to a csv or json file.

# Parameters

| Parameter | Description | Type | Default |
| --- | --- | --- | --- |
| items_per_page | Number of items per page | int | 5 |
| asn | Autonomous System Number | int | None |
| date_before | Date before | str | None |
| date_after | Date after | str | None |
| date_strict_before | Date strict before | str | None |
| date_strict_after | Date strict after | str | None |
