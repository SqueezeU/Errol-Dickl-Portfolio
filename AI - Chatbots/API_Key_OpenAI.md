## 🔐 How to Configure the OpenAI API Key (Local)

To run local applications with GPT-4 or other OpenAI models, you need to properly configure a personal API key.

---

### 📄 1. Where to Get the Key?

Go to: https://platform.openai.com/account/api-keys  
► Log in and click on **“Create new secret key”**  
► Copy the key (it starts with something like `sk-...`)  
🔐 Save it in a secure location – it will only be shown once.

---

### ⚙️ 2. How to Set the Key Locally (Windows)

1. Open the **System Environment Variables** window  
   *(Control Panel → System → Advanced settings → Environment Variables)*  
2. Under **User Variables**, click on **New...**  
3. Enter:

   - **Variable name:** `OpenAI_API_Key`  
   - **Value:** `sk-...` (your secret key)

4. Click **OK** to save.

---

### ✅ 3. Test the Configuration in JupyterLab

Open a new notebook and run this code:

```python
import os

api_key = os.getenv("OpenAI_API_Key")

if api_key and api_key.startswith("sk-"):
    print("✅ API key detected correctly.")
else:
    print("⚠️ No API key detected.")
