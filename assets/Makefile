PSQL="PGPASSWORD=password psql -h 127.0.0.1 postgres postgres"

bootstrap:
	@sh -c ${PSQL} < bootstrap.sql

dummy:
	@sh -c ${PSQL} < dummy_data.sql

shell:
	@sh -c ${PSQL}
