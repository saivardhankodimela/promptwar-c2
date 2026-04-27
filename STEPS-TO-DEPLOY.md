# 🚀 Deployment Guide: Adaptive Election Agent (Mumbai Edition)

This guide outlines the production deployment using **100% Keyless Identity** in the **Mumbai (asia-south1)** region.

---

## 🔐 Phase 1: Security Strategy (Zero-Trust)

We use an **Identity-Based** approach (No API Keys, No JSON files):

1.  **Vertex AI & Google Cloud Services**:
    - **No Keys Required**: All services use **IAM Identity**.
    - **Locally**: Run `gcloud auth application-default login` once. 
    - **In Production**: Cloud Run attaches the `election-agent-sa` identity automatically.

---

## 🏗️ Phase 2: Deployment (Cloud Run)

The following command deploys the app to the **Mumbai** region, linking the secure service account identity:

```bash
gcloud run deploy election-agent \
  --source . \
  --service-account election-agent-sa@promptwars-c2.iam.gserviceaccount.com \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GCP_PROJECT_ID=promptwars-c2,GCP_LOCATION=asia-south1 \
  --project promptwars-c2
```

---

## ✅ Phase 3: Final Verification

1.  **Backend**: Confirm the Cloud Run URL is active (should end in `asia-south1.run.app`).
2.  **Frontend**: 
    - Update `ChatInterface.jsx` with the new Mumbai URL.
    - Build & Deploy: `npm run build && firebase deploy`

---
*Architected for Mumbai by Antigravity AI*
