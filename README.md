
# 🛒 E-Commerce AI Business Analyst

An end-to-end **E-Commerce Analytics + AI Business Analyst** platform built using real-world e-commerce data, SQL analytics, Power BI, RAG, FAISS, Gemini, and Streamlit.

The system combines **structured business data** with **company policy documents** so users can ask business questions in natural language and receive answers from the appropriate data source.

---

## 🚀 Project Overview

The **E-Commerce AI Business Analyst** analyzes the Brazilian Olist e-commerce dataset and combines traditional business intelligence with Generative AI.

The application can answer questions such as:

- What are the total sales?
- What were the total sales in 2018?
- What is the average delivery time?
- Which product categories generate the most sales?
- What is the repeat customer rate?
- Can a customer cancel an order after shipment?
- What does the refund policy say?
- What is the cancellation rate and what does the refund policy say?

The system automatically determines whether a question requires:

- **SQL** → business data
- **RAG** → company documents
- **BOTH** → business data + company documents

---

## 🏗️ Architecture

```text
                 ┌──────────────────────┐
                 │   Olist E-Commerce   │
                 │       Dataset        │
                 └──────────┬───────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │ Python / Pandas  │
                  │ Data Cleaning    │
                  │ & EDA            │
                  └────────┬─────────┘
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
      ┌──────────────┐           ┌──────────────┐
      │   SQLite     │           │ Company Docs │
      │  Business    │           │   Markdown   │
      │    Data      │           │   Documents  │
      └──────┬───────┘           └──────┬───────┘
             │                          │
             │                          ▼
             │                    ┌──────────────┐
             │                    │ Sentence     │
             │                    │ Transformers │
             │                    └──────┬───────┘
             │                           │
             │                           ▼
             │                    ┌──────────────┐
             │                    │    FAISS     │
             │                    │ Vector Store │
             │                    └──────┬───────┘
             │                           │
             └─────────────┬─────────────┘
                           ▼
                  ┌──────────────────┐
                  │ Question Router  │
                  │ SQL / RAG / BOTH │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │      Gemini      │
                  │   LLM Response   │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │    Streamlit     │
                  │   Chat Interface │
                  └──────────────────┘
````

---

## 📊 Dataset

The project uses the **Brazilian Olist e-commerce dataset**, consisting of 9 interconnected datasets.

### Dataset Tables

| Dataset              | Description                           |
| -------------------- | ------------------------------------- |
| Customers            | Customer information                  |
| Orders               | Order lifecycle and delivery dates    |
| Order Items          | Products purchased within orders      |
| Payments             | Payment transactions                  |
| Reviews              | Customer review scores and comments   |
| Products             | Product information                   |
| Sellers              | Seller information                    |
| Geolocation          | Brazilian ZIP-code geographic data    |
| Category Translation | Portuguese → English category mapping |

The dataset contains approximately **99K orders** and **100K customers**, along with product, seller, payment, review, and delivery information.

---

## 🧹 Data Processing

Python and Pandas were used to:

* Inspect all 9 datasets
* Validate row counts and duplicates
* Analyze missing values
* Standardize column names
* Convert date columns
* Validate delivery dates
* Create cleaned datasets
* Perform exploratory data analysis
* Prepare data for SQLite and Power BI

The raw dataset is kept separate from processed data.

---

## 📈 Business Analytics

SQL and Power BI were used to calculate and analyze important business KPIs.

### Key KPIs

* Total Orders
* Total Customers
* Total Sales
* Average Order Value
* Repeat Customers
* Repeat Customer Rate
* Average Delivery Time
* Late Delivery Rate
* Average Review Score
* Cancellation Rate

### Power BI Dashboard

The dashboard includes analysis of:

* Monthly sales trends
* Top product categories
* Sales by customer state
* Seller performance
* Payment methods
* Customer review scores
* Delivery performance
* Repeat purchase behavior
* Order status distribution

---

## 💡 Key Business Insights

### Customer Retention

Only approximately **3.12% of unique customers** placed more than one order.

This indicates a significant opportunity to improve customer retention through:

* Personalized recommendations
* Loyalty programs
* Targeted offers
* Post-purchase engagement

### Delivery Performance

Average delivery time varies across months.

Longer delivery times are associated with lower customer review scores, with an observed correlation of approximately **-0.334**.

This suggests that delivery performance is an important factor to investigate when improving customer satisfaction.

### Seller Ecosystem

The marketplace has a relatively diversified seller ecosystem.

The top 10 sellers contribute approximately **13.27% of total product sales**.

### Order Performance

The majority of orders were successfully delivered, while a smaller percentage were canceled or remained in other processing states.

The observed cancellation rate is approximately **0.63%**.

---

## 🤖 AI Business Analyst

The project extends traditional BI with a natural-language AI interface.

Instead of requiring users to write SQL or search through company documents manually, users can ask questions in natural language.

### Example

**User:**

> What were the total sales in 2018?

**System:**

```text
Question
   ↓
