#!/usr/bin/env python3
"""
PathFinder - A lightning-fast web reconnaissance tool
"""

import sys
import asyncio
import aiohttp
import dns.resolver
from typing import List, Dict, Optional, Union
from pathlib import Path
import argparse
from datetime import datetime
import json
import csv
import logging
import os
import re
from rich.console import Console
from rich.progress import Progress

__version__ = "1.0.0"
__author__ = "Zeeshan01001"

# Get the directory where pathfinder.py is located
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

console = Console()

class PathFinder:
    def __init__(
        self,
        target: str,
        wordlist: Union[str, List[str]] = None,
        threads: int = 20,
        timeout: int = 3,
        thorough: bool = False,
        types: List[str] = None,
        verify_ssl: bool = True,
        user_agent: str = None,
        output_format: str = "txt",
        simple_mode: bool = False
    ):
        self.target = target.rstrip("/")
        self.simple_mode = simple_mode
        
        # In simple mode, use smaller wordlist and common web extensions
        if simple_mode:
            wordlist = os.path.join(PACKAGE_DIR, "wordlists.txt")
            types = ['php', 'html', 'js']
            threads = 10
            timeout = 5
        
        # Use default wordlist if none provided
        if wordlist is None:
            wordlist = os.path.join(PACKAGE_DIR, "wordlists.txt")
            
        self.wordlist = self._load_wordlist(wordlist)
        self.threads = threads
        self.timeout = timeout
        self.thorough = thorough
        self.types = types or []
        self.verify_ssl = verify_ssl
        self.user_agent = user_agent or f"PathFinder/{__version__}"
        self.output_format = output_format
        
        self.results = []
        self.session = None
        self.dns_resolver = dns.resolver.Resolver()
        
        logging.basicConfig(
            level=logging.INFO if not simple_mode else logging.WARNING,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("PathFinder")

    def _load_wordlist(self, wordlist: Union[str, List[str]]) -> List[str]:
        """Load wordlist from file or list."""
        if isinstance(wordlist, list):
            return wordlist
        
        wordlist_path = Path(wordlist)
        if not wordlist_path.exists():
            raise FileNotFoundError(f"Wordlist not found: {wordlist}")
        
        paths = []
        with open(wordlist_path) as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    paths.append(line)
        
        if not paths:
            raise ValueError("Wordlist is empty")
            
        return paths

    async def _init_session(self):
        """Initialize HTTP session."""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers={"User-Agent": self.user_agent},
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )

    async def _close_session(self):
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def _check_url(self, path: str) -> Optional[Dict]:
        """Check if a URL exists."""
        url = f"{self.target}/{path.lstrip('/')}"
        try:
            async with self.session.get(url, ssl=self.verify_ssl, allow_redirects=False) as response:
                return {
                    'url': url,
                    'status_code': response.status,
                    'content_length': len(await response.read()),
                    'redirect_location': response.headers.get('Location'),
                    'timestamp': datetime.now().isoformat()
                }
        except aiohttp.ClientError as e:
            self.logger.debug(f"Error checking {url}: {str(e)}")
            return None

    async def scan_directories(self):
        """Scan for directories and files."""
        await self._init_session()
        try:
            if self.simple_mode:
                console.print("🔍 Starting quick scan...\n")
            else:
                console.print(f"\n🔍 PathFinder v{__version__} - Scanning {self.target}\n")
            
            with Progress() as progress:
                task = progress.add_task(
                    "[cyan]Quick scan in progress..." if self.simple_mode else "[cyan]Scanning directories...",
                    total=len(self.wordlist)
                )
                
                for i in range(0, len(self.wordlist), self.threads):
                    batch = self.wordlist[i:i + self.threads]
                    tasks = []
                    
                    for path in batch:
                        tasks.append(self._check_url(path))
                        for ext in self.types:
                            if not path.endswith(ext):
                                tasks.append(self._check_url(f"{path}.{ext}"))
                    
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    valid_results = [r for r in results if isinstance(r, dict)]
                    self.results.extend(valid_results)
                    
                    progress.update(task, advance=len(batch))
                    
                    for result in valid_results:
                        if 200 <= result['status_code'] < 400:
                            path = result['url'].replace(self.target, '')
                            console.print(
                                f"[green]✓[/] Found: {path}"
                                if self.simple_mode else
                                f"[green][+][/] Found: {path} (Status: {result['status_code']})"
                            )
            
            if self.simple_mode:
                console.print(f"\n✨ Done! Found {len(self.results)} paths\n")
            else:
                console.print(f"\n✨ Scan completed! Found {len(self.results)} results.\n")
        finally:
            await self._close_session()

    async def scan_subdomains(self):
        """Scan for subdomains."""
        if self.simple_mode:
            console.print("🔍 Looking for subdomains...\n")
        else:
            console.print(f"\n🔍 PathFinder v{__version__} - Scanning subdomains of {self.target}\n")
        
        with Progress() as progress:
            task = progress.add_task(
                "[cyan]Quick search in progress..." if self.simple_mode else "[cyan]Scanning subdomains...",
                total=len(self.wordlist)
            )
            found = 0
            
            for subdomain in self.wordlist:
                full_domain = f"{subdomain}.{self.target}"
                try:
                    answers = self.dns_resolver.resolve(full_domain)
                    for rdata in answers:
                        result = {
                            'subdomain': full_domain,
                            'ip': str(rdata),
                            'timestamp': datetime.now().isoformat()
                        }
                        self.results.append(result)
                        console.print(
                            f"[green]✓[/] Found: {full_domain}"
                            if self.simple_mode else
                            f"[green][+][/] Found: {full_domain} -> {rdata}"
                        )
                        found += 1
                except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                    pass
                except Exception as e:
                    self.logger.debug(f"Error resolving {full_domain}: {str(e)}")
                
                progress.update(task, advance=1)
            
            if self.simple_mode:
                console.print(f"\n✨ Done! Found {found} subdomains\n")
            else:
                console.print(f"\n✨ Scan completed! Found {found} subdomains.\n")

    def export_results(self, output_file: str):
        """Export results to file."""
        if not self.results:
            return

        output_path = Path(output_file)
        
        if self.output_format == "json":
            with open(output_path, 'w') as f:
                json.dump(self.results, f, indent=2)
        
        elif self.output_format == "csv":
            if not self.results:
                return
                
            fieldnames = self.results[0].keys()
            with open(output_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.results)
        
        else:  # txt format
            with open(output_path, 'w') as f:
                for result in self.results:
                    if 'url' in result:
                        path = result['url'].replace(self.target, '')
                        f.write(f"{path} - Status: {result['status_code']}\n")
                    else:
                        f.write(f"{result['subdomain']} -> {result['ip']}\n")

