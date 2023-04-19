# Generated by Django 4.1.7 on 2023-03-27 18:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('likes', models.IntegerField(blank=True, default=0, editable=False)),
                ('views', models.IntegerField(blank=True, default=0, editable=False)),
                ('time_create', models.TimeField(auto_now_add=True)),
                ('time_update', models.TimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('content', models.TextField(blank=True, null=True)),
                ('pre_karma', models.IntegerField(blank=True, db_index=True, editable=False, null=True)),
                ('karma', models.IntegerField(blank=True, default=0, editable=False)),
                ('contentlen', models.IntegerField(editable=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.language')),
            ],
        ),
        migrations.CreateModel(
            name='Relations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='backend.branch')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.branch')),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='links',
            field=models.ManyToManyField(blank=True, through='backend.Relations', to='backend.branch'),
        ),
        migrations.AddField(
            model_name='branch',
            name='tags',
            field=models.ManyToManyField(blank=True, to='common.tag'),
        ),
        migrations.AddField(
            model_name='branch',
            name='users_learned',
            field=models.ManyToManyField(blank=True, editable=False, related_name='user_learned_Branches', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='branch',
            name='users_liked',
            field=models.ManyToManyField(blank=True, editable=False, related_name='user_liked_Branches', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='branch',
            name='users_wanted',
            field=models.ManyToManyField(blank=True, related_name='user_wanted_to_learn_Branches', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunSQL("""
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
            set karma = sel.karma + pre_karma/sqrt(contentlen + 1)
            from
            (select bb.id as idiot, round((avg(backend_branch.pre_karma))) as karma
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
        """),
        migrations.RunSQL("""
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
        """),


    ]
