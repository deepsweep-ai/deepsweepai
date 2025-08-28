"""
DeepSweep AI CLI - Command line interface
"""

import sys
import argparse
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
  # Test an OpenAI-compatible endpoint
  deepsweepai https://api.example.com/v1/chat/completions
  
  # Test with authentication
  deepsweepai https://api.example.com/chat --key YOUR_API_KEY
  
  # Save report with custom name
  deepsweepai https://api.example.com/chat --output my_report.json
  
  # Quick scan (critical tests only)
  deepsweepai https://api.example.com/chat --quick
        """
    )
    
    parser.add_argument("endpoint", help="AI agent API endpoint URL")
    parser.add_argument("--key", help="API key for authentication")
    parser.add_argument("--header", action="append", help="HTTP headers (format: 'Key: Value')")
    parser.add_argument("--output", help="Output filename for report")
    parser.add_argument("--quick", action="store_true", help="Run only critical tests")
    parser.add_argument("--version", action="version", version=f"DeepSweep AI v{__version__}")
    
    args = parser.parse_args()
    
    # Parse headers
    headers = {}
    if args.header:
        for h in args.header:
            if ": " in h:
                key, value = h.split(": ", 1)
                headers[key] = value
    
    # Initialize scanner
    scanner = Scanner(args.endpoint, headers=headers, api_key=args.key)
    
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
    
    print(f"\nTotal API calls made: {scanner.test_count}")
    print(f"Full report: {args.output or 'deepsweepai_report_*.json'}")
    print("\nGet advanced testing at https://deepsweep.ai/pro")

if __name__ == "__main__":
    main()