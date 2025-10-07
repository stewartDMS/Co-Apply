# Vercel Project Configuration

This directory contains the Vercel project configuration that links this repository to the existing Vercel project.

## project.json

The `project.json` file contains:
- `projectId`: The unique identifier for the Vercel project
- `orgId`: The organization/team ID (or user ID) that owns the project

## How to Get Your Project IDs

### Option 1: Using Vercel CLI

After deploying once with `vercel`, the CLI will automatically create this file with the correct IDs.

### Option 2: From Vercel Dashboard

1. Go to your project on [vercel.com](https://vercel.com)
2. Navigate to **Settings** → **General**
3. Find the **Project ID** in the project settings
4. Find the **Team/Org ID** in your account settings

### Option 3: From .vercel directory after first deployment

If you've deployed before, check `.vercel/project.json` in your local copy.

## Important Notes

- **Do NOT commit** this directory to git if it contains real project IDs
- The `.vercel` directory is already in `.gitignore`
- This directory is only committed with placeholder values for documentation purposes
- Contributors will need to link to the actual project using `vercel link` or by deploying

## For Contributors

If you're a contributor who needs to deploy:

1. Contact the repository maintainer for the actual project IDs
2. OR use `vercel link` to link to the existing project:
   ```bash
   vercel link
   ```
   Select "Link to existing project" and choose the 'co-apply' project

3. OR simply run `vercel` and when asked "Link to existing project?", select **Yes** and choose 'co-apply'
