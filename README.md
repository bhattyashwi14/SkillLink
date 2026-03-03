# SkillLink – Skill Exchange & Hiring Platform

SkillLink is a full-stack Django-based platform that integrates peer-to-peer learning with project-based hiring inside a structured campus ecosystem.

The platform operates through three role-based dashboards: Learner, Tutor, and Client — each designed with dedicated workflows, verification layers, and interaction systems.

---

# Authentication & Security

All users (Learners, Tutors, Clients):

- Register using email
- Verify account via OTP sent through the application
- Create a secure passcode (validated with defined rules)
- Log in using verified credentials
- Users can edit and update their profile details at any time after onboarding.

This ensures secure, verified onboarding across all roles.

---

# 1️⃣ Learner Dashboard

## Onboarding

After registration and OTP verification:

- Learner must complete profile before accessing dashboard.
- Required fields:
  - Full Name
  - Semester
  - Department
  - GitHub link
  - LinkedIn link

Once completed, learner is redirected to the dashboard.

---

## Dashboard Overview

At the top, four dynamic cards are displayed:

1. Profile Completion Percentage  
2. Learning Streak (consecutive active days)  
3. Skills Learned  
4. Upcoming Sessions  

Top-right corner:
- Alphabet-based avatar (generated from name)
- Dropdown options: View Profile / Logout

---

## Smart Chatbot Assistant

The Learner Dashboard includes an integrated smart chatbot that dynamically fetches relevant data from the database.

The chatbot assists learners by Providing information about a:
- Available skills
- Booked sessions
- Skills learnt
- Profile completion status

This adds an intelligent interaction layer, enhancing usability and engagement within the learning ecosystem.

## Skill Discovery

Below the dashboard metrics:

- Skill cards are displayed dynamically.
- Each card shows number of available tutors for that skill.

When a learner selects a skill:

- List of tutor cards is displayed.
- Each tutor card shows:
  - Name
  - Rating
  - Bio
  - View Profile button
  - Book Slots button

---

## Tutor Profile View

On clicking **View Profile**, learner can see:

- Tutor GitHub link
- Tutor LinkedIn link
- Rating graph
- Proof of work

---

## Slot Booking System

On clicking **Book Slots**:

- Available time slots of tutor are displayed.
- Learner selects preferred slot.
- Booking confirmation screen shows:
  - Session details
  - Meeting link
  - Download receipt option

Once a session is successfully booked:

- A confirmation email containing session details and meeting link is sent to both the learner and the tutor.
- The session automatically appears in the **Upcoming Sessions** card on the learner dashboard.

After session completion:

- Learner marks session as completed.
- Learner submits rating for tutor.

This rating directly affects tutor credibility and hiring visibility.

---

# 2️⃣ Tutor Dashboard

## Registration & Verification

New tutor:

- Registers using email
- Verifies via OTP
- Completes profile with:
  - Full Name
  - GitHub profile
  - LinkedIn profile
  - Technical skills
  - Teaching skills
  - Available teaching slots
  - Proof of teaching skill (certificate/sample work)

After submission:

- Profile enters verification stage.
- Admin reviews:
  - GitHub authenticity
  - LinkedIn authenticity
  - Skill proof

Only after admin approval:

- Tutor profile becomes visible to learners and clients.
- If not approved, profile remains hidden.

---

## Tutor Dashboard Features

Once approved, tutor dashboard displays:

- Complete profile details
- Total students taught
- Average rating
- Active slots 
- Upcoming teaching sessions with student history and meeting link
- Completed sessions with student history

Tutors can:

- Edit and update their profile details
- Manage time slots
- Track performance
- Accept or reject learning bookings
- Receive hiring requests from clients

Ratings enhance tutor visibility and improve hiring chances.

---

# 3️⃣ Client Dashboard

Clients may include:

- Students
- Startups
- Companies
- Freelancers

---

## Client Onboarding

- Email registration
- OTP verification
- Secure login

After login, client is directed to dashboard.

---

## Skill-Based Tutor Discovery

- Skill cards dynamically generated from database.
- When new skill is added by tutors, new skill card appears automatically.

When client selects a skill:

- List of relevant tutors (intern candidates) is displayed.
- Each profile includes:
  - Skills
  - Work proof
  - Ratings
  - GitHub & LinkedIn links

---

## Hiring Workflow

After reviewing profile:

Client can send structured hiring request including:

- Required skill
- Project description
- Duration
- Budget

Tutor receives notification and can:

- Accept request
- Reject request

Client can track request status through:

"My Requests" section

Status updates reflect tutor response in real-time.

---

# Admin Layer

Through Django Admin Panel:

- Tutor verification is handled.
- Skill database is managed.
- System-level validation is enforced.

This ensures authenticity and quality control within the ecosystem.

---

# System Workflow Summary

1. Verified onboarding via OTP.
2. Role-based dashboard redirection.
3. Skill discovery & filtering.
4. Structured booking & session tracking.
5. Rating-driven credibility system.
6. Intelligent chatbot assistance integrated with database queries.
7. Project-based hiring with approval workflow. 

---

# Tech Stack

- Backend: Django (Python)
- Frontend: HTML, CSS
- Database: SQLite
- Authentication: OTP-based email verification
- Architecture: Multi-app Django structure (Client, Tutor, Learn, Core)

---

# Purpose

SkillLink bridges academic learning with real-world exposure by:

- Enabling structured peer learning
- Building credibility through ratings
- Creating internship-style hiring opportunities
- Ensuring verified and moderated participation

It transforms campus skill-sharing into a transparent, accountable, and opportunity-driven ecosystem.

