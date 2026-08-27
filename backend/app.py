from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Union
import chromadb
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

# Custom dummy embedding function to prevent external downloads/network calls on Render
class CustomLightweightEmbedding(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        # Returns a simple deterministic vector based on document length/char codes
        embeddings = []
        for text in input:
            vec = [float(ord(c)) for c in text[:16].ljust(16, ' ')]
            embeddings.append(vec)
        return embeddings

DB_DIR = "./course_db"
embedding_fn = CustomLightweightEmbedding()
client = chromadb.PersistentClient(path=DB_DIR)

collection = client.get_or_create_collection(
    name="career_catalog",
    embedding_function=embedding_fn
)

def seed_catalog():
    """Populates the vector store if records do not exist."""
    existing_ids = collection.get()["ids"]
    
    initial_courses = [
        ("c1", "Applied Data Science & Machine Learning", "Statistical modeling, predictive algorithms, data preprocessing, feature engineering, Python, Pandas, and SQL database manipulation.", "Data & AI"),
        ("c2", "Quantitative Analysis & Financial Econometrics", "Advanced mathematical modeling, time-series forecasting, GARCH modeling, macro-financial risk evaluation, and economic data analysis.", "Quantitative Finance"),
        ("c3", "Data Engineering & Pipeline Architecture", "Scalable data pipelines, ETL automation, data warehousing, Apache Spark, Airflow, and cloud database infrastructure.", "Data Infrastructure"),
        ("c4", "AI & RAG Systems Engineering", "LLM integration, Retrieval-Augmented Generation, vector database indexing, AI agents, LangChain, and FastAPI deployment.", "Artificial Intelligence"),
        ("c5", "Full-Stack Web Development", "End-to-end web applications, React frontend interfaces, Node.js REST API architecture, HTML/CSS, and database management.", "Software Engineering"),
        ("c6", "Cloud Computing & DevOps Engineering", "Infrastructure automation, CI/CD pipelines, containerization with Docker, Kubernetes, and cloud system architecture.", "Cloud & Infrastructure"),
        ("c7", "UI/UX Design & Product Strategy", "User research, wireframing, Figma prototyping, visual interaction design, information architecture, and usability testing.", "Product & Design"),
        ("c8", "Cybersecurity & Threat Analysis", "Network defense, vulnerability assessments, security monitoring, threat detection, penetration testing, and incident response.", "Cybersecurity")
    ]
    
    for c_id, title, desc, track in initial_courses:
        if c_id not in existing_ids:
            collection.add(
                ids=[c_id],
                documents=[f"Course: {title}. Career Track: {track}. Summary: {desc}"],
                metadatas=[{"title": title, "track": track}]
            )
    print("🚀 Catalog successfully loaded into ChromaDB!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_catalog()
    yield

app = FastAPI(
    title="Career Roadmap & Recommendation Vector API",
    description="Vector search backend for matching student goals to tech career tracks and generating structured step-by-step career roadmaps.",
    version="1.1.0",
    lifespan=lifespan
)

ROADMAP_DATA: Dict[str, dict] = {
    "c1": {
        "career_track": "Data & AI",
        "title": "Applied Data Science & Machine Learning",
        "estimated_duration": "4 - 6 Months",
        "phases": [
            {
                "phase": "Phase 1: Foundations",
                "focus": "Python, Data Manipulation & Exploratory Data Analysis",
                "key_skills": ["Python", "Pandas", "NumPy", "SQL Basics", "Data Cleaning"],
                "milestone": "Perform EDA on real-world tabular datasets and present statistical summaries."
            },
            {
                "phase": "Phase 2: Core Machine Learning",
                "focus": "Supervised & Unsupervised Model Development",
                "key_skills": ["Scikit-Learn", "Regression & Classification", "Feature Engineering", "Model Evaluation"],
                "milestone": "Build, evaluate, and tune cross-validated predictive ML models."
            },
            {
                "phase": "Phase 3: Advanced Capstone & Deployment",
                "focus": "Model Interpretability, API Deployment & Portfolio",
                "key_skills": ["SHAP / LIME", "FastAPI / Streamlit", "Docker Basics", "GitHub Documentation"],
                "milestone": "Deploy a machine learning web app containerized with Docker."
            }
        ]
    },
    "c2": {
        "career_track": "Quantitative Finance",
        "title": "Quantitative Analysis & Financial Econometrics",
        "estimated_duration": "5 - 7 Months",
        "phases": [
            {
                "phase": "Phase 1: Foundations",
                "focus": "Probability, Linear Algebra & Econometric Theory",
                "key_skills": ["Statistics", "Linear Models", "Time Series Basics", "Python/R"],
                "milestone": "Analyze structural breaks, stationary tests, and cointegration in financial data."
            },
            {
                "phase": "Phase 2: Advanced Volatility & Forecasting",
                "focus": "GARCH Models, Volatility Dynamics & Risk Evaluation",
                "key_skills": ["ARCH/GARCH", "Value at Risk (VaR)", "Exchange Rate Modeling", "Forecasting"],
                "milestone": "Construct time-series econometric models to forecast market volatility."
            },
            {
                "phase": "Phase 3: Quantitative Portfolio & Strategy",
                "focus": "Algorithmic Backtesting & Macro Risk Reports",
                "key_skills": ["Backtesting Frameworks", "Portfolio Optimization", "Research Paper Deposition"],
                "milestone": "Publish an empirical econometric research paper or backtested trading strategy."
            }
        ]
    },
    "c3": {
        "career_track": "Data Infrastructure",
        "title": "Data Engineering & Pipeline Architecture",
        "estimated_duration": "4 - 6 Months",
        "phases": [
            {
                "phase": "Phase 1: Foundations",
                "focus": "Advanced SQL, Relational Modeling & Scripting",
                "key_skills": ["Complex SQL Queries", "Database Design", "Python Scripting", "Data Warehousing"],
                "milestone": "Design an optimized relational schema and automated data extraction scripts."
            },
            {
                "phase": "Phase 2: Orchestration & ETL Processing",
                "focus": "Batch & Stream Data Processing",
                "key_skills": ["Apache Airflow", "Apache Spark", "ETL Pipelines", "Docker"],
                "milestone": "Build automated ETL pipelines triggered by Airflow DAGs."
            },
            {
                "phase": "Phase 3: Cloud & Enterprise Infrastructure",
                "focus": "Cloud Warehousing & Big Data Architecture",
                "key_skills": ["Snowflake / BigQuery", "AWS / GCP Data Services", "CI/CD"],
                "milestone": "Deploy an enterprise-grade cloud data pipeline with live monitoring."
            }
        ]
    },
    "c4": {
        "career_track": "Artificial Intelligence",
        "title": "AI & RAG Systems Engineering",
        "estimated_duration": "3 - 5 Months",
        "phases": [
            {
                "phase": "Phase 1: Foundations",
                "focus": "Vector Embeddings & API Ingestion",
                "key_skills": ["Python", "Hugging Face Embeddings", "ChromaDB / Pinecone", "FastAPI"],
                "milestone": "Build a local vector similarity search engine over custom documents."
            },
            {
                "phase": "Phase 2: RAG Pipeline Design",
                "focus": "Retrieval-Augmented Generation & Prompt Engineering",
                "key_skills": ["LangChain / LlamaIndex", "Context Retrieval", "Chunking Strategies", "LLM APIs"],
                "milestone": "Create an AI Q&A system with document grounding and citation tracking."
            },
            {
                "phase": "Phase 3: Autonomous AI Agents & Production",
                "focus": "Tool Calling, Memory Systems & Microservice Deployment",
                "key_skills": ["AI Agents", "Function Calling", "Docker", "Cloud Microservices"],
                "milestone": "Deploy a multi-agent conversational assistant as a scalable REST API."
            }
        ]
    },
    "c5": {
        "career_track": "Software Engineering",
        "title": "Full-Stack Web Development",
        "estimated_duration": "4 - 6 Months",
        "phases": [
            {
                "phase": "Phase 1: Frontend Fundamentals",
                "focus": "UI Development & Responsive Design",
                "key_skills": ["HTML5/CSS3", "JavaScript (ES6+)", "Responsive UI", "DOM Manipulation"],
                "milestone": "Build responsive frontend interfaces connected to external public APIs."
            },
            {
                "phase": "Phase 2: Backend & Database Engineering",
                "focus": "RESTful API Architecture & Data Persistence",
                "key_skills": ["Node.js / Express", "Python Flask / FastAPI", "PostgreSQL / MongoDB"],
                "milestone": "Develop secure backend APIs with user authentication and database models."
            },
            {
                "phase": "Phase 3: Full-Stack Integration & Cloud Hosting",
                "focus": "State Management, Integration & Continuous Deployment",
                "key_skills": ["React", "State Management", "Docker", "Render / Vercel"],
                "milestone": "Launch a full-stack web application with complete database integration."
            }
        ]
    },
    "c6": {
        "career_track": "Cloud & Infrastructure",
        "title": "Cloud Computing & DevOps Engineering",
        "estimated_duration": "4 - 6 Months",
        "phases": [
            {
                "phase": "Phase 1: Systems & Networking",
                "focus": "Linux Administration & Virtualization",
                "key_skills": ["Linux Shell", "Bash Scripting", "Networking Protocols", "Git"],
                "milestone": "Automate server configuration and system monitoring scripts."
            },
            {
                "phase": "Phase 2: Containerization & Cloud Infrastructure",
                "focus": "Docker Orchestration & Cloud Services",
                "key_skills": ["Docker", "Kubernetes", "AWS / Azure Basics", "Terraform"],
                "milestone": "Containerize multi-container applications and manage deployment manifests."
            },
            {
                "phase": "Phase 3: CI/CD & Production Operations",
                "focus": "Automated Pipelines & System Reliability",
                "key_skills": ["GitHub Actions", "CI/CD Automation", "Prometheus / Grafana"],
                "milestone": "Build automated CI/CD deployment pipelines with real-time health alerts."
            }
        ]
    },
    "c7": {
        "career_track": "Product & Design",
        "title": "UI/UX Design & Product Strategy",
        "estimated_duration": "3 - 5 Months",
        "phases": [
            {
                "phase": "Phase 1: User Research & Wireframing",
                "focus": "Information Architecture & User Needs Analysis",
                "key_skills": ["User Persona Mapping", "Wireframing", "Figma Fundamentals"],
                "milestone": "Produce wireframes and journey maps based on user research."
            },
            {
                "phase": "Phase 2: High-Fidelity Prototyping",
                "focus": "Design Systems & Visual Interaction",
                "key_skills": ["Interactive Prototyping", "Design Systems", "UI Components"],
                "milestone": "Create clickable high-fidelity interactive prototypes in Figma."
            },
            {
                "phase": "Phase 3: Usability Testing & Hand-Off",
                "focus": "Design Validation & Developer Handoff",
                "key_skills": ["Usability Testing", "A/B Testing", "Developer Spec Documentation"],
                "milestone": "Publish a comprehensive UI/UX case study ready for portfolio review."
            }
        ]
    },
    "c8": {
        "career_track": "Cybersecurity",
        "title": "Cybersecurity & Threat Analysis",
        "estimated_duration": "5 - 7 Months",
        "phases": [
            {
                "phase": "Phase 1: Security Fundamentals",
                "focus": "Network Architecture & Operating System Defense",
                "key_skills": ["TCP/IP Networking", "Linux Security", "Cryptography Basics"],
                "milestone": "Perform network packet analysis and vulnerability identification."
            },
            {
                "phase": "Phase 2: Defensive Operations & SIEM",
                "focus": "Threat Detection & Incident Response",
                "key_skills": ["SIEM Platforms", "Log Analysis", "Threat Hunting", "Incident Playbooks"],
                "milestone": "Analyze intrusion logs and configure automated threat alerts."
            },
            {
                "phase": "Phase 3: Offensive Testing & Compliance",
                "focus": "Vulnerability Testing & Risk Governance",
                "key_skills": ["Penetration Testing Tools", "Metasploit", "Security Auditing"],
                "milestone": "Deliver an audit report and vulnerability assessment write-up."
            }
        ]
    }
}

class Questionnaire(BaseModel):
    goal: str
    skills: Union[List[str], str]
    preferences: Union[List[str], str]
    top_k: Optional[int] = 3

class RoadmapPhase(BaseModel):
    phase: str
    focus: str
    key_skills: List[str]
    milestone: str

class CareerRoadmap(BaseModel):
    estimated_duration: str
    phases: List[RoadmapPhase]

class RecommendationResult(BaseModel):
    rank: int
    course_id: str
    title: str
    career_track: str
    match_score: float
    summary: str
    roadmap: CareerRoadmap

@app.get("/")
def home():
    return {"status": "online", "message": "Career Roadmap & Recommendation Engine is operational!"}

@app.post("/recommend/", response_model=List[RecommendationResult])
def get_recommendations_and_roadmaps(payload: Questionnaire):
    try:
        skills_str = ", ".join(payload.skills) if isinstance(payload.skills, list) else payload.skills
        prefs_str = ", ".join(payload.preferences) if isinstance(payload.preferences, list) else payload.preferences

        query_text = (
            f"GOALS & CAREER PIVOT: {payload.goal}. "
            f"CURRENT/TARGET SKILLS: {skills_str}. "
            f"LEARNING PREFERENCES: {prefs_str}."
        )
        
        n_res = payload.top_k if payload.top_k else 3
        results = collection.query(query_texts=[query_text], n_results=n_res)
        
        output = []
        if results and results.get("ids") and len(results["ids"][0]) > 0:
            for i in range(len(results["ids"][0])):
                c_id = results["ids"][0][i]
                title = results["metadatas"][0][i]["title"]
                track = results["metadatas"][0][i]["track"]
                distance = results["distances"][0][i]
                
                # Updated line for accurate match percentage:
                match_score = round(max(0.0, 100.0 / (1.0 + distance)), 1)
                
                doc = results["documents"][0][i]
                
                rm_info = ROADMAP_DATA.get(c_id, {
                    "estimated_duration": "3 - 6 Months",
                    "phases": [
                        {
                            "phase": "Phase 1: Core Fundamentals",
                            "focus": f"Foundational concepts in {track}",
                            "key_skills": ["Fundamental concepts", "Core toolstack setup"],
                            "milestone": "Complete initial project exercises."
                        }
                    ]
                })
                
                output.append(RecommendationResult(
                    rank=i + 1,
                    course_id=c_id,
                    title=title,
                    career_track=track,
                    match_score=match_score,
                    summary=doc,
                    roadmap=CareerRoadmap(
                        estimated_duration=rm_info["estimated_duration"],
                        phases=[
                            RoadmapPhase(
                                phase=p["phase"],
                                focus=p["focus"],
                                key_skills=p["key_skills"],
                                milestone=p["milestone"]
                            ) for p in rm_info["phases"]
                        ]
                    )
                ))
        return output

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))