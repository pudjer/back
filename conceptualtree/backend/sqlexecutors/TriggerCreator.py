from django.db import connection


def my_custom_sql(root_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE OR REPLACE FUNCTION check_cyclicity() RETURNS trigger AS $$
            DECLARE
              found_cycle boolean;
            BEGIN
                IF not exists (select 1 from backend_relations where backend_relations.child_id = NEW.parent_id)  THEN
                RETURN NEW;
              END IF;
              -- Check for cyclicity in the updated rows
              WITH RECURSIVE search_graph(child_id, parent_id, depth, path) AS (
                SELECT child_id, parent_id, 1, ARRAY[child_id]
                FROM backend_relations
                UNION ALL
                SELECT ur.child_id, ur.parent_id, sg.depth + 1, path || ur.child_id
                FROM search_graph sg, backend_relations ur
                WHERE sg.parent_id = ur.child_id AND NOT ur.child_id = ANY(path)
              )
              SELECT 1 FROM search_graph WHERE child_id = NEW.parent_id LIMIT 1 INTO found_cycle;
            
              IF found_cycle THEN
                RAISE EXCEPTION 'Cyclicity detected';
              END IF;
            
              RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
            
            
            
            CREATE or replace TRIGGER check_cyclicity_trigger
            BEFORE INSERT or update ON backend_relations
            FOR EACH ROW
            EXECUTE FUNCTION check_cyclicity();
        """)