


#import DictCursor to get results as dictionary
from psycopg2.extras import DictCursor
# db connection to create db cursor to run queries
from app.db.checkDbConection import get_db_connection
# import logger to log messages
from app.utils.logger import log_message

#fuction to get all templates
def get_all_templates():

    #logs
    with log_message("DATABASE", "#0000F9", "SELECT id, title, language, description, created_at FROM course_templates"):
        #get db connection
        conn = get_db_connection()
        # create db cursor
        cursor = conn.cursor(cursor_factory=DictCursor)
        # execute the query
        cursor.execute("SELECT id, title, language, description, created_at FROM course_templates")
        #fetch all the results
        rows = cursor.fetchall()
        #close the cursor
        cursor.close()
        #close the connection
        conn.close()
        #return the results
        return rows

#fuction to get a single template by id 
def select_template_by_id(template_id: str):
    
    #logs
    with log_message("DATABASE", "#0000F9", f"SELECT * FROM course_templates WHERE id = '{template_id}'"):
        #get db connection
        conn = get_db_connection()
        # create db cursor
        cursor = conn.cursor(cursor_factory=DictCursor)
        # execute the query
        cursor.execute("SELECT * FROM course_templates WHERE id = %s", (template_id,))
        #fetch all the results
        row = cursor.fetchone()
        #close the cursor
        cursor.close()
        #close the connection
        conn.close()
        #return the results
        return row
    
