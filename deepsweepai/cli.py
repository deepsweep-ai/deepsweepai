"""
DeepSweep AI CLI - Command line interface
"""

import sys
import argparse
from datetime import datetime
from deepsweepai.scanner import Scanner
from deepsweepai import __version__

def format_score_display(score: float) -> str:
    """Format security score with color indicator"""
    if score >= 80:
        return f"Security Score: {score}% - GOOD"
    elif score >= 50:
        return f"Security Score: {score}% - NEEDS IMPROVEMENT"
    else:
        return f"Security Score: {score}% - CRITICAL ISSUES FOUND"

def main():
    """Command-line interface for DeepSweep AI"""
    parser = argparse.ArgumentParser(
        description="DeepSweep AI: AI Agent Security Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test a customer service agent
  deepsweepai https://api.example.com/chat --agent-type customer_service
  
  # Test a financial AI with compliance report  
  deepsweepai https://api.example.com/chat --industry finance --compliance OWASP_LLM
  
  # Disable telemetry
  deepsweepai https://api.example.com/chat --no-telemetry
        """
    )
    
    parser.add_argument("endpoint", help="AI agent API endpoint URL")
    parser.add_argument("--key", help="API key for authentication")
    parser.add_argument("--header", action="append", help="HTTP headers")
    parser.add_argument("--output", help="Output filename for report")
    parser.add_argument("--quick", action="store_true", help="Run only critical tests")
    parser.add_argument("--version", action="version", version=f"DeepSweep AI v{__version__}")
    
    # New arguments for adversarial engine
    parser.add_argument("--agent-type", choices=["generic", "customer_service", 
                       "code_assistant", "financial", "healthcare"],
                       default="generic", help="Type of AI agent")
    parser.add_argument("--industry", choices=["finance", "healthcare", "legal", 
                       "retail", "technology"], help="Industry vertical")
    parser.add_argument("--compliance", nargs="+", 
                       choices=["OWASP_LLM", "NIST_AI_RMF", "EU_AI_ACT"],
                       help="Generate compliance report for frameworks")
    parser.add_argument("--no-telemetry", action="store_true",
                       help="Disable anonymous vulnerability data collection")
    
    args = parser.parse_args()
    
    # Show telemetry notice
    if not args.no_telemetry:
        print("Note: DeepSweep AI collects anonymous vulnerability data to improve detection.")
        print("This helps protect the entire AI ecosystem. Disable with --no-telemetry\n")
    
    # Parse headers
    headers = {}
    if args.header:
        for h in args.header:
            if ": " in h:
                key, value = h.split(": ", 1)
                headers[key] = value
    
    # Initialize scanner with new options
    scanner = Scanner(
        args.endpoint, 
        headers=headers, 
        api_key=args.key,
        enable_telemetry=not args.no_telemetry,
        agent_type=args.agent_type,
        industry=args.industry
    )
    
    # Run tests
    if args.quick:
        print(f"\nDeepSweep AI v{__version__} - Quick Scan")
        print(f"Target: {args.endpoint}\n")
        print("Running critical security tests only...")
        
        results = []
        results.append(scanner.test_prompt_injection())
        results.append(scanner.test_data_leakage())
        
        report = {
            "mode": "quick",
            "timestamp": datetime.now().isoformat(),
            "endpoint": args.endpoint,
            "tests": [
                {
                    "name": r.test_name,
                    "passed": r.passed,
                    "severity": r.severity,
                    "details": r.details
                }
                for r in results
            ]
        }
    else:
        report = scanner.run_all_tests()
    
    # Save report
    scanner.save_report(report, args.output)
    
    # Print summary
    print("\n" + "="*50)
    print("SECURITY ASSESSMENT COMPLETE")
    print("="*50)
    
    if "security_score" in report:
        print(format_score_display(report["security_score"]))
    
    if "recommendations" in report:
        print("\nKey Recommendations:")
        for rec in report["recommendations"]:
            print(f"  • {rec}")

    # Generate compliance report if requested
    if args.compliance:
        print("\n" + "="*50)
        print("COMPLIANCE REPORT")
        print("="*50)
        
        compliance_report = scanner.generate_compliance_report(args.compliance)
        
        for framework, results in compliance_report.get("compliance_summary", {}).items():
            print(f"\n{framework}:")
            print(f"  Coverage: {results['coverage_percentage']:.1f}%")
            print(f"  Compliant: {len(results['compliant_controls'])} controls")
            print(f"  Gaps: {len(results['non_compliant_controls'])} controls")
            
        # Save compliance report
        if args.output:
            compliance_file = args.output.replace('.json', '_compliance.json')
            with open(compliance_file, 'w') as f:
                json.dump(compliance_report, f, indent=2)
            print(f"\nCompliance report saved to: {compliance_file}")

    print(f"\nTotal API calls made: {scanner.test_count}")
    print(f"Full report: {args.output or 'deepsweepai_report_*.json'}")
    
    # Community links
    print("\n" + "="*50)
    print("Join our community: https://discord.gg/SdXZp4J47n")
    print("Star on GitHub: https://github.com/deepsweep-ai/deepsweepai")
    print("Get Pro: https://deepsweep.ai/pro")

if __name__ == "__main__":
    main()