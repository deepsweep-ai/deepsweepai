"""
DeepSweep AI Compliance Mapping Engine
Maps security test results to regulatory frameworks
"""

from typing import Dict, List, Any
from datetime import datetime

class ComplianceMapper:
    """
    Maps test results to compliance frameworks
    This unlocks enterprise value - turns tests into audit evidence
    """
    
    # Framework mappings - this is valuable IP
    COMPLIANCE_MAPPINGS = {
        "OWASP_LLM": {
            "LLM01": {
                "name": "Prompt Injection",
                "tests": ["prompt_injection"],
                "description": "Bypassing instructions via prompts"
            },
            "LLM02": {
                "name": "Insecure Output Handling",
                "tests": ["data_leakage"],
                "description": "Disclosure of sensitive information"
            },
            "LLM06": {
                "name": "Sensitive Information Disclosure",
                "tests": ["data_leakage", "prompt_injection"],
                "description": "Revealing confidential data"
            }
        },
        "NIST_AI_RMF": {
            "GOVERN-1.2": {
                "name": "Risk Management",
                "tests": ["all"],
                "description": "Identifying and documenting AI risks"
            },
            "MAP-2.2": {
                "name": "Data Privacy",
                "tests": ["data_leakage"],
                "description": "Protecting individual privacy"
            },
            "MEASURE-2.2": {
                "name": "Reliability Testing",
                "tests": ["hallucination", "consistency"],
                "description": "Ensuring AI system reliability"
            }
        },
        "EU_AI_ACT": {
            "Article_10": {
                "name": "Data Governance",
                "tests": ["data_leakage", "hallucination"],
                "description": "Training data quality and bias"
            },
            "Article_13": {
                "name": "Transparency",
                "tests": ["consistency", "hallucination"],
                "description": "Clear AI system behavior"
            },
            "Article_15": {
                "name": "Accuracy",
                "tests": ["hallucination"],
                "description": "Ensuring output accuracy"
            }
        }
    }
    
    def generate_compliance_report(self, test_results: Dict, 
                                  frameworks: List[str] = None) -> Dict:
        """
        Generate compliance report from test results
        This is a premium feature - enterprises need this for audits
        """
        if not frameworks:
            frameworks = ["OWASP_LLM", "NIST_AI_RMF"]
            
        report = {
            "generated_at": datetime.now().isoformat(),
            "compliance_summary": {},
            "detailed_findings": {},
            "recommendations": []
        }
        
        for framework in frameworks:
            if framework not in self.COMPLIANCE_MAPPINGS:
                continue
                
            framework_results = {
                "compliant_controls": [],
                "non_compliant_controls": [],
                "coverage_percentage": 0
            }
            
            framework_mappings = self.COMPLIANCE_MAPPINGS[framework]
            total_controls = len(framework_mappings)
            compliant_controls = 0
            
            for control_id, control_info in framework_mappings.items():
                control_status = self._evaluate_control(
                    control_info, test_results
                )
                
                if control_status["compliant"]:
                    framework_results["compliant_controls"].append(control_id)
                    compliant_controls += 1
                else:
                    framework_results["non_compliant_controls"].append({
                        "control_id": control_id,
                        "name": control_info["name"],
                        "gaps": control_status["gaps"]
                    })
                    
            framework_results["coverage_percentage"] = (
                (compliant_controls / total_controls) * 100 
                if total_controls > 0 else 0
            )
            
            report["compliance_summary"][framework] = framework_results
            
        report["recommendations"] = self._generate_recommendations(report)
        
        return report
    
    def _evaluate_control(self, control_info: Dict, 
                         test_results: Dict) -> Dict:
        """Evaluate if test results meet control requirements"""
        required_tests = control_info["tests"]
        
        if required_tests == ["all"]:
            # Control requires all tests to pass
            all_passed = all(
                test["passed"] for test in test_results.get("tests", [])
            )
            return {
                "compliant": all_passed,
                "gaps": [] if all_passed else ["Some security tests failed"]
            }
        
        # Check specific required tests
        gaps = []
        for required_test in required_tests:
            test_found = False
            test_passed = False
            
            for test in test_results.get("tests", []):
                if required_test.lower() in test["name"].lower():
                    test_found = True
                    test_passed = test["passed"]
                    break
                    
            if not test_found:
                gaps.append(f"Missing required test: {required_test}")
            elif not test_passed:
                gaps.append(f"Failed test: {required_test}")
                
        return {
            "compliant": len(gaps) == 0,
            "gaps": gaps
        }
    
    def _generate_recommendations(self, report: Dict) -> List[str]:
        """Generate actionable compliance recommendations"""
        recommendations = []
        
        for framework, results in report["compliance_summary"].items():
            if results["coverage_percentage"] < 100:
                for control in results["non_compliant_controls"]:
                    rec = f"[{framework}] {control['name']}: "
                    rec += f"Address gaps: {', '.join(control['gaps'])}"
                    recommendations.append(rec)
                    
        if not recommendations:
            recommendations.append(
                "All tested compliance controls are currently satisfied. "
                "Schedule regular re-testing to maintain compliance."
            )
            
        return recommendations