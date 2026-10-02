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

# 1. Update Kronumos-Aion
print("1. Updating Kronumos/Kronumos-Aion...")
try:
    aion_readme_path = api.hf_hub_download(repo_id="Kronumos/Kronumos-Aion", filename="README.md")
    with open(aion_readme_path, "r", encoding="utf-8") as f:
        aion_content = f.read()

    # Replace pipeline_tag: reinforcement-learning with pipeline_tag: text-generation
    new_aion_content = aion_content.replace(
        "pipeline_tag: reinforcement-learning",
        "pipeline_tag: text-generation"
    )

    if new_aion_content != aion_content:
        pr_aion = api.upload_file(
            path_or_fileobj=new_aion_content.encode("utf-8"),
            path_in_repo="README.md",
            repo_id="Kronumos/Kronumos-Aion",
            repo_type="model",
            commit_message="Fix pipeline_tag to text-generation to eliminate video preview bug",
            create_pr=True
        )
        print(f"   -> PR Created for Kronumos-Aion: {pr_aion}")
    else:
        print("   -> Aion already up to date.")
except Exception as e:
    print(f"   -> Error updating Aion: {e}")

# 2. Update Kronumos-14B-Kairos
print("\n2. Updating Kronumos/Kronumos-14B-Kairos...")
try:
    k14_readme_path = api.hf_hub_download(repo_id="Kronumos/Kronumos-14B-Kairos", filename="README.md")
    with open(k14_readme_path, "r", encoding="utf-8") as f:
        k14_content = f.read()

    new_k14_content = k14_content.replace(
        "pipeline_tag: reinforcement-learning",
        "pipeline_tag: text-generation"
    ).replace(
        "https://huggingface.co/NadevA23/Kronumos-Aion",
        "https://huggingface.co/Kronumos/Kronumos-Aion"
    ).replace(
        "https://huggingface.co/NadevA23/Kronumos-Kairos-v2",
        "https://huggingface.co/Kronumos/Kronumos-Kairos-v2"
    ).replace(
        "For cloud planetary scale, see [Kronumos Aion (671B MoE)]",
        "For cloud planetary scale, see [Kronumos Aion]"
    ).replace(
        "For ultra-lightweight offline edge, see [Kronumos 2 Kairos (7B)]",
        "For high-velocity offline edge, see [Kronumos Kairos]"
    )

    if new_k14_content != k14_content:
        pr_k14 = api.upload_file(
            path_or_fileobj=new_k14_content.encode("utf-8"),
            path_in_repo="README.md",
            repo_id="Kronumos/Kronumos-14B-Kairos",
            repo_type="model",
            commit_message="Fix pipeline_tag to text-generation and update Kronumos org links",
            create_pr=True
        )
        print(f"   -> PR Created for Kronumos-14B-Kairos: {pr_k14}")
    else:
        print("   -> Kronumos-14B-Kairos already up to date.")
except Exception as e:
    print(f"   -> Error updating Kronumos-14B-Kairos: {e}")

# 3. Update Kronumos/README (Org Card)
print("\n3. Updating Kronumos/README (Org Profile Space)...")
try:
    org_readme_path = api.hf_hub_download(repo_id="Kronumos/README", filename="README.md", repo_type="space")
    with open(org_readme_path, "r", encoding="utf-8") as f:
        org_content = f.read()

    # Add Live Workbench link in the center navigation
    old_links = '<p align="center">\n  <a href="https://doi.org/10.21203/rs.3.rs-11205335/v1"><b>[📄 Research Preprint]</b></a>'
    new_links = '<p align="center">\n  <a href="https://huggingface.co/spaces/NadevA23/Kronumos-2-Kairos"><b>[⚡ Live Interactive Workbench]</b></a> •\n  <a href="https://doi.org/10.21203/rs.3.rs-11205335/v1"><b>[📄 Research Preprint]</b></a>'

    new_org_content = org_content.replace(old_links, new_links)
    
    # Also add Live Workbench entry in Production Engines
    if "https://huggingface.co/spaces/NadevA23/Kronumos-2-Kairos" not in new_org_content:
        new_org_content = new_org_content.replace(
            "| ⚡ [**Kronumos Kairos**](https://huggingface.co/Kronumos/Kronumos-Kairos-v2) | **Edge / Workstation** | High-velocity local bug remediation & offline CI/CD pipelines | Zero-latency local execution, 100% air-gapped |",
            "| ⚡ [**Kronumos Kairos**](https://huggingface.co/Kronumos/Kronumos-Kairos-v2) | **Edge / Workstation** | High-velocity local bug remediation & offline CI/CD pipelines | Zero-latency local execution, 100% air-gapped |\n| 🌐 [**Interactive Workbench**](https://huggingface.co/spaces/NadevA23/Kronumos-2-Kairos) | **Live Web App / Cloud** | Real-time AST token surgery demo & benchmark playground | 1-click browser testing, zero installation |"
        )

    if new_org_content != org_content:
        pr_org = api.upload_file(
            path_or_fileobj=new_org_content.encode("utf-8"),
            path_in_repo="README.md",
            repo_id="Kronumos/README",
            repo_type="space",
            commit_message="Add Live Interactive Workbench link to official org showcase",
            create_pr=True
        )
        print(f"   -> PR Created for Kronumos/README: {pr_org}")
    else:
        print("   -> Kronumos/README already up to date.")
except Exception as e:
    print(f"   -> Error updating Kronumos/README: {e}")

print("\nAll tasks executed.")
