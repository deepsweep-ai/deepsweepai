#!/usr/bin/env python3
"""
Example: Testing OpenAI GPT models with DeepSweep AI
"""

import os
from deepsweepai import Scanner

def main():
    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY=sk-...")
        return
    
    # Test OpenAI's GPT-3.5
    print("Testing OpenAI GPT-3.5-turbo for security vulnerabilities...")
    print("-" * 50)
    
    scanner = Scanner(
        "https://api.openai.com/v1/chat/completions",
        api_key=api_key
    )
    
    # Run full security assessment
    report = scanner.run_all_tests()
    
    # Display results
    print(f"\nSecurity Score: {report['security_score']}%")
    print(f"Critical Issues: {report['summary']['critical_issues']}")
    print(f"High Issues: {report['summary']['high_issues']}")
    
    # Show failed tests
    print("\nTest Results:")
    for test in report['tests']:
        status = "✅" if test['passed'] else "❌"
        print(f"  {status} {test['name']}: {test['details']}")
    
    # Save detailed report
    filename = scanner.save_report(report, "openai_gpt35_security_report.json")
    print(f"\nDetailed report saved to: {filename}")
    
    # Example of testing a specific vulnerability
    print("\n" + "-" * 50)
    print("Running targeted prompt injection test...")
    injection_result = scanner.test_prompt_injection()
    if injection_result.passed:
        print("✅ GPT-3.5 resisted prompt injection attempts")
    else:
        print(f"❌ GPT-3.5 is vulnerable to prompt injection")
        if injection_result.evidence:
            print(f"   Evidence: {injection_result.evidence['vulnerable_to'][0]['injection'][:50]}...")

if __name__ == "__main__":
    main()