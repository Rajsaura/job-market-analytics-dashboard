

 # **Job Market Analytics Dashboard**
A real-time data analytics platform built with FastAPI, PostgreSQL, and Chart.js to track, aggregate, and visualize job market trends, salary distributions, and hiring demands.

**#Overview**
The Job Market Analytics Dashboard bridges the gap between raw job board data and actionable career insights. It features an asynchronous data ingestion pipeline, a structured relational database, and a lightweight, responsive frontend dashboard providing dynamic visual analytics.

**#Key Features**
Asynchronous API Endpoints: Powered by FastAPI for high-throughput data processing.

Dynamic Analytics: Frontend charts built with Chart.js to display job role distributions, salary percentiles, and top-hiring locations.

Relational Data Modeling: Structured PostgreSQL schemas optimized for analytical aggregation queries.

**#Tech Stack**
Backend: FastAPI (Python 3.10+)

Database: PostgreSQL

Frontend: HTML5, Tailwind CSS, Chart.js

Data Ingestion: BeautifulSoup4 / Requests (Scraper components)


# **Architecture & Data Flow**
Scraper Layer: Targets specific job boards to fetch unstructured HTML postings.

ETL Pipeline: Parses, cleans, and transforms raw data into structured payloads.

Storage Layer: Upserts normalized records into PostgreSQL database tables.

API Service: FastAPI queries the database and serves aggregated JSON endpoints.

UI Presentation: Chart.js consumes the API endpoints to render real-time analytics graphs.

**#Current Project Issues & Engineering Limitations**
As this project is in an active development and refinement phase, please be aware of the following known constraints:

1. Automation Ingestion Block (CI/CD Limitations)
Issue: GitHub Actions workflows designed to automate the scraping pipeline are currently blocked by target job boards (specifically Naukri.com) due to strict anti-bot mitigations (Cloudflare/IP-rate limiting on GitHub runner IP ranges).

Impact: Scheduled data refreshes cannot currently run seamlessly in the cloud environment. Data updates must be triggered from local machines or proxy-backed servers.

2. Limited Scraping Scope
Issue: The web-scraping modules are currently optimized only for a selected subset of high-demand job profiles on Naukri.com.

Impact: The dashboard does not reflect the entire breadth of the job market; expanding selectors for diverse roles is an active area of contribution.

3. Synthetic Production Data
Issue: To maintain a smooth production environment and a functional frontend layout despite the automation blocks listed above, the repository currently utilizes a synthetic dataset.

Impact: Because the automated replacement pipeline failed under the CI/CD block, the live metrics represent simulated baseline data rather than real-time original market figures.

4. Severe Initial Load Latency (50s - 1.5m)
**Issue:** The initial load of the dashboard can take anywhere from 50 seconds to 1.5 minutes if the application has been idle.
**Root Cause:** This is caused by a combination of infrastructure tiers:
  1. **Render Free Tier Spin-up:** Render spins down web services after 15 minutes of inactivity. The initial request triggers a container cold start.
  2. **Neon Serverless DB Compute Activation:** Neon Postgres automatically places compute nodes into a "sleep" state after 5 minutes of inactivity to save resources. 
  3. **The Chain Reaction:** When a user hits the dashboard, Render must wake up first, then attempt to connect to Neon, which must then wake up the database compute node. This sequential wake-up chain introduces massive latency.
**Impact:** Poor initial User Experience (UX), though subsequent requests are near-instantaneous once both services are warm.

** #Getting Started**
Prerequisites
Python 3.10 or higher

PostgreSQL instance running locally or via Docker

Installation & Setup
Clone the Repository:

Bash
git clone https://github.com/Rajsaura/job-market-analytics-dashboard.git
cd job-market-analytics-dashboard
Set Up a Virtual Environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file in the root directory:

Code snippet
DATABASE_URL=postgresql://user:password@localhost:5432/job_analytics_db
ENV_MODE=production  # Set to 'development' to run local scripts
Initialize Database Tables:

Bash
# Run your database migration or creation script
python app/db/init_db.py
Run the Application:

Bash
uvicorn app.main:app --reload
Access the local server at http://127.0.0.1:8000.

📈 Roadmap & Future Scope
[ ] Proxy Integration: Integrate residential proxy rotation to bypass GitHub Action blocking mechanisms.

[ ] Broaden Selectors: Update the parser layout engine to scale beyond limited profiles.

[ ] Data Pipeline Decoupling: Move synthetic data out of the production main branch to a separate staging seed file.
[ ] ADDING MORE BETTER ANALYSIS: Better analysis feature which give deeper insights 

**LIVE LINK:-** = https://job-market-analytics-dashboard.onrender.com/dashboard


🤝 Contributing
Contributions are welcome! Please submit a Pull Request or open an Issue to discuss potential architectural enhancements, especially regarding web-scraping resiliency and proxy management.


**AUTHOR**
SAURABH RAJ
