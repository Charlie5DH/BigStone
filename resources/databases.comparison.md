## SQLite

### Overview and features

SQLite is an embedded, file-based `RDBMS` that does not require any installation or setup. This, in turn, means that the application does not run under a separate server process that needs to be started, stopped, or configured. This serverless architecture `enables the database to be cross-platform compatible.`

The complete SQL database is contained within a single disk file and all reads and writes take place directly on this disk file. As the data is directly written back to the disk file, SQLite adheres to the ACID properties to safeguard transactions against memory allocation failures and disk I/O errors that can result from unexpected system crashes or power failures.

### Advantages and use cases

The SQLite library is one of the most compact libraries in this list where the size of the library can easily be under 600 KB. Due to its very small footprint and the nature of the RDBMS, it is a very good fit for IoT and embedded devices.

Some other good use cases include `low-to-medium traffic websites (~ 100K requests a day)`, testing and internal development purposes, data analysis using Tcl or Python and `educational purposes` (this is simple to set up and can be used to teach SQL concepts to students).

One major advantage of SQLite is how it can act as a complementary solution for client/server enterprise RDBMS. For example, it `can cache data from client/server RDBMS locally` and thereby reduce the latency for queries and keep the end application alive in case of enterprise RDBMS outages.

### Disadvantages

One of the main drawbacks of the SQLite system is `its lack of multi-user capabilities` which can be found in full-fledged RDBMS systems like MySQL and PostgreSQL. This translates to a lack of granular access control, a friendly user management system, `and security capabilities beyond encrypting the database file itself`. This is a major drawback when designing multi-user applications like CRM and SaaS applications and is normally not favored when building multi-user or multi-tenant applications. `(Note: SQLite does support multiple users but only one user can write to the database at a time. This is not a problem for read-heavy applications but can be a major bottleneck for write-heavy applications)`

Also worth noting is the lack of any Database as a Service (DBaaS) offering from any major cloud provider. With the advent of the public cloud, use of PaaS services (like DBaaS) by developers and DevOps teams have become common place. Lack of a managed service offering from top public cloud providers means that the common management tasks must be the responsibility of the DB Admin thus increasing OPEX costs.
