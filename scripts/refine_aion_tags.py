import os
from huggingface_hub import HfApi

token = None
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("HF_TOKEN="):
                token = line.strip().split("=", 1)[1].strip("\"'")

if not token:
    raise ValueError("HF_TOKEN not found in .env")

api = HfApi(token=token)

# 1. Refine Kronumos-Aion
print("1. Updating Kronumos/Kronumos-Aion...")
try:
    aion_path = api.hf_hub_download(repo_id="Kronumos/Kronumos-Aion", filename="README.md")
    with open(aion_path, "r", encoding="utf-8") as f:
        aion_text = f.read()

    new_aion_text = aion_text.replace(
        "license_name: tokenectomy-enterprise-dual-1.0",
        "license_name: Tokenectomy Dual License (TDL 1.0)"
    ).replace(
        "pipeline_tag: text-generation\n",
        ""
    )

    if new_aion_text != aion_text:
        pr_aion = api.upload_file(
            path_or_fileobj=new_aion_text.encode("utf-8"),
            path_in_repo="README.md",
            repo_id="Kronumos/Kronumos-Aion",
            repo_type="model",
            commit_message="Refine license to Tokenectomy Dual License (TDL 1.0) and remove generic pipeline tag",
            create_pr=True
        )
        print(f"   -> PR Created for Kronumos-Aion: {pr_aion}")
    else:
        print("   -> No changes needed for Aion.")
except Exception as e:
    print(f"   -> Error updating Aion: {e}")

# 2. Refine Kronumos-14B-Kairos
print("\n2. Updating Kronumos/Kronumos-14B-Kairos...")
try:
    k14_path = api.hf_hub_download(repo_id="Kronumos/Kronumos-14B-Kairos", filename="README.md")
    with open(k14_path, "r", encoding="utf-8") as f:
        k14_text = f.read()

    new_k14_text = k14_text.replace(
        "pipeline_tag: text-generation\n",
        ""
    )

    if new_k14_text != k14_text:
        pr_k14 = api.upload_file(
            path_or_fileobj=new_k14_text.encode("utf-8"),
            path_in_repo="README.md",
            repo_id="Kronumos/Kronumos-14B-Kairos",
            repo_type="model",
            commit_message="Remove generic pipeline_tag to focus on specialized autonomous APR tags",
            create_pr=True
        )
        print(f"   -> PR Created for Kronumos-14B-Kairos: {pr_k14}")
    else:
        print("   -> No changes needed for 14B.")
except Exception as e:
    print(f"   -> Error updating 14B: {e}")

print("\nDone!")
