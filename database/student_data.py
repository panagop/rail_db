"""""""""

Student grades data import module

"""Student grades data import moduleStudent grades data import module

import json

import os""""""

from .connection import DatabaseManager

import jsonimport json



class StudentDataImporter:import osimport os

    """Class to handle student grades data import operations"""

    from .connection import DatabaseManagerfrom .connection import DatabaseManager

    @staticmethod

    def load_student_data():

        """Load student data from the JavaScript file"""

        js_file_path = os.path.join(os.path.dirname(__file__), '..', 'old_files', 'betongrades.js')

        

        with open(js_file_path, 'r') as file:class StudentDataImporter:class StudentDataImporter:

            content = file.read()

            """Class to handle student grades data import operations"""    """Class to handle student grades data import operations"""

        # Extract the JSON array from the JavaScript variable declaration

        # Find the start of the array    

        start_index = content.find('[')

        if start_index == -1:    @staticmethod    @staticmethod

            raise ValueError("Could not find JSON array in the file")

            def load_student_data():    def load_student_data():

        # Extract just the JSON array part

        json_data = content[start_index:]        """Load student data from the JavaScript file"""        """Load student data from the JavaScript file"""

        

        # Parse the JSON data        js_file_path = os.path.join(os.path.dirname(__file__), '..', 'old_files', 'betongrades.js')        js_file_path = os.path.join(os.path.dirname(__file__), '..', 'old_files', 'betongrades.js')

        student_grades = json.loads(json_data)

                        

        print(f"✅ Loaded {len(student_grades)} student grade records")

        return student_grades        with open(js_file_path, 'r') as file:        with open(js_file_path, 'r') as file:



    @staticmethod            content = file.read()            content = file.read()

    def create_student_grades_table():

        """Create the student_grades table"""                

        create_table_sql = """

        CREATE TABLE IF NOT EXISTS student_grades (        # Extract the JSON array from the JavaScript variable declaration        # Extract the JSON array from the JavaScript variable declaration

            id SERIAL PRIMARY KEY,

            aem INTEGER NOT NULL,        # Find the start of the array        # Find the start of the array

            test VARCHAR(50) NOT NULL,

            grade DECIMAL(10, 8) NOT NULL,        start_index = content.find('[')        start_index = content.find('[')

            year INTEGER NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,        if start_index == -1:        if start_index == -1:

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(aem, test, year)            raise ValueError("Could not find JSON array in the file")            raise ValueError("Could not find JSON array in the file")

        );

        """                

        

        # Create index for better query performance        # Extract just the JSON array part        # Extract just the JSON array part

        create_indexes_sql = [

            "CREATE INDEX IF NOT EXISTS idx_student_grades_aem ON student_grades(aem);",        json_data = content[start_index:]        json_data = content[start_index:]

            "CREATE INDEX IF NOT EXISTS idx_student_grades_year ON student_grades(year);",

            "CREATE INDEX IF NOT EXISTS idx_student_grades_test ON student_grades(test);",                

            "CREATE INDEX IF NOT EXISTS idx_student_grades_grade ON student_grades(grade);"

        ]        # Parse the JSON data        # Parse the JSON data

        

        with DatabaseManager() as db:        student_grades = json.loads(json_data)        student_grades = json.loads(json_data)

            # Create table

            if db.execute_command(create_table_sql):                

                print("✅ Student grades table created successfully!")

                    print(f"✅ Loaded {len(student_grades)} student grade records")        print(f"✅ Loaded {len(student_grades)} student grade records")

            # Create indexes

            for index_sql in create_indexes_sql:        return student_grades        return student_grades

                db.execute_command(index_sql)

            

            print("✅ Database indexes created successfully!")

    @staticmethod    @staticmethod

    @staticmethod

    def import_student_data():    def create_student_grades_table():    def create_student_grades_table():

        """Import student data into the database"""

        try:        """Create the student_grades table"""        """Create the student_grades table"""

            # Load data from file

            student_data = StudentDataImporter.load_student_data()        create_table_sql = """        create_table_sql = """

            

            # Create table        CREATE TABLE IF NOT EXISTS student_grades (        CREATE TABLE IF NOT EXISTS student_grades (

            StudentDataImporter.create_student_grades_table()

                        id SERIAL PRIMARY KEY,            id SERIAL PRIMARY KEY,

            # Insert data

            with DatabaseManager() as db:            aem INTEGER NOT NULL,            aem INTEGER NOT NULL,

                insert_sql = """

                INSERT INTO student_grades (aem, test, grade, year)             test VARCHAR(50) NOT NULL,            test VARCHAR(50) NOT NULL,

                VALUES (%s, %s, %s, %s) 

                ON CONFLICT (aem, test, year) DO UPDATE SET            grade DECIMAL(10, 8) NOT NULL,            grade DECIMAL(10, 8) NOT NULL,

                    grade = EXCLUDED.grade,

                    updated_at = CURRENT_TIMESTAMP;            year INTEGER NOT NULL,            year INTEGER NOT NULL,

                """

                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                inserted_count = 0

                updated_count = 0            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                

                for record in student_data:            UNIQUE(aem, test, year)  -- Prevent duplicate entries for same student/test/year            UNIQUE(aem, test, year)  -- Prevent duplicate entries for same student/test/year

                    aem = record['AEM']

                    test = record['Test']        );        );

                    grade = record['Grade']

                    year = record['Year']        """        """

                    

                    # Check if record exists                

                    check_sql = "SELECT id FROM student_grades WHERE aem = %s AND test = %s AND year = %s;"

                    existing = db.execute_query(check_sql, (aem, test, year))        # Create index for better query performance        # Create index for better query performance

                    

                    if db.execute_command(insert_sql, (aem, test, grade, year)):        create_indexes_sql = [        create_indexes_sql = [

                        if existing:

                            updated_count += 1            "CREATE INDEX IF NOT EXISTS idx_student_grades_aem ON student_grades(aem);",            "CREATE INDEX IF NOT EXISTS idx_student_grades_aem ON student_grades(aem);",

                        else:

                            inserted_count += 1            "CREATE INDEX IF NOT EXISTS idx_student_grades_year ON student_grades(year);",            "CREATE INDEX IF NOT EXISTS idx_student_grades_year ON student_grades(year);",

                

                print(f"✅ Data import completed!")            "CREATE INDEX IF NOT EXISTS idx_student_grades_test ON student_grades(test);",            "CREATE INDEX IF NOT EXISTS idx_student_grades_test ON student_grades(test);",

                print(f"   📊 New records inserted: {inserted_count}")

                print(f"   🔄 Records updated: {updated_count}")            "CREATE INDEX IF NOT EXISTS idx_student_grades_grade ON student_grades(grade);"            "CREATE INDEX IF NOT EXISTS idx_student_grades_grade ON student_grades(grade);"

                print(f"   📋 Total records processed: {len(student_data)}")

                        ]        ]

            return True

                            

        except Exception as e:

            print(f"❌ Error importing data: {e}")        with DatabaseManager() as db:        with DatabaseManager() as db:

            return False

            # Create table            # Create table

    @staticmethod

    def get_student_data_summary():            if db.execute_command(create_table_sql):            if db.execute_command(create_table_sql):

        """Get summary statistics of the imported data"""

        with DatabaseManager() as db:                print("✅ Student grades table created successfully!")                print("✅ Student grades table created successfully!")

            print("\\n📊 STUDENT GRADES DATA SUMMARY")

            print("=" * 50)                        

            

            # Total records            # Create indexes            # Create indexes

            total_records = db.execute_query("SELECT COUNT(*) as total FROM student_grades;")

            if total_records:            for index_sql in create_indexes_sql:            for index_sql in create_indexes_sql:

                print(f"📋 Total Records: {total_records[0]['total']:,}")

                            db.execute_command(index_sql)                db.execute_command(index_sql)

            # Unique students

            unique_students = db.execute_query("SELECT COUNT(DISTINCT aem) as students FROM student_grades;")                        

            if unique_students:

                print(f"👥 Unique Students: {unique_students[0]['students']:,}")            print("✅ Database indexes created successfully!")            print("✅ Database indexes created successfully!")

            

            # Years covered

            year_range = db.execute_query("SELECT MIN(year) as min_year, MAX(year) as max_year FROM student_grades;")

            if year_range:    @staticmethod    @staticmethod

                print(f"📅 Years Covered: {year_range[0]['min_year']} - {year_range[0]['max_year']}")

                def import_student_data():    def import_student_data():

            # Tests available

            tests = db.execute_query("SELECT DISTINCT test FROM student_grades ORDER BY test;")        """Import student data into the database"""        """Import student data into the database"""

            if tests:

                test_list = [test['test'] for test in tests]        try:        try:

                print(f"📝 Available Tests: {', '.join(test_list)}")

            # Load data from file        # Load data from file

    @classmethod

    def run_import(cls):            student_data = StudentDataImporter.load_student_data()        student_data = StudentDataImporter.load_student_data()

        """Main function to run the student data import"""

        print("🚀 STUDENT GRADES DATA IMPORT")                    

        print("=" * 50)

                    # Create table        # Create table

        if cls.import_student_data():

            cls.get_student_data_summary()            StudentDataImporter.create_student_grades_table()        StudentDataImporter.create_student_grades_table()

        else:

            print("❌ Import failed. Please check the error messages above.")                    



            # Insert data        # Insert data

