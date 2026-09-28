#!/usr/bin/env python3
import argparse
import glob
import json
import os
import sys

def main():
    parser = argparse.ArgumentParser(description="Aggregate SWE-bench results across matrix jobs")
    parser.add_argument('--input_dir', default='downloaded_artifacts', help='Directory with downloaded artifacts')
    parser.add_argument('--output_json', default='kronumos_verified_500_final_report.json', help='Output unified report JSON')
    args = parser.parse_args()

    print(f"[Aggregator] Searching for benchmark reports in {args.input_dir}...")
    report_files = glob.glob(os.path.join(args.input_dir, '**', '*.json'), recursive=True)

    all_resolved = set()
    all_unresolved = set()
    all_errors = set()

    for rf in report_files:
        # Skip predictions file
        if 'predictions' in os.path.basename(rf):
            continue
        try:
            with open(rf, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if not isinstance(data, dict):
                continue
            
            # Check for standard SWE-bench report keys
            if any(k in data for k in ['resolved_instances', 'resolved', 'unresolved_instances', 'error_instances']):
                res = data.get('resolved_instances', [])
                unres = data.get('unresolved_instances', [])
                errs = data.get('error_instances', [])

                if isinstance(res, list): all_resolved.update(res)
                elif isinstance(res, dict): all_resolved.update(res.keys())

                if isinstance(unres, list): all_unresolved.update(unres)
                elif isinstance(unres, dict): all_unresolved.update(unres.keys())

                if isinstance(errs, list): all_errors.update(errs)
                elif isinstance(errs, dict): all_errors.update(errs.keys())
                print(f"[Aggregator] Processed report: {rf} -> {len(res)} resolved, {len(unres)} unresolved")
        except Exception as e:
            print(f"[Aggregator] Notice: Could not parse {rf}: {e}")

    resolved_list = sorted(list(all_resolved))
    unresolved_list = sorted(list(all_unresolved - all_resolved))
    error_list = sorted(list(all_errors - all_resolved - all_unresolved))
    total_tested = len(resolved_list) + len(unresolved_list) + len(error_list)

    repo_breakdown = {}
    for inst in resolved_list:
        repo = inst.split('__')[0]
        repo_breakdown[repo] = repo_breakdown.get(repo, 0) + 1

    rate_500 = (len(resolved_list) / 500.0 * 100) if 500 > 0 else 0
    rate_tested = (len(resolved_list) / total_tested * 100) if total_tested > 0 else 0

    print("==================================================")
    print("🥊 KRONUMOS 2 KAIROS — SWE-BENCH VERIFIED OFFICIAL SCORECARD")
    print(f"Total Benchmark Instances : 500")
    print(f"Total Instances Evaluated : {total_tested}")
    print(f"Resolved Instances (PASS) : {len(resolved_list)} ({rate_500:.2f}% of 500)")
    print(f"Unresolved Instances      : {len(unresolved_list)}")
    print(f"Error / Timeouts          : {len(error_list)}")
    print("Per-repo resolved:")
    for r, c in sorted(repo_breakdown.items(), key=lambda x: -x[1]):
        print(f"  - {r}: {c}")
    print("==================================================")

    # Save final report
    final_report = {
        'system': 'Kronumos 2 Kairos (Tokenectomy Labs)',
        'dataset': 'SWE-bench/SWE-bench_Verified',
        'total_instances': 500,
        'evaluated_instances': total_tested,
        'resolved_count': len(resolved_list),
        'resolved_rate_total_500': rate_500,
        'resolved_rate_tested': rate_tested,
        'resolved_instances': resolved_list,
        'unresolved_instances': unresolved_list,
        'error_instances': error_list,
        'repo_breakdown': repo_breakdown
    }

    with open(args.output_json, 'w', encoding='utf-8') as f:
        json.dump(final_report, f, indent=2)
    print(f"[Aggregator] Saved final scorecard to {args.output_json}")

    # Write to GitHub Step Summary if available
    step_summary = os.environ.get('GITHUB_STEP_SUMMARY')
    if step_summary:
        with open(step_summary, 'a', encoding='utf-8') as f:
            f.write("### 🥊 Kronumos 2 Kairos — SWE-bench Verified Official Scorecard\n\n")
            f.write("| Metric | Empirical Value |\n")
            f.write("| :--- | :--- |\n")
            f.write("| **Total Benchmark Instances** | 500 |\n")
            f.write(f"| **Evaluated Instances** | {total_tested} |\n")
            f.write(f"| **Resolved Tasks (PASSED)** | **{len(resolved_list)}** |\n")
            f.write(f"| **Unresolved Tasks** | {len(unresolved_list)} |\n")
            f.write(f"| **Errors / Timeouts** | {len(error_list)} |\n")
            f.write(f"| **Official Resolve Rate (on 500)** | **{rate_500:.2f}%** |\n\n")
            f.write("#### 📂 Per-Repository Resolved Breakdown\n\n")
            for r, c in sorted(repo_breakdown.items(), key=lambda x: -x[1]):
                f.write(f"- **{r}**: {c} tasks resolved\n")

if __name__ == '__main__':
    main()
