# Vercel Quick Start Guide

Get Co-Apply deployed to Vercel in under 5 minutes!

## 🚀 One-Click Deploy

The fastest way to deploy Co-Apply:

1. Click the button below:

   [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/stewartDMS/Co-Apply)

2. Sign in to Vercel (or create a free account)

3. Click "Create" to deploy

4. Wait ~2 minutes for deployment to complete

5. Visit your new URL: `https://co-apply-[random-id].vercel.app`

That's it! Your Co-Apply API is now live! 🎉

## 🔧 Deploy via Vercel CLI

For more control over deployment:

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Clone and Navigate

```bash
git clone https://github.com/stewartDMS/Co-Apply.git
cd Co-Apply
```

### Step 3: Login to Vercel

```bash
vercel login
```

### Step 4: Link to Existing Project

This repository is configured for the existing 'co-apply' Vercel project.

```bash
vercel link
```

Follow the prompts:
- Link to existing project? **Yes**
- Which scope? **(select the account with the co-apply project)**
- Link to which project? **co-apply**

> **For Contributors**: If you don't have access to the main project, you can create your own fork deployment. See "Alternative Setup" below.

### Step 5: Deploy

```bash
vercel
```

### Step 6: Deploy to Production

```bash
vercel --prod
```

Your app is now live! 🎊

### Alternative Setup (Create Your Own Project)

If you're forking and need your own deployment:

```bash
vercel
```

Follow the prompts:
- Set up and deploy? **Yes**
- Which scope? **(select your account)**
- Link to existing project? **No**
- Project name? **co-apply-fork** (use a different name)
- In which directory is your code? **./
- Want to override settings? **No**

## 📱 Connect to GitHub (Recommended)

For automatic deployments on every push:

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository
4. Click "Deploy"

Now every push to `main` automatically deploys! 🔄

## ✅ Verify Deployment

Test your deployment:

```bash
# Replace with your actual Vercel URL
curl https://your-app.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Co-Apply API",
  "version": "0.1.0"
}
```

## 🧪 Run Test Suite

Test all endpoints against your live deployment:

```bash
python test_api.py --url https://your-app.vercel.app
```

## 📊 View Your Deployment

Visit your Vercel URL in a browser to see:
- 📋 Beautiful landing page with API docs
- 🔗 Direct links to test endpoints
- 📚 Complete API reference
- ✅ Live status indicator

## 🔑 Environment Variables (Optional)

If you need to add environment variables:

### Via Dashboard
1. Go to your project on vercel.com
2. Click "Settings" → "Environment Variables"
3. Add variables (e.g., `FLASK_ENV=production`)

### Via CLI
```bash
vercel env add VARIABLE_NAME
```

## 🐛 Troubleshooting

### Build fails?
- Check that `requirements.txt` includes all dependencies
- Verify `vercel.json` is in the root directory

### Import errors?
- Check function logs in Vercel dashboard
- Ensure `PYTHONPATH` is set in `vercel.json`

### Slow cold starts?
- Normal for free tier
- Consider Vercel Pro for better performance

## 📖 Next Steps

After deployment:

1. ✅ Test all endpoints with `test_api.py`
2. 📝 Read [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions
3. 🔍 Check [API_REFERENCE.md](API_REFERENCE.md) for complete API docs
4. 🎨 Customize the landing page in `api/index.py`
5. 🔒 Add authentication if needed
6. 📊 Set up monitoring and alerts

## 💡 Tips

- **Free tier**: 100GB bandwidth, 100hrs execution time/month
- **Custom domains**: Add in Vercel dashboard settings
- **Preview deployments**: Every PR gets a preview URL
- **Logs**: View real-time logs in Vercel dashboard
- **Rollback**: Easy one-click rollback to previous versions

## 🆘 Need Help?

- [Full Deployment Guide](DEPLOYMENT.md)
- [API Reference](API_REFERENCE.md)
- [GitHub Issues](https://github.com/stewartDMS/Co-Apply/issues)
- [Vercel Documentation](https://vercel.com/docs)

---

**Happy Deploying!** 🚀
