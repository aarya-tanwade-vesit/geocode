# Git & GitHub Instructions

## 1. Clone the Repository

Do this only once when setting up the project.

    git clone https://github.com/aarya-tanwade-vesit/geocode.git
    cd geocode

## 2. Before Starting Work

Always get the latest code before starting a task.

    git checkout main
    git pull origin main

## 3. Create Your Branch

Never work directly on `main`.

    git checkout -b feature/<feature-name>

Examples:
    feature/beacon-detection
    feature/udp
    feature/kalman
    feature/disturbances
    feature/gui

## 4. Make Changes & Commit

Check your changes:

    git status

Add changes:

    git add .

Commit:

    git commit -m "Describe your changes"

Example:

    git commit -m "Add OpenCV beacon detection"

## 5. Push Your Branch

    git push -u origin feature/<feature-name>

After the first push:

    git push

## 6. Pull Request

After pushing:

1. Open the repository on GitHub.
2. Create a Pull Request from your branch → `main`.
3. Add a short description of your changes.
4. Inform the relevant team member.
5. Merge only after team agreement.

## Important Rules

- Do NOT work directly on `main`.
- One branch = one task/feature.
- Pull the latest `main` before starting.
- Keep commits small and meaningful.
- Test before pushing.
- Inform the team before changing shared interfaces/data formats.
- Do not force-push unless agreed by the team.
- Do not commit `.env`, passwords, API keys or unnecessary generated files.
- Keep `main` stable and runnable.

## Quick Workflow

    git checkout main
    git pull origin main
    git checkout -b feature/<feature-name>

    # Make your changes

    git status
    git add .
    git commit -m "Describe your changes"
    git push -u origin feature/<feature-name>

Then create a Pull Request on GitHub.
