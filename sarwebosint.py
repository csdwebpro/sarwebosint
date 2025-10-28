#!/usr/bin/env python3
"""
DARKFORGE-X GITHUB READY WEB EXPLOITATION FRAMEWORK
Optimized for public repository deployment with CI/CD
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Optional
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import logging

# Add src to path for module imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.exploiter import AdvancedWebExploiter
from core.vulnerability_scanner import VulnerabilityScanner
from utils.report_generator import ReportGenerator

class DarkForgeGitHubCLI:
    """
    GitHub-optimized CLI interface for DarkForge-X
    """
    
    def __init__(self):
        self.setup_logging()
        self.config = self.load_config()
        
    def setup_logging(self):
        """Setup comprehensive logging for GitHub Actions"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('darkforge_scan.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self) -> Dict:
        """Load configuration from file"""
        config_path = os.path.join('config', 'settings.py')
        default_config = {
            "max_threads": 10,
            "timeout": 30,
            "user_agent": "DarkForge-X Security Scanner",
            "rate_limit_delay": 0.5
        }
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except:
            return default_config
            
    def run_scan(self, target: str, scan_type: str = "full") -> Dict:
        """
        Execute security scan based on type
        """
        self.logger.info(f"Starting {scan_type} scan on {target}")
        
        exploiter = AdvancedWebExploiter(
            target_url=target,
            config=self.config
        )
        
        scan_results = {
            "target": target,
            "scan_type": scan_type,
            "timestamp": self.get_timestamp(),
            "vulnerabilities": []
        }
        
        try:
            if scan_type in ["recon", "full"]:
                scan_results["reconnaissance"] = exploiter.perform_advanced_reconnaissance()
                
            if scan_type in ["scan", "full"]:
                scan_results["vulnerabilities"] = exploiter.execute_comprehensive_scan()
                
            # Generate reports
            report_gen = ReportGenerator(scan_results)
            scan_results["html_report"] = report_gen.generate_html_report()
            scan_results["json_report"] = report_gen.generate_json_report()
            
        except Exception as e:
            self.logger.error(f"Scan failed: {e}")
            scan_results["error"] = str(e)
            
        return scan_results
        
    def get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

def main():
    """Main CLI entry point optimized for GitHub"""
    parser = argparse.ArgumentParser(
        description='DarkForge-X Web Security Scanner - GitHub Ready',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic reconnaissance scan
  python darkforge_cli.py https://example.com --scan-type recon
  
  # Full vulnerability assessment
  python darkforge_cli.py https://example.com --scan-type full
  
  # Save results to file
  python darkforge_cli.py https://example.com --output results.json
        """
    )
    
    parser.add_argument('target', help='Target URL to scan')
    parser.add_argument('--scan-type', choices=['recon', 'scan', 'full'], 
                       default='full', help='Type of scan to perform')
    parser.add_argument('--output', '-o', help='Output file for results')
    parser.add_argument('--format', choices=['json', 'html', 'both'],
                       default='json', help='Output format')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = DarkForgeGitHubCLI()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        # Execute scan
        results = cli.run_scan(args.target, args.scan_type)
        
        # Handle output
        if args.output:
            if args.format in ['json', 'both']:
                with open(f"{args.output}.json", 'w') as f:
                    json.dump(results, f, indent=2)
                    
            if args.format in ['html', 'both']:
                with open(f"{args.output}.html", 'w') as f:
                    f.write(results.get('html_report', ''))
                    
            cli.logger.info(f"Results saved to {args.output}")
        else:
            # Print JSON results to stdout for GitHub Actions
            print(json.dumps(results, indent=2))
            
        # Exit with appropriate code
        vulnerabilities_found = len(results.get('vulnerabilities', []))
        if vulnerabilities_found > 0:
            cli.logger.warning(f"Found {vulnerabilities_found} vulnerabilities")
            sys.exit(1)  # Exit with error for CI/CD to detect
        else:
            cli.logger.info("No vulnerabilities found")
            sys.exit(0)
            
    except KeyboardInterrupt:
        cli.logger.info("Scan interrupted by user")
        sys.exit(130)
    except Exception as e:
        cli.logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
