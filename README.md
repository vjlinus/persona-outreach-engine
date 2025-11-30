# Persona/Painpoint-Driven Outreach Engine

This is a **prototype AI-driven email outreach engine** that generates hyper-personalized emails based on persona and painpoints.  

## Features
- Generates emails using Google Gemini LLM.
- Sends emails only to recipients with empty 'Email Status'.
- Updates Excel file with `Email Status` and `Sent Time`.
- Fully secret-safe using `.env` file.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/vjlinus/persona-outreach-engine.git
cd persona-outreach-engine