if __name__ == "__main__":

    StudentDataImporter.run_import()            with DatabaseManager() as db:        with DatabaseManager() as db:

                insert_sql = """            insert_sql = """

                INSERT INTO student_grades (aem, test, grade, year)             INSERT INTO student_grades (aem, test, grade, year) 

                VALUES (%s, %s, %s, %s)             VALUES (%s, %s, %s, %s) 

                ON CONFLICT (aem, test, year) DO UPDATE SET            ON CONFLICT (aem, test, year) DO UPDATE SET

                    grade = EXCLUDED.grade,                grade = EXCLUDED.grade,

                    updated_at = CURRENT_TIMESTAMP;                updated_at = CURRENT_TIMESTAMP;

                """            """

                            

                inserted_count = 0            inserted_count = 0

                updated_count = 0            updated_count = 0

                            

                for record in student_data:            for record in student_data:

                    aem = record['AEM']                aem = record['AEM']

                    test = record['Test']                test = record['Test']

                    grade = record['Grade']                grade = record['Grade']

                    year = record['Year']                year = record['Year']

                                    

                    # Check if record exists                # Check if record exists

                    check_sql = "SELECT id FROM student_grades WHERE aem = %s AND test = %s AND year = %s;"                check_sql = "SELECT id FROM student_grades WHERE aem = %s AND test = %s AND year = %s;"

                    existing = db.execute_query(check_sql, (aem, test, year))                existing = db.execute_query(check_sql, (aem, test, year))

                                    

                    if db.execute_command(insert_sql, (aem, test, grade, year)):                if db.execute_command(insert_sql, (aem, test, grade, year)):

                        if existing:                    if existing:

                            updated_count += 1                        updated_count += 1

                        else:                    else:

                            inserted_count += 1                        inserted_count += 1

                            

                print(f"✅ Data import completed!")            print(f"✅ Data import completed!")

                print(f"   📊 New records inserted: {inserted_count}")            print(f"   📊 New records inserted: {inserted_count}")

                print(f"   🔄 Records updated: {updated_count}")            print(f"   🔄 Records updated: {updated_count}")

                print(f"   📋 Total records processed: {len(student_data)}")            print(f"   📋 Total records processed: {len(student_data)}")

                            

            return True        return True

                    

        except Exception as e:    except Exception as e:

            print(f"❌ Error importing data: {e}")        print(f"❌ Error importing data: {e}")

            return False        return False



    @staticmethod    @staticmethod

    def get_student_data_summary():    def get_student_data_summary():

        """Get summary statistics of the imported data"""        """Get summary statistics of the imported data"""

        with DatabaseManager() as db:    with DatabaseManager() as db:

            print("\n📊 STUDENT GRADES DATA SUMMARY")        print("\n📊 STUDENT GRADES DATA SUMMARY")

            print("=" * 50)        print("=" * 50)

                    

            # Total records        # Total records

            total_records = db.execute_query("SELECT COUNT(*) as total FROM student_grades;")        total_records = db.execute_query("SELECT COUNT(*) as total FROM student_grades;")

            if total_records:        if total_records:

                print(f"📋 Total Records: {total_records[0]['total']:,}")            print(f"📋 Total Records: {total_records[0]['total']:,}")

                    

            # Unique students        # Unique students

            unique_students = db.execute_query("SELECT COUNT(DISTINCT aem) as students FROM student_grades;")        unique_students = db.execute_query("SELECT COUNT(DISTINCT aem) as students FROM student_grades;")

            if unique_students:        if unique_students:

                print(f"👥 Unique Students: {unique_students[0]['students']:,}")            print(f"👥 Unique Students: {unique_students[0]['students']:,}")

                    

            # Years covered        # Years covered

            year_range = db.execute_query("SELECT MIN(year) as min_year, MAX(year) as max_year FROM student_grades;")        year_range = db.execute_query("SELECT MIN(year) as min_year, MAX(year) as max_year FROM student_grades;")

            if year_range:        if year_range:

                print(f"📅 Years Covered: {year_range[0]['min_year']} - {year_range[0]['max_year']}")            print(f"📅 Years Covered: {year_range[0]['min_year']} - {year_range[0]['max_year']}")

                    

            # Tests available        # Tests available

            tests = db.execute_query("SELECT DISTINCT test FROM student_grades ORDER BY test;")        tests = db.execute_query("SELECT DISTINCT test FROM student_grades ORDER BY test;")

            if tests:        if tests:

                test_list = [test['test'] for test in tests]            test_list = [test['test'] for test in tests]

                print(f"📝 Available Tests: {', '.join(test_list)}")            print(f"📝 Available Tests: {', '.join(test_list)}")

                    

            # Grade statistics        # Grade statistics

            grade_stats = db.execute_query("""        grade_stats = db.execute_query("""

                SELECT             SELECT 

                    ROUND(AVG(grade), 2) as avg_grade,                ROUND(AVG(grade), 2) as avg_grade,

                    ROUND(MIN(grade), 2) as min_grade,                ROUND(MIN(grade), 2) as min_grade,

                    ROUND(MAX(grade), 2) as max_grade,                ROUND(MAX(grade), 2) as max_grade,

                    ROUND(STDDEV(grade), 2) as std_dev                ROUND(STDDEV(grade), 2) as std_dev

                FROM student_grades;            FROM student_grades;

            """)        """)

            if grade_stats:        if grade_stats:

                stats = grade_stats[0]            stats = grade_stats[0]

                print(f"📈 Grade Statistics:")            print(f"📈 Grade Statistics:")

                print(f"   Average: {stats['avg_grade']}")            print(f"   Average: {stats['avg_grade']}")

                print(f"   Range: {stats['min_grade']} - {stats['max_grade']}")            print(f"   Range: {stats['min_grade']} - {stats['max_grade']}")

                print(f"   Std Dev: {stats['std_dev']}")            print(f"   Std Dev: {stats['std_dev']}")

                    

            # Records per year        # Records per year

            yearly_stats = db.execute_query("""        yearly_stats = db.execute_query("""

                SELECT             SELECT 

                    year,                 year, 

                    COUNT(*) as record_count,                COUNT(*) as record_count,

                    COUNT(DISTINCT aem) as student_count,                COUNT(DISTINCT aem) as student_count,

                    ROUND(AVG(grade), 2) as avg_grade                ROUND(AVG(grade), 2) as avg_grade

                FROM student_grades             FROM student_grades 

                GROUP BY year             GROUP BY year 

                ORDER BY year;            ORDER BY year;

            """)        """)

            if yearly_stats:        if yearly_stats:

                print(f"\n📊 Records by Year:")            print(f"\n📊 Records by Year:")

                for year_data in yearly_stats:            for year_data in yearly_stats:

                    print(f"   {year_data['year']}: {year_data['record_count']} records, "                print(f"   {year_data['year']}: {year_data['record_count']} records, "

                          f"{year_data['student_count']} students, "                      f"{year_data['student_count']} students, "

                          f"avg grade: {year_data['avg_grade']}")                      f"avg grade: {year_data['avg_grade']}")

                    

            # Records per test        # Records per test

            test_stats = db.execute_query("""        test_stats = db.execute_query("""

                SELECT             SELECT 

                    test,                 test, 

                    COUNT(*) as record_count,                COUNT(*) as record_count,

                    ROUND(AVG(grade), 2) as avg_grade,                ROUND(AVG(grade), 2) as avg_grade,

                    ROUND(MIN(grade), 2) as min_grade,                ROUND(MIN(grade), 2) as min_grade,

                    ROUND(MAX(grade), 2) as max_grade                ROUND(MAX(grade), 2) as max_grade

                FROM student_grades             FROM student_grades 

                GROUP BY test             GROUP BY test 

                ORDER BY test;            ORDER BY test;

            """)        """)

            if test_stats:        if test_stats:

                print(f"\n📝 Statistics by Test:")            print(f"\n📝 Statistics by Test:")

                for test_data in test_stats:            for test_data in test_stats:

                    print(f"   {test_data['test']}: {test_data['record_count']} records, "                print(f"   {test_data['test']}: {test_data['record_count']} records, "

                          f"avg: {test_data['avg_grade']}, "                      f"avg: {test_data['avg_grade']}, "

                          f"range: {test_data['min_grade']}-{test_data['max_grade']}")                      f"range: {test_data['min_grade']}-{test_data['max_grade']}")



    @classmethod    @classmethod

    def run_import(cls):    def run_import(cls):

        """Main function to run the student data import"""        """Main function to run the student data import"""

        print("🚀 STUDENT GRADES DATA IMPORT")    print("🚀 STUDENT GRADES DATA IMPORT")

        print("=" * 50)    print("=" * 50)

            

        if cls.import_student_data():    if cls.import_student_data():

            cls.get_student_data_summary()        cls.get_student_data_summary()

                    

            print(f"\n💡 Sample Queries:")        print(f"\n💡 Sample Queries:")

            print(f"   SELECT * FROM student_grades WHERE aem = 6609;")        print(f"   SELECT * FROM student_grades WHERE aem = 6609;")

            print(f"   SELECT * FROM student_grades WHERE test = 'Test 1' AND year = 2024;")        print(f"   SELECT * FROM student_grades WHERE test = 'Test 1' AND year = 2024;")

            print(f"   SELECT aem, AVG(grade) as avg_grade FROM student_grades GROUP BY aem ORDER BY avg_grade DESC;")        print(f"   SELECT aem, AVG(grade) as avg_grade FROM student_grades GROUP BY aem ORDER BY avg_grade DESC;")

            print(f"   SELECT year, test, AVG(grade) as avg_grade FROM student_grades GROUP BY year, test ORDER BY year, test;")        print(f"   SELECT year, test, AVG(grade) as avg_grade FROM student_grades GROUP BY year, test ORDER BY year, test;")

        else:    else:

            print("❌ Import failed. Please check the error messages above.")        print("❌ Import failed. Please check the error messages above.")



if __name__ == "__main__":

if __name__ == "__main__":    StudentDataImporter.run_import()
    StudentDataImporter.run_import()