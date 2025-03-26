# App Metrics Dashboard

A web application for exploring, analyzing, and visualizing App Store metrics including downloads, revenue, ratings, screenshots, privacy data, and reviews. Built with a modular microservice architecture, the platform supports scraping, data transformation, a RESTful API, and a rich frontend dashboard.

---

## 🚀 Setup Instructions

### Prerequisites

- Node.js (v18+)
- pnpm (v8+)
- Python 3.12
- Docker + Docker Compose

### Clone the Repository

```bash
git clone https://github.com/your-org/app-metrics-dashboard.git
cd app-metrics-dashboard
```

### Start the Services

```bash
docker-compose up --build
```

### Frontend Setup

```bash
cd front-end-microservice
pnpm install
pnpm dev
```

### API (FastAPI) Dev Run (optional outside Docker)

```bash
cd api-microservice
uvicorn src.main:app --reload
```

---

## 🧰 Architecture Overview

### Monorepo Structure

```
root/
├── docker-compose.yml
├── front-end-microservice/         # React + Tailwind + shadcn/ui dashboard
├── api-microservice/               # FastAPI with async SQLAlchemy
├── scraper-microservice/           # Authenticated scraping (Sensor Tower, App Store)
├── data-processor-microservice/    # Data normalization and PostgreSQL persistence
├── post-processor-microservice/    # Generate AI Labels and Cluster Analysis
└── shared/                     # Shared configs, models, utilities
```

### Key Technologies

- **FastAPI** (API layer)
- **PostgreSQL** (normalized data storage)
- **MongoDB** (raw scraped data)
- **Celery + RabbitMQ** (task queue for async processing)
- **React + Tailwind CSS + shadcn/ui** (frontend dashboard)
- **Selenium + BeautifulSoup** (authenticated scraping)
- **Docker Compose** (orchestration)

### Design Decisions

- Modular microservices for separation of concerns
- Async SQLAlchemy + `asyncpg` for performant DB access
- Celery workers to enable scalable data pipeline
- Scraped data stored raw first, then transformed into clean relational model
- Monorepo for unified deployment management

---

## 📊 API Documentation

### Base URL

```
http://localhost:8000
```

### Key Endpoints

#### `GET /apps`

Paginated list of apps with support for filters and sorting.

Query Params:

- `category`, `list_type`, `sort_by`, `sort_order`
- `price_min`, `downloads_min`, `revenue_min`, `rating_min`, etc.

#### `GET /apps/search?q=...`

Search apps using full-text matching.

#### `GET /apps/{apple_id}`

Fetch details of a single app including:

- Metadata, description, screenshots, reviews, stats

#### `GET /apps/filters/categories`

List all available categories.

#### `GET /apps/filters/labels`

List all extracted app labels.

#### `GET /analysis/downloads`

List download number per category.

#### `GET /analysis/revenue`

List revenue amount per category.

#### `GET /analysis/mrr-downloads`

List MRR / download number rate per category.

---

## ⚡ Challenges Faced & Solutions

### 🍏 Scraping the App Store at Scale

**Challenge:** Efficiently scrape thousands of apps without being blocked.

- **Solution:** We first scraped app listings by category, storing basic info quickly. Then, a second stage was used to fetch detailed data (like screenshots, reviews, metadata) for each app.
- **Techniques Used:** 
  - Rotating user agents
  - Random delays between requests
  - Multithreaded task dispatch per category to speed up collection

### 🧠 Complex App Details Parsing

**Challenge:** App Store detail pages contain a lot of noise — irrelevant images, irregular descriptions, mixed HTML tags.

- **Solution:** 
  - Filter screenshots using CSS class specific to actual iOS screenshots.
  - Extract all `<p>` tags inside the description container, preserving line breaks and semantics.
  - Created an expandable description UI to show formatted text.

### Sensor Tower Authenticated Scraping

**Challenge:** Sensor Tower requires authenticated sessions to access app metrics like downloads and revenue.

- **Solution:**
  - Used Selenium to perform login and persist the session.
  - Regular HTTP sessions failed due to aggressive bot protection.
  - Implemented request pacing with timers and moved scraping to a separate long-running task queue. With separated data-processing tasks.

### Data Processing Pipeline

**Challenge:** Some scraped data (like screenshots and optional fields) were inconsistent or noisy.

- **Solution:** A separate processor service cleans raw MongoDB documents, normalizes them, and saves them in PostgreSQL.
- Screenshot scraping was fixed by filtering for platform-specific classes.

### Full-Text Search in PostgreSQL

**Challenge:** Provide relevant search results quickly and avoid over-fetching data on the frontend.

- **Solution:** Used index and full-text-search in PostgreSQL to power the `/search` endpoint.

### ⚖️ Task Coordination & Syncing

**Challenge:** Ensure that data scraped asynchronously (especially Sensor Tower metrics) doesn’t trigger redundant processing and is safely persisted.

- **Solution:** 
  - Added processed flags in raw data
  - Separate task queues per stage

---

## ✨ Future Improvements

- Improve full text search for apps
- In time scrape for apps without full details
- Push new dashboard with graphs
- Create the Cluster Analysis page

---

Im still improving it! Until tomorrow wanna make more pushs - so tired now :')

