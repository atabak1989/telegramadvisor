# Replit.md

## Overview

This repository contains a Telegram bot for assessing study abroad eligibility and providing personalized recommendations. The bot guides users through a conversational flow to collect academic information and provides tailored advice based on predefined criteria and study programs data.

## User Preferences

Preferred communication style: Simple, everyday language.
User Interface Language: Persian (Farsi) - All bot messages and responses are in Persian.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Bot Layer**: Telegram bot handlers managing user interactions and conversation flow
- **Business Logic Layer**: Eligibility assessment and recommendation generation
- **Data Layer**: JSON-based data storage for study programs and country information
- **Utility Layer**: Input validation and helper functions

## Key Components

### 1. Bot Handlers (`bot_handlers.py`)
- Manages Telegram bot conversation states using ConversationHandler pattern
- Implements state machine for collecting user data (age, major, degree, GPA, language, country)
- Integrates with eligibility checker and recommendation engine

### 2. Eligibility Checker (`eligibility_checker.py`)
- Assesses user eligibility based on minimum requirements:
  - Minimum GPA: 13.0/20
  - Maximum age: 40
  - Minimum language level: B1
- Provides detailed feedback on issues and warnings

### 3. Recommendation Engine (`recommendation_engine.py`)
- Generates personalized study abroad recommendations
- Matches user profile with available programs and countries
- Uses JSON data files for program and country information

### 4. Configuration (`config.py`)
- Centralized configuration for bot settings
- Defines conversation states and constants
- Contains predefined lists for majors, degree types, and language levels

### 5. Validators (`utils/validators.py`)
- Input validation for all user data
- Ensures data integrity before processing
- Provides type checking and range validation

## Data Flow

1. User initiates conversation with `/start` command
2. Bot guides user through sequential data collection:
   - Age validation (16-80 years)
   - Major selection from predefined list
   - Degree type selection with special validation for associate degrees
   - Field of study collection for bachelor's and master's degrees
   - GPA input (0-20 scale)
   - Language proficiency level (A1-C2)
   - Budget range selection (under 2B, 2-3B, over 3B Tomans)
   - Country recommendation and selection based on budget
3. Collected data is passed to eligibility checker with enhanced validation
4. If eligible, recommendation engine provides personalized suggestions
5. Results are formatted and sent back to user

## External Dependencies

### Core Dependencies
- **python-telegram-bot**: Telegram bot API integration
- **Python standard library**: json, logging, os, random, typing

### Data Sources
- Static JSON files for study programs and country information
- No external database or API dependencies

## Deployment Strategy

### Environment Configuration
- Bot token configured via environment variable `TELEGRAM_BOT_TOKEN`
- Fallback to default token for development

### Architecture Decisions

**Problem**: Need for structured conversation flow with state management
**Solution**: ConversationHandler pattern with defined states
**Rationale**: Provides clear conversation flow and maintains user context

**Problem**: Data validation and integrity
**Solution**: Dedicated validator utility class
**Rationale**: Ensures data quality and provides reusable validation logic

**Problem**: Flexible recommendation system
**Solution**: JSON-based data storage with matching algorithms
**Rationale**: Easy to update and maintain without database overhead

**Problem**: Modular and maintainable code structure
**Solution**: Separation of concerns with dedicated classes for each responsibility
**Rationale**: Improves code maintainability and testing capabilities

### Current Limitations
- No persistent data storage (conversations are stateless)
- Static data sources (JSON files)
- Limited to predefined criteria and programs
- No user authentication or session management

### Recent Changes (July 19, 2025)
- Added associate degree age restriction (under 23 years for bachelor's eligibility)
- Implemented field of study collection for bachelor's and master's degrees
- Added budget-based country recommendation system with three tiers
- Enhanced conversation flow with additional validation steps
- Expanded data collection to include budget and educational background

### Potential Enhancements
- Database integration for persistent storage
- Dynamic program and country data updates
- User profile management
- Advanced recommendation algorithms
- Multi-language support