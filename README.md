# VeriTask

VeriTask is a human-only microtask marketplace built for the World Mini Apps ecosystem.

It helps real people post tasks, accept work, submit proof, receive escrow-backed payouts, and build portable reputation from verified completions.

## Why VeriTask

Online task markets often struggle with:
- fake identities
- bot farming
- spam submissions
- unpaid work
- low-trust interactions

VeriTask addresses this by combining:
- World-aligned human verification flow
- escrow-backed task funding
- proof-of-work submission
- completion-based reputation

## Core Flow

1. Poster creates a task
2. Poster funds escrow
3. Worker accepts the task
4. Worker submits proof of completion
5. Poster approves the work
6. Payout is released
7. Reputation is updated

## Features

- Human-only marketplace UX
- Mobile-first interface
- Task creation and task feed
- Task detail view
- Escrow funding flow
- Task acceptance flow
- Proof submission flow
- Approval and payout release flow
- Reputation dashboard

## Tech Stack

### Frontend
- Next.js
- TypeScript
- Tailwind CSS

### Backend
- FastAPI
- In-memory task flow for demo
- REST API endpoints for task lifecycle

## Project Structure

### Frontend
- `apps/web/app/page.tsx` - landing page
- `apps/web/app/marketplace/page.tsx` - task marketplace
- `apps/web/app/tasks/new/page.tsx` - create task
- `apps/web/app/tasks/[id]/page.tsx` - task detail and actions
- `apps/web/app/me/page.tsx` - reputation page
- `apps/web/lib/api.ts` - frontend API helper

### Backend
- `apps/api/app/main.py` - FastAPI app entry
- `apps/api/app/api/v1/routes.py` - API routes
- `apps/api/app/schemas/marketplace.py` - marketplace schemas
- `apps/api/app/schemas/world.py` - world verification schema

## API Endpoints

- `GET /api/v1/health`
- `GET /api/v1/tasks`
- `GET /api/v1/tasks/{task_id}`
- `POST /api/v1/tasks`
- `POST /api/v1/tasks/{task_id}/accept`
- `POST /api/v1/tasks/{task_id}/submit`
- `POST /api/v1/tasks/{task_id}/approve`
- `POST /api/v1/escrow/fund`
- `GET /api/v1/reputation/{user_id}`
- `GET /api/v1/world/status/{user_id}`

## Local Setup

### Frontend
```bash
cd apps/web
npm install
npm run dev

## Vercel deployment plan

Vercel is ideal for your Next.js frontend. Official Vercel docs recommend deploying Next.js either from Git or with the Vercel CLI. 3

### Deploy frontend to Vercel

From `apps/web`:

```bash
npm install -g vercel
vercel
