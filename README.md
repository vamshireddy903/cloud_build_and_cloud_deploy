If you want to create your own service account and use it with Cloud Build, the service account must have the following permissions.

<img width="887" height="468" alt="image" src="https://github.com/user-attachments/assets/411174f3-a8e2-4af2-a180-25aeaa5c96bb" />

cloudbuild.yaml explaination:

# Overall structure  
steps:    → list of tasks to run in order  
images:   → final image to store in Artifact Registry  
options:  → build settings  

# Step 1: Build Docker image

<img width="774" height="646" alt="image" src="https://github.com/user-attachments/assets/e529821f-4843-4cd6-aec8-77f540d15df9" />

# Step 2: Push image to Artifact Registry

<img width="763" height="490" alt="image" src="https://github.com/user-attachments/assets/e93dc68d-cb97-4ae3-838e-284b3c7d03bd" />

# Step 3: Deploy to Cloud Run

<img width="592" height="561" alt="image" src="https://github.com/user-attachments/assets/5c39fd7f-3729-4824-b8af-394abc02a40b" />

<img width="867" height="384" alt="image" src="https://github.com/user-attachments/assets/411c842a-20ef-4631-b8bf-3179c19a8d1e" />

```
options:
  logging: CLOUD_LOGGING_ONLY
```

**What it does:**
```
sends all build logs to Google Cloud Logging only
avoids storing logs in GCS bucket
cheaper and simpler for logging
```

---

## Full flow in one picture
```
cloudbuild.yaml runs
        ↓
Step 1: docker build
        reads Dockerfile
        creates image tagged with commit SHA
        ↓
Step 2: docker push
        uploads image to Artifact Registry
        asia-south1-docker.pkg.dev/vamsi-project-488603/demo-repo/my-app:a1b2c3d
        ↓
Step 3: gcloud run deploy
        pulls image from Artifact Registry
        creates/updates Cloud Run service
        app goes live at → https://my-app-service-xxxx.run.app
        ↓
images: registers image in build history
options: logs go to Cloud Logging

```
```
Cloud Build = runs commands and moves on
Cloud Deploy = manages the JOURNEY of your release
```
```
Think of it this way
Cloud Build deploying to prod is like:
Developer pushes code
        ↓
Cloud Build runs kubectl apply / gcloud run deploy
        ↓
DIRECTLY hits production ⚠️
        ↓
No one approved it
No canary testing
No rollback plan
```

# Real world scenario — what can go wrong:
```
9:00 AM - developer pushes bad code
9:01 AM - Cloud Build auto deploys to PROD
9:01 AM - 10,000 users hit errors 😱
9:01 AM - team scrambles to fix
9:45 AM - finally rolled back manually
          45 mins of downtime!
```
# With Cloud Deploy:\
```
9:00 AM - developer pushes code
9:01 AM - auto deploys to DEV ✅
9:05 AM - auto deploys to STAGING ✅
9:10 AM - STOPS ⏸️ waits for approval
9:10 AM - manager reviews staging
9:15 AM - manager approves PROD
9:16 AM - deploys 10% canary to PROD
9:20 AM - metrics look good
9:21 AM - full 100% rollout ✅

Bad code scenario:
9:16 AM - deploys 10% canary
9:17 AM - errors detected on 10% traffic
9:17 AM - ONE CLICK rollback ✅
          only 1 min, only 10% users affected!
```

<img width="856" height="482" alt="image" src="https://github.com/user-attachments/assets/4871c636-e75c-4e9c-9db5-95730f010c4b" />