def main():
    parser = argparse.ArgumentParser(
        description="🔍 PathFinder - Lightning-Fast Web Scanner with 150+ Common Paths",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Basic Scan:             pathfinder example.com
  With Custom Wordlist:   pathfinder example.com -w custom.txt
  Find Subdomains:        pathfinder -s example.com
  Save Results:           pathfinder example.com -o results.txt
  Thorough Scan:          pathfinder example.com --thorough
"""
    )
    
    parser.add_argument('target', help="Target website (e.g., example.com)")
    parser.add_argument('-s', '--subdomains', action='store_true', help="Search for subdomains")
    parser.add_argument('-w', '--wordlist', help="Custom wordlist file (default: built-in 150+ paths)")
    parser.add_argument('-o', '--out', help="Save results to file")
    parser.add_argument('--thorough', action='store_true', help="Enable thorough scanning")
    parser.add_argument('--types', help="File extensions to check (e.g., php,html,js)")
    parser.add_argument('--threads', type=int, default=20, help="Number of threads (default: 20)")
    parser.add_argument('--timeout', type=int, default=3, help="Request timeout in seconds (default: 3)")
    parser.add_argument('--no-ssl', action='store_true', help="Skip SSL verification")
    parser.add_argument('--format', choices=['txt', 'json', 'csv'], default='txt', help="Output format")
    parser.add_argument('--simple', action='store_true', help="Simple output mode")

    args = parser.parse_args()

    try:
        # Prepare finder settings
        settings = {
            'target': args.target,
            'wordlist': args.wordlist,
            'simple_mode': args.simple,
            'verify_ssl': not args.no_ssl,
        }
        
        if args.threads:
            settings['threads'] = args.threads
        if args.types:
            settings['types'] = args.types.split(',')
        if args.format:
            settings['output_format'] = args.format

        # Initialize and run finder
        if args.subdomains:
            finder = PathFinder(**settings)
            asyncio.run(finder.scan_subdomains())
        else:
            if not args.target.startswith(('http://', 'https://')):
                settings['target'] = f"https://{args.target}"
            finder = PathFinder(**settings)
            asyncio.run(finder.scan_directories())
        
        # Export results if needed
        if args.out:
            finder.export_results(args.out)
            console.print(f"[green]Results saved to {args.out}[/]")

    except KeyboardInterrupt:
        console.print("\n[red]Scan interrupted by user[/]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/]")
        sys.exit(1)

if __name__ == "__main__":
    main() 