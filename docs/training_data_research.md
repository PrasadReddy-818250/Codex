# Training Data Research Map

This file consolidates the research swarm output for the local SQL/Python assistant dataset. It is a source and coverage map, not a training corpus.

Use these sources to verify behavior and then write original synthetic examples. Do not copy vendor docs, book examples, course material, LinkedIn posts, Stack Overflow answers, screenshots, or proprietary text into training data unless the license has been reviewed and recorded.

## Licensing Rule

Training records in this repo must remain `synthetic` or clearly `green` under `training.dataset_schema`.

Allowed:

- Original examples written for this project.
- Short factual API/syntax references.
- Permissive material only when license obligations are tracked.

Disallowed by default:

- Oracle/MySQL, IBM, AWS, Microsoft, course, book, blog, LinkedIn, or Stack Overflow prose copied into records.
- Private customer data, credentials, logs, tickets, database dumps, or proprietary manuals.
- Exact vendor examples unless license review explicitly permits reuse.

## Topic Coverage

| Topic | High-value coverage |
|---|---|
| PostgreSQL | `ON CONFLICT`, transactions, isolation, locks, indexes, GIN/BRIN, window functions, CTEs, JSONB, `EXPLAIN`, `COPY`, roles, grants, row security |
| MySQL | `ON DUPLICATE KEY UPDATE`, isolation, deadlocks, composite indexes, `EXPLAIN`, window functions, JSON, `LOAD DATA`, `DATETIME` vs `TIMESTAMP`, `utf8mb4`, collation |
| Db2 LUW | `MERGE`, identity/generated columns, `SYSCAT` catalog views, CS/RS/RR/UR isolation, indexes, explain, `LOAD` vs `IMPORT`, datetime functions, `ibm_db` |
| Db2 for i / AS400 | IBM i naming, library list, SQL services, QSYS2/SYSTOOLS, catalog differences from LUW, journaling, commitment control, ACS Run SQL Scripts |
| SQL conversion | Pagination, upsert/merge, date arithmetic, string functions, null-safe equality, identity/autoincrement, schema/name quoting across PostgreSQL, MySQL, SQLite, Db2 LUW, Db2 for i |
| SQL performance | Plan reading, sargability, composite/covering/partial indexes, join blowups, aggregation/sort costs, stale stats, keyset pagination, locking, injection-safe dynamic SQL |
| DB drivers | DB-API parameter styles, SQLAlchemy 2.0 Core/ORM, psycopg/psycopg2, PyMySQL, mysql-connector, pyodbc, sqlite3, ibm_db, pooling, exceptions, transactions |
| pandas/numpy | merge validation, groupby/transform, missing values, nullable dtypes, timezone handling, chunked CSV, Excel dtype drift, vectorization, memory reduction |
| boto3/fsspec | S3 pagination, credentials, retries, presigned URLs, multipart upload, streaming objects, fsspec URLs, s3fs/gcsfs/adlfs `storage_options` |
| PySpark | joins, anti/semi joins, null-safe equality, windows, schemas, partitioned Parquet, shuffles, broadcast joins, skew, UDF pitfalls, `collect()`/`toPandas()` risks |
| Airflow | parse-time side effects, TaskFlow, retries, schedules/data intervals, connections, XCom limits, sensors, deferrable operators, catchup/backfill, idempotency |
| requests/httpx/kafka | explicit timeouts, sessions/clients, streaming, JSON errors, retry boundaries, secret-safe logging, HTTPX async, Kafka offsets, commits, serializers |
| Excel/files | openpyxl vs XlsxWriter, formulas not calculated by Python libs, large workbook modes, pandas Excel IO, CSV encodings/newlines, safe path constraints |
| Safety/style | direct answers, explicit uncertainty, no fake execution claims, no secret dumping, no malware, confirmation before destructive SQL/filesystem actions |

## Primary Source Map

PostgreSQL:

- https://www.postgresql.org/docs/current/sql-insert.html
- https://www.postgresql.org/docs/current/tutorial-transactions.html
- https://www.postgresql.org/docs/current/transaction-iso.html
- https://www.postgresql.org/docs/current/indexes.html
- https://www.postgresql.org/docs/current/functions-window.html
- https://www.postgresql.org/docs/current/queries-with.html
- https://www.postgresql.org/docs/current/datatype-json.html
- https://www.postgresql.org/docs/current/using-explain.html
- https://www.postgresql.org/docs/current/sql-copy.html
- https://www.postgresql.org/docs/current/ddl-priv.html

MySQL:

- https://dev.mysql.com/doc/refman/8.4/en/insert-on-duplicate.html
- https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html
- https://dev.mysql.com/doc/refman/8.4/en/explain.html
- https://dev.mysql.com/doc/refman/8.4/en/window-functions.html
- https://dev.mysql.com/doc/refman/8.4/en/json-functions.html
- https://dev.mysql.com/doc/refman/8.4/en/load-data.html
- https://dev.mysql.com/doc/refman/8.4/en/date-and-time-functions.html
- https://dev.mysql.com/doc/refman/8.4/en/charset-unicode-utf8mb4.html

