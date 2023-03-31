from django.db import connection


def create_trigger():
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
              WITH RECURSIVE search_graph(child_id, parent_id, is_cycle) AS (
                SELECT child_id, parent_id, false
                FROM backend_relations as br
				where br.parent_id = NEW.child_id
                UNION
                SELECT ur.child_id, ur.parent_id, ur.child_id = NEW.parent_id
                FROM backend_relations ur 
				join search_graph sg on sg.child_id = ur.parent_id
              )
              SELECT  1 FROM search_graph WHERE is_cycle is true LIMIT 1 INTO found_cycle;
            
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