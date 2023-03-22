from django.db import connection


def create_update_karma():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE OR REPLACE PROCEDURE update_karma() as $$
            BEGIN
            
            
            update backend_branch
            set pre_karma = NULL;
            
            
            update backend_branch
            set pre_karma = backend_branch.likes
            from backend_relations as br
            Right join backend_branch as bb on br.child_id = bb.id
            where br.child_id is Null and bb.id = backend_branch.id;
            
            -- in loop while exist parent_karma is null
            WHILE EXISTS (SELECT 1 FROM backend_branch WHERE pre_karma IS NULL) LOOP
            update backend_branch
            set pre_karma = se.karma + backend_branch.likes
            from
                (select bb.id as idi, sum(bp.pre_karma) as karma
                from backend_branch as bn
                join backend_relations as rn on bn.id = rn.parent_id and bn.pre_karma is null
                right join backend_relations as r on r.child_id = rn.child_id
                join backend_branch as bb on r.child_id = bb.id and bb.pre_karma is null
                join backend_branch as bp on r.parent_id = bp.id
                where bn.id is null
                group by bb.id
                ) se
            where backend_branch.id = se.idi;
            -- end loop
            END LOOP;
            
            update backend_branch
            set karma = 0;
			
			update backend_branch
            set karma = bb.likes
			from backend_branch as bb
			left join backend_relations as bc on bb.id = bc.child_id
			left join backend_relations as bp on bb.id = bc.parent_id
			where bc.child_id is null and bp.child_id is null and backend_branch.id = bb.id;
			
			
            
            update backend_branch
            set karma = sel.karma + likes
            from
            (select bb.id as idiot, round((avg(backend_branch.pre_karma))/sqrt(bb.contentlen + 1)) as karma
            from backend_relations as br
            join backend_branch as bb on bb.id = br.parent_id
            join backend_relations as brc on br.child_id = brc.child_id
            join backend_branch on backend_branch.id = brc.parent_id
            group by bb.id, bb.contentlen) as sel
            where backend_branch.id = sel.idiot;
            
            update backend_branch
            set karma = backend_branch.karma + sel.karma
            from
            (select br.child_id as idiot, sum(backend_branch.pre_karma) as karma
            from backend_relations as br
             join backend_branch on backend_branch.id= br.parent_id
            group by br.child_id) as sel
            where backend_branch.id = sel.idiot;
            
            END;
            $$ LANGUAGE plpgsql;
        """)


def update_karma():
    with connection.cursor() as cursor:
        cursor.execute('call update_karma()')