IBM Db2:

- https://www.ibm.com/docs/en/db2/11.5.x?topic=statements-merge
- https://www.ibm.com/docs/en/db2/11.5.x?topic=views-syscattables
- https://www.ibm.com/docs/en/db2/11.5.x?topic=views-syscatcolumns
- https://www.ibm.com/docs/en/db2/11.5.x?topic=views-syscatindexes
- https://www.ibm.com/docs/en/db2/11.5.x?topic=optimization-explain-facility
- https://www.ibm.com/docs/en/db2/11.5.x?topic=commands-load
- https://www.ibm.com/docs/en/db2/11.5.x?topic=commands-import
- https://www.ibm.com/support/pages/ibm-i-services-sql
- https://www.ibm.com/docs/en/i/7.4.0?topic=concepts-sql-system-naming-conventions
- https://www.ibm.com/docs/en/i/7.5?topic=integrity-commitment-control

SQLite:

- https://www.sqlite.org/lang_select.html
- https://sqlite.org/lang_upsert.html
- https://www.sqlite.org/queryplanner.html
- https://sqlite.org/eqp.html
- https://www.sqlite.org/lang_datefunc.html
- https://www.sqlite.org/lang_keywords.html

Python data engineering:

- https://docs.sqlalchemy.org/20/
- https://peps.python.org/pep-0249/
- https://www.psycopg.org/psycopg3/docs/
- https://www.psycopg.org/docs/
- https://pymysql.readthedocs.io/
- https://dev.mysql.com/doc/connector-python/en/
- https://github.com/mkleehammer/pyodbc/wiki
- https://docs.python.org/3/library/sqlite3.html
- https://pandas.pydata.org/docs/
- https://numpy.org/doc/stable/
- https://spark.apache.org/docs/latest/
- https://airflow.apache.org/docs/apache-airflow/stable/
- https://requests.readthedocs.io/
- https://www.python-httpx.org/
- https://kafka-python.readthedocs.io/
- https://docs.aws.amazon.com/boto3/latest/
- https://filesystem-spec.readthedocs.io/
- https://s3fs.readthedocs.io/
- https://gcsfs.readthedocs.io/
- https://fsspec.github.io/adlfs/
- https://openpyxl.readthedocs.io/
- https://xlsxwriter.readthedocs.io/

Safety and security:

- https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- https://owasp.org/www-project-top-10-for-large-language-model-applications/
- https://cwe.mitre.org/data/definitions/89.html
- https://docs.python.org/3/library/subprocess.html#security-considerations
- https://www.nist.gov/itl/ai-risk-management-framework

## Example-Idea Backlog

Convert these into original JSONL records in batches:

- PostgreSQL: atomic upserts, stale-event guarded updates, partial/expression indexes, top-N per group, JSONB search, `COPY` staging, least-privilege roles.
- MySQL: duplicate-key upserts, multiple unique-key risks, row alias upsert style, deadlock retry, `LOAD DATA`, `utf8mb4`, collation mismatch fixes.
- Db2 LUW: `MERGE` staging sync, identity/generated columns, catalog introspection, isolation choice, explain workflow, `LOAD`/`IMPORT`, Python `ibm_db`.
- Db2 for i: SQL vs system naming, library-list resolution, SQL services, journaling/commitment control, ACS scripts, LUW migration checklist.
- Conversion: MySQL `LIMIT offset,count`, upsert/merge mappings, date arithmetic, string concatenation, null-safe equality, identity DDL, quoted identifiers.
- Performance: non-sargable predicates, composite index order, keyset pagination, stale stats, accidental inner joins, deadlocks, safe dynamic sort columns.
- DB drivers: placeholder differences, failed transaction rollback, SQLAlchemy `URL.create`, `engine.begin`, `Result.mappings`, pools, exceptions.
- pandas/numpy: merge validation, `_merge` audit, groupby transform, nullable integer IDs, DST localization, chunked CSV, Excel sheet normalization.
- boto3/fsspec: S3 paginator, presigned POST constraints, multipart cleanup, object streaming, fsspec local/S3/GCS/Azure URL handling.
- PySpark: anti joins, duplicate columns, null-safe joins, window ranking, explicit schemas, partition pruning, skew, UDF null handling.
- Airflow: no top-level network/DB calls, TaskFlow execution timing, XCom size limits, retry-safe writes, catchup vs backfill, deferrable sensors.
- requests/httpx/kafka: no unbounded requests, secret-safe logs, async HTTPX, JSON decode handling, Kafka manual commit next offset, dead-letter bad JSON.
- Excel/files: preserve IDs as text, append sheets safely, formulas not calculated by openpyxl, streaming large workbooks, CSV encoding/newline handling, path containment.
- Safety/style: refuse secret dumps and malware, fix injection, ask before destructive execution, state “not verified” when tests/files were not actually checked.
