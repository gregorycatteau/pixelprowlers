-- Maintenance/schema-owner connection only. No password in this file.
-- psql -v db_name=... -v owner_role=... -f runtime-role.sql
CREATE ROLE pixelprowlers_app NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS;
GRANT CONNECT ON DATABASE :"db_name" TO pixelprowlers_app;
GRANT USAGE ON SCHEMA public TO pixelprowlers_app;
-- Active historical apps only; orphan api_* tables are deliberately excluded.
SELECT format('GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE %I.%I TO pixelprowlers_app', schemaname, tablename)
FROM pg_tables WHERE schemaname='public'
AND tablename ~ '^(audits_|crm_|urgencies_|tracking_|auth_|django_session$|django_admin_log$)'
\gexec
GRANT SELECT ON TABLE django_content_type, django_migrations TO pixelprowlers_app;
SELECT format('GRANT USAGE, SELECT ON SEQUENCE %I.%I TO pixelprowlers_app', schemaname, sequencename)
FROM pg_sequences WHERE schemaname='public'
AND sequencename ~ '^(audits_|crm_|urgencies_|tracking_|auth_|django_session_|django_admin_log_)'
\gexec
-- No ownership transfer, schema CREATE, or blanket future/default grants.
-- After a later migration, review and reapply the GRANT section for new app tables.
-- PostgreSQL 15 normally gives PUBLIC no CREATE on public: verify before activation.
-- If legacy grants differ, review a separate REVOKE CREATE FROM PUBLIC operation.
-- Provision LOGIN/password interactively only after approval (\password).