SQL Intent Detection
   ↓
SQLite
   ↓
Gemini
   ↓
Natural Language Answer
```

Another example:

**User:**

> Can a customer cancel an order after shipment?

The system routes the question to the company-document knowledge base:

```text
Question
   ↓
RAG Detection
   ↓
FAISS Retrieval
   ↓
Relevant Company Documents
   ↓
Gemini
   ↓
Natural Language Answer
```

---

## 🔀 Intelligent Question Routing

The question router determines the appropriate information source.

| Route | Used For                                              |
| ----- | ----------------------------------------------------- |
| SQL   | Business metrics and structured data                  |
| RAG   | Company policies and documents                        |
| BOTH  | Questions requiring business data + company knowledge |

This allows the application to combine **Business Intelligence** and **Generative AI** in a single workflow.

---

## 📚 RAG System

The RAG pipeline uses fictional Mercato company documents covering:

* Company overview
* Refund policy
* Delivery policy
* Seller policy
* Customer support policy
* Business insights

### RAG Pipeline

```text
Company Documents
       ↓
Text Chunking
       ↓
Sentence Transformers
       ↓
Embeddings
       ↓
FAISS
       ↓
Semantic Retrieval
       ↓
Relevant Context
       ↓
Gemini
       ↓
Answer
```

Embedding model:

```text
all-MiniLM-L6-v2
```

Vector database:

```text
FAISS
```

---

## 🧠 Technology Stack

### Data Analytics

* Python
* Pandas
* NumPy
* Excel

### Database & SQL

* SQLite
* SQL
* DB Browser for SQLite

### Business Intelligence

* Power BI
* DAX
* Plotly

### Generative AI

* LangChain
* Sentence Transformers
* FAISS
* Gemini API
* Retrieval-Augmented Generation (RAG)

### Application

* Streamlit

### Development Tools

* VS Code
* Git
* GitHub
* Jupyter Notebook

---

## 📁 Project Structure

```text
ecommerce-ai-business-analyst/
│
├── Notebooks/
│   └── notebooks/
│       ├── 01_data_understanding.ipynb
│       ├── 02_create_database.ipynb
│       ├── 03_eda.ipynb
│       ├── 03_rag_setup.ipynb
│       ├── 04_question_router.ipynb
│       └── 05_testing.ipynb
│
├── PowerBI/
│   └── E-Commerce Business Analytics Dashboard.pbix
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── business_insights.md
│   ├── company_overview.md
│   ├── customer_support_policy.md
│   ├── delivery_policy.md
│   ├── refund_policy.md
│   └── seller_policy.md
│
├── sql/
│   └── kpi_queries.sql
│
├── src/
│   ├── config.py
│   ├── llm_engine.py
│   ├── rag_engine.py
│   ├── router.py
│   └── sql_engine.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Ayushisinhaxvii/ecommerce-ai-business-analyst.git
```

### 2. Navigate to the project

```bash
cd ecommerce-ai-business-analyst
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Gemini

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=your_available_gemini_model
```

### 7. Run the Streamlit application

```bash
python -m streamlit run app.py
```

---

## 🔐 Security

API keys and environment variables are stored in `.env`.

The `.env` file is excluded from Git using `.gitignore`.

Never commit API keys or other secrets to GitHub.

---

## 📌 Project Status

### Completed

* [x] Data understanding
* [x] Excel exploration
* [x] Python/Pandas cleaning
* [x] SQLite database
* [x] SQL KPI analysis
* [x] Python EDA
* [x] Power BI dashboard
* [x] Business insights
* [x] Company knowledge documents
* [x] RAG pipeline
* [x] FAISS vector search
* [x] Gemini integration
* [x] SQL/RAG/BOTH question routing
* [x] Streamlit application
* [x] Testing
* [x] Git/GitHub setup

### Future Improvements

* [ ] Improve natural-language-to-SQL capabilities
* [ ] Add more advanced business question handling
* [ ] Improve RAG evaluation
* [ ] Add additional dashboard insights
* [ ] Deploy the Streamlit application
* [ ] Add automated testing
* [ ] Improve production error handling

---

## 👩‍💻 Author

**Ayushi Sinha**

GitHub:
[https://github.com/Ayushisinhaxvii](https://github.com/Ayushisinhaxvii)

````

### Step 3 — Save

Press:

```text
Ctrl + S
````

---
