# Import the SQL functions from our SQL engine
from src.sql_engine import (
    answer_sql_question,
    detect_sql_intent
)

# Import the RAG retrieval function
from src.rag_engine import retrieve

# Import the Gemini answer function
from src.llm_engine import generate_answer


# Define words and phrases that indicate a company-document question
RAG_KEYWORDS = [
    "policy",
    "policies",
    "refund",
    "return",
    "cancel after shipment",
    "cancel after shipping",
    "after shipment",
    "after shipping",
    "seller responsibility",
    "seller responsibilities",
    "customer support",
    "support policy",
    "delivery policy",
    "business priorities",
    "company policy"
]


# Decide whether a question needs SQL, RAG, or both
def route_question(question):

    # Convert the question to lowercase
    question_lower = question.lower()

    # Check whether the question matches a SQL business intent
    has_sql = detect_sql_intent(question) is not None

    # Check whether the question contains a RAG-related keyword
    has_rag = any(
        keyword in question_lower
        for keyword in RAG_KEYWORDS
    )

    # Use BOTH when both sources are needed
    if has_sql and has_rag:
        return "BOTH"

    # Use SQL when only business data is needed
    if has_sql:
        return "SQL"

    # Use RAG when only company documents are needed
    if has_rag:
        return "RAG"

    # Use UNKNOWN when no route matches
    return "UNKNOWN"


# Answer a question using company documents
def answer_rag_question(question):

    # Retrieve the most relevant document chunks
    results = retrieve(
        question,
        top_k=3
    )

    # Combine the retrieved chunks into one context
    context = "\n\n".join(
        result["chunk"].page_content
        for result in results
    )

    # Create a prompt that restricts Gemini to our documents
    prompt = f"""
You are Mercato's AI Business Analyst.

Use ONLY the company context provided below.

Rules:
- Do not invent Mercato policies or facts.
- Do not use outside knowledge.
- If the documents do not contain enough information, say so.
- Give a concise and professional answer.

Company Context:
{context}

User Question:
{question}
"""

    # Ask Gemini to generate the answer
    answer = generate_answer(prompt)

    # Return the answer and source documents
    return {
        "answer": answer,
        "sources": results
    }


# Answer a question using both business data and company documents
def answer_both_question(question):

    # Get the numerical result from SQLite
    sql_result = answer_sql_question(question)

    # Retrieve relevant company-document chunks
    rag_results = retrieve(
        question,
        top_k=3
    )

    # Combine the document chunks
    context = "\n\n".join(
        result["chunk"].page_content
        for result in rag_results
    )

    # Convert the SQL result into readable text
    sql_data = sql_result["result"].to_string(
        index=False
    )

    # Create a prompt containing both sources
    prompt = f"""
You are Mercato's AI Business Analyst.

Answer the user's question using the business data
and company documentation provided below.

BUSINESS DATA FROM SQLITE:
{sql_data}

COMPANY DOCUMENTATION:
{context}

USER QUESTION:
{question}

Rules:
- Use SQLite results for numerical claims.
- Use company documentation for policy claims.
- Do not invent numbers.
- Do not invent Mercato policies.
- Clearly distinguish business data from company policy.
- If either source lacks enough information, say so.
- Give a concise professional answer.
"""

    # Ask Gemini to combine both sources
    answer = generate_answer(prompt)

    # Return the combined result
    return {
        "answer": answer,
        "sql_result": sql_result,
        "rag_sources": rag_results
    }


# Answer any supported business question
def answer_business_question(question):

    # Determine which source is needed
    route = route_question(question)


    # Handle a SQL question
    if route == "SQL":

        # Get the trusted business result from SQLite
        result = answer_sql_question(question)

        # Convert the SQL result into readable text
        sql_data = result["result"].to_string(
            index=False
        )

        # Ask Gemini to explain the trusted SQL result
        prompt = f"""
You are Mercato's AI Business Analyst.

Answer the user's question using ONLY the SQL result provided below.

SQL RESULT:
{sql_data}

USER QUESTION:
{question}

Rules:
- Do not change or invent any numbers.
- Use the SQL result as the source of truth.
- Give a concise professional business answer.
- Clearly state the relevant metric and value.
- Do not mention information that is not supported by the SQL result.
"""

        # Ask Gemini to generate the natural-language answer
        answer = generate_answer(prompt)

        # Return the final SQL response
        return {
            "route": "SQL",
            "answer": answer,
            "details": result
        }


    # Handle a company-document question
    if route == "RAG":

        # Generate the RAG answer
        result = answer_rag_question(question)

        # Return the final response
        return {
            "route": "RAG",
            "answer": result["answer"],
            "details": result
        }


    # Handle a question requiring both sources
    if route == "BOTH":

        # Generate the combined answer
        result = answer_both_question(question)

        # Return the final response
        return {
            "route": "BOTH",
            "answer": result["answer"],
            "details": result
        }


    # Handle unsupported questions
    return {
        "route": "UNKNOWN",
        "answer": (
            "I could not determine which business data "
            "or company document is needed to answer this question."
        ),
        "details": None
    }