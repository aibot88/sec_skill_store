---
name: shaper-setup
description: Ensure Shaper CLI is installed, configure shaper.json, authenticate, and safely pull remote dashboards/tasks.
---

# Shaper Environment Setup Skill

Use this skill to prepare the local workspace for Shaper dashboard development. It ensures the environment meets all requirements, the Shaper CLI is installed, authentication is configured, and remote resources are safely pulled.

## Workflow

Follow these steps sequentially to setup the environment:

### 1. Operating System Validation
- **Requirement**: Shaper is supported **only** on macOS and Linux. Windows is not supported.
- **Action**: Check the current OS. If the user is running Windows, inform them that Shaper is not supported and halt.

### 2. Verify Shaper CLI Installation
- **Action**: Run `shaper --version`.
- **Handling**:
  - If the command succeeds, proceed to Step 3.
  - If the command fails or `shaper` is not found, stop and instruct the user to install the Shaper CLI by following the official documentation:
    👉 https://taleshape.com/shaper/docs/installing-shaper/

### 3. Manage Configuration File (`shaper.json`)
- **Config Override**: Commands take an optional `--config-file` flag to override the default file path. Check if a custom config file path is passed/configured. The default path is `./shaper.json`.
- **Action**: Check if the configuration file exists at `./shaper.json` (or the path specified by `--config-file`).
- **If the config file does NOT exist**:
  1. Ask the user for the **URL of their Shaper instance** and the **directory to use** (default directory is `.`).
  2. Create the configuration file with the following JSON structure:
     ```json
     {
       "url": "<USER_PROVIDED_URL>",
       "directory": "<USER_PROVIDED_DIRECTORY_OR_DOT>",
       "schemaIgnore": []
     }
     ```
  3. Ensure the JSON is properly formatted and saved.

### 4. Git Status Check & Data Pulling
- **Safety Rule**: To avoid overwriting work, never pull remote changes if there are uncommitted local edits.
- **Action**: Check the repository's git status by running `git status --porcelain`.
- **Handling**:
  - If there are uncommitted changes, **abort** the pull and warn the user. Ask them to commit or stash their changes first.
  - If git status is clean, run the pull command:
    ```bash
    shaper pull --yes
    # Or, if using a custom config:
    shaper pull --yes --config-file <PATH_TO_CONFIG>
    ```

### 5. Authentication & Git Hygiene
- **First Pull Behavior**: The first time `shaper pull --yes` runs, it will attempt to open a browser window for the user to confirm authentication.
- **Token Storage**: Successful authentication saves an auth token in a local `.shaper-auth` file (located in the same directory as the configuration or command invocation).
- **Git Hygiene**:
  - Check if `.shaper-auth` is added to your `.gitignore`.
  - If `.gitignore` does not exist, create it.
  - Append `.shaper-auth` to `.gitignore` if it is not already present, ensuring the token is never committed to version control.
