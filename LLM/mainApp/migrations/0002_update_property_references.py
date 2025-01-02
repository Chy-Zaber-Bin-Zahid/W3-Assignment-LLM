# mainApp/migrations/0002_update_property_references.py
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        # First, ensure hotel_id is unique in hotels table
        migrations.RunSQL(
            sql='''
            CREATE UNIQUE INDEX IF NOT EXISTS hotels_hotel_id_unique 
            ON hotels(hotel_id);
            ''',
            reverse_sql='DROP INDEX IF EXISTS hotels_hotel_id_unique;'
        ),
        
        # Modify property_id columns to be VARCHAR to match hotel_id
        migrations.RunSQL(
            sql='''
            ALTER TABLE property_summaries 
            ALTER COLUMN property_id TYPE VARCHAR(50);
            
            ALTER TABLE property_reviews 
            ALTER COLUMN property_id TYPE VARCHAR(50);
            ''',
            reverse_sql='''
            ALTER TABLE property_summaries 
            ALTER COLUMN property_id TYPE INTEGER;
            
            ALTER TABLE property_reviews 
            ALTER COLUMN property_id TYPE INTEGER;
            '''
        ),
        
        # Add foreign key constraints
        migrations.RunSQL(
            sql='''
            ALTER TABLE property_summaries
            ADD CONSTRAINT fk_property_summaries_hotel
            FOREIGN KEY (property_id)
            REFERENCES hotels(hotel_id)
            ON DELETE CASCADE;
            
            ALTER TABLE property_reviews
            ADD CONSTRAINT fk_property_reviews_hotel
            FOREIGN KEY (property_id)
            REFERENCES hotels(hotel_id)
            ON DELETE CASCADE;
            ''',
            reverse_sql='''
            ALTER TABLE property_summaries
            DROP CONSTRAINT IF EXISTS fk_property_summaries_hotel;
            
            ALTER TABLE property_reviews
            DROP CONSTRAINT IF EXISTS fk_property_reviews_hotel;
            '''
        ),
    ]