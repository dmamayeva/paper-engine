import os
import psycopg2
from psycopg2 import sql, errors
from psycopg2.extras import DictCursor
from datetime import datetime
from zoneinfo import ZoneInfo

tz = ZoneInfo("Europe/Berlin")

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        database=os.getenv("POSTGRES_DB", "course_assisstant"),
        user=os.getenv("POSTGRES_USER", "your_username"),
        password=os.getenv("POSTGRES_PASSWORD", "your_password"),
    )

def execute_query(conn, query, params=None, fetch=False):
    with conn.cursor(cursor_factory=DictCursor) as cur:
        try:
            cur.execute(query, params)
            conn.commit()
            if fetch:
                return [dict(row) for row in cur.fetchall()]
        except errors.UndefinedTable:
            conn.rollback()
            create_tables(conn)
            cur.execute(query, params)
            conn.commit()
            if fetch:
                return [dict(row) for row in cur.fetchall()]
        except errors.ForeignKeyViolation as e:
            conn.rollback()
            print(f"Foreign key violation: {e}")
            raise
        except Exception as e:
            conn.rollback()
            print(f"Error executing query: {e}")
            raise

def create_tables(conn):
    queries = [
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            response_time FLOAT NOT NULL,
            relevance TEXT NOT NULL,
            relevance_explanation TEXT NOT NULL,
            prompt_tokens INTEGER NOT NULL,
            completion_tokens INTEGER NOT NULL,
            total_tokens INTEGER NOT NULL,
            eval_prompt_tokens INTEGER NOT NULL,
            eval_completion_tokens INTEGER NOT NULL,
            eval_total_tokens INTEGER NOT NULL,
            openai_cost FLOAT NOT NULL,
            timestamp TIMESTAMP WITH TIME ZONE NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id SERIAL PRIMARY KEY,
            conversation_id TEXT REFERENCES conversations(id),
            feedback INTEGER NOT NULL,
            timestamp TIMESTAMP WITH TIME ZONE NOT NULL
        )
        """
    ]
    for query in queries:
        execute_query(conn, query)

def save_conversation(conversation_id, question, answer_data, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now(tz)

    query = """
    INSERT INTO conversations 
    (id, question, answer, response_time, relevance, 
    relevance_explanation, prompt_tokens, completion_tokens, total_tokens, 
    eval_prompt_tokens, eval_completion_tokens, eval_total_tokens, openai_cost, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, COALESCE(%s, CURRENT_TIMESTAMP))
    """
    params = (
        conversation_id,
        question,
        answer_data["answer"],
        answer_data["response_time"],
        answer_data["relevance"],
        answer_data["relevance_explanation"],
        answer_data["prompt_tokens"],
        answer_data["completion_tokens"],
        answer_data["total_tokens"],
        answer_data["eval_prompt_tokens"],
        answer_data["eval_completion_tokens"],
        answer_data["eval_total_tokens"],
        answer_data["openai_cost"],
        timestamp,
    )

    with get_db_connection() as conn:
        execute_query(conn, query, params)

def save_feedback(conversation_id, feedback, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now(tz)

    # First, check if the conversation exists
    check_query = "SELECT id FROM conversations WHERE id = %s"
    
    with get_db_connection() as conn:
        result = execute_query(conn, check_query, (conversation_id,), fetch=True)
        if not result:
            print(f"Conversation with id {conversation_id} does not exist.")
            return

        query = "INSERT INTO feedback (conversation_id, feedback, timestamp) VALUES (%s, %s, COALESCE(%s, CURRENT_TIMESTAMP))"
        params = (conversation_id, feedback, timestamp)
        execute_query(conn, query, params)

def get_recent_conversations(limit=5, relevance=None):
    query = """
        SELECT c.id, c.question, c.answer, c.relevance, f.feedback
        FROM conversations c
        LEFT JOIN feedback f ON c.id = f.conversation_id
    """
    if relevance:
        query += " WHERE c.relevance = %s"
    query += " ORDER BY c.timestamp DESC LIMIT %s"

    params = (relevance, limit) if relevance else (limit,)

    with get_db_connection() as conn:
        return execute_query(conn, query, params, fetch=True)

def get_feedback_stats():
    query = """
        SELECT 
            COALESCE(SUM(CASE WHEN feedback > 0 THEN 1 ELSE 0 END), 0) as thumbs_up,
            COALESCE(SUM(CASE WHEN feedback < 0 THEN 1 ELSE 0 END), 0) as thumbs_down
        FROM feedback
    """

    with get_db_connection() as conn:
        result = execute_query(conn, query, fetch=True)
        if result and len(result) > 0:
            return result[0]  # This should now be a dictionary with 'thumbs_up' and 'thumbs_down' keys
        return {'thumbs_up': 0, 'thumbs_down': 0}
