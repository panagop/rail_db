"""
Advanced database operations and examples
"""
from .connection import DatabaseManager
from datetime import datetime, date
import random

class UserOperations:
    """Class to handle user-related database operations"""
    
    @staticmethod
    def create_additional_tables():
        """Create additional tables to demonstrate relationships"""
        with DatabaseManager() as db:
            # Create departments table
            create_departments = """
            CREATE TABLE IF NOT EXISTS departments (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) UNIQUE NOT NULL,
                budget DECIMAL(12, 2),
                location VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            
            # Create user_activities table for tracking user actions
            create_activities = """
            CREATE TABLE IF NOT EXISTS user_activities (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                activity_type VARCHAR(50) NOT NULL,
                description TEXT,
                activity_date DATE DEFAULT CURRENT_DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            
            # Add department_id to users table if it doesn't exist
            add_department_column = """
            ALTER TABLE users 
            ADD COLUMN IF NOT EXISTS department_id INTEGER REFERENCES departments(id);
            """
            
            db.execute_command(create_departments)
            db.execute_command(create_activities)
            db.execute_command(add_department_column)
            
            print("✅ Additional tables created successfully!")
    
    @staticmethod
    def seed_departments():
        """Add sample departments"""
        departments = [
            ("Engineering", 500000.00, "San Francisco"),
            ("Marketing", 250000.00, "New York"),
            ("Sales", 300000.00, "Chicago"),
            ("HR", 150000.00, "Austin"),
            ("Finance", 200000.00, "Boston")
        ]
        
        with DatabaseManager() as db:
            insert_dept = """
            INSERT INTO departments (name, budget, location) 
            VALUES (%s, %s, %s) 
            ON CONFLICT (name) DO NOTHING;
            """
            
            for dept in departments:
                db.execute_command(insert_dept, dept)
            
            print("✅ Departments seeded successfully!")
    
    @staticmethod
    def assign_users_to_departments():
        """Randomly assign users to departments"""
        with DatabaseManager() as db:
            # Get all users and departments
            users = db.execute_query("SELECT id FROM users;")
            departments = db.execute_query("SELECT id FROM departments;")
            
            if users and departments:
                dept_ids = [dept['id'] for dept in departments]
                
                for user in users:
                    # Randomly assign department
                    dept_id = random.choice(dept_ids)
                    update_user = "UPDATE users SET department_id = %s WHERE id = %s;"
                    db.execute_command(update_user, (dept_id, user['id']))
                
                print("✅ Users assigned to departments!")
    
    @staticmethod
    def add_user_activities():
        """Add sample user activities"""
        activities = [
            "Login", "Updated Profile", "Created Report", "Attended Meeting", 
            "Submitted Task", "Reviewed Document", "Posted Update", "Joined Project"
        ]
        
        with DatabaseManager() as db:
            users = db.execute_query("SELECT id FROM users;")
            
            if users:
                insert_activity = """
                INSERT INTO user_activities (user_id, activity_type, description, activity_date) 
                VALUES (%s, %s, %s, %s);
                """
                
                for user in users:
                    # Add 2-5 random activities per user
                    num_activities = random.randint(2, 5)
                    for _ in range(num_activities):
                        activity = random.choice(activities)
                        description = f"User performed: {activity}"
                        # Random date in the last 30 days
                        days_ago = random.randint(0, 30)
                        activity_date = date.today().replace(day=max(1, date.today().day - days_ago))
                        
                        db.execute_command(insert_activity, (
                            user['id'], activity, description, activity_date
                        ))
                
                print("✅ User activities added!")
    
    @staticmethod
    def generate_reports():
        """Generate various analytical reports"""
        with DatabaseManager() as db:
            print("\n📈 COMPREHENSIVE DATABASE REPORTS")
            print("=" * 60)
            
            # 1. Department Summary Report
            dept_report = db.execute_query("""
                SELECT 
                    d.name as department,
                    d.location,
                    d.budget,
                    COUNT(u.id) as employee_count,
                    AVG(u.salary) as avg_salary,
                    MAX(u.salary) as max_salary,
                    MIN(u.salary) as min_salary
                FROM departments d
                LEFT JOIN users u ON d.id = u.department_id AND u.is_active = TRUE
                GROUP BY d.id, d.name, d.location, d.budget
                ORDER BY employee_count DESC;
            """)
            
            if dept_report:
                print("\n🏢 DEPARTMENT SUMMARY:")
                print("-" * 40)
                for dept in dept_report:
                    print(f"📍 {dept['department']} ({dept['location']})")
                    print(f"   Budget: ${dept['budget']:,.2f}")
                    print(f"   Employees: {dept['employee_count']}")
                    if dept['avg_salary']:
                        print(f"   Avg Salary: ${float(dept['avg_salary']):,.2f}")
                        print(f"   Salary Range: ${float(dept['min_salary']):,.2f} - ${float(dept['max_salary']):,.2f}")
                    print()
            
            # 2. Activity Summary Report
            activity_report = db.execute_query("""
                SELECT 
                    activity_type,
                    COUNT(*) as total_activities,
                    COUNT(DISTINCT user_id) as unique_users,
                    MAX(activity_date) as last_activity
                FROM user_activities
                GROUP BY activity_type
                ORDER BY total_activities DESC;
            """)
            
            if activity_report:
                print("📊 ACTIVITY SUMMARY:")
                print("-" * 40)
                for activity in activity_report:
                    print(f"🔹 {activity['activity_type']}")
                    print(f"   Total: {activity['total_activities']} activities")
                    print(f"   Users: {activity['unique_users']} unique users")
                    print(f"   Last: {activity['last_activity']}")
                    print()
            
            # 3. User Performance Report (based on activities)
            user_performance = db.execute_query("""
                SELECT 
                    u.full_name,
                    u.username,
                    d.name as department,
                    COUNT(ua.id) as total_activities,
                    COUNT(DISTINCT ua.activity_type) as activity_types,
                    MAX(ua.activity_date) as last_active
                FROM users u
                LEFT JOIN user_activities ua ON u.id = ua.user_id
                LEFT JOIN departments d ON u.department_id = d.id
                WHERE u.is_active = TRUE
                GROUP BY u.id, u.full_name, u.username, d.name
                ORDER BY total_activities DESC
                LIMIT 5;
            """)
            
            if user_performance:
                print("🏆 TOP ACTIVE USERS:")
                print("-" * 40)
                for i, user in enumerate(user_performance, 1):
                    print(f"{i}. {user['full_name']} (@{user['username']})")
                    print(f"   Department: {user['department'] or 'Unassigned'}")
                    print(f"   Activities: {user['total_activities']} ({user['activity_types']} types)")
                    print(f"   Last Active: {user['last_active']}")
                    print()

def run_advanced_demo():
    """Run the advanced database demonstration"""
    print("🚀 ADVANCED DATABASE OPERATIONS DEMO")
    print("=" * 60)
    
    try:
        # Create additional tables
        UserOperations.create_additional_tables()
        
        # Seed departments
        UserOperations.seed_departments()
        
        # Assign users to departments
        UserOperations.assign_users_to_departments()
        
        # Add user activities
        UserOperations.add_user_activities()
        
        # Generate comprehensive reports
        UserOperations.generate_reports()
        
        print("\n✨ Advanced demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in advanced demo: {e}")

if __name__ == "__main__":
    run_advanced_demo()